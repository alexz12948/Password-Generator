"""
Name: Alexander Zsikla
Date: March 2023

Holds the model program and all of the relevant functions to hold the
state of the program at all times and the generator of the password
"""

import secrets
import subprocess
from string import ascii_lowercase, ascii_uppercase, digits, punctuation


class PasswordGeneratorModel:
    """The relevant functions for holding state and utility of the program

    Attributes:
        length: an integer that holds the current length of the password
        symbols: a boolean that determines whether symbols should be included in the password
        digits: a boolean that determines whether digits should be included in the password
        password: a string that is the most recently generated password
    """

    def __init__(self):
        self.length = 20
        self.symbols = True
        self.digits = True
        self.generate_password()

    def has_password_requirements(self, pwd: str) -> bool:
        """Returns whether the given password has all of the following requirements

        * It must have both upper and lower case letters
        * It must have at least 2 digits in the password if `digits` is True
        * It must have symbols if `symbols` is True
        """
        has_lower = any(c in ascii_lowercase for c in pwd)
        has_upper = any(c in ascii_uppercase for c in pwd)
        has_numbers = sum(c in digits for c in pwd) >= 2 if self.digits else True
        has_special = any(c in punctuation for c in pwd) if self.symbols else True
        return has_lower and has_upper and has_numbers and has_special

    def generate_password(self):
        """Creates alphabet and continuously generates passwords until
        it has all the requirements and stores it inside the attribute `password`
        """

        alphabet = ascii_lowercase + ascii_uppercase
        if self.digits:
            alphabet += digits

        if self.symbols:
            alphabet += punctuation

        while True:
            pwd = ""
            for _ in range(self.length):
                pwd += secrets.choice(alphabet)

            if self.has_password_requirements(pwd):
                break

        self.password = pwd

    def copy_to_clipboard(self):
        """Copies `password` to the clipboard"""
        subprocess.run("pbcopy", input=self.password.encode("utf-8"), check=True)
