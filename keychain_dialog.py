"""
Name: Alexander Zsikla
Date: March 2023

Holds the view for the dialog to enter the server and username
for storing all information to iCloud Keychain
"""

from PyQt6.QtWidgets import (QDialog, QDialogButtonBox, QLabel, QLineEdit,
                             QMessageBox, QVBoxLayout)


class KeychainDialog(QDialog):
    """The view of the dialog

    Attributes:
        button_box: 2 buttons for canceling or saving the information
        layout: A vertical layout that holds all widgets
        server_input: The input for the server url
        username_input: The input for the username
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add Password to Apple Keychain")
        self.setFixedSize(400, 150)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self.confirm)
        self.button_box.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Server"))

        self.server_input = QLineEdit()
        self.layout.addWidget(self.server_input)

        self.layout.addWidget(QLabel("Username"))

        self.username_input = QLineEdit()
        self.layout.addWidget(self.username_input)

        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def confirm(self):
        """Creates a QMessageBox to confirm the inputted information"""
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Confirm Inputs")
        dlg.setText(
            "Are you sure this information is correct?\n"
            f"Server: {self.server_input.text()}\n"
            f"Username: {self.username_input.text()}"
        )
        dlg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        dlg.setIcon(QMessageBox.Icon.Question)
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Yes:
            self.accept()
