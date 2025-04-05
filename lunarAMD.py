import json
import os
import sys
import random
import platform
import hashlib
from pynput import keyboard
from termcolor import colored
import time
import ctypes

class Security:
    @staticmethod
    def random_delay(min=0.01, max=0.2):
        time.sleep(random.uniform(min, max))
    
    @staticmethod
    def obfuscate_name():
        return hashlib.md5(str(time.time()).encode()).hexdigest()[:8]

class AMD_Optimizer:
    @staticmethod
    def check_amd_hardware():
        try:
            if platform.processor().lower().find('amd') != -1:
                return True
            return False
        except:
            return False
    
    @staticmethod
    def setup_amd_environment():
        if AMD_Optimizer.check_amd_hardware():
            os.environ['HIP_VISIBLE_DEVICES'] = '0' 
            os.environ['HSA_OVERRIDE_GFX_VERSION'] = '10.3.0'
            return True
        return False

def on_release(key):
    try:
        Security.random_delay(0.01, 0.05)
        if key == keyboard.Key.f1:
            Aimbot.update_status_aimbot()
        if key == keyboard.Key.f2:
            Aimbot.clean_up()
    except NameError:
        pass
    except Exception as e:
        print(f"[SECURITY] Input handling error: {str(e)}")

def main():
    global lunar
    instance_name = Security.obfuscate_name()
    lunar = Aimbot(collect_data="collect_data" in sys.argv)
    lunar.start()

def setup():
    path = "lib/config"
    if not os.path.exists(path):
        os.makedirs(path)

    print("[INFO] In-game X and Y axis sensitivity should be the same")
    
    def prompt(prompt_str):
        valid_input = False
        while not valid_input:
            try:
                number = float(input(prompt_str))
                valid_input = True
            except ValueError:
                print("[!] Invalid Input. Make sure to enter only the number (e.g. 6.9)")
            Security.random_delay()
        return number

    xy_sens = prompt("X-Axis and Y-Axis Sensitivity (from in-game settings): ")
    targeting_sens = prompt("Targeting Sensitivity (from in-game settings): ")

    print("[INFO] Your in-game targeting sensitivity must be the same as your scoping sensitivity")
    sensitivity_settings = {
        "xy_sens": xy_sens, 
        "targeting_sens": targeting_sens, 
        "xy_scale": 10/xy_sens, 
        "targeting_scale": 1000/(targeting_sens * xy_sens)
    }

    with open('lib/config/config.json', 'w') as outfile:
        json.dump(sensitivity_settings, outfile)
    print("[INFO] Sensitivity configuration complete")

if __name__ == "__main__":
    if hasattr(sys, 'gettrace') and sys.gettrace() is not None:
        print("[SECURITY] Debugger detected - exiting")
        sys.exit(1)
        
    clear_method = random.choice([0, 1])
    if clear_method == 0:
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        print("\n" * 100)
    
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
    
    if AMD_Optimizer.setup_amd_environment():
        print(colored("[INFO] AMD hardware detected - applying optimizations", "yellow"))
    
    banner = r'''
  _                            _      _ _                  __  __ _____  
 | |                          | |    (_) |           /\   |  \/  |  __ \ 
 | |    _   _ _ __   __ _ _ __| |     _| |_ ___     /  \  | \  / | |  | |
 | |   | | | | '_ \ / _` | '__| |    | | __/ _ \   / /\ \ | |\/| | |  | |
 | |___| |_| | | | | (_| | |  | |____| | ||  __/  / ____ \| |  | | |__| |
 |______\__,_|_| |_|\__,_|_|  |______|_|\__\___| /_/    \_\_|  |_|_____/ 
    '''
    print(colored(banner, "green"))
    
    print(colored('To get full version of Lunar V2, visit https://gannonr.com/lunar OR join the discord: discord.gg/aiaimbot\n', "red"))
    print(colored('Lunar Lite was modified by github.com/eteb to support AMD systems exclusively and reduce detection risk.\n', "green"))

    check_files = ["lib/config/config.json", "lib/data"]
    random.shuffle(check_files)
    
    path_exists = os.path.exists(check_files[0])
    if not path_exists or ("setup" in sys.argv):
        if not path_exists:
            print("[!] Sensitivity configuration is not set")
        setup()
    
    if "collect_data" in sys.argv and not os.path.exists(check_files[1]):
        os.makedirs("lib/data")
    
    Security.random_delay(0.1, 0.5)
    from lib.aimbot import Aimbot
    
    listener = keyboard.Listener(on_release=on_release)
    listener.name = Security.obfuscate_name()
    listener.start()
    
    Security.random_delay(0.2, 0.5)
    main()