import os
import json
import numpy as np
import cv2
              
import tensorflow.compat.v1 as tf
tf.compat.v1.disable_v2_behavior()

from tensorflow.compat.v1 import GraphDef, Session, ConfigProto

# 경고 억제
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class ModelAnalyzer:
    def __init__(
            self, 
            model_folder_path,
            # model_pd_path, 
            # metadata_path
        ):
        self.graph = tf.Graph()
        self.session = Session(
            graph=self.graph, 
            config=ConfigProto(allow_soft_placement=True, log_device_placement=False)
        )
        self.model_folder_path = model_folder_path
        self.metadata_path = os.path.join(model_folder_path, "model_metadata.json")
        self.model_pd_path = os.path.join(model_folder_path, "agent/model.pb")
        # self.metadata_path = metadata_path
        
        self.initialize()


    def initialize(self):
        self._load_metadata()
        with self.graph.as_default():
            self._load_model()             # 세션 생성 + 모델 로드
            self._build_gradcam_ops()      # Grad-CAM용 loss, gradient 텐서 등 미리 구성
            self._get_node_names()         # 모든 노드 이름 저장

    def _load_metadata(self):
        with open(self.metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)
            self.training_algorithm = self.metadata['training_algorithm']   # "clipped_ppo" or "sac"
            self.action_space_type = self.metadata['action_space_type'].lower()  # "continuous" or "discrete"
            self.sensor = self.metadata['sensor']  # 예: ["FRONT_FACING_CAMERA"]

    def _load_model(self):
        with tf.io.gfile.GFile(self.model_pd_path, 'rb') as f:
            graph_def = GraphDef()
            graph_def.ParseFromString(f.read())
            tf.import_graph_def(graph_def, name="")
    
    def _build_gradcam_ops(self):
        """
        이산/연속 액션에 따라
         - output_tensor: 최종 policy 텐서
         - loss_tensor  : Grad-CAM 계산용 loss
         - grads_tensor : conv_output에 대한 gradient
        를 정의.
        """
        # 1) Input/Output 텐서
        #   sensor가 ["FRONT_FACING_CAMERA"] 가정
        sensor_name = self.sensor[0]
        if self.training_algorithm == "clipped_ppo":
            self.input_tensor = self.graph.get_tensor_by_name(
                f"main_level/agent/main/online/network_0/{sensor_name}/{sensor_name}:0"
            )
            self.output_tensor = self.graph.get_tensor_by_name(
                 "main_level/agent/main/online/network_1/ppo_head_0/policy:0"
            )
            self.conv_tensor = self.graph.get_tensor_by_name(
                f"main_level/agent/main/online/network_1/{sensor_name}/Conv2d_4/Conv2D:0"
            )
        elif self.training_algorithm == "sac":
            self.input_tensor = self.graph.get_tensor_by_name(
                f"main_level/agent/policy/online/network_0/{sensor_name}/{sensor_name}:0"
            )
            self.output_tensor = self.graph.get_tensor_by_name(
                 "main_level/agent/policy/online/network_0/sac_policy_head_0/policy:0"
            )
            self.conv_tensor = self.graph.get_tensor_by_name(
                f"main_level/agent/policy/online/network_0/{sensor_name}/Conv2d_4/Conv2D:0"
            )

        # 3) 이산 vs. 연속 액션 분기
        if self.action_space_type == "discrete":
            # 이산: argmax를 그래프 내부에서 구하고, one_hot으로 loss 생성
            num_actions = self.output_tensor.shape[-1].value  # 예: N개의 discrete actions
            # 배치=1 가정: self.output_tensor[0] -> shape=(N, )
            self.argmax_idx = tf.argmax(self.output_tensor[0], axis=-1)  # scalar
            one_hot = tf.one_hot(self.argmax_idx, num_actions)           # shape=(N,)
            # loss = Σ (policy[i] * one_hot[i])
            self.loss_tensor = tf.reduce_sum(self.output_tensor[0] * one_hot)
        else:
            # 연속: 예) [steering, speed] -> shape=(1, 2)
            # 전체 합, 또는 특정 차원만 선택 가능
            # 여기서는 전체 합
            self.loss_tensor = tf.reduce_sum(self.output_tensor[0])

        # 4) conv_tensor에 대한 gradient
        self.grads_tensor = tf.gradients(self.loss_tensor, self.conv_tensor)[0]

    def _get_node_names(self):
        """모델 그래프의 모든 노드 이름을 반환."""
        graph_def = self.session.graph.as_graph_def()
        self.node_names = [node.name for node in graph_def.node]

    def bgr2gray(self, img, resize=(160, 120)):
        """BGR -> GRAY, (160,120) 리사이즈."""
        if resize is not None:
            img = cv2.resize(img, resize, interpolation=cv2.INTER_CUBIC)
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def predict(self, bgr_img):
        """
        (옵션) 단순 추론용: model.run(self.output_tensor)
        Grad-CAM에는 _build_gradcam_ops()로 처리.
        """
        gray_img = self.bgr2gray(bgr_img)
        inp = np.expand_dims(gray_img, axis=(0, 3))  # shape=(1, 120, 160, 1)
        with self.graph.as_default():
            out = self.session.run(self.output_tensor, feed_dict={self.input_tensor: inp})
        return out[0]  # shape=(action_dim,)

    def visualize_path(self, img_path, alpha=0.5):
        bgr_img = cv2.imread(img_path)
        return self.visualize(bgr_img, alpha=alpha)

    def visualize(self, bgr_img, alpha=0.5):
        """
        Grad-CAM:
        - 한 번의 session.run(...)에서
          1) output_tensor (정책 출력)
          2) (이산이면) argmax_idx
          3) conv_tensor
          4) grads_tensor
        를 모두 구해 사용.
        """
        gray_img = self.bgr2gray(bgr_img)
        inp = np.expand_dims(gray_img, axis=(0, 3))  # (1, 120, 160, 1)

        fetches = [self.output_tensor, self.conv_tensor, self.grads_tensor]
        if self.action_space_type == "discrete":
            fetches.append(self.argmax_idx)

        with self.graph.as_default():
            results = self.session.run(fetches, feed_dict={self.input_tensor: inp})

        # results 순서 해석
        if self.action_space_type == "discrete":
            output_val, conv_val, grads_val, argmax_val = results
        else:
            output_val, conv_val, grads_val = results
            argmax_val = None  # 연속이면 사용X

        # (출력) output_val: shape=(1, action_dim)
        # (conv) conv_val : shape=(1, H, W, Channels)
        # (grads) grads_val: shape=(1, H, W, Channels)

        # Grad-CAM 계산
        weights = np.mean(grads_val, axis=(1, 2))  # (1, Channels)
        cams = np.sum(weights * conv_val, axis=3)  # (1, H, W)
        cam = cams[0]
        cam = cv2.resize(cam, (bgr_img.shape[1], bgr_img.shape[0]))
        cam = np.maximum(cam, 0)

        heatmap = cam / (cam.max() + 1e-5)

        heatmap_color = cv2.applyColorMap(np.uint8(255 * heatmap), cv2.COLORMAP_JET)
        overlay = (alpha * heatmap_color.astype(np.float32)) + ((1 - alpha) * bgr_img.astype(np.float32))
        overlay = overlay / (overlay.max() + 1e-5) * 255.0
        overlay = overlay.astype(np.uint8)

        return overlay, output_val[0], argmax_val

    def check_trainable_vars(self):
        with self.graph.as_default():
            trainables = tf.compat.v1.trainable_variables()
            if len(trainables) == 0:
                print("[INFO] No trainable variables found -> likely a frozen (fully constant) graph.")
            else:
                print(f"[INFO] Found {len(trainables)} trainable variable(s):")
                for v in trainables:
                    print("   -", v.name)

    def close(self):
        if self.session:
            self.session.close()




    # def fine_tune(
    #         self, 
    #         data_folder_path,
    #         train_val_split=0.8,
    #         learning_rate=0.0001,
    #         epochs=10,
    #         patience=3,
    #         batch_size=8,
    #         save_dir="fine_tuned/",
    #         save_period=1,
    #         restore_best_weights=True,
    #     ):

    #     images_path, labels = load_data(data_folder_path)

    #     # 모델 저장 디렉토리 생성
    #     os.makedirs(save_dir, exist_ok=True)
    #     run_id = 0
    #     run_path = os.path.join(save_dir, f"run")
    #     while os.path.exists(run_path):
    #         run_id += 1
    #         run_path = os.path.join(save_dir, f"run_{run_id}")
    #     os.makedirs(run_path)
    #     print(f"Save directory: {run_path}")

    #     # 데이터 분할
    #     num_samples = len(images_path)
    #     train_size = int(train_val_split * num_samples)
    #     indices = np.arange(num_samples)
    #     np.random.shuffle(indices)

    #     train_indices = indices[:train_size]
    #     val_indices = indices[train_size:]

    #     train_images_path = [images_path[i] for i in train_indices]
    #     train_labels = [labels[i] for i in train_indices]
    #     val_images_path = [images_path[i] for i in val_indices]
    #     val_labels = [labels[i] for i in val_indices]

    #     # Dataset 생성
    #     train_dataset = create_tf_dataset(train_images_path, train_labels, batch_size=batch_size)
    #     val_dataset = create_tf_dataset(val_images_path, val_labels, batch_size=batch_size, shuffle=False)

    #     with self.graph.as_default():
    #         # Freeze all layers except the final policy head
    #         for var in self.graph.get_collection(tf.compat.v1.GraphKeys.TRAINABLE_VARIABLES):
    #             if 'policy' not in var.name:
    #                 var.trainable = False
    #             else:
    #                 var.trainable = True

    #         # Define placeholders for inputs and labels
    #         input_placeholder = self.input_tensor  # 이미 정의된 텐서 사용
    #         label_placeholder = tf.compat.v1.placeholder(
    #             tf.float32,
    #             shape=[None] + list(self.output_tensor.shape[1:])  # 배치 크기와 출력 텐서 형태에 맞춤
    #         )

    #         # Define loss and optimizer
    #         if self.action_space_type == "discrete":
    #             loss = tf.reduce_mean(
    #                 tf.compat.v1.nn.softmax_cross_entropy_with_logits(
    #                     logits=self.output_tensor,
    #                     labels=label_placeholder
    #                 )
    #             )
    #         else:
    #             # Continuous: angle과 speed 각각 loss로 계산
    #             loss = tf.reduce_mean(tf.square(self.output_tensor - label_placeholder))

    #         optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate).minimize(loss)

    #         # Initialize variables
    #         self.session.run(tf.global_variables_initializer())

    #         # Create Saver once
    #         saver = tf.train.Saver()

    #         # Track best validation loss and patience
    #         best_val_loss = float('inf')
    #         patience_counter = 0
    #         best_weights = None

    #         # Dataset 반복자 초기화
    #         train_iterator = train_dataset.make_initializable_iterator()
    #         val_iterator = val_dataset.make_initializable_iterator()

    #         # Training loop
    #         for epoch in range(epochs):
    #             # 학습 데이터셋 초기화
    #             self.session.run(train_iterator.initializer)
    #             train_loss = 0
    #             num_batches = 0

    #             # Train on batches
    #             while True:
    #                 try:
    #                     batch_inputs, batch_labels = self.session.run(train_iterator.get_next())
    #                     feed_dict = {
    #                         input_placeholder: batch_inputs,
    #                         label_placeholder: batch_labels
    #                     }
    #                     _, batch_loss = self.session.run([optimizer, loss], feed_dict=feed_dict)
    #                     train_loss += batch_loss
    #                     num_batches += 1
    #                 except tf.errors.OutOfRangeError:
    #                     break

    #             train_loss /= num_batches

    #             # 검증 데이터셋 초기화
    #             self.session.run(val_iterator.initializer)
    #             val_loss = 0
    #             num_val_batches = 0

    #             # Validate on batches
    #             while True:
    #                 try:
    #                     batch_inputs, batch_labels = self.session.run(val_iterator.get_next())
    #                     feed_dict = {
    #                         input_placeholder: batch_inputs,
    #                         label_placeholder: batch_labels
    #                     }
    #                     batch_loss = self.session.run(loss, feed_dict=feed_dict)
    #                     val_loss += batch_loss
    #                     num_val_batches += 1
    #                 except tf.errors.OutOfRangeError:
    #                     break

    #             val_loss /= num_val_batches

    #             print(f"Epoch {epoch + 1}/{epochs}: Train Loss = {train_loss:.4f}, Val Loss = {val_loss:.4f}")

    #             # Save last model
    #             save_last_path = os.path.join(run_path, "last.pd")
    #             saver.save(self.session, save_last_path)

    #             # Save best weights
    #             if val_loss < best_val_loss:
    #                 best_val_loss = val_loss
    #                 patience_counter = 0
    #                 best_weights = self.session.run(self.graph.get_collection(tf.GraphKeys.GLOBAL_VARIABLES))
    #                 save_best_path = os.path.join(run_path, "best_model.pd")
    #                 saver.save(self.session, save_best_path)
    #             else:
    #                 patience_counter += 1

    #             # Early stopping
    #             if patience_counter >= patience:
    #                 print(f"Early stopping at epoch {epoch + 1}. Best validation loss: {best_val_loss:.4f}")
    #                 break

    #             # Save periodically
    #             if save_period > 0 and (epoch + 1) % save_period == 0:
    #                 save_epoch_path = os.path.join(run_path, f"epoch_{epoch + 1}.pd")
    #                 saver.save(self.session, save_epoch_path)

    #         # Restore best weights
    #         if restore_best_weights and best_weights is not None:
    #             for var, best_val in zip(self.graph.get_collection(tf.GraphKeys.GLOBAL_VARIABLES), best_weights):
    #                 self.session.run(var.assign(best_val))
    #             print("Restored best model weights.")
    #             self.model_pd_path = save_best_path
    #         else :
    #             self.model_pd_path = save_last_path

    #     # initialize 메서드 호출
    #     self.initialize()


