import ctypes
import cv2
import json
import math
import mss
import os
import sys
import time
import torch
import numpy as np
import uuid
import win32api
from termcolor import colored
from ultralytics import YOLO
import random
import hashlib
import platform

class AMDSecurity:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AMDSecurity, cls).__new__(cls)
            cls._instance.init_security()
        return cls._instance
    
    def init_security(self):
        self.obfuscated_names = {}
        self.last_activity_time = time.time()
        self.random_delays_enabled = True
        self.amd_optimized = self._check_amd_hardware()
        
        if self.amd_optimized:
            self._setup_amd_environment()
    
    def _check_amd_hardware(self):
        try:
            if platform.processor().lower().find('amd') != -1:
                return True
            if torch.cuda.is_available():
                device_name = torch.cuda.get_device_name(0).lower()
                if 'amd' in device_name or 'radeon' in device_name:
                    return True
            return False
        except:
            return False
    
    def _setup_amd_environment(self):
        try:
            os.environ['HIP_VISIBLE_DEVICES'] = '0'
            os.environ['HSA_OVERRIDE_GFX_VERSION'] = '10.3.0'
            torch.backends.opt_einsum.enabled = False
            torch.backends.cudnn.benchmark = True
            torch.backends.cudnn.deterministic = False
        except Exception as e:
            print(f"[AMD] Optimization error: {str(e)}")
    
    def random_delay(self, min=0.01, max=0.1):
        if self.random_delays_enabled:
            time.sleep(random.uniform(min, max))
    
    def obfuscate_name(self, original):
        if original not in self.obfuscated_names:
            self.obfuscated_names[original] = hashlib.sha256(
                f"{original}{time.time()}".encode()
            ).hexdigest()[:12]
        return self.obfuscated_names[original]

def get_screen_res():
    try:
        user32 = ctypes.windll.user32
        screensize = {
            'X': user32.GetSystemMetrics(0),
            'Y': user32.GetSystemMetrics(1)
        }
        return screensize
    except:
        return {'X': 1920, 'Y': 1080}

screensize = get_screen_res()
screen_res_x = screensize['X']
screen_res_y = screensize['Y']
screen_x = int(screen_res_x / 2)
screen_y = int(screen_res_y / 2)

aim_height = random.randint(8, 12)
fov = 350 + random.randint(-10, 10)
confidence = 0.45
use_trigger_bot = True

class ObfuscatedInput:
    def __init__(self):
        self.security = AMDSecurity()
        self.PUL = ctypes.POINTER(ctypes.c_ulong)
        
        class KeyBdInput(ctypes.Structure):
            _fields_ = [(self.security.obfuscate_name("wVk"), ctypes.c_ushort),
                        (self.security.obfuscate_name("wScan"), ctypes.c_ushort),
                        (self.security.obfuscate_name("dwFlags"), ctypes.c_ulong),
                        (self.security.obfuscate_name("time"), ctypes.c_ulong),
                        (self.security.obfuscate_name("dwExtraInfo"), self.PUL)]

        class HardwareInput(ctypes.Structure):
            _fields_ = [(self.security.obfuscate_name("uMsg"), ctypes.c_ulong),
                        (self.security.obfuscate_name("wParamL"), ctypes.c_short),
                        (self.security.obfuscate_name("wParamH"), ctypes.c_ushort)]

        class MouseInput(ctypes.Structure):
            _fields_ = [(self.security.obfuscate_name("dx"), ctypes.c_long),
                        (self.security.obfuscate_name("dy"), ctypes.c_long),
                        (self.security.obfuscate_name("mouseData"), ctypes.c_ulong),
                        (self.security.obfuscate_name("dwFlags"), ctypes.c_ulong),
                        (self.security.obfuscate_name("time"), ctypes.c_ulong),
                        (self.security.obfuscate_name("dwExtraInfo"), self.PUL)]

        class Input_I(ctypes.Union):
            _fields_ = [(self.security.obfuscate_name("ki"), KeyBdInput),
                        (self.security.obfuscate_name("mi"), MouseInput),
                        (self.security.obfuscate_name("hi"), HardwareInput)]

        class Input(ctypes.Structure):
            _fields_ = [(self.security.obfuscate_name("type"), ctypes.c_ulong),
                        (self.security.obfuscate_name("ii"), Input_I)]

        self.KeyBdInput = KeyBdInput
        self.HardwareInput = HardwareInput
        self.MouseInput = MouseInput
        self.Input_I = Input_I
        self.Input = Input

