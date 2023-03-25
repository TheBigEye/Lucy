import json
import os
import random
import re as regex
import time
import unicodedata

from source.core.prompt import prompt

class brain:
    last_response: str = None

    @staticmethod
    def redaction(responses: list) -> str:
        """ Devuelve un texto aleatorio completo de una lista de textos """
        response = random.choice(responses)
        while response == brain.last_response:
            response = random.choice(responses)
        brain.last_response = response
        return response


    @staticmethod
    def comprehension(first_string: str, second_string: str) -> float:
        """
            The Levenshtein distance algorithm
            - This function computes the similarity between two strings based on their characters.

            ### Arguments:
            - `first_string (str)`: The first string.
            - `second_string(str)`: The second string.

            ### Returns:
            - A value between 0 and 1 indicating the similarity between the two strings, where 1 means they are identical.
        """
        ### I could use SequenceMatcher, but it is too boring

        # Get the length of each string
        first_length: int = len(first_string)
        second_length: int = len(second_string)

        # Swap strings if the first string is longer than the other
        if first_length > second_length:
            first_string, second_string = second_string, first_string
            first_length, second_length = second_length, first_length

        # Initialize the first row of the matrix
        previous_row = range(first_length + 1)


        # We iterate over each character in the second string
        for i, c2 in enumerate(second_string):
            current_row = [i + 1]

            # We iterate over each character in the first string
            for j, c1 in enumerate(first_string):
                # Compute the cost of the current edit operation
                cost = 0 if c1 == c2 else 1

                # Compute the minimum of three possible edit paths
                insert_cost = current_row[j] + 1
                delete_cost = previous_row[j + 1] + 1
                replace_cost = previous_row[j] + cost
                current_row.append(min(insert_cost, delete_cost, replace_cost))

            # Update the previous row for the next iteration
            previous_row = current_row

        # Normalize the distance to a similarity score
        distance = previous_row[-1]
        max_len = max(first_length, second_length)
        return 1.0 - distance / max_len


    @staticmethod
    def calculate(equation) -> str:
        try:
            return "The result is " + str(eval(equation))
        except:
            return "Sorry, I can't perform that math operation"

    @staticmethod
    def equation(string):
        # Yeah, this thing is toooooo long, but it works .-.
        match = regex.search("([-]?\d*\.\d+|\d+)([\+\-\*/]([-]?\d*\.\d+|\d+))+", string)
        if match:
            return match.group(0)
        else:
            return None


class response:
    ### Why not use constants?
    # because are boring and i cant add them docstrings :(
    # (If something is not NICE for me, it does not work for me)

    @staticmethod
    def no_found() -> str:
        """ - Message when an answer is not found """
        responses = [
            "Sorry, i don't have an answer for that question ...",
            "Sorry, i haven't found an answer to that ...",
            "Sorry, i don't have the answer :(",
            "Sorry, i do not know :("
        ]
        return brain.redaction(responses)

    @staticmethod
    def is_empty() -> str:
        """ - Message when trying to learn an empty answer """
        responses = [
            "Sorry, i can't learn an empty answer...",
            "Sorry, you didn't give me the answer :(",
            "Sorry, you didn't write an answer for that :("
        ]
        return brain.redaction(responses)

    @staticmethod
    def is_interesting() -> str:
        """ - If you know what it feels like to be ignored, you know what this is """
        responses = [
            "That sounds interesting ...",
            "Interesting, tell me more ...",
            "That's interesting :D",
            "Very interesting :D"
        ]
        return brain.redaction(responses)

    @staticmethod
    def was_learned() -> str:
        """ - Message indicating that a response has been learned """
        responses = [
            "I understand, now I can answer that question...",
            "Now I know how to answer that question...",
            "Great, I learned something new :D",
            "Yay!, you have taught me something new :D"
        ]
        return brain.redaction(responses)


class memory:

    @staticmethod
    def load(memory_file: str) -> dict:
        """Load the bot memory data"""

        # If the "memory.json" file does not exist, an empty one is created
        if not os.path.exists(memory_file):
            with open(memory_file, 'w', encoding="UTF-8") as memory_data:
                json.dump({}, memory_data, ensure_ascii=False, indent=4)
            return {}

        try:
            # Load the data from the bot's memory
            with open(memory_file, 'r', encoding="UTF-8") as memory_data:
                data = json.load(memory_data)
                return data
        except json.JSONDecodeError as exception:
            # Handle case where memory_file contains invalid JSON
            print(f"Error loading memory_file: {exception}")
            return {}


    @staticmethod
    def save(memory_file: str, current_memory: dict):
        """ Save learned bot data to the memory file """

        with open(memory_file, 'w', encoding="UTF-8") as memory_data:
            json.dump(current_memory, memory_data, ensure_ascii=False, indent=4)


    @staticmethod
    def suggestion(memory_file: str) -> list:
        # Load the questions from memory file
        memory_data: dict = memory.load(memory_file)

        # Create a list of questions that end with a question mark
        questions: list = list(question for question in memory_data.keys() if question.endswith('?'))

        # Randomly shuffle the questions
        random.shuffle(questions)

        # Take the first 3 questions from the list
        questions: list = questions[:3]

        # Return the selected questions
        return questions


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
            - A message confirming whether the bot successfully learned the new answer, as a string. If the answer was
              empty or invalid, a corresponding error message is returned.
        """

        # Convert words to lowercase and remove accents (if are)
        given_message: str = unicodedata.normalize("NFD", given_message.lower()).encode("ascii", "ignore").decode("utf-8")

        with prompt.status("Processing answer", "point"):
            memory.save(memory_file, current_memory)
            time.sleep(1)

            # Empty or invalid answers are not accepted
            if not given_answer.strip():
                return response.is_empty()

            # Add answer to existing message, or create new entry in the brain
            if given_message in current_memory:
                current_memory[given_message].append(given_answer.strip())
            else:
                current_memory[given_message] = [given_answer.strip()]

        with prompt.status("Saving answer", "point"):
            memory.save(memory_file, current_memory)
            time.sleep(1)

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

        with prompt.status("I'm thinking", "point"):
            time.sleep(2)

            # Convert words to lowercase and remove accents
            given_message: str = unicodedata.normalize("NFD", given_message.lower()).encode("ascii", "ignore").decode("utf-8")

            # Check if the input is a equation, if true, try resolve it
            if (brain.equation(given_message)):
                return brain.calculate(brain.equation(given_message))

            # Remove punctuation marks from the message
            given_message: str = regex.sub(r"[^\w\s]+", "", given_message)

            # Find the most similar key in the memory
            best_match = max(
                current_memory.keys(),
                key=lambda x: brain.comprehension(x, given_message)
            )

            # Check if the best match is similar enough to the message
            match_ratio = brain.comprehension(best_match, given_message)
            if match_ratio >= 0.50: # a similarity threshold of 50% is used (equivalent to the temperature)
                responses = current_memory[best_match]
                return random.choice(responses)
            else:
                # If no response is found, a default phrase is returned
                return response.no_found()
