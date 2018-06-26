"""This is going to be a simple game engine for a game called 'Gothons from
Planet Percal #25'

THEME:

Aliens have invaded a space ship and our hero has to go through a maze of rooms
defeating them so he can escape into an escape pod to the planet below. The game
will be more like a Zork or Adventure type of game with text outputs and funny
ways to die. The game will involve an engine that runs a map full of rooms or
scenes. Each room will print its own description when the player enters it and
then tell the engine what room to run next out of the map.
"""

from sys import exit
from random import randint
from random import choice
from textwrap import dedent
from math import floor
import os

CHEAT = "smeg"
POSSIBLE_ACTIONS = [
"run",
"flee",
"dodge",
"fight",
"shoot",
"tell a joke",
"throw (item)",
"place (item)"
]
PRINT_POS_ACTIONS = f"Possible actions (all might not be available in all rooms):\n{POSSIBLE_ACTIONS}\n"

class Scene():

    def enter(self):
        print("This scene is not yet configured.")
        print("Subclass it and implement enter().")
        exit(1)

    def fighting(self, scene_name, gothons):

        print(dedent("""
            You have chosen to engage in a gun-fight. Brave or stupid is something that
            only time will tell. Choose between 'shoot' or 'dodge'
            """))

        g_shots = 5

        while True:
            accuracy = 10
            g_accuracy = 3
            action = input("> ")

            if action == 'dodge':
                print("You choose to dodge and the accuracy of the Gothons is very low")
                g_accuracy = 1
                for _ in range(0, gothons):
                    if g_accuracy >= randint(1,20):
                        return "dead"
                print("You have to make another choice: 'shoot' or 'dodge'")
            elif action == 'shoot':
                print("You choose to shoot and hope for the best.")
                if accuracy >= randint(1,20):
                    gothons -= 1
                    if gothons == 0:
                        return "alive"
                    print(dedent("You've killed a Gothon but %d remain!" % gothons))
                else:
                    print(dedent("""
                    You take aim but the fluttering clown clothes distract you and your
                    shot goes wide.
                    """))
                for _ in range(0, gothons):
                    if g_accuracy >= randint(1,20):
                        return "dead"
                print("You have to make another choice: 'shoot' or 'dodge'")
            else:
                print("Please choose a valid action!")

class Engine():

    def __init__(self, scene_map):
        self.scene_map = scene_map

    def play(self):
        #print(self.scene_map.scene)
        current_scene = self.scene_map.opening_scene()
        last_scene = self.scene_map.next_scene("finished")

        while current_scene != last_scene:
            next_scene_name = current_scene.enter()
            current_scene = self.scene_map.next_scene(next_scene_name)

class Death(Scene):

    quips = [
    "You died. You need some more practice... ALOT of practice!",
    "Rimmer would be proud, a fellow Smeghead!",
    "Such a looooser!",
    "I have a pet cats that're better at this",
    "You're worse than Dad jokes."
    ]

    def enter(self):
        self.description = Death.quips[randint(0, len(self.quips) - 1)]
        print(dedent(self.description) + "\n\n\t\t\tGAME OVER!!!\n")
        exit(1)

