import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QLabel, QTextEdit, QLineEdit, QFileDialog, QMessageBox, QInputDialog
)
from PyQt6.QtWidgets import QLineEdit as QLineEditWidget
from de_coder import text_to_wav, wav_to_text
from aes import encrypt_aes, decrypt_aes
'''
Moduł GUI do kodowania tekstu do pliku WAV z szyfrowaniem AES oraz dekodowania pliku WAV do tekstu z odszyfrowaniem AES.
Używa tonów o różnych częstotliwościach do reprezentacji znaków ASCII.
'''
class TextWavApp(QWidget):
    def __init__(self):
        '''
        Inicjalizacja GUI aplikacji do kodowania i dekodowania tekstu z użyciem WAV i AES.
        '''
        super().__init__()
        # Ustawienia głównego okna programu
        self.setWindowTitle("Text <-> WAV (ASCII encoder/decoder)")
        self.resize(400, 300)  # kompaktowy rozmiar okna
        layout = QVBoxLayout(self)  # pionowy layout dla wszystkich widgetów

        # Nagłówek programu
        layout.addWidget(QLabel("Text <-> WAV Converter (+AES encryption)"))

        # Pole tekstowe do wpisania wiadomości
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Wpisz tekst do zaszyfrowania...")
        layout.addWidget(self.text_input)

        # Przycisk do importu tekstu z pliku .txt
        btn_load = QPushButton("Wczytaj tekst z pliku .txt")
        btn_load.clicked.connect(self.load_text)
        layout.addWidget(btn_load)

        # Przycisk: kodowanie tekstu do pliku .wav
        btn_encode = QPushButton("Zamień tekst na WAV")
        btn_encode.clicked.connect(self.encode_text)
        layout.addWidget(btn_encode)

        # Pole wejściowe do wpisania/zładowania pliku .wav do dekodowania
        self.wav_input = QLineEdit()
        self.wav_input.setPlaceholderText("Plik WAV do odczytu")
        layout.addWidget(self.wav_input)

        # Przycisk do dekodowania pliku .wav do tekstu
        btn_decode = QPushButton("Odczytaj tekst z WAV (wymaga hasła)")
        btn_decode.clicked.connect(self.decode_wav)
        layout.addWidget(btn_decode)

    def load_text(self):
        # Otwiera okno dialogowe by wybrać plik .txt i ładuje jego zawartość do self.text_input
        path, _ = QFileDialog.getOpenFileName(self, "TXT", filter="*.txt")
        if path:
            with open(path, "r", encoding="utf-8") as f:
                self.text_input.setPlainText(f.read())

    def encode_text(self):
        # Koduje tekst z self.text_input do pliku .wav, zapisuje poprzez okno dialogowe
        text = self.text_input.toPlainText().strip()
        if not text:
            return QMessageBox.information(self, "Brak tekstu", "Pole tekstowe jest puste.")
        
        password, ok = QInputDialog.getText(self, "Hasło", "Wpisz hasło do szyfrowania:", QLineEditWidget.EchoMode.Password)
        if not ok or not password:
            return QMessageBox.information(self, "Brak hasła", "Szyfrowanie wymaga hasła.")
        
        encrypted_msg = encrypt_aes(text, password)

        path, _ = QFileDialog.getSaveFileName(self, "Zapisz WAV", filter="*.wav")
        if path:
            if not path.lower().endswith('.wav'):
                path += '.wav'  # automatyczne dodanie .wav jeśli brak
            try:
                text_to_wav(encrypted_msg, path)
                QMessageBox.information(self, "OK", f"WAV zapisany jako:\n{path}")
            except Exception as e:
                QMessageBox.critical(self, "Błąd", str(e))

    def decode_wav(self):
        # Dekoduje plik .wav do tekstu, pokazuje wynik w okienku
        path = self.wav_input.text().strip()

        # Jeśli użytkownik wpisał ścieżkę, upewnij się, że ma rozszerzenie .wav
        if path and not path.lower().endswith('.wav'):
            path += '.wav'  # automatyczne dodanie .wav jeśli brak

        # Jeśli pole jest puste, otwórz okno dialogowe do wyboru pliku
        if not path:
            path, _ = QFileDialog.getOpenFileName(self, "Wybierz WAV", filter="*.wav")
            if not path:
                return
        try:
            encrypted_msg = wav_to_text(path)
            password, ok = QInputDialog.getText(self, "Hasło", "Wpisz hasło do odszyfrowania:", QLineEditWidget.EchoMode.Password)
            if not ok or not password:
                return QMessageBox.information(self, "Brak hasła", "Odszyfrowanie wymaga hasła.")
            decrypted_msg = decrypt_aes(encrypted_msg, password)
            QMessageBox.information(self, "Odczytano", decrypted_msg)
        except Exception as e:
            QMessageBox.critical(self, "Błąd", str(e))

def create_ui():
    app = QApplication(sys.argv)
    win = TextWavApp()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    create_ui() 