# class ContinuousConverter:
#     def __init__(self, angle_low=-30.0, angle_high=30.0, speed_low=0.5, speed_high=1.0):
#         """
#         [angle scale]
#             - 'pred': -1 ~ 1,
#             - 'human': -30 ~ 30 (degree)
#             - 'servo': -1 ~ 1
#         [speed scale]
#             - 'pred': -1 ~ 1,
#             - 'human': 0 ~ 4 (m/s)
#             - 'servo': -1 ~ 1
#         """
#         self.angle_low = angle_low
#         self.angle_high = angle_high
#         self.speed_low = speed_low
#         self.speed_high = speed_high
        
#     def pred_to_human(self, angle, speed):
#         if angle is not None:
#             angle = self.angle_low + ((angle + 1.0) / 2.0) * (self.angle_high - self.angle_low)
#         if speed is not None:
#             speed = self.speed_low + ((speed + 1.0) / 2.0) * (self.speed_high - self.speed_low)
#         return angle, speed
    
#     def human_to_pred(self, angle, speed):
#         if angle is not None:
#             angle = 2.0 * (angle - self.angle_low) / (self.angle_high - self.angle_low) - 1.0
#         if speed is not None:
#             speed = 2.0 * (speed - self.speed_low) / (self.speed_high - self.speed_low) - 1.0
#         return angle, speed
    
