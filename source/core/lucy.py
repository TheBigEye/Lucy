import threading
import time

from source.core.brain import memory
from source.core.prompt import prompt

class lucy:
    # Bot stattes and data variables
    awake_status: bool = True # Time to wake up and talk
    sleep_status: bool = False # It's not time to sleep :(
    memory_file: str = ("./resources/data/memory.json")

    # Bot commands
    learn_commands: tuple = ("learn ->", "train ->")
    clear_commands: list = ["clear"]
    exit_commands: list = ["exit"]


    @staticmethod
    def process():
        """ Update logic """

        # Message styles
        user_style: str = "[italic bold yellow]"
        lucy_style: str = "[italic bold green]"

        # Gets the user input and load the memory file
        current_input = prompt.get(user_style, "You: ")
        current_memory = memory.load(lucy.memory_file)

        # Parse instructions
        if current_input.lower() in lucy.exit_commands:
            lucy.sleep()
            return

        if current_input.lower() in lucy.clear_commands:
            prompt.clear()
            return

        if current_input.startswith(lucy.learn_commands):
            given_message = current_input.split("->")[1].strip()
            given_answer = prompt.get(lucy_style, "Answer: ")
            prompt.write(lucy_style, memory.train(given_message, given_answer, current_memory, lucy.memory_file) + "\n")
            return

        current_answer = memory.get(current_input, current_memory)
        if (current_answer.startswith("Sorry, ")): # Fixed :)
            given_choice = prompt.get(lucy_style, "Do you want to show me an answer for that?: ")

            if given_choice.lower() in ["y", "yes"]:
                given_answer = prompt.get(lucy_style, "Answer ")
                prompt.write(lucy_style, memory.train(current_input, given_answer, current_memory, lucy.memory_file) + "\n")
            else:
                prompt.write(lucy_style, "Lucy: " + current_answer + "\n")
            return

        prompt.write(lucy_style, "Lucy: " + current_answer + "\n")


    @staticmethod
    def lifeloop():
        """ The main loop, the heart of it all """

        # Clear the shit from the console
        prompt.clear()

        with prompt.status("Loading memory", "bouncingBar"):
            suggested = memory.suggestion(lucy.memory_file)
            time.sleep(2)

        prompt.newline()
        prompt.set("[italic bold green]", "(i) Suggested questions of the day:")
        for question in suggested:
            prompt.write("[italic dim white]", "- " + question + "\n")
        prompt.newline()

        while lucy.awake_status:
            lucy.process()
            if lucy.sleep_status:
                lucy.awake_status = False


    @staticmethod
    def sleep():
        """ Makes Lucy go to sleep """
        lucy.sleep_status = True


    @staticmethod
    def suicide():
        # Self destruct assured, but I'm too lazy to implement this :b
        pass


    @staticmethod
    def initialize():
        # Likewise, for obvious design reasons, I will remove this at some point in the future, unless a feature requires it
        life_status = threading.Thread(target=lucy.lifeloop) # Why and thread? why Lucy hates run along side with the Python interpreter
        life_status.start()
