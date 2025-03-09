import sys
import random
import string
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QSpinBox, QCheckBox, QPushButton, QLineEdit, QMessageBox, QComboBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class PasswordGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.languages = {
            "English": {
                "title": "Open Random Password Generator",
                "password_length": "Password Length:",
                "uppercase": "Uppercase Letters (A-Z)",
                "lowercase": "Lowercase Letters (a-z)",
                "numbers": "Numbers (0-9)",
                "special": "Special Characters (!@#$%^&*)",
                "generate": "Generate Password",
                "copy": "Copy to Clipboard",
                "show_password": "Show Password",
                "error": "Error",
                "select_char_type": "Please select at least one character type!",
                "success": "Success",
                "copied": "Password copied to clipboard!"
            },
            "Turkish": {
                "title": "Open Random Password Generator",
                "password_length": "Şifre Uzunluğu:",
                "uppercase": "Büyük Harfler (A-Z)",
                "lowercase": "Küçük Harfler (a-z)",
                "numbers": "Rakamlar (0-9)",
                "special": "Özel Karakterler (!@#$%^&*)",
                "generate": "Şifre Oluştur",
                "copy": "Panoya Kopyala",
                "show_password": "Şifreyi Göster",
                "error": "Hata",
                "select_char_type": "Lütfen en az bir karakter türü seçin!",
                "success": "Başarılı",
                "copied": "Şifre panoya kopyalandı!"
            }
        }
        self.current_language = "English"
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.languages[self.current_language]["title"])
        self.setGeometry(200, 200, 500, 400)
        self.setStyleSheet("background-color: #1E1E2E; color: #CDD6F4; font-size: 14px; font-family: Arial;")

        layout = QVBoxLayout()

        # Language selection
        self.language_selector = QComboBox()
        self.language_selector.addItems(["English", "Turkish"])
        self.language_selector.currentTextChanged.connect(self.change_language)
        self.language_selector.setStyleSheet("background-color: #313244; color: #CDD6F4; padding: 6px; border-radius: 8px;")

        # Password length
        self.length_label = QLabel()
        self.length_spinbox = QSpinBox()
        self.length_spinbox.setRange(4, 64)
        self.length_spinbox.setValue(12)
        self.length_spinbox.setStyleSheet("background-color: #313244; color: #CDD6F4; padding: 6px; border-radius: 8px;")

        # Options (default checked)
        self.uppercase_checkbox = QCheckBox()
        self.uppercase_checkbox.setChecked(True)

        self.lowercase_checkbox = QCheckBox()
        self.lowercase_checkbox.setChecked(True)

        self.numbers_checkbox = QCheckBox()
        self.numbers_checkbox.setChecked(True)

        self.special_checkbox = QCheckBox()
        self.special_checkbox.setChecked(True)

        # Generate password button
        self.generate_button = QPushButton()
        self.generate_button.setStyleSheet("background-color: #89B4FA; color: #1E1E2E; padding: 12px; border-radius: 8px; font-weight: bold;")
        self.generate_button.clicked.connect(self.generate_password)

        # Password output
        self.result_text = QLineEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setFont(QFont("Courier", 14))
        self.result_text.setStyleSheet("background-color: #313244; color: #CDD6F4; padding: 6px; border-radius: 8px;")
        self.result_text.setEchoMode(QLineEdit.EchoMode.Password)  # Varsayılan olarak gizli

        # Show password checkbox
        self.show_password_checkbox = QCheckBox()
        self.show_password_checkbox.setChecked(False)
        self.show_password_checkbox.setStyleSheet("padding: 6px;")
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)

        # Copy to clipboard button
        self.copy_button = QPushButton()
        self.copy_button.setStyleSheet("background-color: #A6E3A1; color: #1E1E2E; padding: 12px; border-radius: 8px; font-weight: bold;")
        self.copy_button.clicked.connect(self.copy_to_clipboard)

        # Layout structure
        layout.addWidget(self.language_selector)
        layout.addWidget(self.length_label)
        layout.addWidget(self.length_spinbox)
        layout.addWidget(self.uppercase_checkbox)
        layout.addWidget(self.lowercase_checkbox)
        layout.addWidget(self.numbers_checkbox)
        layout.addWidget(self.special_checkbox)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.result_text)
        layout.addWidget(self.show_password_checkbox)
        layout.addWidget(self.copy_button)

        self.setLayout(layout)
        self.update_texts()

    def update_texts(self):
        lang = self.languages[self.current_language]
        self.setWindowTitle(lang["title"])
        self.length_label.setText(lang["password_length"])
        self.uppercase_checkbox.setText(lang["uppercase"])
        self.lowercase_checkbox.setText(lang["lowercase"])
        self.numbers_checkbox.setText(lang["numbers"])
        self.special_checkbox.setText(lang["special"])
        self.generate_button.setText(lang["generate"])
        self.copy_button.setText(lang["copy"])
        self.show_password_checkbox.setText(lang["show_password"])

    def change_language(self, language):
        self.current_language = language
        self.update_texts()

    def generate_password(self):
        length = self.length_spinbox.value()
        charset = ""
        lang = self.languages[self.current_language]

        if self.uppercase_checkbox.isChecked():
            charset += string.ascii_uppercase
        if self.lowercase_checkbox.isChecked():
            charset += string.ascii_lowercase
        if self.numbers_checkbox.isChecked():
            charset += string.digits
        if self.special_checkbox.isChecked():
            charset += "!@#$%^&*"

        if not charset:
            QMessageBox.warning(self, lang["error"], lang["select_char_type"])
            return

        password = ''.join(random.choice(charset) for _ in range(length))
        self.result_text.setText(password)

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.result_text.text())
        QMessageBox.information(self, self.languages[self.current_language]["success"], self.languages[self.current_language]["copied"])

    def toggle_password_visibility(self):
        if self.show_password_checkbox.isChecked():
            self.result_text.setEchoMode(QLineEdit.EchoMode.Normal)  # Şifreyi göster
        else:
            self.result_text.setEchoMode(QLineEdit.EchoMode.Password)  # Şifreyi gizle

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordGenerator()
    window.show()
    sys.exit(app.exec())
