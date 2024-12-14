import os

class utils:
    @staticmethod
    def clear_terminal():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def bold(text):
        return f"\033[1m{text}\033[0m"