import random
import time

class Character:
    def __init__(self, name, hp, atk):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.atk = atk
        self.potions= 3

    def attack(self, enemy):
        dmg = random.randint(int(self.atk * 0.8), int(self.atk * 1.2))
        enemy.hp -= dmg
        return dmg
    
    def use_potion(self):
        if self.potions > 0:
            heal = 30
            self.hp = min(self.max_hp, self.hp + heal)
            self.potions -= 1
            return heal
        return 0
    
    def is_alive(self):
        return self.hp > 0
    

class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, 140, 25)

    def power_strike(self, enemy):
        dmg = random.randint(30, 45)
        enemy.hp -= dmg
        return dmg

class Mage(Character):
    def __init__(self, name):
        super().__init__(name, 100, 35)

    def fireball(self, enemy):
        dmg = random.randint(35, 35)
        enemy.hp -= dmg
        return dmg
    
class Archer(Character):
    def __init__(self, name):
        super().__init__(name, 110, 20)

    def quick_shot(self, enemy):
        dmg = random.randint(15, 25) * 2
        enemy.hp -= dmg
        return dmg
    
class EvilWizard(Character):
    def __init__(self):
        super().__init__("Dark Wizard", 160, 18)

# Game Logic

def choose_character():
    print("Choose your class:")
    print("1. Warrior")
    print("2. Mage")
    print("3.Archer")
    choice = input("Enter number:")
    name = input("Enter your hero's name:")

    if choice == "1":
        return Warrior(name)
    elif choice == "2":
        return Mage(name)
    else:
        return Archer(name)

def display_stats(player, enemy):
    print(f"\n{player.name} HP: {player.hp}/player.max_hp | Potions: {player.potions}")
    print(f"{enemy.name} HP: {enemy.hp}/{enemy.max_hp}\n")

def battle(player, enemy):
    log = []
    print(f"\n🧙 A wild {enemy.name} appears!\n")
    while player.is_alive() and enemy.is_alive():
        display_stats(player, enemy)
        print("Choose action:")
        print("1. Attack")
        print("2. Special")
        print("3. Use Potion")
        print("4. View Stats")
        choice = input("Enter number:")

        if choice == "1":
            dmg = player.attack(enemy)
            print(f"⚔️ You attack {enemy.name} for {dmg} damage!")
        elif choice == "2":
            if isinstance(player, Warrior):
                dmg = player.power_strike(enemy)
                print(f"💥 Power Strike hits {enemy.name} for {dmg} damage!")
            elif isinstance(player, Mage):
                dmg = player.fireball(enemy)
                print(f"🔥 Fireball hits {enemy.name} for {dmg} damage!")
            elif isinstance(player, Archer):
                dmg = player.quick_shot(enemy)
                print(f"🏹 Quick Shot hits {enemy.name} for {dmg} damage!")
        elif choice == "3":
            heal = player.use_potion()
            if heal > 0:
                print(f"🧪 You healed {heal} HP!")
            else:
                print("❌ No potions left!")
        elif choice == "4":
            display_stats(player, enemy)
            continue
        else:
            print("❌ Invalid choice!")
            continue

        # Enemy turn
        if enemy.is_alive():
            dmg = enemy.attack(player)
            print(f"🔥 {enemy.name} attacks you for {dmg} damage!")

        time.sleep(1)
        print("-" * 40)

    if player.is_alive():
        print(f"\n🏆 Congratulations! You defeated {enemy.name}!")
    else:
        print(f"\n💀 You were defeated by {enemy.name}...")



def main():
    player = choose_character()
    enemy = EvilWizard()
    battle(player, enemy)

if __name__ == "__main__":
    main()