class CentralCorridor(Scene):

    def enter(self):
        self.description = """
            The Gothons of Planet Percal #25 have invaded your ship and destroyed
            your entire crew. You are the last surviving member and your last mission
            is to get the netron destruct bomb from the Weapons Armory, put it on
            the bridge, and blow the ship up after getting into an escape pod.

            You're running down the central corridor to the Weapons Armory when
            a Gothon jumps out, red scaly skin, dark grimy teeth, and an evil clown
            costume flowing around his hate-filled body. He is blocking the door to
            the Armory and about to pull a weapon to blast you.
            """
        print(dedent(self.description))

        print(PRINT_POS_ACTIONS)

        action = input("> ")

        if action == CHEAT:
            action = 'joke'

        if 'shoot' in action or 'fight' in action:
            result = self.fighting("central_corridor", 1)
            if result == "dead":
                print(dedent("""
                    Quick on the draw you yank out your blaster and fire it at the Gothon.
                    His clown costume is flowing and moving around his body, which throws
                    off your aim. Your laser hits his costume but misses him entirely.
                    This completely ruins his brand new costume his mother has made for him,
                    which makes him fly into an insane rage and blast you repeatedly in
                    the face until you are dead. Then he eats you.
                    """))
                return "death"
            else:
                print(dedent("""
                    Lucky for you this Gothon apparently couldn't hit a barn door.
                    His unaimed blasts blow past you as you steadily take aim on his evil
                    face. After you squeeze the trigger his head blows up and his body
                    falls down dead on the ground. With the way clear you jump into the
                    Weapon Armory room."""))
                return "laser_weapon_armory"
        elif 'dodge' in action or 'run' in action or 'flee' in action:
            print(dedent("""
                Like a world class boxer you dodge, weave, slip and slide right as
                the Gothon blaster cranks a laser past your head. In the middle of
                your artful dodge your foot slips and you bang your head on the metal
                wall and paass out. You wake up shortly after only to die as the
                Gothon stomps on your head and eats you.
                """))
            return "death"
        elif 'joke' in action:
            print(dedent("""
                Lucky for you they made you learn Gothon insults in the academy.
                You tell the one gothon joke you know: 'yue okau jze as ert tty oopa
                ietry' which roughly translates to 'Your mother ate you and you came
                out the other end' (no one said it made sense).

                The Gothon stops and tries not to laugh but he (if it is a he) can't
                hold it in. He burst out laughing and can't move. While he is distracted
                you pull your blaster and shoot him in the face putting him down.
                You then jump through the Weapon Armory door."""))
            return "laser_weapon_armory"
        else:
            print("Do not understand action: %s in this context. Please elaborate and try again." % action)
            return "central_corridor"

class LaserWeaponArmory(Scene):

    def enter(self):
        self.description = """
            You do a dive roll into the Weapon Armory, crouch and scan the room for
            more Gothons that might be hiding. It's dead quiet... too quiet.
            You stand up and run to the far side of the room and find the neutron bomb
            in its container.

            There is a keypad lock on the box and you need the code to get the bomb out.
            If you get the code wrong 10 times then the lock closes forever and you
            won't be able to get the bomb. The code is two digits long and for some
            reason Gothons only use the numbers 1-5 giving you pretty good odds. This
            might be due to the fact that Gothons have terrible memory.
            """
        print(dedent(self.description))

        code = f"{randint(1,5)}{randint(1,5)}"
        guess = input("[keypad] - xx > ")
        if guess == CHEAT:
            guess = code
        nr_guesses = 1

        while guess != code and nr_guesses < 10:
            print("BZZZZZEDOD! \n%d Attempts left" % (10-nr_guesses))
            guess = input("[keypad]> ")
            if guess == CHEAT:
                guess = code
            nr_guesses += 1

        if guess == code:
            print(dedent("""
                The container clicks open and the seal breaks, letting some gas out.
                You grab the neutron bomb, strap it to your backpack and run as fast
                as you can towards the bridge where you must place it to destroy the
                entire ship."""))
            return "the_bridge"
        else:
            print(dedent("""
                The lock buzzes one last time and then you hear a sickening melting
                sound as the mechanism is fused together. You decide to sit there
                giving up since there is no way you are leaving before blowing up
                this bastard ship. The Gothons finally find you and you go down in
                a blase of glory. But you still die.
                """))
            return "death"