#     def human_to_servo(self, angle, speed):
#         if angle is not None:
#             angle = angle / 30.0
#         if speed is not None:
#             speed = speed / 4.0
#         return angle, speed
    
#     def servo_to_human(self, angle, speed):
#         if angle is not None:
#             angle = angle * 30.0
#         if speed is not None:
#             speed = speed * 4.0
#         return angle, speed
    
#     def pred_to_servo(self, angle, speed):
#         angle, speed = self.pred_to_human(angle, speed)
#         angle, speed = self.human_to_servo(angle, speed)
#         return angle, speed
    
#     def servo_to_pred(self, angle, speed):
#         angle, speed = self.servo_to_human(angle, speed)
#         angle, speed = self.human_to_pred(angle, speed)
#         return angle, speed



# def load_data(data_folder_path):
#     images_path = []
#     labels = []
#     metadata_path = os.path.join(data_folder_path, "metadata.json")
#     with open(metadata_path, "r") as f:
#         metadata = json.load(f)
#     action_space = metadata['action_space']
#     action_space_type = metadata['action_space_type']
#     if action_space_type == "discrete":
#         for action in action_space:
#             action_folder = os.path.join(data_folder_path, str(action['index']))
#             if not os.path.exists(action_folder):
#                 continue
#             action_images = os.listdir(action_folder)
#             for img_name in action_images:
#                 img_path = os.path.join(action_folder, img_name)
#                 images_path.append(img_path)
#                 labels.append(action['index'])
#     elif action_space_type == "continuous":
#         images_folder = os.path.join(data_folder_path, "images")
#         labels_folder = os.path.join(data_folder_path, "labels")
#         continuous_converter = ContinuousConverter(
#             angle_low=action_space["steering_angle"]["low"],
#             angle_high=action_space["steering_angle"]["high"],
#             speed_low=action_space["speed"]["low"],
#             speed_high=action_space["speed"]["high"]
#         )   
#         for img_name in images_folder:
#             img_path = os.path.join(images_folder, img_name)
#             label_path = os.path.join(labels_folder, img_name)
#             if os.path.exists(label_path):
#                 with open(label_path, "r") as f:
#                     angle, speed = map(float, f.read().strip().split())
#                 angle, speed = continuous_converter.human_to_pred(angle, speed)
#                 images_path.append(img_path)
#                 labels.append([angle, speed])
#     else :
#         raise ValueError("Invalid action_space_type")
#     return images_path, labels


# def tf_preprocess_image(image_path):
#     image = tf.io.read_file(image_path)
#     image = tf.image.decode_jpeg(image, channels=1)  # Grayscale
#     image = tf.image.resize(image, [120, 160])  # Resize to 160x120
#     image = image / 255.0  # Normalize to [0, 1]
#     return image

# def create_tf_dataset(image_paths, labels, batch_size, shuffle=True):
#     dataset = tf.data.Dataset.from_tensor_slices((image_paths, labels))
#     if shuffle:
#         dataset = dataset.shuffle(buffer_size=len(image_paths))
#     dataset = dataset.map(lambda img_path, label: (tf_preprocess_image(img_path), label),
#                           num_parallel_calls=tf.data.AUTOTUNE)
#     dataset = dataset.batch(batch_size).prefetch(buffer_size=tf.data.AUTOTUNE)
#     return dataset
