import logging
import sys
import requests
import urllib3
import json
import time
import cv2
import numpy as np
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bs4 import BeautifulSoup
import os
import threading
from collections import deque
from pynput import keyboard
from datetime import datetime
import paramiko
import time
from tqdm import tqdm


from aicastle.deepracer.vehicle.api.controller import (
    DiscreteController,
    ContinuousController,
    KeyboardController
)
from aicastle.deepracer.vehicle.api.constant import (
    INFERENCE_IMG_HEIGHT,
    INFERENCE_IMG_WIDTH,
    MAX_IMG_HEIGHT,
    MAX_IMG_WIDTH,
    DEFAULT_IMG_HEIGHT,
    DEFAULT_IMG_WIDTH
)
from aicastle.deepracer.vehicle.api.ssh import (
    RebootTrigger,
    ssh_connect,
    ssh_sudo_command,
    ssh_remote_content_update,
    vehicle_control_module_content_update
)
from aicastle.deepracer.vehicle.api.utils import (
    KeyboardListener,
    get_time_now,
    show_image,
    show_info
)


logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logging.getLogger().setLevel(logging.INFO)

class DeepracerVehicleApiError(Exception):
	pass


def get_csrf_token(session, URL):
    response = session.get(URL, verify=False, timeout=10)  # Cannot verify with Deep Racer
    # print(response.text)
    soup = BeautifulSoup(response.text, 'lxml')
    csrf_token = soup.select_one('meta[name="csrf-token"]')['content']
    return csrf_token

def get_headers(csrf_token, URL):
    headers = {
        'X-CSRFToken': csrf_token,
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
        "referer": URL + "/home",
        "origin": URL,
        "accept-encoding": "gzip, deflate, br",
        "content-type": "application/json;charset=UTF-8",
        "accept": "*/*",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "accept-language": "en-US,en;q=0.9",
        "x-requested-with": "XMLHttpRequest"
    }
    return headers



