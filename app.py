from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "game_secret"

# Characters
class Character:
    def __init__(self, name, hp, atk):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.atk = atk

    def attack(self, enemy):
        dmg = random.randint(int(self.atk * 0.8), int(self.atk * 1.2))
        enemy.hp -= dmg
        return dmg
    

class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, 140, 25)

class Mage(Character):
    def __init__(self, name):
        super().__init__(name, 100, 35)

class Archer(Character):
    def __init__(self, name):
        super().__init__(name, 110, 20)

class EvilWizard(Character):
    def __init__(self):
        super().__init__("Dark Wizard",150, 18)

# Game Helpers

def save(player, wizard, log):
    session["player"] = player.__dict__
    session["wizard"] = wizard.__dict__
    session["log"] = log

def load():
    p = session["player"]
    w = session["wizard"]

    player= Character(p["name"], p["max_hp"], p["atk"])
    player.hp = p["hp"]

    wizard = Character(w["name"], w["max_hp"],w["atk"])
    wizard.hp = w["hp"]

    return player, wizard, session.get("log", [])

# Routes

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        cls = request.form["class"]

        if cls == "Warrior":
            player = Warrior(name)
        elif cls == "Mage":
            player = Mage(name)
        else:
            player = Archer(name)
        wizard = EvilWizard()
        save(player, wizard, ["🧙 The battle begins!"])
        return redirect("/battle")
    
    return render_template("index.html")

@app.route("/battle")
def battle():
    player, wizard, log = load()
    return render_template("battle.html", player=player, wizard=wizard, log=log)

@app.route("/action/<move>")
def action(move):
    player, wizard, log = load()

    if player.hp <= 0 or wizard.hp <= 0:
        return redirect("/battle")
    
    if move == "attack":
        dmg = player.attack(wizard)
        log.append(f"⚔️ You hit the wizard for {dmg} damage!")
    elif move == "heal":
        player.hp = min(player.max_hp, player.hp + 20)
        log.append("✨ You heal for 20 HP!")

    if wizard.hp > 0:
        dmg = wizard.attack(player)
        log.append(f"🔥 Wizard hits you for {dmg} damage!")

    if player.hp <= 0:
        log.append("💀 You were defeated!")
    elif wizard.hp <= 0:
        log.append("🏆 You defeated the wizard!")

    save(player, wizard, log)
    return redirect("/battle")

if __name__ == "__main__":
    app.run(debug=True)