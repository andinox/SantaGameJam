import signal
from simple_term_menu import TerminalMenu
import sys
import time
from random import randint
import statistics
from sqlalchemy.sql.functions import random
import math
from DataBase import MobDatabase
from utils import utils
import yaml

def block_ctrl_c(signal_received, frame): pass

class Game:
    def __init__(self):
        self.mob = self.get_all_mobs()
        self.data = MobDatabase()
        self.start()

    @staticmethod
    def get_all_mobs():
        with open("./mob.yml") as mob:
            return yaml.safe_load(mob)

    def start(self):
        utils.clear_terminal()
        self.print_poke_int()
        actions = ["Voir le PokeInt Index","Voir mes PokeInt", "Se Balader", "Quitter"]
        terminal_menu = TerminalMenu(actions)
        menu_entry_index = terminal_menu.show()
        match menu_entry_index:
            case 0:
                self.show_mob_index()
            case 1:
                self.show_own_mob()
            case 2:
                self.promenade()
            case 3:
                return -1

    def show_mob_index(self):
        mobs = [
            f"{mob}" for mob in self.mob.keys()
        ]
        mobs_ = [
            (f"aka: {self.mob[mob]['aka']}"
             f"\nAttaque: "
             f"\n    {self.mob[mob]['attack'][1]['name']}:"
             f"\n        - Dégats: {self.mob[mob]['attack'][1]['damage']}"
             f"\n        - Précision: {self.mob[mob]['attack'][1]['taux']*100}%"
             f"\n    {self.mob[mob]['attack'][2]['name']}:"
             f"\n        - Dégats: {self.mob[mob]['attack'][2]['damage']}"
             f"\n        - Précision: {self.mob[mob]['attack'][2]['taux']*100}%"
             f"\n    {self.mob[mob]['attack'][3]['name']}:"
             f"\n        - Dégats: {self.mob[mob]['attack'][3]['damage']}"
             f"\n        - Précision: {self.mob[mob]['attack'][3]['taux']*100}%")
            for mob in self.mob.keys()
        ]
        stat = {
            f"{mobs[i]}": mobs_[i] for i in range(len(mobs))
        }
        terminal_menu = TerminalMenu(mobs, title="PokeInt Index", preview_command=lambda selected_option: stat[selected_option], preview_title="Statistiques", preview_size=11)
        menu_entry_index = terminal_menu.show()
        self.start()


    def loading_dots(self, message="Chargement", duration=1):
        end_time = time.time() + duration
        while time.time() < end_time:
            for dots in range(4):
                sys.stdout.write(f"\r{message}{'.' * dots}   ")
                sys.stdout.flush()
                time.sleep(0.5)



    def promenade(self):
        self.loading_dots(message="Tu te balades simplement dans ce monde paisible ")
        mob = self.get_random_mob()
        lvl = self.get_lvl_random_mob()
        print(f'\nTu tombes sur {mob} lvl {int(lvl)} sauvage !')
        actions = ["Attaquer", "Fuir"]
        terminal_menu = TerminalMenu(actions)
        menu_entry_index = terminal_menu.show()
        match menu_entry_index:
            case 0:
                self.attack(mob,int(lvl))
            case 1:
                self.start()

    def get_lvl_random_mob(self):
        mobs = self.data.get_mobs()
        all_lvl = [mob.xp/100 for mob in mobs]
        return statistics.median(all_lvl)

    @staticmethod
    def print_poke_int():
        print("""
         ____       _          ___ _   _ _____ 
        |  _ \ ___ | | _____  |_ _| \ | |_   _|
        | |_) / _ \| |/ / _ \  | ||  \| | | |  
        |  __/ (_) |   <  __/  | || |\  | | |  
        |_|   \___/|_|\_\___| |___|_| \_| |_|  
        """)

    def get_random_mob(self):
        a = [i for i in self.mob.keys()]
        return a[randint(0, len(a) - 1)]

    def show_own_mob(self):
        mobs = [
            f'[{int(mob.xp / 100)}]{mob.name}' for mob in self.data.get_mobs()
        ]
        mobs_ = [mob.name for mob in self.data.get_mobs()]
        mobs.append("Retour")
        terminal_menu = TerminalMenu(mobs, title="Vos PokeInt:")
        menu_entry_index = terminal_menu.show()
        if menu_entry_index == len(mobs) - 1:
            self.start()
        else:
            self.show_mob(mobs_[menu_entry_index])

    def show_mob(self, name):
        mob = self.mob[name]
        own = self.data.get_mob_by_name(name)
        print(utils.bold(name))
        print(f"AKA: {mob['aka']}")
        print("Attaque: ")
        for i in range(1,4):
            print(f"    {mob['attack'][i]["name"]}:")
            print(f"        - Dégats: {utils.bold(int(mob['attack'][i]["damage"]*math.sqrt((own.xp+100)/100)))}")
            print(f"        - Précision: {utils.bold(mob['attack'][i]["taux"])}")
        terminal = TerminalMenu(["Retour"])
        terminal.show()
        self.start()

    def attack(self, mob, lvl):
        mobs = [
            f'[{int(mob.xp / 100)}]{mob.name}' for mob in self.data.get_mobs()
        ]
        mobs = [
            mob.name for mob in self.data.get_mobs()
        ]
        mobs.append("[←] Etre une tapette et fuir")
        terminal_menu = TerminalMenu(mobs, title="Choisir avec quel PokeInt attaquer:")
        menu_entry_index = terminal_menu.show()
        self.combat(mob, lvl, self.data.get_mob_by_name(mobs[menu_entry_index]))


    def combat(self,mob, lvl, own_mob):
        player_lvl = own_mob.xp / 100
        mob_lvl = lvl + 1
        player_pv = 100
        mob_pv = 100

        utils.clear_terminal()
        while player_pv > 0 and mob_pv > 0:
            utils.clear_terminal()
            self.print_poke_int()
            print(f"Vous avez {utils.bold(player_pv)} PV")
            print(f"{mob} a {utils.bold(mob_pv)} PV \n")
            attacks = [
                self.mob[own_mob.name]["attack"][i]["name"]
                for i in range(1,4)
            ]
            p = [
                f"Précision: {self.mob[own_mob.name]['attack'][i]['taux']*100}% | Dégats: {int(self.mob[own_mob.name]['attack'][i]['damage']*math.sqrt(player_lvl))}"
                for i in range(1,4)
            ]
            preview = {
                attacks[i]: p[i] for i in range(3)
            }
            terminal_menu = TerminalMenu(attacks, title="Choisir une attaque:", preview_command=lambda selected_option: preview[selected_option], preview_title="Statistiques")
            menu_entry_index = terminal_menu.show()
            précision = randint(1,100)
            match menu_entry_index:
                case 0:
                    if précision <= self.mob[own_mob.name]["attack"][1]["taux"]*100:
                        print(f"Vous utilisez {self.mob[own_mob.name]['attack'][1]['name']} et infligez {int(self.mob[own_mob.name]['attack'][1]['damage']*math.sqrt(player_lvl))} dégats")
                        mob_pv -= self.mob[own_mob.name]["attack"][1]["damage"]*math.sqrt(player_lvl)
                    else:
                        print(f"Vous utilisez {self.mob[own_mob.name]['attack'][1]['name']} mais vous ratez")
                case 1:
                    if précision <= self.mob[own_mob.name]["attack"][2]["taux"]*100:
                        print(f"Vous utilisez {self.mob[own_mob.name]['attack'][2]['name']} et infligez {int(self.mob[own_mob.name]['attack'][2]['damage']*math.sqrt(player_lvl))} dégats")
                        mob_pv -= self.mob[own_mob.name]["attack"][2]["damage"]*math.sqrt(player_lvl)
                    else:
                        print(f"Vous utilisez {self.mob[own_mob.name]['attack'][2]['name']} mais vous ratez")
                case 2:
                    if précision <= self.mob[own_mob.name]["attack"][3]["taux"]*100:
                        print(f"Vous utilisez {self.mob[own_mob.name]['attack'][3]['name']} et infligez {int(self.mob[own_mob.name]['attack'][3]['damage']*math.sqrt(player_lvl))} dégats")
                        mob_pv -= self.mob[own_mob.name]["attack"][3]["damage"]*math.sqrt(player_lvl)
                    else:
                        print(f"Vous utilisez {self.mob[own_mob.name]['attack'][3]['name']} mais vous ratez")
            if mob_pv > 0:
                mob_attack = randint(1,3)
                pression = randint(1,100)
                if pression <= self.mob[mob]["attack"][mob_attack]["taux"]*100:
                    player_pv -= self.mob[mob]["attack"][mob_attack]["damage"]
                    print(f"{mob} utilise {self.mob[mob]['attack'][mob_attack]['name']} et vous inflige {int(self.mob[mob]['attack'][mob_attack]['damage']*math.sqrt(mob_lvl))} dégats")
                else:
                    print(f"{mob} utilise {self.mob[mob]['attack'][mob_attack]['name']} mais rate")
            else:
                print(f"Vous avez vaincu {mob} !")
                print(f"Vous attrapez {mob}")
                d = [i.name for i in self.data.get_mobs()]
                if mob not in d:
                    self.data.add_mob(mob,0)
                self.data.add_xp_to_mob(own_mob.name,100)
                t = TerminalMenu(["Continuer"])
                t.show()
                break
            if player_pv <= 0:
                print(f"{mob} vous a vaincu ! mais vous gangnez quand même de l'expérience")
                self.data.add_xp_to_mob(own_mob.name,50)
                t = TerminalMenu(["Continuer"])
                t.show()
                break
            t = TerminalMenu(["Continuer"])
            t.show()
        self.start()



if __name__ == "__main__":
    signal.signal(signal.SIGINT, block_ctrl_c)
    utils.clear_terminal()
    Game()
