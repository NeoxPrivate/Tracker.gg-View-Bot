import os, platform
import time
from os import system, name
from datetime import datetime
from colorama import Fore, Style, init
from src.modules.helper.config import Config
from pystyle import Colors, Colorate, Center, Write

logo = """
███╗   ██╗███████╗ ██████╗ ██╗  ██╗
████╗  ██║██╔════╝██╔════╝ ██║  ██║
██╔██╗ ██║█████╗  ██║  ███╗███████║
██║╚██╗██║██╔══╝  ██║   ██║██╔══██║
██║ ╚████║███████╗╚██████╔╝██║  ██║
╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝"""

class Logger:

    def __init__(self):
        self.log_types = {
            "INFO": Fore.CYAN,
            "SUCCESS": Fore.GREEN,
            "OK": Fore.GREEN,
            "WARNING": Fore.YELLOW,
            "SLEEP": Fore.YELLOW,
            "ERROR": Fore.RED,
            "BAD": Fore.RED,
            "INPUT": Fore.BLUE,
        }
        self.config = Config()

    def clear(self):
        system("cls" if name in ("nt", "dos") else "clear")
    def animate_logo(self, text):
        for line in text.split("\n"):
          Write.Print(Center.XCenter(line) + "\n", Colors.white_to_blue, interval=0.01)
        time.sleep(0.3)
    def print_logo(self):
        self.clear()
        self.animate_logo(logo)
        print(Center.XCenter(Colorate.Vertical(Colors.blue_to_purple, "────────────────────────────────────────────\n", 1)))
        print(Center.XCenter(Colorate.Vertical(Colors.blue_to_purple, "Welcome to NEOX View Bot! - Creds to zaptons\n\n", 1)))
        os.system(f"title Neox's View Bot {self.config.build_version}")

    def log(self, type, message):
        color = self.log_types[type]
        now = datetime.now()
        current_time = now.strftime("%d/%m/%Y • %H:%M:%S")
        print(f"{Style.DIM}{current_time} • {Style.RESET_ALL}{Style.BRIGHT}{color}[{Style.RESET_ALL}{type}{Style.BRIGHT}{color}] {Style.RESET_ALL}{Style.BRIGHT}{Fore.WHITE}{message}")

    def change_title(self, title):
        if platform.system() == 'Windows':
            os.system(f'title {title}')
        elif platform.system() == 'Linux':
            os.system(f'echo -ne "\033]0;{title}\007"')