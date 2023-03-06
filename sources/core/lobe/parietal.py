"""
The parietal lobe is an important part of the human brain that is responsible for several
important functions, including:

- Sensation: The parietal lobe is involved in sensory perception, including tactile, thermal
  and pain sensation.

- Sensory integration: The parietal lobe is also responsible for integrating sensory information
  from different areas ofthe body to form a complete representation of the environment.

- Mathematics and calculation: The parietal lobe is essential for mathematical calculation and
  the understanding of geometry and proportion.

- Spatiality: The parietal lobe is also involved in spatial perception and orientation in space.
"""

import os
import random
import time


class parietal_lobe:
    pass

class scribble:

    @staticmethod
    def write(given_text: str):
        """ Writes the bot's response character by character with a pause between each comma """

        in_parentheses = False

        for character in given_text:
            if character == '(':
                in_parentheses = True
                print(character, end='', flush=True)
                time.sleep(1)
            elif character == ')':
                in_parentheses = False
                print(character, end='', flush=True)
                time.sleep(random.uniform(0.03, 0.1))
            elif in_parentheses:
                print(character, end='', flush=True)
                time.sleep(0.01)  # Adjust the speed for characters inside parentheses
            elif character == ',':
                print(character, end='', flush=True)
                time.sleep(1)
            else:
                print(character, end='', flush=True)
                time.sleep(random.uniform(0.03, 0.1))



    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')