class VehicleClient:
    def __init__(self, 
            ip, 
            password, 
            speed_percent=50,
            speed_percent_increase=1,
            width=INFERENCE_IMG_WIDTH,   # or DEFAULT_IMG_WIDTH
            height=INFERENCE_IMG_HEIGHT,   # or DEFAULT_IMG_HEIGHT
            stream_chunk_size=1024,
            frame_queue_maxlen=10,
            max_human_angle=30,
            max_human_speed=4,
            ssh_password='DeepRacer111!!!',
            ssh_module_update=False,
            ssh_module_update_custom=True,
        ):

        ########### 초기화 ###########
        self.ip = ip.strip()
        self.URL = "https://" + self.ip
        self.password = password
        self.ssh_password = ssh_password

        # step 1. 로그인
        self.login(retry=1, timeout=10)

        # step 2. vehicle_control_module 수정
        if ssh_module_update:
            original_isSshEnabled = self.is_ssh_enabled()
            self.enable_ssh()
            if not self.is_ssh_default_password_changed():
                self.reset_ssh_password(new_password=self.ssh_password)
            reboot_trigger = vehicle_control_module_content_update(
                hostname=self.ip, 
                username="deepracer", 
                password=self.ssh_password, 
                custom=ssh_module_update_custom
            )
            if original_isSshEnabled:
                self.enable_ssh()
            else :
                self.disable_ssh()
            if reboot_trigger:
                reboot_trigger.run()  # 재부팅
                self.login(retry=50, timeout=5)  # 재로그인

        ########### 설정 ###########
        self.speed_percent = speed_percent
        self.speed_percent_increase = speed_percent_increase
        self.width = width
        self.height = height
        self.stream_chunk_size = stream_chunk_size
        self.frame_queue_maxlen = frame_queue_maxlen
        self.max_human_angle = max_human_angle
        self.max_human_speed = max_human_speed

        # information
        self.info = {"ip": self.ip}

        # stream 데이터 가져오기 (실시간)
        self.get_stream()
        self.fetch_stream()
        
        # 배터리 레벨 모니터링 (실시간)
        self.get_battery_level()
        
        #  usb 연결 상태 모니터링 (실시간)
        self.get_usb_connected()

        # 센서 상태 모니터링 (실시간)
        self.get_sensor_status()

        # drive 초기화
        self.model_loading_status = None
        self.model = None
        self.drive_mode = None
        self.last_move_kwargs = {"angle":0, "speed":0}
        self.set_speed_percent(self.speed_percent)
        self.get_calibration_angle()
        self.get_calibration_speed()

        #     "ip": self.ip,
        #     "speed_percent": self.speed_percent,
        #     "drive_mode": self.drive_mode,
        #     "model": self.model,
        #     "fetch_fps": self.fetch_fps,
        #     "battery_level": self.battery_level,
        #     "usb_connected": self.usb_connected,
        #     "camera_status": self.camera_status,
        #     "lidar_status": self.lidar_status,
        #     "stereo_status": self.stereo_status,
        #     "angle_center": self.angle_center,
        #     "angle_left": self.angle_left,
        #     "angle_right": self.angle_right,
        #     "speed_stopped": self.speed_stopped,
        #     "speed_forward": self.speed_forward,
        #     "speed_backward": self.speed_backward
        # }

    def login(self, retry=1, timeout=10):
        print(f"Login to {self.ip}", end=" ")
        login_success = False
        for i in range(retry):
            print(".", end="")
            try :
                self.session = requests.Session()
                urllib3.disable_warnings()
                self.csrf_token = get_csrf_token(self.session, self.URL)
                self.headers = get_headers(self.csrf_token, self.URL)
                login_post = self.session.post(
                    url= self.URL + "/login", 
                    data={'password': self.password}, 
                    # headers = self.headers,
                    headers={
                        'X-CSRFToken': self.csrf_token,
                        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
                    }, 
                    verify=False,
                    timeout=timeout
                )
                if login_post.status_code != 200:
                    raise DeepracerVehicleApiError("Log in failed. Error message {}".format(login_post.text))
                else :
                    login_success = True
                    break
            except :
                time.sleep(timeout)

        if login_success:
            print("Success!")
            return True
        else :
            raise DeepracerVehicleApiError("Log in failed")

    ############# ssh #############
    def is_ssh_enabled(self, timeout=20):
        response = self._get(path="/api/isSshEnabled", timeout=timeout)
        if response and response.status_code == 200:
            response = response.json()
            return response['isSshEnabled']
        else :
            raise DeepracerVehicleApiError("Failed to get ssh status")
    
    def enable_ssh(self, timeout=20):
        response = self._get(path="/api/enableSsh", timeout=timeout)
        if response and response.status_code == 200:
            response = response.json()
            return response
        else :
            raise DeepracerVehicleApiError("Failed to enable ssh")

    def disable_ssh(self, timeout=20):
        response = self._get(path="/api/disableSsh", timeout=timeout)
        if response and response.status_code == 200:
            response = response.json()
            return response['isSshEnabled']
        else :
            raise DeepracerVehicleApiError("Failed to disable ssh")

    def is_ssh_default_password_changed(self, timeout=20):
        response = self._get(path="/api/isSshDefaultPasswordChanged", timeout=timeout)
        if response and response.status_code == 200:
            response = response.json()
            return response['isDefaultSshPasswordChanged']
        else :
            raise DeepracerVehicleApiError("Failed to get ssh default password status")
        
    def reset_ssh_password(self, new_password, old_password="deepracer", timeout=30):
        if self.is_ssh_default_password_changed():
            return True

        data = {"oldPassword":old_password, "newPassword":new_password}
        response = self._put(path="/api/resetSshPassword", headers=self.headers, data=data, timeout=timeout, raise_exception=True)
        if response and response.json()['success']:
            return True
        else :
            raise DeepracerVehicleApiError("Failed to reset ssh password")

    ############# stream #############
    def get_stream(self):
        image_url = self.URL + f"/route?topic=/camera_pkg/display_mjpeg&width={self.width}&height={self.height}"
        # lidar_overlay_url = f"/route?topic=/sensor_fusion_pkg/overlay_msg&width={self.width}&height={self.height}"
        # object_detection_url = f"/route?topic=/object_detection_pkg/detection_display&width={self.width}&height={self.height}"
        # qr_detection_url = f"/route?topic=/qr_detection_pkg/qr_detection_display&width={self.width}&height={self.height}"
        self.stream = self.session.get(image_url, headers=self.headers, stream=True, verify=False)
        if not self.stream.status_code == 200:
            raise Exception()

    def fetch_stream(self, async_=True, waiting_time=10):
        if async_:
            self.frame_queue = deque(maxlen=self.frame_queue_maxlen)
            self.fetch_stop_event = threading.Event()
            self.fetch_fps = None
            self.fetch_stream_thread = threading.Thread(
                target=self.fetch_stream,
                kwargs={"async_":False},
                daemon=True
            )
            self.fetch_stream_thread.start()
            s_time = time.time()
            while True:
                if len(self.frame_queue) > 0 :
                    return
                elif (time.time() - s_time) > waiting_time :
                    raise Exception()
                else :
                    time.sleep(0.1)
        else :
            byte_data = bytes()
            self.spf_deque = deque(maxlen=30)
            s_time = time.time()
            for chunk in self.stream.iter_content(chunk_size=self.stream_chunk_size):
                byte_data += chunk
                a = byte_data.find(b'\xff\xd8')
                b = byte_data.find(b'\xff\xd9')
                if a != -1 and b != -1:
                    jpg = byte_data[a:b+2]
                    byte_data = byte_data[b+2:]
                    img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    self.frame_queue.append(img)
                    f_time = time.time()
                    self.spf_deque.append(f_time-s_time)
                    fetch_spf = max(sum(self.spf_deque) / len(self.spf_deque), 0.01)
                    self.fetch_fps = round(1 / fetch_spf)
                    self.info["fetch_fps"] = self.fetch_fps
                    s_time = time.time()

                    # 평균값 내고 fps 계산
                if self.fetch_stop_event.is_set():
                    break


    ############# image #############
    def get_image(self, width=None, height=None, color='bgr'):
        width = width if width else self.width
        height = height if height else self.height
        img = self.frame_queue[-1]
        if (width != self.width) or (height != self.height):
            img = cv2.resize(img, (width, height))
        
        if color == 'bgr':
            return img
        elif color == 'rgb':
            return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        elif color == 'gray':
            return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def save_image(self, save_dir=None, format='jpg', width=None, height=None):
        if save_dir is None:
            save_dir = "data/images/"
            os.makedirs(save_dir, exist_ok=True)
        save_time = get_time_now(milliseconds=True)
        path = os.path.join(save_dir, f"{save_time}.{format}")
        img = self.get_image(width=width, height=height, color='bgr')
        cv2.imwrite(path, img)
        return path

    ############# request #############
    def _get(self, path, headers=None, timeout=10, raise_exception=False):
        url = self.URL + path
        logging.debug("> Get %s",url)
        headers = headers if headers is None else self.headers
        try :
            response = self.session.get(url=url, headers=headers, verify=False, timeout=timeout)
            return response
        except Exception as e:
            if raise_exception:
                raise e
            return None
        
    def _put(self, path, headers=None, data=None, json_content=True, timeout=10, raise_exception=False):
        url = self.URL + path
        logging.debug("> Put %s with %s",url, data)
        headers = self.headers if headers is None else headers
        data = {} if data is None else data
        try :
            if json_content:
                response = self.session.put(url, json=data, headers=headers, verify=False, timeout=timeout)
            else :
                response = self.session.put(url, data=data, headers=headers, verify=False, timeout=timeout)
            return response
        except Exception as e:
            if raise_exception:
                raise e
            return None

    ############# control #############
    def stop(self, timeout=5):
        response = self._put(path="/api/start_stop", data={'start_stop': "stop"}, timeout=timeout)
        if self.drive_mode == "manual":
            self.drive_mode = None
            self.last_move_kwargs = {"angle":0, "speed":0}
        return response

    # autonomous mode
    def start(self, timeout=5):
        response = self._put(path="/api/start_stop", data={'start_stop': "start"}, timeout=timeout)
        return response

    def get_speed_percent(self):
        return self.speed_percent

    def set_speed_percent(self, speed_percent, timeout=1):
        self.speed_percent = max(min(speed_percent, 100), 1)
        self.info["speed_percent"] = self.speed_percent
        # if self.drive_mode == "auto":
        data = {"throttle":self.speed_percent}
        self._put(path="/api/max_nav_throttle", data = data, timeout=timeout)
        if self.drive_mode == "manual":
            self.move(**self.last_move_kwargs)
        return self.speed_percent
    
    def speed_percent_up(self, speed_percent_increase=None):
        speed_percent_increase = speed_percent_increase if speed_percent_increase is not None else self.speed_percent_increase
        self.set_speed_percent(self.speed_percent + speed_percent_increase)
        return self.speed_percent
    
    def speed_percent_down(self, speed_percent_increase=None):
        speed_percent_increase = speed_percent_increase if speed_percent_increase is not None else self.speed_percent_increase
        self.set_speed_percent(self.speed_percent - speed_percent_increase)
        return self.speed_percent
    
    ############# calibration #############
    def calibration_mode(self, timeout=5):
        self.stop()
        response = self._get(path="/api/set_calibration_mode", timeout=timeout)
        self.drive_mode = "calibration"
        self.info["drive_mode"] = self.drive_mode
        return response

    def get_calibration_angle(self, timeout=5):
        if self.drive_mode != "calibration":
            self.calibration_mode()
        response = self._get(path="/api/get_calibration/angle", timeout=timeout)
        response_data = response.json()
        self.angle_center = response_data['mid']
        self.angle_left = response_data['max']
        self.angle_right = response_data['min']
        self.info["angle_center"] = self.angle_center
        self.info["angle_left"] = self.angle_left
        self.info["angle_right"] = self.angle_right
        return {"center":self.angle_center, "left":self.angle_left, "right":self.angle_right}

    def get_calibration_speed(self, timeout=5):
        if self.drive_mode != "calibration":
            self.calibration_mode()
        response = self._get(path="/api/get_calibration/throttle", timeout=timeout)
        response_data = response.json()
        self.speed_stopped = response_data['mid']
        self.speed_forward = response_data['min']
        self.speed_backward = response_data['max']
        self.info["speed_stopped"] = self.speed_stopped
        self.info["speed_forward"] = self.speed_forward
        self.info["speed_backward"] = self.speed_backward
        return {"stopped":self.speed_stopped, "forward":self.speed_forward, "backward":self.speed_backward}
    
    def set_calibration_angle(self, center=None, left=None, right=None, polarity=1, timeout=5):
        self.get_calibration_angle()
        data = {
            "max": left if left is not None else self.angle_left,
            "mid": center if center is not None else self.angle_center,
            "min": right if right is not None else self.angle_right,
            "polarity": polarity
        }
        self._put(path="/api/set_calibration/angle", data=data, timeout=timeout)
        return self.get_calibration_angle()
    
    def set_calibration_speed(self, stopped=None, forward=None, backward=None, polarity=-1, timeout=5):
        self.get_calibration_speed()
        data = {
            "max": backward if backward is not None else self.speed_backward,
            "mid": stopped if stopped is not None else self.speed_stopped,
            "min": forward if forward is not None else self.speed_forward,
            "polarity": polarity
        }
        self._put(path="/api/set_calibration/throttle", data=data, timeout=timeout)
        return self.get_calibration_speed()

    ##### auto mode
    def auto_mode(self, timeout=1):
        self.stop()
        response = self._put(path="/api/drive_mode",data={'drive_mode': "auto"}, timeout=timeout)
        self.drive_mode = "auto"
        self.info["drive_mode"] = self.drive_mode
        self.set_speed_percent(self.speed_percent)
        return response
                
    ##### manual mode
    def manual_mode(self, timeout=2):
        self.stop()
        response = self._put(path="/api/drive_mode",data={'drive_mode': "manual"}, timeout=timeout)
        self.drive_mode = "manual"
        self.last_move_kwargs = {"angle":0, "speed":0}
        self.info["drive_mode"] = self.drive_mode
        self.start()
        return response
    
    def move(self, angle, speed, scale='human', timeout=1):
        if self.drive_mode != "manual":
            self.manual_mode()

        self.last_move_kwargs = {"angle":angle, "speed":speed, "scale":scale, "timeout":timeout}
        if scale == 'human':
            angle = angle / self.max_human_angle
            speed = speed / self.max_human_speed
        elif scale == 'robot':
            angle = angle
            speed = speed
        else:
            raise DeepracerVehicleApiError("Invalid scale")
        data = {'angle': -max(-1, min(1, angle)), 'throttle': -max(-1, min(1, speed)), "max_speed":self.speed_percent / 100}
        response = self._put(path="/api/manual_drive", data = data, timeout=timeout)
        return response

    def move_forward(self, duration=1):
        self.move(0, 0.7, scale='robot')
        time.sleep(duration)
        self.move(0, 0, scale='robot')

    def move_backward(self, duration=1):
        self.move(0, -0.7, scale='robot')
        time.sleep(duration)
        self.move(0, 0, scale='robot')

    def move_left(self, duration=1):
        self.move(1, 0.7, scale='robot')
        time.sleep(duration)
        self.move(0, 0, scale='robot')

    def move_right(self, duration=1):        
        self.move(-1, 0.7, scale='robot')
        time.sleep(duration)
        self.move(0, 0, scale='robot')

    ############# model #############
    def get_model_list(self, timeout=5):
        response = self._get(path="/api/models", timeout=timeout)
        if response and response.status_code == 200:
            response = response.json()
            return response
        else :
            return None

    def upload_model(self, model_zip_path):
        model_file = open(model_zip_path, 'rb')
        model_basename = os.path.basename(model_zip_path)
        model_folder_name = model_basename.split('.')[0]
        headers = self.headers.copy()
        multipart_data = MultipartEncoder(
            fields={
                # a file upload field
                'file': (model_basename, model_file, None)
            }
        )
        headers['content-type'] = multipart_data.content_type
        # response = self.session.put(self.URL + "/api/uploadModels", data=multipart_data, headers=headers, verify=False, timeout=60)
        response = self._put(path="/api/uploadModels", headers=headers, data=multipart_data, json_content=False, timeout=60)
        if response and response.json()['success']:
            return model_folder_name
        else :
            raise DeepracerVehicleApiError("Failed to upload model")
    
    def uploaded_model_list(self, timeout=5):
        response = self._get(path="/api/uploaded_model_list", timeout=timeout)
        if response and response.status_code == 200:
            response = response.json()
            return {model_info["name"]:model_info for model_info in response}
        else :
            raise DeepracerVehicleApiError("Failed to get uploaded model list")

    def is_model_loading(self, timeout=5):
        response = self._get(path="/api/isModelLoading", timeout=timeout)
        if response and response.status_code == 200:
            response = response.json()
            model_loading_status = response['isModelLoading']
            self.model_loading_status = model_loading_status
            return model_loading_status
        else :
            raise DeepracerVehicleApiError("Failed to get model loading status")

    def load_model(self, model_folder_name, model_name='model'):
        # auto mode로 변경
        if self.drive_mode != 'auto':
            response = self.auto_mode(timeout=10)
            if not response or response.status_code != 200:
                raise DeepracerVehicleApiError("Failed to set auto mode")
        else :
            self.stop()
        
        # 이미 로드된 모델인지 확인인
        if self.model_loading_status == 'loaded':
            if self.model == model_folder_name:
                return

        # 모델 로드
        response = self._put(path=f"/api/models/{model_folder_name}/{model_name}", timeout=10)
        if response and response.status_code == 200:
            # 모델 로드 확인
            loaded = False
            for i in range(100):
                try :
                    model_loading_status = self.is_model_loading()
                except :
                    time.sleep(0.5)
                    continue
                
                if model_loading_status == 'loaded':
                    loaded = True
                    self.model = model_folder_name
                    self.info["model"] = self.model
                    break  
                elif model_loading_status == 'loading':
                    time.sleep(0.5)
                elif model_loading_status == 'error':
                    raise DeepracerVehicleApiError("Failed to load model")
            if not loaded:
                raise DeepracerVehicleApiError("Failed to load model")
        else:
            raise DeepracerVehicleApiError("Failed to load model")


    ############ deviece info ############
    def get_battery_level(self, async_=True, timeout=5):
        if async_ :
            self.battery_level = None
            thread = threading.Thread(
                target=self.get_battery_level,
                kwargs={"async_":False, "timeout":timeout}
            )
            thread.start()
        else :
            while True :
                response = self._get(path="/api/get_battery_level", timeout=timeout)
                if response and response.status_code == 200:
                    response = response.json()
                    self.battery_level = response['battery_level']
                else :
                    self.battery_level = None

                self.info["battery_level"] = self.battery_level 
                time.sleep(timeout)

    def get_usb_connected(self, async_=True, timeout=5):
        if async_ :
            self.usb_connected = None
            thread = threading.Thread(
                target=self.get_usb_connected,
                kwargs={"async_":False, "timeout":timeout}
            )
            thread.start()
        else :
            while True :
                response = self._get(path="/api/is_usb_connected", timeout=timeout)
                if response and response.status_code == 200:
                    response = response.json()
                    self.usb_connected = response['is_usb_connected']
                else :
                    self.usb_connected = None

                self.info["usb_connected"] = self.usb_connected
                time.sleep(timeout)

    def get_sensor_status(self, async_=True, timeout=5):
        if async_ :
            self.camera_status = None
            self.lidar_status = None
            self.stereo_status = None
            thread = threading.Thread(
                target=self.get_sensor_status,
                kwargs={"async_":False, "timeout":timeout}
            )
            thread.start()
        else :
            while True :
                response = self._get(path="/api/get_sensor_status", timeout=timeout)
                if response and response.status_code == 200:
                    response = response.json()
                    self.camera_status = response['camera_status']
                    self.lidar_status = response['lidar_status']
                    self.stereo_status = response['stereo_status']
                else :
                    self.camera_status = None
                    self.lidar_status = None
                    self.stereo_status = None

                self.info["camera_status"] = self.camera_status
                self.info["lidar_status"] = self.lidar_status
                self.info["stereo_status"] = self.stereo_status
                time.sleep(timeout)