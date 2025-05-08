
import json
import time
import os
import time
from aicastle.deepracer.vehicle.api.constant import (
    INFERENCE_IMG_HEIGHT,
    INFERENCE_IMG_WIDTH,
    MAX_IMG_HEIGHT,
    MAX_IMG_WIDTH,
    DEFAULT_IMG_HEIGHT,
    DEFAULT_IMG_WIDTH
)
from aicastle.deepracer.vehicle.api.utils import (
    KeyboardListener,
    get_time_now,
    show_image,
    show_info
)

class ManualController:
    def __init__(self,
            vehicle,
            move_interval=0.05,
            move_timeout=1,
            action_space=None,
            action_space_type=None, # continuous, discrete
            save=False,
            save_dir='data/images/',
            save_with_time_dir=True, # save_dir에 시간을 추가하여 디렉토리 생성
            save_format='jpg',
            save_interval=0.5, # 저장 간격 (초)
            save_width=None,
            save_height=None,
        ):
        self.vehicle = vehicle
        self.move_interval = move_interval
        self.move_timeout = move_timeout
        self.action_space = action_space
        self.action_space_type = action_space_type
        if self.action_space_type == 'discrete':
            self.index_action_map = {action["index"]: action for action in self.action_space}
        self.save = save
        self.save_dir = save_dir
        self.save_with_time_dir = save_with_time_dir
        self.save_format = save_format
        self.save_interval = save_interval
        self.save_width = save_width
        self.save_height = save_height
        if self.save:
            self.save_setting()
            self.save_setting_done = True
        else :
            self.save_setting_done = False

        self.angle = 0
        self.speed = 0
        self.last_move_time = -1
        self.last_save_time = -1

    def save_setting(self):
        if self.save_with_time_dir : 
            self.save_dir = os.path.join(self.save_dir, get_time_now(milliseconds=False))
        os.makedirs(self.save_dir, exist_ok=True)
        print(f"save_dir: {self.save_dir}")
        # metadata.json 저장
        with open(os.path.join(self.save_dir, "metadata.json"), 'w') as f:
            metadata = {
                "action_space": self.action_space,   
                "action_space_type": self.action_space_type,
                "save_format": self.save_format,
                "save_width": self.save_width,
                "save_height": self.save_height,
                "save_interval": self.save_interval
            }
            json.dump(metadata, f, indent=2)

        # 폴더 세팅
        if self.action_space_type == 'continuous':
            os.makedirs(os.path.join(self.save_dir, "images"), exist_ok=True)
            os.makedirs(os.path.join(self.save_dir, "labels"), exist_ok=True)
        
        if self.action_space_type == 'discrete':
            for action in self.action_space:
                os.makedirs(os.path.join(self.save_dir, str(action["index"])), exist_ok=True)

    def move_continuous(self, angle=None, speed=None, move_timeout=None, save=None):
        if (angle is None) and (speed is None):
            raise Exception("At least one of angle, speed must be entered.")
        self.angle = self.angle if angle is None else angle
        self.speed = self.speed if speed is None else speed
        move_timeout = self.move_timeout if move_timeout is None else move_timeout
        last_time = time.time()
        
        ##### move
        if (last_time - self.last_move_time) > self.move_interval:
            self.vehicle.move(
                angle = self.angle, 
                speed = self.speed,
                scale = 'human', 
                timeout = move_timeout,
            )
            self.last_move_time = last_time

        ##### save
        save = self.save if save is None else save
        if save and (not self.save_setting_done):
            self.save_setting()
            self.save_setting_done = True
        if save and (last_time - self.last_save_time) > self.save_interval:
            image_save_dir = os.path.join(self.save_dir, "images")
            try :
                image_save_path = self.vehicle.save_image(
                    save_dir=image_save_dir, 
                    format=self.save_format, 
                    width=self.save_width, 
                    height=self.save_height
                )
            except :
                image_save_path = None

            if image_save_path:
                label_save_path = os.path.join(self.save_dir, "labels", f"{os.path.basename(image_save_path).split('.')[0]}.txt")
                with open(label_save_path, 'w') as f:
                    f.write(f"{self.angle} {self.speed}")
                self.last_save_time = last_time

    def move_discrete(self, action_index=None, move_timeout=None, save=None):
        if action_index is None:
            raise Exception("action_index must be entered.")
        action = self.index_action_map[action_index]
        angle = action["steering_angle"]
        speed = action["speed"]
        self.angle = angle
        self.speed = speed
        move_timeout = self.move_timeout if move_timeout is None else move_timeout
        last_time = time.time()
        
        ##### move
        if (last_time - self.last_move_time) > self.move_interval:
            self.vehicle.move(
                angle = self.angle, 
                speed = self.speed,
                scale = 'human', 
                timeout = move_timeout,
            )
            self.last_move_time = last_time

        ##### save
        save = self.save if save is None else save
        if save and (not self.save_setting_done):
            self.save_setting()
            self.save_setting_done = True
        if save and (last_time - self.last_save_time) > self.save_interval:
            if action_index in self.index_action_map:
                image_save_dir = os.path.join(self.save_dir, str(action_index))
                try :
                    image_save_path = self.vehicle.save_image(
                        save_dir=image_save_dir, 
                        format=self.save_format, 
                        width=self.save_width, 
                        height=self.save_height
                    )
                except :
                    image_save_path = None

                if image_save_path: 
                    self.last_save_time = last_time

    def stop(self):
        self.vehicle.move(angle=0, speed=0, scale='human', timeout=self.move_timeout)


