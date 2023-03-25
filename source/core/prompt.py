import os
import random
import time

from rich.console import Console

class prompt:
    """ Provides functions for handling terminal/chat text output """

    @staticmethod
    def write(style: str, message: str) -> str:
        """ Writes the bot's response character by character with a pause between each comma """

        # We get our console
        console = Console()

        # characters for which we want an additional pause
        pause_chars = {',', ';', '.', '?', '!'}

        # determines if we are inside parentheses
        parentheses: bool = False

        # We write character by character to make it look natural
        for character in message:

            if character == '(':
                parentheses = True
            elif character == ')':
                parentheses = False

            # print the character
            console.print(style + character + "[/]", end='')

            # make a little pause if are a dot or comma
            # write very fast if the text is beetween parentheses
            # write the characters like an human
            if parentheses:
                time.sleep(0.01)
            elif character in pause_chars:
                time.sleep(0.50)
            else:
                time.sleep(random.uniform(0.03, 0.08))

        return message


    @staticmethod
    def set(style: str, message: str):
        """ Sets the terminal output style and writes the message """
        # We get our console
        console = Console()

        # Print output
        console.print(style + message + "[/]")


    @staticmethod
    def get(style: str, message: str) -> str:
        """ Sets the terminal output style and gets user input """
        # We get our console
        console = Console()

        # Get input
        return console.input(style + message + "[/]")


    @staticmethod
    def newline():
        """ Writes a newline character """
        # We get our console
        console = Console()

        # Print newline
        console.print("\n")


    @staticmethod
    def status(message: str, spin: str):
        """ Displays a status message with a spinner animation """
        console = Console()
        return console.status(message, spinner=spin)


    @staticmethod
    def clear():
        """ Clears the terminal screen """
        with prompt.status("Cleaning buffer", "bouncingBar"):
            os.system("cls" if os.name == "nt" else "clear")
            time.sleep(2)
