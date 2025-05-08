import cv2
import sys
import time
import threading
from datetime import datetime
from pynput import keyboard
import os
import tarfile
import base64
import math

class KeyboardListener: 
    def __init__(self, on_press_callback=None, on_release_callback=None):
        self.on_press_callback = on_press_callback if on_press_callback is not None else {}
        self.on_release_callback = on_release_callback if on_release_callback is not None else {}
        self.pressed_key = None
        self.pressed_keys = set()
        self.info = {"pressed_key": self.pressed_key, "pressed_keys": self.pressed_keys}
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def on_press(self, key):
        try:
            key_str = key.char  # 일반 키
        except :
            key_str = str(key)  # 특수 키
        self.pressed_key = key_str
        self.pressed_keys.add(key_str)
        if key_str in self.on_press_callback:
            for target_function in self.on_press_callback[key_str]:
                target_function()
        self.info["pressed_key"] = self.pressed_key
        self.info["pressed_keys"] = self.pressed_keys

    def on_release(self, key):
        try:
            key_str = key.char  # 일반 키
        except :
            key_str = str(key)  # 특수 키
        self.pressed_key = None if key_str == self.pressed_key else self.pressed_key
        self.pressed_keys.discard(key_str)
        if key_str in self.on_release_callback:
            for target_function in self.on_release_callback[key_str]:
                target_function()
        self.info["pressed_key"] = self.pressed_key
        self.info["pressed_keys"] = self.pressed_keys


def get_time_now(milliseconds=True):
    if milliseconds:
        return datetime.now().strftime('%Y-%m-%dT%H-%M-%S-%f')[:-3]
    else:
        return datetime.now().strftime('%Y-%m-%dT%H-%M-%S')


def show_image(frame_queue, window_name="show_image", stop_key=None, stop_event=None, async_=True):
    if async_ :
        stop_event = threading.Event()
        thread = threading.Thread(
            target = show_image,
            kwargs={"frame_queue":frame_queue, "window_name":window_name, "stop_key":stop_key, "stop_event":stop_event, "async_":False}
        )
        thread.start()
        return stop_event
    else :
        # 창 이름 정의 및 크기 조정 가능 설정
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)  # 창 크기 조정 가능
        cv2.setWindowProperty(window_name, cv2.WND_PROP_ASPECT_RATIO, cv2.WINDOW_KEEPRATIO)
        while True:
            if len(frame_queue) > 0:
                img = frame_queue[-1]
                cv2.imshow(window_name, img)
                key = cv2.waitKey(1)
                if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1 or (stop_key is not None and key == stop_key) or stop_event.is_set():
                    break
            else :
                time.sleep(0.1)

        # cv2.destroyWindow(window_name)


def clear_output():
    if 'ipykernel' in sys.modules:
        # Jupyter Notebook 환경
        from IPython.display import clear_output as jupyter_clear_output
        jupyter_clear_output(wait=True)
    else:
        # 일반 터미널 환경
        os.system('cls' if os.name == 'nt' else 'clear')

def show_info(info_containers, show_keys=None, print_interval=0.1, ljust=10, stop_event=None, async_=True):
    if async_:
        if show_keys is None:
            show_keys = []
            for container in info_containers:
                show_keys += list(container.keys())
        stop_event = threading.Event()
        thread = threading.Thread(
            target=show_info,
            kwargs={"info_containers": info_containers, "show_keys": show_keys, "print_interval": print_interval, "ljust":ljust, "stop_event": stop_event, "async_": False},
        )
        thread.start()
        return stop_event
    
    else :
        while not stop_event.is_set():
            container_combine = {}
            for container in info_containers:
                for key in show_keys:
                    if key in container:
                        container_combine[key] = container[key]

            output = "\r|"
            for key in container_combine:
                output += f"{key}: {str(container_combine[key]).ljust(ljust)} | "
            sys.stdout.write(output)
            sys.stdout.flush()
            time.sleep(print_interval)

        sys.stdout.write(f"\r{'show info finished.....'.ljust(100)}") 
        sys.stdout.flush()

def extract_model(model_zip_path, model_folder_path=None):
    """tar.gz 모델 파일을 지정된 폴더로 추출."""
    model_folder_name = os.path.basename(model_zip_path).split('.')[0]
    if model_folder_path is None:
        model_folder_path = os.path.join(os.path.dirname(model_zip_path), model_folder_name)
    os.makedirs(model_folder_path, exist_ok=True)
    with tarfile.open(model_zip_path, 'r:gz') as tar:
        tar.extractall(model_folder_path)
    return model_folder_path


def read_image(image_path, width=None, height=None, color="rgb"):
    image = cv2.imread(image_path)

    # resize
    h, w = image.shape[:2]
    if width and height:
        image = cv2.resize(image, (width, height))
    elif width:
        ratio = width / w
        image = cv2.resize(image, (width, math.ceil(h * ratio)))
    elif height:
        ratio = height / h
        image = cv2.resize(image, (math.ceil(w * ratio), height))
    
    # color
    if color.lower() == "rgb":
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    elif color.lower() == "gray":
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)   
    
    return image


def get_image_base64(image, format=".jpg"):
    image_encoded = cv2.imencode(f".{format}", image)[1]
    image_base64 = base64.b64encode(image_encoded).decode("utf-8")
    return image_base64