class DiscreteController(ManualController):
    def __init__(self, **kwargs):
        kwargs["action_space_type"] = 'discrete'
        kwargs["action_space"] = [
            {"steering_angle": 0, "speed": 2, "index": 0},
            {"steering_angle": 30, "speed": 2, "index": 1},
            {"steering_angle": -30, "speed": 2, "index": 2},
            {"steering_angle": 0, "speed": -2, "index": 3},
        ] if kwargs["action_space"] is None else kwargs["action_space"]
        super().__init__(**kwargs)

    def move(self, action_index, **kwargs):
        super().move_discrete(action_index=action_index, **kwargs)


class ContinuousController(ManualController):
    def __init__(self, **kwargs):
        kwargs["action_space_type"] = 'continuous'
        kwargs["action_space"] = {
            "steering_angle": {
                "high": 30, 
                "low": -30
            },
            "speed": {
                "high": 4, 
                "low": 0.5
            },
        }
        super().__init__(**kwargs)

    def move(self, angle=None, speed=None, **kwargs):
        angle = min(self.action_space["steering_angle"]["high"], max(self.action_space["steering_angle"]["low"], angle))
        speed = min(self.action_space["speed"]["high"], max(self.action_space["speed"]["low"], speed))
        super().move_continuous(angle=angle, speed=speed, **kwargs)


class KeyboardController(DiscreteController):
    def __init__(self, keyboard_listener, index_key_map=None, **kwargs):
        self.keyboard_listener = keyboard_listener
        super().__init__(**kwargs)

        self.index_key_map = {
            0: "Key.up",
            1: "Key.left",
            2: "Key.right",
            3: "Key.down",
        } if index_key_map is None else index_key_map
        self.key_action_map = {self.index_key_map[action["index"]]: action for action in self.action_space}

    def run(self, exit_key='Key.esc', move_timeout=None, save=None):
        print(f"Press {exit_key} to stop")
        running = False
        while True:
            pressed_key = self.keyboard_listener.pressed_key
            if pressed_key == exit_key:
                break
            
            if pressed_key and pressed_key in self.key_action_map:
                action_index = self.key_action_map[pressed_key]["index"]
                response = self.move(
                    action_index = action_index, 
                    move_timeout=move_timeout, 
                    save=save,
                )
                running = True
            else:
                if running:
                    response = self.stop()
                    if response and response.status_code == 200:
                        running = False


class AutoModelLoadController:
    def __init__(self, vehicle, key_model_map, keyboard_listener):
        self.vehicle = vehicle
        self.key_model_map = key_model_map
        self.keyboard_listener = keyboard_listener
        self.loaded_model = None

    def run(self, exit_key='Key.esc'):
        print(f"Press {exit_key} to exit")
        while True:
            pressed_key = self.keyboard_listener.pressed_key
            if pressed_key == exit_key:
                break
            elif pressed_key and pressed_key in self.key_model_map:
                model_folder_name = self.key_model_map[pressed_key]
                if self.loaded_model != model_folder_name:
                    print(f"Model Loading: {model_folder_name}")
                    self.vehicle.load_model(model_folder_name)
                    self.loaded_model = model_folder_name
                    print(f"Model loaded")
            else:
                pass

                