import boto3
import os
from datetime import datetime, timezone, timedelta
import json
import pytz
import subprocess
import platform
from pathlib import Path
import yaml
import paramiko
import pandas as pd
import time
from matplotlib import pyplot as plt
from IPython.display import display

from dotenv import load_dotenv
load_dotenv()

class DRfCAWSClient:
    def __init__(self, config=None):
        if config is None :
            with open('config.yml') as f:
                self.config = yaml.safe_load(f)
        else :
            self.config = config

        if self.config['ec2-user'] is None:
            self.config['ec2-user'] = "ubuntu"

        self.ec2 = boto3.client('ec2',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=self.config['region']
        )

        self.s3 = boto3.client('s3',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=self.config['region']
        )

        self.cloudtrail = boto3.client('cloudtrail',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=self.config['region']
        )

        self.ssh = None
        self.remote_path = f"/home/{self.config['ec2-user']}/deepracer-for-cloud"
        self.view_url = "http://aws-deepracer-school.s3.us-east-1.amazonaws.com/DRfC-multi-view.html"
        
    def get_instance_state(self):
        response = self.ec2.describe_instances(InstanceIds=[self.config['instance-id']])
        return response['Reservations'][0]['Instances'][0]['State']['Name']

    def get_instance_public_ip(self):
        if self.get_instance_state() != 'running':
            raise Exception("Instance is not running.")
        response = self.ec2.describe_instances(InstanceIds=[self.config['instance-id']])
        return response['Reservations'][0]['Instances'][0]['PublicIpAddress']

    def instance_wait_until_running(self):
        waiter = self.ec2.get_waiter('instance_running')
        waiter.wait(InstanceIds=[self.config['instance-id']])

    def instance_wait_until_stopped(self):
        waiter = self.ec2.get_waiter('instance_stopped')
        waiter.wait(InstanceIds=[self.config['instance-id']])

    def instance_wait_until_terminated(self):
        waiter = self.ec2.get_waiter('instance_terminated')
        waiter.wait(InstanceIds=[self.config['instance-id']])

    def start_instance(self, wait=True):
        self.ec2.start_instances(InstanceIds=[self.config['instance-id']])
        if wait:
            self.instance_wait_until_running()
        return self.get_instance_state()

    def stop_instance(self, wait=True):
        self.ec2.stop_instances(InstanceIds=[self.config['instance-id']])
        if wait:
            self.instance_wait_until_stopped()
        return self.get_instance_state()

    def terminate_instance(self, wait=True):
        self.ec2.terminate_instances(InstanceIds=[self.config['instance-id']])
        if wait:
            self.instance_wait_until_terminated(self.config['instance-id'])
        return self.get_instance_state()

    def get_s3_bucket_url(self):
        return f"https://{self.config["region"]}.console.aws.amazon.com/s3/buckets/{self.config['s3-bucket']}"

    def get_cloudtrail_events(self, start_utc=None):
        end_time = datetime.now(timezone.utc)
        if start_utc is None:
            if self.config["start-utc"] is None:
                start_time = end_time - timedelta(days=90)
            else :
                start_time = datetime.strptime(self.config["start-utc"], "%Y-%m-%dT%H:%M:%SZ")
        else :
            start_time = datetime.strptime(self.config["start-utc"], "%Y-%m-%dT%H:%M:%SZ")

        # 이벤트 이름으로 필터
        events = []
        for event_name in ["StartInstances", "StopInstances"]:
            response = self.cloudtrail.lookup_events(
                LookupAttributes=[
                    {
                        'AttributeKey': 'EventName',
                        'AttributeValue': event_name
                    },
                ],
                StartTime=start_time,
                EndTime=end_time
            )
            events.extend(response.get('Events', []))

        return events

    def calculate_instance_running_time(self, events=None, start_utc=None, instance_id=None, unit="hour", _print=False, print_tz_name="Asia/Seoul"):
        if events is None:
            events = self.get_cloudtrail_events(start_utc)
        if instance_id is None:
            instance_id = self.config['instance-id']
        
        ############ events 필터링 ############
        filtered_events = []
        for event in events:
            cloudtrail_event = event['CloudTrailEvent']
            detail = json.loads(cloudtrail_event)
            request_params = detail.get('requestParameters', {})
            instances_set = request_params.get("instancesSet", {})
            items = instances_set.get("items", [])
            instance_ids = []
            for item in items:
                if "instanceId" in item:
                    instance_ids.append(item["instanceId"])

            if instance_id in instance_ids:
                filtered_events.append(event)
        filtered_events.sort(key=lambda x: x['EventTime'])
        
        ############ 총 실행 시간 계산 ############
        if _print:
            try:
                tz = pytz.timezone(print_tz_name)
            except Exception as e:
                tz = timezone.utc

        total_running_time = timedelta(0)
        last_start_time = None
        for event in filtered_events:
            event_time = event['EventTime']
            event_name = event['EventName']

            if event_name == "StartInstances":
                if last_start_time is None:
                    last_start_time = event_time
                    # 한국 시간대로 변환하여 출력
                    if _print:
                        print(f"Start at {event_time.astimezone(tz)}")
                else:
                    if _print:
                        print(f"연속된 StartInstances 이벤트 발견. 이전 Start at {last_start_time.astimezone(tz)}, 현재 Start at {event_time.astimezone(tz)}. 이전 Start를 무시하고 최신 Start로 갱신하지 않습니다.")
            elif event_name == "StopInstances":
                if last_start_time is not None:
                    if event_time > last_start_time:
                        running_duration = event_time - last_start_time
                        total_running_time += running_duration
                        last_start_time = None
                        if _print:
                            print(f"Stop at {event_time.astimezone(tz)}, Duration: {running_duration}")
                    else:
                        if _print:
                            print(f"StopInstances 이벤트의 시간이 StartInstances 이전입니다. Stop at {event_time.astimezone(tz)}, Start at {last_start_time.astimezone(tz)}. 무시합니다.")
                else:
                    if _print:
                        print(f"StopInstances 이벤트가 StartInstances 없이 발생했습니다. Stop at {event_time.astimezone(tz)}. 무시합니다.")

        # 인스턴스가 현재 실행 중인 경우, 마지막 Start부터 현재까지의 시간을 추가
        if last_start_time is not None:
            end_time = datetime.now(timezone.utc)
            running_duration = end_time - last_start_time
            if running_duration.total_seconds() > 0:
                total_running_time += running_duration
                if _print:
                    print(f"Instance is currently running. Adding running duration from {last_start_time.astimezone(tz)} to {end_time.astimezone(tz)}: {running_duration}")
            else:
                if _print:
                    print(f"현재 시간보다 StartInstances 이벤트 시간이 더 큽니다. Start at {last_start_time.astimezone(tz)}, End at {end_time.astimezone(tz)}. 무시합니다.")

        total_sec = total_running_time.total_seconds()
        if unit == "second":
            return total_sec
        elif unit == "minute":
            return total_sec / 60
        elif unit == "hour":
            return total_sec / 3600
        else:
            return total_running_time
    
    ######### ssh #########
    def get_ssh_connect_command(self, chmod=True): 
        if chmod:
            self.chmod_instance_key()
        public_ip = self.get_instance_public_ip()
        return (
            f"ssh -i {self.config['instance-key-path']} "
            f"-o StrictHostKeyChecking=no "
            f"-o UserKnownHostsFile=/dev/null "
            f"-o ServerAliveInterval=60 "  # 60초마다 서버에 Ping
            f"-o ServerAliveCountMax=3 "  # 3번 실패 시 종료
            f"{self.config['ec2-user'].strip()}@{public_ip}"
        )


    def chmod_instance_key(self):
        if not os.path.exists(self.config['instance-key-path']):
            raise Exception(f"key file '{self.config['instance-key-path']}' not found")
        
        os_type = platform.system().lower()
        if os_type in ["linux", "darwin"]:
            subprocess.run(f"chmod 400 {self.config['instance-key-path']}", shell=True)
        elif os_type == "windows":
            subprocess.run(f"icacls {self.config['instance-key-path']} /inheritance:r /grant:r %USERNAME%:R", shell=True)
        else :
            raise Exception(f"Unsupported OS type: {os_type}")

    def get_ssh(self, force=False, chmod=True):
        if (self.ssh is None) or force :
            if chmod:
                self.chmod_instance_key()

            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(
                hostname = self.get_instance_public_ip(),
                username = self.config['ec2-user'],
                key_filename= self.config['instance-key-path']
            )

            # keep alive
            transport = self.ssh.get_transport()
            transport.set_keepalive(30)

            # sftp
            self.sftp = self.ssh.open_sftp()

        return self.ssh


    def ssh_command(self, command, prefix=True, timeout=None):
        ssh = self.get_ssh()
        command_prefix = (
            "source ~/.bashrc && "
            "source ~/deepracer-for-cloud/bin/activate.sh && "
        )
        command = command_prefix + command if prefix else command
        # print(command)
        stdin, stdout, stderr = ssh.exec_command(command, timeout=timeout)
        exit_code = stdout.channel.recv_exit_status()
        output = stdout.read().decode()
        error = stderr.read().decode()
        if exit_code != 0:
            raise Exception(f"{error}\n{output}")

        return output

    def get_model_name(self):
        output = self.ssh_command('''grep "^DR_LOCAL_S3_MODEL_PREFIX=" ~/deepracer-for-cloud/run.env | cut -d'=' -f2''', prefix=False)
        return output.strip()

    def ssh_start_xrog(self):
        try :
            self.ssh_command("source ~/deepracer-for-cloud/utils/start-xorg.sh", timeout=10)
        except :
            pass

    def upload_best_model(self, local=True):
        command = "dr-upload-model -fb"
        command += "L" if local else ""
        self.ssh_command(command)

    def upload_car_zip(self, local=True):
        command = "dr-upload-car-zip -f"
        command += "L" if local else ""
        self.ssh_command(command)

    def upload_best_model_car_zip(self, _print=True):
        model_name_origin = self.get_model_name()
        model_name_best = model_name_origin + '-1'
        model_name_temp = model_name_origin + '-1-temp'
        print(f"[Best Model Name] {model_name_best}") if _print else None
        print("Best model uploading...", end="") if _print else None
        try :
            self.upload_best_model(local=True)
            upload_model_success = True
            print("done") if _print else None
            
        except :
            upload_model_success = False
            print("failed") if _print else None

        if upload_model_success :
            origin_DR_LOCAL_S3_MODEL_PREFIX = self.get_main_env("DR_LOCAL_S3_MODEL_PREFIX")
            self.set_main_env(DR_LOCAL_S3_MODEL_PREFIX=model_name_temp)
            origin_DR_LOCAL_S3_PRETRAINED = self.get_main_env("DR_LOCAL_S3_PRETRAINED")
            self.set_main_env(DR_LOCAL_S3_PRETRAINED=True)
            origin_DR_LOCAL_S3_PRETRAINED_PREFIX = self.get_main_env("DR_LOCAL_S3_PRETRAINED_PREFIX")
            self.set_main_env(DR_LOCAL_S3_PRETRAINED_PREFIX=model_name_best)
            origin_DR_WORKERS = self.get_main_env("DR_WORKERS")
            self.set_main_env(DR_WORKERS=1)

            prev_step_success = True
            if prev_step_success :
                try :
                    print("Start Sagemaker...", end="") if _print else None
                    self.start_training(wipes=True, retries=3, _print=False, suffix_force=True)
                    print("done") if _print else None
                except :
                    print("failed") if _print else None
                    prev_step_success = False

            self.set_main_env(force=True, DR_LOCAL_S3_MODEL_PREFIX=origin_DR_LOCAL_S3_MODEL_PREFIX)
            self.set_main_env(force=True, DR_LOCAL_S3_PRETRAINED=origin_DR_LOCAL_S3_PRETRAINED)
            self.set_main_env(force=True, DR_LOCAL_S3_PRETRAINED_PREFIX=origin_DR_LOCAL_S3_PRETRAINED_PREFIX)
            self.set_main_env(force=True, DR_WORKERS=origin_DR_WORKERS)

            if prev_step_success :
                try :
                    print("Upload car zip...", end="") if _print else None
                    self.upload_car_zip(local=True)
                    print("done") if _print else None
                except :
                    print("failed") if _print else None
                    prev_step_success = False

            try :
                print("Stop Sagemaker...", end="") if _print else None
                self.ssh_command("dr-stop-training")
                print("done") if _print else None
            except :
                print("failed") if _print else None

            try :
                print("Delete Temp Folder...", end="") if _print else None
                self.s3.delete_object(Bucket=self.config['s3-bucket'], Key=f"{model_name_temp}/")
                while True:
                    response = self.s3.list_objects_v2(Bucket=self.config['s3-bucket'], Prefix=f"{model_name_temp}/")
                    if 'Contents' not in response:
                        break

                    delete_keys = [{'Key': obj['Key']} for obj in response['Contents']]
                    self.s3.delete_objects(Bucket=self.config['s3-bucket'], Delete={'Objects': delete_keys})
                    if not response.get('NextContinuationToken'):
                        break
                print("done") if _print else None
            except :
                print("failed") if _print else None
            
            best_model_s3_url = f"https://{self.config["region"]}.console.aws.amazon.com/s3/buckets/{self.config['s3-bucket']}/{model_name_best}/"
            print(f"Finished best model uploading: {best_model_s3_url}") if _print else None
        else :
            print("Skip best model uploading car zip.") if _print else None

    def get_train_viewer_url(self):
        return self.view_url + f"?ip={self.get_instance_public_ip()}"

    def get_eval_viewer_url(self):
        if not self.is_evaluating():
            raise Exception("Evaluation is not running.")
        docker_ps_info = self.get_docker_ps_info()
        eval_info = docker_ps_info["eval"][0]
        return f"http://{self.get_instance_public_ip()}:{eval_info['port']}/stream_viewer?topic=/racecar/deepracer/kvs_stream"

    def is_training(self):
        docker_ps_info = self.get_docker_ps_info()
        if (len(docker_ps_info["train"]) > 0) or (len(docker_ps_info["rl_coach"]) > 0) or (len(docker_ps_info["sagemaker"]) > 0):
            return True
        else :
            return False
        
    def is_evaluating(self):
        docker_ps_info = self.get_docker_ps_info()
        if len(docker_ps_info["eval"]) > 0:
            return True
        else :
            return False
        
    def start_evaluation(self, _print=True):
        if self.is_evaluating():
            raise Exception("Evaluation is already running. Stop Evaluation first.")
        if self.is_training():
            raise Exception("Training is running. Stop Training first.")
        
        print(f"[Model Name] {self.get_model_name()}") if _print else None

        if self.get_main_env("DR_HOST_X") == "True":
            print("start xrog...", end="") if _print else None
            self.ssh_start_xrog()
            print("done") if _print else None

        success_keyword = "agent: Starting evaluation phase"
        timeout = 120
        command = (
            "dr-stop-evaluation && "
            "dr-start-evaluation"
        )
        try :
            output = self.ssh_command_pty(command, success_keyword, timeout)
            print(f"Evaluation Viewer: {self.get_eval_viewer_url()}") if _print else None
        except :
            # 실패 시, dr-stop-evaluation 실행
            try :
                self.ssh_command("dr-stop-evaluation")
            except :
                pass
            raise Exception("Failed to start evaluation. Retry please.")


        
    def stop_evaluation(self, _print=True):
        if not self.is_evaluating():
            print("Evaluation is not running.") if _print else None
            return
        print(f"[Model Name] {self.get_model_name()}") if _print else None
        print("Stopping evaluation...") if _print else None
        self.ssh_command("dr-stop-evaluation")
        print("Evaluation stopped.") if _print else None


    def start_training(self, wipes=False, retries=2, _print=True, suffix_force=False):
        model_name = self.get_model_name().strip()
        
        if self.is_training():
            print(f"Training Viewer : {self.get_train_viewer_url()}") if _print else None
            print(f"Model S3 URL : {self.get_s3_bucket_url()}/{model_name}/") if _print else None
            raise Exception("Training is already running. Stop training first.")
        if self.is_evaluating():
            raise Exception("Evaluation is running. Stop Evaluation first.")
        
        if not suffix_force :
            if model_name[-2:] == "-1":
                raise Exception((
                    f"Model name '{model_name}' is not allowed. "
                    "Model name must not end with '-1'. "
                    "Please change the model name."
                ))

        print(f"[Model Name] {model_name}") if _print else None

        if self.get_main_env("DR_HOST_X") == "True":
            print("start xrog...", end="") if _print else None
            self.ssh_start_xrog()
            print("done") if _print else None

        command = (
            "dr-stop-training && "
            "dr-update && "
            "dr-upload-custom-files && "
            "dr-start-training"
        )
        success_keyword = "DoorMan: installing SIGINT, SIGTERM"
        timeout = 60 * 5  # 5분

        dr_workers_env = int(drfc.get_main_env("DR_WORKERS"))
        for i in range(retries):
            try:
                print(f"Trying to start training ({i+1})...", end="") if _print else None
                output = self.ssh_command_pty(command + (" -w" if wipes else ""), success_keyword, timeout)
                dr_workers_real = len(drfc.get_docker_ps_info()['train'])
                
                if dr_workers_real != dr_workers_env:
                    raise Exception(f"DR_WORKERS is not matched. Expected: {dr_workers_env}, Real: {dr_workers_real}")
                
                # 성공하면 루프 탈출
                print("done") if _print else None
                break
            except Exception as e:
                print("failed")
                if "use -w option" in str(e):
                    raise Exception((
                        f"{self.get_model_name()} already exists.\n"
                        f"Use wipes option or delete the model from S3 bucket : {self.get_s3_bucket_url()}"
                    ))
                
                if i == retries - 1:
                    # 마지막 시도 실패
                    self.stop_training(_print=False)
                    print(f"Failed to start training after {retries} retries.") if _print else None
                    
                    raise e
                
                print(f"Retrying...") if _print else None
        
        print(f"Training Viewer : {self.get_train_viewer_url()}") if _print else None
        print(f"Model S3 URL : {self.get_s3_bucket_url()}/{model_name}/") if _print else None

    def stop_training(self, upload_best=True, _print=True):
        model_name_origin = self.get_model_name()
        print(f"[Model Name] {model_name_origin}") if _print else None

        if not self.is_training():
            print("Training is not running.") if _print else None
        else :
            print("Stopping training...", end="") if _print else None
            self.ssh_command("dr-stop-training")
            print("done") if _print else None

        if upload_best:
            print()
            self.upload_best_model_car_zip(_print=_print)


    def ssh_command_pty(self, command, success_keyword, timeout=60, prefix=True):
        ssh = self.get_ssh()
        command_prefix = (
            "source ~/.bashrc && "
            "source ~/deepracer-for-cloud/bin/activate.sh && "
        )
        command = command_prefix + command if prefix else command
        # print(command)
        stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)

        channel = stdout.channel
        start_time = time.time()
        last_line = ""  # 가장 마지막으로 본 라인
        while True:
            # 1) stdout에 새 데이터가 들어왔는지 확인
            if channel.recv_ready():
                data = channel.recv(4096)  # 바이트로 받음
                data_decoded = data.decode('utf-8', errors='replace')  # 디코딩
                lines = data_decoded.split('\n')

                for line in lines:
                    if line.strip():
                        last_line = line
                    # 'Success' 키워드가 있으면 즉시 정상 종료
                    if success_keyword in line:
                        # 채널 닫아서 프로세스도 종료 시도 (tail -f 등은 강제 종료될 수 있음)
                        channel.close()
                        return last_line

            # 2) stderr에 새 데이터가 들어왔는지 확인
            #    여기선 "조금이라도 stderr가 찍히면 에러"로 판단
            if channel.recv_stderr_ready():
                err_data = channel.recv_stderr(4096)
                err_decoded = err_data.decode('utf-8', errors='replace')
                lines = err_decoded.split('\n')

                # 마지막 줄 갱신
                for line in lines:
                    if line.strip():
                        last_line = line

                # stderr에 뭔가 찍혔으니 곧바로 에러로 처리
                channel.close()
                raise Exception(last_line)
            
            # 3) 프로세스가 종료되었는지 (exit_status_ready) 확인
            #    정상(0) 종료면 True 리턴, 비정상 종료면 에러
            if channel.exit_status_ready():
                exit_code = channel.recv_exit_status()
                if exit_code == 0:
                    return last_line
                else:
                    raise Exception(last_line)

            if time.time() - start_time > timeout:
                channel.close()
                raise Exception(last_line)
            
            # 0.1초 대기 (CPU 과부하 방지)
            time.sleep(0.1)
        
    def ssh_sed(self, target_path, default_path=None, copy=False, **kwargs): 
        command = ""
        if copy:
            command += f"cp {default_path} {target_path}" + "\n"
        for key, value in kwargs.items():
            command += f'''sed -i \'s/\\(^{key}=\\).*/\\1{value}/\' {target_path}''' + "\n"

        self.ssh_command(command, prefix=False)

    def get_main_env(self, variable_name):
        system_output = drfc.ssh_command(f"grep '^{variable_name}=' ~/deepracer-for-cloud/system.env | cut -d '=' -f 2-", prefix=False).strip()
        run_output = drfc.ssh_command(f"grep '^{variable_name}=' ~/deepracer-for-cloud/run.env | cut -d '=' -f 2-", prefix=False).strip()
        env_value = system_output or run_output or None
        return env_value
    
    def set_main_env(self, copy=False, force=False, **kwargs):
        if not force :
            if self.is_training():
                raise Exception("Training is running. Stop Training first.")
            if self.is_evaluating():
                raise Exception("Evaluation is running. Stop Evaluation first.")
        
        # system.env
        env_file_path = os.path.join(self.remote_path, 'system.env')
        env_default_file_path = os.path.join(self.remote_path, 'defaults', 'template-system.env')
        self.ssh_sed(env_file_path, env_default_file_path, False, **kwargs)
        # run.env
        env_file_path = os.path.join(self.remote_path, 'run.env')
        env_default_file_path = os.path.join(self.remote_path, 'defaults', 'template-run.env')
        self.ssh_sed(env_file_path, env_default_file_path, copy, **kwargs)

    def set_subworker_env(self, worker_id, copy=False, force=False, **kwargs):
        if not force :
            if self.is_training():
                raise Exception("Training is running. Stop Training first.")
            if self.is_evaluating():
                raise Exception("Evaluation is running. Stop Evaluation first.")
        
        if not ((worker_id > 1) and isinstance(worker_id, int)):
            raise Exception("worker_id must be 2 or more int")
        
        env_file_path = os.path.join(self.remote_path, f'worker-{worker_id}.env')
        # env_default_file_path = os.path.join(self.remote_path, 'defaults', 'template-worker.env')
        env_default_file_path = os.path.join(self.remote_path, 'run.env')
        self.ssh_sed(env_file_path, env_default_file_path, copy, **kwargs)

    def ssh_echo(self, string, remote_file_path):
        command = f"echo '{string}' > {remote_file_path}"
        self.ssh_command(command, prefix=False)

    def set_reward_function(self, file_path="reward_function.py", force=False):
        if not force:
            if self.is_training():
                raise Exception("Training is running. Stop Training first.")
            if self.is_evaluating():
                raise Exception("Evaluation is running. Stop Evaluation first.")

        with open(file_path, 'r') as f:
            reward_function_str = f.read()

        remote_file_path = os.path.join(self.remote_path, "custom_files", "reward_function.py")
        command = f"cat > {remote_file_path} << EOF\n{reward_function_str}\nEOF"
        self.ssh_command(command, prefix=False)

    def set_hyperparameters(self, dict_data, force=False):
        if not force:
            if self.is_training():
                raise Exception("Training is running. Stop Training first.")
            if self.is_evaluating():
                raise Exception("Evaluation is running. Stop Evaluation first.")
        
        remote_file_path = os.path.join(self.remote_path, "custom_files", "hyperparameters.json")
        self.ssh_echo(json.dumps(dict_data), remote_file_path)

    def set_model_metadata(self, dict_data, force=False):
        if not force :
            if self.is_training():
                raise Exception("Training is running. Stop Training first.")
            if self.is_evaluating():
                raise Exception("Evaluation is running. Stop Evaluation first.")
        
        remote_file_path = os.path.join(self.remote_path, "custom_files", "model_metadata.json")
        self.ssh_echo(json.dumps(dict_data), remote_file_path)

    def cat_run_env(self):
        command = "cat ~/deepracer-for-cloud/run.env"
        print(self.ssh_command(command))

    def cat_system_env(self):
        command = "cat ~/deepracer-for-cloud/system.env"
        print(self.ssh_command(command))

    def cat_worker_env(self, worker_id):
        if not ((worker_id > 1) and isinstance(worker_id, int)):
            raise Exception("worker_id must be 2 or more int")
        command = f"cat ~/deepracer-for-cloud/worker-{worker_id}.env"
        print(self.ssh_command(command))

    def cat_hyperparameters(self):
        # json 파일을 불러와서 dict로 print
        command = "cat ~/deepracer-for-cloud/custom_files/hyperparameters.json"
        output = self.ssh_command(command)
        # print 할 때 예쁘게
        print(json.dumps(json.loads(output), indent=4))

    def cat_model_metadata(self):
        # json 파일을 불러와서 dict로 print
        command = "cat ~/deepracer-for-cloud/custom_files/model_metadata.json"
        output = self.ssh_command(command)
        print(json.dumps(json.loads(output), indent=4))
    
    def cat_reward_function(self):
        command = "cat ~/deepracer-for-cloud/custom_files/reward_function.py"
        print(self.ssh_command(command))


    def get_df_docker_ps(self):
        command = "docker ps --format '{{.ID}};{{.Image}};{{.Command}};{{.CreatedAt}};{{.Status}};{{.Ports}};{{.Names}}'"
        output = self.ssh_command(command, prefix=False)
        lines = output.strip().split('\n')
        data = [line.split(';') for line in lines if line.strip()]

        columns = ['ID', 'Image', 'Command', 'CreatedAt', 'Status', 'Ports', 'Names']
        df = pd.DataFrame(data, columns=columns)
        return df
    
    def get_docker_ps_info(self):
        df_docker_ps = self.get_df_docker_ps()
        docker_ps_info = {"train":[], "eval":[], "rl_coach":[], "sagemaker":[], "viewer":[], "analysis":[], "unknown":[]}
        df_len = df_docker_ps.shape[0]
        for i in range(df_len):
            row = df_docker_ps.iloc[i]
            port = None
            index = None
            if '-robomaker-' in row['Names']:
                if 'eval' in row['Names']:
                    container_type = 'eval'
                else :
                    container_type = 'train'
                port = row['Ports'].split('->8080/tcp')[0].split(':')[-1]
                index = row['Names'].split('-')[-1]
            elif '-rl_coach-' in row['Names']:
                container_type = 'rl_coach'
            elif '-algo-' in row['Names']:
                container_type = 'sagemaker'
            elif '-viewer-' in row['Names']:
                container_type = 'viewer'
                port = row['Ports'].split('->80/tcp')[0].split(':')[-1]
            elif 'deepracer-analysis' in row['Names']:
                container_type = 'analysis'
            else :
                container_type = 'unknown'

            docker_ps_info[container_type].append({"index":index, "port":port, "row":row})

        return docker_ps_info

    ######### mount #########
    def mount_install(self):
        os_type = platform.system().lower()
        if os_type == "linux":
            # SSHFS 설치 여부 확인
            result = subprocess.run(["which", "sshfs"], capture_output=True, text=True)
            if result.returncode != 0:
                print("Installing SSHFS...")
                subprocess.run(["sudo", "apt-get", "update"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run(["sudo", "apt-get", "install", "-y", "sshfs"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif os_type == "darwin":
            # macOS에서 Homebrew를 사용하여 SSHFS 설치 여부 확인
            result = subprocess.run(["brew", "list", "sshfs"], capture_output=True, text=True)
            if "Not installed" in result.stderr or result.returncode != 0:
                print("Installing SSHFS...")
                subprocess.run(["brew", "update"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run(["brew", "install", "sshfs"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else :
            raise Exception(f"Unsupported OS type: {os_type}")

    def is_mounted(self, mount_path='./mnt/deepracer-for-cloud'):
        mount_path = os.path.abspath(mount_path)
        result = subprocess.run(["mountpoint", "-q", mount_path])
        return result.returncode == 0

    def mount(self, mount_path='./mnt/deepracer-for-cloud', chmode=True):
        self.mount_install()
        mount_path = os.path.abspath(mount_path)
        Path(mount_path).mkdir(parents=True, exist_ok=True)

        public_ip = self.get_instance_public_ip()
        if chmode:
            self.chmod_instance_key()

        # 이미 마운트되어 있는지 확인
        if self.is_mounted(mount_path):
            print(f"Already mounted to '{mount_path}'.")
            return
        else:
            print(f"Mounting to '{mount_path}'...")

        # SSHFS를 사용하여 마운트
        sshfs_command = [
            "sshfs",
            "-o", "StrictHostKeyChecking=no",         # 호스트 키 확인 생략
            "-o", "UserKnownHostsFile=/dev/null",     # 호스트 키 저장 안함
            "-o", "reconnect",                        # 재연결 시도
            "-o", "ServerAliveInterval=15",           # 서버에 주기적인 패킷 전송
            "-o", "ServerAliveCountMax=3",            # 서버 응답 없는 경우 재연결 횟수
            "-o", f'''IdentityFile="{os.path.abspath(self.config["instance-key-path"])}"''',       # SSH 키 파일 지정
            f"{self.config['ec2-user'].strip()}@{public_ip}:{self.remote_path}",   # 원격 경로
            mount_path                             # 로컬 마운트 포인트
        ]

        # SSHFS 명령어를 백그라운드에서 실행하도록 Popen 사용
        process = subprocess.Popen(
            sshfs_command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid
        )

        # SSHFS가 제대로 마운트되었는지 확인
        stdout, stderr = process.communicate(timeout=30)  # 30초 내에 마운트 완료 여부 확인

        if process.returncode == 0:
            print(f"Successfully mounted '{public_ip}:{self.remote_path}' to '{mount_path}'.")
        else:
            print(f"Failed to mount '{public_ip}:{self.remote_path}' to '{mount_path}'.")
            print("Error Output:")
            print(stderr.decode())
            raise subprocess.CalledProcessError(
                returncode=process.returncode,
                cmd=sshfs_command,
                output=stdout,
                stderr=stderr
            )

        # subprocess.run(sshfs_command, shell=True, check=True)
        # print(f"Successfully mounted '{public_ip}:{remote_dir}' to '{local_dir}'.")

    def unmout(self, mount_path='./mnt/deepracer-for-cloud'):
        mount_path = os.path.abspath(mount_path)
        if self.is_mounted(mount_path):
            subprocess.run(["umount", mount_path], check=True)
            print(f"Successfully unmounted '{mount_path}'.")
        else:
            print(f"'{mount_path}' is not mounted.")

    ###### metrics ######
    def get_metrics_key_list(self, model_name=None, target=None):
        if model_name is None:
            model_name = self.get_model_name()
        
        response = self.s3.list_objects_v2(
            Bucket=self.config['s3-bucket'],
            Prefix=os.path.join(model_name, "metrics")
        )

        if "Contents" in response:
            metrics_key_list = [content["Key"] for content in response["Contents"]]
        else :
            metrics_key_list = []

        if target == "training":
            metrics_key_list = [key for key in metrics_key_list if "TrainingMetrics" in key]
        elif target == "evaluation":
            metrics_key_list = [key for key in metrics_key_list if "evaluation" in key]

        metrics_key_list.sort()
        return metrics_key_list

    def show_training_metrics_from_key(self, metrics_key, alpha=0.15, ma_window=10):
        data = self.s3.get_object(
            Bucket=self.config['s3-bucket'],
            Key=metrics_key
        )["Body"].read().decode("utf-8")
        data_dict = json.loads(data)
        df_metrics = pd.DataFrame(data_dict['metrics'])
        df_training = df_metrics[df_metrics['phase'] == 'training'].copy()
        df_evaluation = df_metrics[df_metrics['phase'] == 'evaluation'].copy()
        df_training['reward_score_ma'] = df_training['reward_score'].rolling(window=ma_window).mean()
        df_training['completion_percentage_ma'] = df_training['completion_percentage'].rolling(window=ma_window).mean()
        df_evaluation_group = df_evaluation.groupby('episode')

        # x축의 전체 범위 계산
        x_min = 0
        x_max = max(df_training['episode'].max(), df_evaluation['episode'].max())

        # Subplots 생성 (공유 x축 사용)
        fig, axes = plt.subplots(2, 1, figsize=(10, 10), sharex=True, constrained_layout=True)

        # reward score plot
        axes[0].scatter(df_training['episode'], df_training['reward_score'], alpha=alpha, c='green')
        axes[0].plot(df_training['episode'], df_training['reward_score_ma'], c='green', label='training')
        axes[0].scatter(df_evaluation['episode'], df_evaluation['reward_score'], alpha=alpha, c='magenta')
        axes[0].plot(df_evaluation_group['episode'].first(), df_evaluation_group['reward_score'].mean(), c='magenta', label='evaluation')
        axes[0].legend()
        axes[0].set_ylabel('reward')
        axes[0].set_title('Reward Score')
        axes[0].grid()

        # completion percentage plot
        axes[1].scatter(df_training['episode'], df_training['completion_percentage'], alpha=alpha, c='blue')
        axes[1].plot(df_training['episode'], df_training['completion_percentage_ma'], c='blue', label='training')
        axes[1].scatter(df_evaluation['episode'], df_evaluation['completion_percentage'], alpha=alpha, c='red')
        axes[1].plot(df_evaluation_group['episode'].first(), df_evaluation_group['completion_percentage'].mean(), c='red', label='evaluation')
        axes[1].legend()
        axes[1].set_ylim(0, 100)  # completion percentage는 0~100 범위로 고정
        axes[1].set_xlabel('episode')
        axes[1].set_ylabel('completion %')
        axes[1].set_title('Completion Percentage')
        axes[1].grid()

        # x축 범위 및 공유 설정
        axes[0].set_xlim(x_min, x_max)

        # 전체 플롯 표시
        plt.show()

    def show_training_metrics(self, model_name=None, worker_ids=None, alpha=0.07, ma_window=10):
        if model_name is None:
            model_name = self.get_model_name()
        print(f"[Model Name] {model_name}")

        if worker_ids is None:
            worker_ids = [1]
        elif isinstance(worker_ids, int):
            worker_ids = [worker_ids]
        elif isinstance(worker_ids, list):
            pass
        else:
            raise Exception("worker_ids must be int or list of int.")
        
        metrics_key_list = self.get_metrics_key_list(model_name, target="training")
        for worker_id in worker_ids:
            metrics_idx = worker_id - 1
            metrics_suffix = f"_{metrics_idx}" if metrics_idx != 0 else ""
            metrics_key = f"{model_name}/metrics/TrainingMetrics{metrics_suffix}.json"
            if metrics_key in metrics_key_list:
                print(f"Worker {worker_id} : {metrics_key}")
                self.show_training_metrics_from_key(metrics_key, alpha, ma_window)
            else :
                print(f"Worker {worker_id} : No metrics found.")

    def show_evaluation_metrics(self, model_name=None, job_idx=-1):
        if self.is_evaluating():
            raise Exception("Evaluation is running")
        
        if model_name is None:
            model_name = self.get_model_name()

        print(f"[Model Name] {model_name}")
        
        metrics_key_list = self.get_metrics_key_list(model_name, target="evaluation")
        if len(metrics_key_list) < 1:
            print("No evaluation metrics found.")
            return

        # df_metrics
        metrics_key = metrics_key_list[job_idx]
        data = self.s3.get_object(
            Bucket=self.config['s3-bucket'],
            Key=metrics_key
        )["Body"].read().decode("utf-8")
        data_dict = json.loads(data)
        df_metrics = pd.DataFrame(data_dict['metrics'])
        df_metrics['lap_time'] = df_metrics['elapsed_time_in_milliseconds'] / 1000
        df_metrics['total_lap_time'] = df_metrics['lap_time'].cumsum()
        df_metrics = df_metrics[['trial', 'total_lap_time', 'lap_time', 'off_track_count', 'crash_count']]
        display(df_metrics)
        
        # Job name
        metrics_basename = os.path.basename(metrics_key)
        eval_job_name = metrics_basename.split(".")[0]
        print(f"Job Name: {eval_job_name}")

        # show video url
        try :
            presigned_url = self.s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.config['s3-bucket'], 'Key': f"{model_name}/mp4/camera-pip/0-video.mp4"},
                ExpiresIn=3600
            )
            print(f"Video URL: {presigned_url}")
        except:
            print("Video not found.")
        

drfc = DRfCAWSClient()