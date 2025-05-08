import os
import importlib.util

def get_module_content(module_name):
    # 모듈 스펙 가져오기
    spec = importlib.util.find_spec(module_name)
    if spec and spec.origin:
        module_path = spec.origin
        # print(f"Module Path: {module_path}")
        
        # 파일 내용 읽기
        with open(module_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content

# 파일 경로 확인 및 내용 가져오기
origin_content = get_module_content(
    "aicastle.deepracer.vehicle.api.vehicle_control_module_content.origin"
)

custom_content = get_module_content(
    "aicastle.deepracer.vehicle.api.vehicle_control_module_content.custom"
)