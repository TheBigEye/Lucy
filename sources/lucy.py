import threading

import colorama
from colorama import Fore

from sources.core.lobe.temporal import memory
from sources.core.lobe.parietal import scribble


class AI:
    def __init__(self):
        colorama.init()                     # Initialize colorama for nice console colored texts
        scribble.clear()                    # Clear the shit from the console

        self.awake = True                   # Time to wake up and talk
        self.sleeping = False               # It's not time to sleep :(

        self.memory = "./resources/data/memory.json"   # Here you have the knowledge
        self.name = "Lucy"                             # Your girlfr.. i said.. your friend
        self.friend = "You"                           # your name


    def process(self):
        """ Update logic """

        friend_message = input(Fore.YELLOW + self.friend + ": " + Fore.RESET)

        if (friend_message == "exit"):
            self.sleep()
            return

        current_memory = memory.load(self.memory)

        if (friend_message.startswith(("learn ->", "train ->", "l ->", "t ->"))):
            given_friend_message = friend_message.split("->")[1].strip()
            expected_response = input(Fore.YELLOW + "Me: " + Fore.RESET)
            print(Fore.GREEN + memory.train(given_friend_message, expected_response, current_memory, self.memory))
        else:
            current_response = memory.get(friend_message, current_memory)
            if (current_response.startswith("Lo siento")):
                given_friend_response = input(Fore.GREEN + "Quieres enseñarme una respuesta para esta pregunta? (s/n) " + Fore.RESET)

                if (given_friend_response.lower() == 's'):
                    expected_response = input(Fore.YELLOW + "Me: " + Fore.RESET)
                    print(Fore.GREEN + memory.train(friend_message, expected_response, current_memory, self.memory))

                else:
                    print(Fore.GREEN + self.name + ": " + current_response + Fore.RESET)

            else:
                scribble.write(Fore.GREEN + self.name + ": " + current_response + Fore.RESET + "\n")


    def lifeloop(self):
        while self.awake:
            self.process()
            if self.sleeping:
                self.awake = False


    def sleep(self):
        """ Makes emmy go to sleep """
        self.sleeping = True


    def suicide(self):
        # Self destruct assured, but I'm lazy to implement this :b
        pass


    def initialize(self):
        life = threading.Thread(target=self.lifeloop) # Why and thread? why Lucy hates run along side with the Python interpreter
        life.start()