class TheBridge(Scene):

    def enter(self):
        self.description = """
            You bring out the neutron bomb as you burst onto the Bridge surprising
            5 Gothons who are trying to take control of the ship. Each of them have
            an even uglier clow costume than the last.
            None of them draw their weapons since they can see the active bomb in
            your hand and are afraid to set it off.
            """
        print(dedent(self.description))

        print(PRINT_POS_ACTIONS)

        action = input("> ")

        if action == CHEAT:
            action = 'place bomb'

        if 'throw' in action and 'bomb' in action:
            print(dedent("""
                In a panic you throw the bomb at the group of Gothons and make a leap
                for the door. Right as the bomb leaves your hand and you turn around a
                Gothon shoots you in the back. While you slowly feel the life in you
                ebb away, you see another Gothon frantically trying to disarm the bomb.
                You die knowing that at least these 5 will probably meet their end when
                the bomb goes off.
                """))
            return "death"
        elif 'place' in action and 'bomb' in action:
            print(dedent("""
                You point your blaster at the bomb under your arm. The Gothons put their
                hands over their heads and start to sweat. You inch backwards toward
                the door, open it, and then carfully place the bomb on the floor,
                keeping your blaster pointed at it the entire time.

                You quickly jump back through the door, punch the close button and
                blast the lock so the Gothons can' get out. With the bomb placed you
                run towards the escape pods to get off this tin can of a ship."""))
            return "escape_pod"
        elif 'fight' in action or 'shoot' in action:
            print("Despite the odds you face off against the 5 Gothons.")
            result = self.fighting("the_bridge", 5)
            if result == "dead":
                print(dedent("""
                    As you take aim towards the Gothons they see no other option but to
                    draw their blasters and fire back. One of the blasts hit the bomb in
                    your arm and sets it off. All you have time to see is a bright light
                    before you are disintigrated into dust.
                    """))
                return "death"
            else:
                print(dedent("""
                    Crazy as it sounds, you manage to blast your way through the 5
                    Gothons killing every single one. With the coast clear you carefully
                    place the bomb under the captains chair. With the bomb placed you
                    run towards the escape pods to get off this tin can of a ship."""))
                return "escape_pod"
        elif 'flee' in action or 'run' in action:
            print(dedent("""
                As you turn your back to run the Gothons see their chance and blast you
                in the back. You have time to see the three new holes in your chest
                as everything goes black and you die.
                """))
                return "death"
        else:
            print("Do not understand action: %s in this context. Please elaborate and try again." % action)
            return "the_bridge"

class EscapePod(Scene):

    def enter(self):
        self.description = """
            You rush through the ship desperately trying to make it to the escape pod
            before the bomb goes off and the whole ship explodes. It seems like hardly
            any Gothons are on the ship so your run is clear of interference. You get
            the chamber with the escape pods and now you need to pick one to take.
            There are three pods (1-3) and you know some might be damaged since Gothons
            aren't big on maintenance. But you don't have time to look so you just got
            to take a shot and choose one.
            """
        print(dedent(self.description))
        good_pod1 = randint(1,3)
        guess = input("(1-3) > ")
        if guess == CHEAT:
            guess = str(good_pod1)

        if int(guess) == good_pod1:
            print(dedent("""
                You jump into pod %s and hit the eject button. The pod easily slides
                out into space heading to the planet below. As it flies to the planet,
                you look back and see your ship implode and then explode like a bright
                star, taking out the nearby gothon ship at the same time.
                You won, congratulations!
                """) % guess)
            print("\t\t\tTHE END!!!\n")
            return "finished"
        else:
            print(dedent("""
                You jump into pod %s and hit the eject button. The pod slides out
                into space. But as soon as you hit the void of space you notice that
                something is leaking. Before you have time to react the hull ruptures,
                crushing your body into jam jelly and killing you instantly.
                """) % guess)
            return "death"

class Finished(Scene):

    def enter(self):
        return "finished"

class Map():

    SCENE_KEY = {
    "central_corridor": CentralCorridor(),
    "laser_weapon_armory": LaserWeaponArmory(),
    "the_bridge": TheBridge(),
    "escape_pod": EscapePod(),
    "death": Death(),
    "finished": Finished()
    }

    def __init__(self, start_scene):
        self.start_scene = start_scene

    def next_scene(self, scene_name):
        self.scene = scene_name
        return Map.SCENE_KEY.get(self.scene)

    def opening_scene(self):
        return self.next_scene(self.start_scene)

os.system('cls' if os.name=='nt' else 'clear')
a_map = Map("central_corridor")
a_game = Engine(a_map)
a_game.play()
print("\t\t\tGame is finished!\n")
