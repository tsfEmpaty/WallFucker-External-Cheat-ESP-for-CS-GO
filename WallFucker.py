import pymem
import pymem.process
import keyboard
from colorama import init
from colorama import Fore, Style


dwEntityList = 0x4DD245C
dwGlowObjectManager = 0x531B048
m_iGlowIndex = 0x10488
m_iTeamNum = 0xF4


def greeting():
    github_link = "https://github.com/tsfEmpaty"

    print(
        Fore.RED + Style.DIM +
        f"""
         █     █░ ▄▄▄       ██▓     ██▓      █████▒█    ██  ▄████▄   ██ ▄█▀▓█████  ██▀███  
        ▓█░ █ ░█░▒████▄    ▓██▒    ▓██▒    ▓██   ▒ ██  ▓██▒▒██▀ ▀█   ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒
        ▒█░ █ ░█ ▒██  ▀█▄  ▒██░    ▒██░    ▒████ ░▓██  ▒██░▒▓█    ▄ ▓███▄░ ▒███   ▓██ ░▄█ ▒
        ░█░ █ ░█ ░██▄▄▄▄██ ▒██░    ▒██░    ░▓█▒  ░▓▓█  ░██░▒▓▓▄ ▄██▒▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄  
        ░░██▒██▓  ▓█   ▓██▒░██████▒░██████▒░▒█░   ▒▒█████▓ ▒ ▓███▀ ░▒██▒ █▄░▒████▒░██▓ ▒██▒
        ░ ▓░▒ ▒   ▒▒   ▓▒█░░ ▒░▓  ░░ ▒░▓  ░ ▒ ░   ░▒▓▒ ▒ ▒ ░ ░▒ ▒  ░▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░
          ▒ ░ ░    ▒   ▒▒ ░░ ░ ▒  ░░ ░ ▒  ░ ░     ░░▒░ ░ ░   ░  ▒   ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░
          ░   ░    ░   ▒     ░ ░     ░ ░    ░ ░    ░░░ ░ ░ ░        ░ ░░ ░    ░     ░░   ░ 
            ░          ░  ░    ░  ░    ░  ░          ░     ░ ░      ░  ░      ░  ░   ░     
                                                           ░                               


                  _____        __       __  __          ____                __      
                 / ___/__  ___/ /__ ___/ / / /  __ __  / __/_ _  ___  ___ _/ /___ __
                / /__/ _ \/ _  / -_) _  / / _ \/ // / / _//  ' \/ _ \/ _ `/ __/ // /
                \___/\___/\_,_/\__/\_,_/ /_.__/\_, / /___/_/_/_/ .__/\_,_/\__/\_, / 
                                              /___/           /_/            /___/  

                              GitHub Page: {github_link}
        """
    )


def main():
    init()
    greeting()

    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(
        pm.process_handle, "client.dll").lpBaseOfDll

    while True:
        if keyboard.is_pressed("end"):
            exit(0)

        glow_manager = pm.read_int(client + dwGlowObjectManager)

        for i in range(1, 32):
            entity = pm.read_int(client + dwEntityList + i * 0x10)

            if entity:
                entity_team_id = pm.read_int(entity + m_iTeamNum)
                entity_glow = pm.read_int(entity + m_iGlowIndex)

                if entity_team_id == 2:  # Terrorist
                    pm.write_float(glow_manager + entity_glow *
                                   0x38 + 0x8, float(1))   # R
                    pm.write_float(glow_manager + entity_glow *
                                   0x38 + 0xC, float(0))   # G
                    pm.write_float(glow_manager + entity_glow *
                                   0x38 + 0x10, float(0))  # B
                    pm.write_float(glow_manager + entity_glow *
                                   0x38 + 0x14, float(1))  # Alpha
                    pm.write_int(glow_manager + entity_glow *
                                 0x38 + 0x28, 1)           # Enable

                elif entity_team_id == 3:  # Counter-terrorist
                    pm.write_float(glow_manager + entity_glow *
                                   0x38 + 0x8, float(0))   # R
                    pm.write_float(glow_manager + entity_glow *
                                   0x38 + 0xC, float(0))   # G
                    pm.write_float(glow_manager + entity_glow *
                                   0x38 + 0x10, float(1))  # B
                    pm.write_float(glow_manager + entity_glow *
                                   0x38 + 0x14, float(1))  # Alpha
                    pm.write_int(glow_manager + entity_glow *
                                 0x38 + 0x28, 1)           # Enable


if __name__ == "__main__":
    main()