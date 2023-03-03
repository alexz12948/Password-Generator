"""
Name: Alexander Zsikla
Date: March 2023

Holds the view/controller for the entire program and all of the relevant
functions to allow the GUI to function
"""

import sys

from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
                             QMainWindow, QMessageBox, QPushButton, QSlider,
                             QVBoxLayout, QWidget)

from keychain_dialog import KeychainDialog
from model import PasswordGeneratorModel

# Min/max lengths of the password
MIN_LEN = 5
MAX_LEN = 40


class PasswordGeneratorWindow(QMainWindow):
    """The view of the window and all the UI elements

    Attributes:
        _model: A class that holds all of the methods responsible for
                the functionality of the password generator
        main_layout: A layout that holds everything in window
        password: A label that holds the generated password
        regenerate_button: A button to generate another password
        copy_button: A button to copy the password to the clipboard
        length_label: A label to display the current length of the password
        length_slider: A slider to adjust the length of the password
        number_checkbox: A checkbox to include digits
        symbol_checkbox: A checkbox to include symbols
        timer: A timer to allow a delay in the animation of the copy button
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Generate Password")
        self.setFixedSize(500, 300)

        self._model = PasswordGeneratorModel()

        self.main_layout = QVBoxLayout()

        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

        self._create_ui()

    def _create_ui(self):
        header = QLabel(
            "<h1>Password Generator</h1>Automatically generate and save passwords to Apple Keychain"
        )
        self.main_layout.addWidget(header, alignment=Qt.AlignmentFlag.AlignTop)

        password_row = QHBoxLayout()

        self.password = QLabel(self._model.password)
        self.regenerate_button = QPushButton("")
        self.regenerate_button.setIcon(QIcon("refresh-icon.png"))
        self.regenerate_button.setIconSize(QSize(20, 20))
        self.regenerate_button.setToolTip("Generate another password")
        self.regenerate_button.clicked.connect(self.regenerate_password)

        password_row.addWidget(self.password)
        password_row.addStretch(1)
        password_row.addWidget(self.regenerate_button)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(password_row)
        self.main_layout.addStretch(1)

        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.main_layout.addWidget(self.copy_button)

        length_row = QHBoxLayout()

        self.length_label = QLabel(f"Length: {self._model.length}")
        self.length_slider = QSlider(Qt.Orientation.Horizontal)
        self.length_slider.setValue(45)
        self.length_slider.valueChanged.connect(self.update_length)

        length_row.addWidget(self.length_label)
        length_row.addWidget(self.length_slider)
        self.main_layout.addLayout(length_row)

        checkbox_row = QHBoxLayout()

        self.number_checkbox = QCheckBox("Digits (ex: 567)")
        self.number_checkbox.toggle()
        self.number_checkbox.stateChanged.connect(self.update_digit)

        self.symbol_checkbox = QCheckBox("Symbols (ex: #@!$)")
        self.symbol_checkbox.toggle()
        self.symbol_checkbox.stateChanged.connect(self.update_symbol)

        checkbox_row.addWidget(QLabel("Include: "))
        checkbox_row.addWidget(self.number_checkbox)
        checkbox_row.addWidget(self.symbol_checkbox)
        self.main_layout.addLayout(checkbox_row)

        self.add_to_keychain_btn = QPushButton("Add to Keychain")
        self.add_to_keychain_btn.clicked.connect(self.add_to_keychain)
        self.main_layout.addWidget(self.add_to_keychain_btn)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_button_to_default)

    def regenerate_password(self):
        """Regenerates the password and updates the GUI to reflect the new password"""
        self._model.generate_password()
        self.password.setText(self._model.password)

    @staticmethod
    def calculate_length(value: int):
        """Takes `value` (an int between 0 and 99) and converts it
        to a value between the min/max password length set as global
        variables at the top of the file
        """
        scale_val = (MAX_LEN - MIN_LEN) / 100
        return int(round(scale_val * value, 0) + MIN_LEN)

    def update_length(self, value: int):
        """Connect slider signal to updating the length"""
        new_len = self.calculate_length(value)

        if new_len != self._model.length:
            self.length_label.setText(f"Length: {new_len}")
            self._model.length = new_len
            self.regenerate_password()

    def update_symbol(self):
        """Connects the symbol button to updating the password requirements"""
        self._model.symbols = not self._model.symbols
        self.regenerate_password()

    def update_digit(self):
        """Connects the digit button to updating the password requirements"""
        self._model.digits = not self._model.digits
        self.regenerate_password()

    def update_button_to_default(self):
        """Updates the button back to the default state

        This is necessary due to the nature of QTimer that
        is set in `_create_ui`
        """
        self.copy_button.setText("Copy to Clipboard")
        self.copy_button.setEnabled(True)

    def copy_to_clipboard(self):
        """Copies the password to the clipboard and updates the GUI
        to have a message so the user knows that it was successfully copied
        """
        self._model.copy_to_clipboard()
        self.copy_button.setText("Copied")
        self.copy_button.setEnabled(False)
        self.timer.start(1000)

    def add_to_keychain(self):
        """Creates a dialog window to prompt for server and username information
        and then saves everything to iCloud Keychain
        """
        dlg = KeychainDialog(self)

        if dlg.exec():
            self._model.add_to_keychain(
                dlg.server_input.text(), dlg.username_input.text()
            )
            QMessageBox.information(
                self,
                "Successful Save",
                f"The password {self.password.text()} was successfully added to your keychain",
            )


def main():
    """Main driver of the program"""
    app = QApplication([])
    window = PasswordGeneratorWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