class Aimbot:
    security = AMDSecurity()
    extra = ctypes.c_ulong(0)
    ii_ = ObfuscatedInput().Input_I()
    screen = mss.mss()
    pixel_increment = 1
    
    try:
        with open("lib/config/config.json") as f:
            sens_config = json.load(f)
    except:
        sens_config = {"xy_scale": 1.0, "targeting_scale": 1.0}
    
    aimbot_status = colored("ENABLED", 'green')

    def __init__(self, box_constant=fov, collect_data=False, mouse_delay=0.0009):
        self.box_constant = box_constant
        self.security.random_delay(0.1, 0.3)
        
        print("[INFO] Loading the neural network model")
        
        if self.security.amd_optimized:
            torch.backends.opt_einsum.enabled = False
            os.environ['HIP_VISIBLE_DEVICES'] = '0'
            self.model = YOLO('lib/best.pt').half()
        else:
            self.model = YOLO('lib/best.pt')
        
        if torch.cuda.is_available():
            device_name = torch.cuda.get_device_name(0)
            print(colored(f"GPU ACCELERATION [ENABLED] on {device_name}", "green"))
            if 'amd' in device_name.lower() or 'radeon' in device_name.lower():
                torch.backends.cudnn.benchmark = True
        else:
            print(colored("[!] GPU ACCELERATION IS UNAVAILABLE", "red"))
            print(colored("[!] Running on CPU - performance will be reduced", "red"))

        self.conf = confidence
        self.iou = 0.45
        self.collect_data = collect_data
        self.mouse_delay = mouse_delay
        self.last_prediction_time = 0
        self.prediction_interval = random.uniform(0.01, 0.03)

        print("\n[INFO] PRESS 'F1' TO TOGGLE AIMBOT\n[INFO] PRESS 'F2' TO QUIT")

    @staticmethod
    def update_status_aimbot():
        if Aimbot.aimbot_status == colored("ENABLED", 'green'):
            Aimbot.aimbot_status = colored("DISABLED", 'red')
        else:
            Aimbot.aimbot_status = colored("ENABLED", 'green')
        sys.stdout.write("\033[K")
        print(f"[!] AIMBOT IS [{Aimbot.aimbot_status}]", end="\r")
        Aimbot.security.random_delay()

    @staticmethod
    def left_click():
        ctypes.windll.user32.mouse_event(0x0002)
        Aimbot.sleep(0.0001)
        ctypes.windll.user32.mouse_event(0x0004)
        Aimbot.security.random_delay(0.01, 0.05)

    @staticmethod
    def sleep(duration, get_now=time.perf_counter):
        if duration == 0:
            return
        now = get_now()
        end = now + duration
        while now < end:
            now = get_now()

    @staticmethod
    def is_aimbot_enabled():
        return Aimbot.aimbot_status == colored("ENABLED", 'green')

    @staticmethod
    def is_shooting():
        try:
            return win32api.GetKeyState(0x01) in (-127, -128)
        except:
            return False
    
    @staticmethod
    def is_targeted():
        try:
            return win32api.GetKeyState(0x02) in (-127, -128)
        except:
            return False

    @staticmethod
    def is_target_locked(x, y):
        threshold = 5 + random.randint(-1, 1)
        return (screen_x - threshold <= x <= screen_x + threshold and 
                screen_y - threshold <= y <= screen_y + threshold)

    def move_crosshair(self, x, y):
        if not Aimbot.is_targeted():
            return

        scale = Aimbot.sens_config["targeting_scale"] * random.uniform(0.95, 1.05)
        
        for rel_x, rel_y in Aimbot.interpolate_coordinates_from_center((x, y), scale):
            input_obj = ObfuscatedInput().Input(
                ctypes.c_ulong(0), 
                ObfuscatedInput().Input_I(mi=ObfuscatedInput().MouseInput(
                    rel_x, rel_y, 0, 0x0001, 0, ctypes.pointer(Aimbot.extra)
                ))
            )
            ctypes.windll.user32.SendInput(1, ctypes.byref(input_obj), ctypes.sizeof(input_obj))
            Aimbot.sleep(self.mouse_delay * random.uniform(0.8, 1.2))

    @staticmethod
    def interpolate_coordinates_from_center(absolute_coordinates, scale):
        diff_x = (absolute_coordinates[0] - screen_x) * scale/Aimbot.pixel_increment
        diff_y = (absolute_coordinates[1] - screen_y) * scale/Aimbot.pixel_increment
        length = int(math.dist((0,0), (diff_x, diff_y)))
        if length == 0: 
            return
        
        unit_x = (diff_x/length) * Aimbot.pixel_increment * random.uniform(0.98, 1.02)
        unit_y = (diff_y/length) * Aimbot.pixel_increment * random.uniform(0.98, 1.02)
        
        x = y = sum_x = sum_y = 0
        for k in range(0, length):
            sum_x += x
            sum_y += y
            x, y = round(unit_x * k - sum_x), round(unit_y * k - sum_y)
            yield x, y

    def start(self):
        print("[INFO] Beginning screen capture")
        Aimbot.update_status_aimbot()
        half_screen_width = ctypes.windll.user32.GetSystemMetrics(0)/2
        half_screen_height = ctypes.windll.user32.GetSystemMetrics(1)/2
        
        box_size = self.box_constant * random.uniform(0.98, 1.02)
        detection_box = {
            'left': int(half_screen_width - box_size//2),
            'top': int(half_screen_height - box_size//2),
            'width': int(box_size),
            'height': int(box_size)
        }

        while True:
            current_time = time.perf_counter()
            if current_time - self.last_prediction_time < self.prediction_interval:
                time.sleep(0.001)
                continue
                
            self.last_prediction_time = current_time
            start_time = time.perf_counter()
            
            try:
                initial_frame = Aimbot.screen.grab(detection_box)
                frame = np.array(initial_frame, dtype=np.uint8)
                if frame is None or frame.size == 0:
                    continue
                    
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                
                if random.random() > 0.05:
                    boxes = self.model.predict(
                        source=frame, 
                        verbose=False, 
                        conf=self.conf, 
                        iou=self.iou, 
                        half=self.security.amd_optimized
                    )
                    result = boxes[0]
                else:
                    result = None
                
                if result and len(result.boxes.xyxy) != 0:
                    least_crosshair_dist = closest_detection = player_in_frame = False
                    
                    for box in result.boxes.xyxy:
                        x1, y1, x2, y2 = map(int, box)
                        x1y1 = (x1, y1)
                        x2y2 = (x2, y2)
                        height = y2 - y1
                        
                        aim_offset = random.uniform(0.9, 1.1)
                        relative_head_X = int((x1 + x2)/2)
                        relative_head_Y = int((y1 + y2)/2 - height/(aim_height * aim_offset))
                        
                        own_player = (x1 < 15 or 
                                     (x1 < self.box_constant/5 and 
                                      y2 > self.box_constant/1.2))

                        crosshair_dist = math.dist(
                            (relative_head_X, relative_head_Y), 
                            (self.box_constant/2, self.box_constant/2)
                        )

                        if not least_crosshair_dist:
                            least_crosshair_dist = crosshair_dist

                        if crosshair_dist <= least_crosshair_dist and not own_player:
                            least_crosshair_dist = crosshair_dist
                            closest_detection = {
                                "x1y1": x1y1,
                                "x2y2": x2y2,
                                "relative_head_X": relative_head_X,
                                "relative_head_Y": relative_head_Y
                            }

                        if own_player and not player_in_frame:
                            player_in_frame = True

                    if closest_detection:
                        if random.random() > 0.1:
                            cv2.circle(
                                frame, 
                                (closest_detection["relative_head_X"], closest_detection["relative_head_Y"]), 
                                5, (115, 244, 113), -1
                            )
                            cv2.line(
                                frame, 
                                (closest_detection["relative_head_X"], closest_detection["relative_head_Y"]), 
                                (self.box_constant//2, self.box_constant//2), 
                                (244, 242, 113), 2
                            )

                        absolute_head_X = closest_detection["relative_head_X"] + detection_box['left']
                        absolute_head_Y = closest_detection["relative_head_Y"] + detection_box['top']
                        x1, y1 = closest_detection["x1y1"]

                        if Aimbot.is_target_locked(absolute_head_X, absolute_head_Y):
                            if use_trigger_bot and not Aimbot.is_shooting():
                                Aimbot.left_click()

                            if random.random() > 0.2:
                                cv2.putText(
                                    frame, "LOCKED", (x1 + 40, y1), 
                                    cv2.FONT_HERSHEY_DUPLEX, 0.5, (115, 244, 113), 2
                                )
                        else:
                            if random.random() > 0.2:
                                cv2.putText(
                                    frame, "TARGETING", (x1 + 40, y1), 
                                    cv2.FONT_HERSHEY_DUPLEX, 0.5, (115, 113, 244), 2
                                )

                        if Aimbot.is_aimbot_enabled():
                            Aimbot.move_crosshair(self, absolute_head_X, absolute_head_Y)

                if random.random() > 0.2:
                    fps = int(1/(time.perf_counter() - start_time))
                    cv2.putText(
                        frame, f"FPS: {fps}", (5, 30), 
                        cv2.FONT_HERSHEY_DUPLEX, 1, (113, 116, 244), 2
                    )
                
                if random.random() > 0.1:
                    cv2.imshow("Lunar Vision", frame)
                
                if cv2.waitKey(1) & 0xFF == ord('0'):
                    break
                    
            except Exception as e:
                print(f"[ERROR] Frame processing error: {str(e)}")
                continue

    @staticmethod
    def clean_up():
        print("\n[INFO] F2 WAS PRESSED. QUITTING...")
        try:
            Aimbot.screen.close()
        except:
            pass
        os._exit(0)

if __name__ == "__main__":
    print("You are in the wrong directory and are running the wrong file; you must run lunar.py")
