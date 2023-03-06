"""
The temporal lobe is an important part of the human brain that is responsible
for several important functions, including:

- Hearing: The temporal lobe is essential for auditory perception and language
  comprehension.

- Memory: The temporal lobe is involved in short-term and long-term memory, as
  well as verbal and non-verbal memory.

- Emotion: The temporal lobe is also involved in emotional regulation and
  identifying emotions in other people.

- Language comprehension: The temporal lobe is essential for the comprehension
  and production of language.
"""

import json
import random
import re as regex
from difflib import SequenceMatcher
from os import path

from unidecode import unidecode


class temporal_lobe:

    @staticmethod
    def comprehension(tag: str):
        with open("./resources/data/brain.json", "r", encoding="utf-8") as lobe_data:
            data = json.load(lobe_data)
            for lobe in data["temporal_lobe"]:
                for comprehension in lobe["comprehension"]:
                    if comprehension["tag"] == tag:
                        return comprehension["responses"]
            return []


class response:
    ### Why not use constants?
    # because are boring and i cant add them docstrings :(
    # (If something is not NICE for me, it does not work for me)

    @staticmethod
    def no_found() -> str:
        """ - Message when an answer is not found """
        responses = temporal_lobe.comprehension("no_found")
        return random.choice(responses)

    @staticmethod
    def is_empty() -> str:
        """ - Message when trying to learn an empty answer """
        responses = temporal_lobe.comprehension("is_empty")
        return random.choice(responses)

    @staticmethod
    def is_interesting() -> str:
        """ - If you know what it feels like to be ignored, you know what this is """
        responses = temporal_lobe.comprehension("is_interesting")
        return random.choice(responses)

    @staticmethod
    def was_learned() -> str:
        """ - Message indicating that a response has been learned """
        responses = temporal_lobe.comprehension("was_learned")
        return random.choice(responses)


class memory:

    @staticmethod
    def load(memory_file: str) -> dict:
        """Load the bot memory data"""

        # If the "memory.json" file does not exist, an empty one is created
        if not path.exists(memory_file):
            with open(memory_file, "w", encoding="utf-8") as memory_data:
                json.dump({}, memory_data, ensure_ascii=False, indent=4)
            return {}

        try:
            # Load the data from the bot's memory
            with open(memory_file, "r", encoding="utf-8") as memory_data:
                data = json.load(memory_data)
                return data
        except json.JSONDecodeError as exception:
            # Handle case where memory_file contains invalid JSON
            print(f"Error loading memory_file: {exception}")
            return {}


    @staticmethod
    def save(memory_file: str, current_memory: dict):
        """ Save learned bot data to the memory file """

        with open(memory_file, "w", encoding="utf-8") as memory_data:
            json.dump(current_memory, memory_data, ensure_ascii=False, indent=4)


    @staticmethod
    def train(given_message: str, given_answer: str, current_memory: dict, memory_file:str) -> str:
        """
        Train the bot by adding a new answer to the memory.

        ### Arguments:
        - `given_message (str)`: The user's message or question to be associated with the answer, as a string.
        - `given_answer (str)`: The answer to the user's question, as a string.
        - `current_memory (dict)`: A dictionary with the current bot's memory.
        - `memory_file (str)`: The file path to save the updated memory.

        ### Returns:
        - A message confirming whether the bot successfully learned the new answer, as a string. If the answer was empty or invalid, a corresponding error message is returned.
        """

        # Convert words to lowercase and remove accents
        given_message = unidecode(given_message.lower())

        # Empty or invalid answers are not accepted
        if not given_answer.strip():
            return response.is_empty()

        # Add answer to existing message, or create new entry in the brain
        if given_message in current_memory:
            current_memory[given_message].append(given_answer.strip())
        else:
            current_memory[given_message] = [given_answer.strip()]

        memory.save(memory_file, current_memory)
        return response.was_learned()


    @staticmethod
    def get(given_message: str, current_memory: dict) -> str:
        """
        This function looks for an answer in the memory of the bot based on the user's question.

        ### Arguments:
        - `given_message (str)`: The user's message or question, as a string.
        - `current_memory (dict)`: A dictionary with the current bot's memory.

        ### Returns:
        - A response to the user's question, as a string. If no response is found, a default phrase is returned.
        """

        # Convert words to lowercase and remove accents
        given_message = unidecode(given_message.lower())

        # Remove punctuation marks from the message
        given_message = regex.sub(r"[^\w\s]+", "", given_message)

        # Find the most similar key in the memory
        best_match = max(current_memory.keys(), key=lambda x: SequenceMatcher(None, x, given_message).ratio())

        # Check if the best match is similar enough to the message
        match_ratio = SequenceMatcher(None, best_match, given_message).ratio()
        if match_ratio >= 0.8: # a similarity threshold of 80% is used (equivalent to the temperature)
            responses = current_memory[best_match]
            return random.choice(responses)
        else:
            # If no response is found, a default phrase is returned
            return response.no_found()
