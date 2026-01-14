# Text2Wav: Szyfrowanie AES i Transmisja Danych w Paśmie Audio

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)]()

**Text2Wav** to aplikacja desktopowa typu *end-to-end*, która umożliwia bezpieczną wymianę wiadomości ukrytych w plikach dźwiękowych. Projekt łączy kryptografię symetryczną (AES) z technikami modulacji sygnału (FSK), pozwalając na zamianę tekstu na dźwięk i odwrotnie.

---

## Możliwości

* **Szyfrowanie AES-CBC:** Wiadomości są zabezpieczane algorytmem AES z użyciem hasła przed konwersją na dźwięk.
* **Audio Steganography / FSK:** Zamiana znaków ASCII na unikalne częstotliwości w paśmie 400Hz - 2000Hz.
* **Analiza Widmowa (FFT):** Dekodowanie dźwięku przy użyciu Szybkiej Transformaty Fouriera (Fast Fourier Transform).
* **GUI (PyQt6):** Nowoczesny i lekki interfejs graficzny.
* **Obsługa plików:** Import tekstów z `.txt` oraz zapis/odczyt plików `.wav`.

---

## Jak to działa "pod maską"? (Deep Dive)

Projekt opiera się na dwóch głównych filarach inżynierii: Kryptografii oraz Cyfrowym Przetwarzaniu Sygnałów (DSP).

### 1. Warstwa Kryptograficzna (AES)
Zanim tekst trafi do modulatora audio, jest on szyfrowany.
* **Algorytm:** AES (Advanced Encryption Standard) w trybie CBC (Cipher Block Chaining).
* **Klucz:** Wyprowadzany z hasła użytkownika (z dopełnieniem do 16 bajtów).
* **Bezpieczeństwo:** Każda wiadomość otrzymuje losowy wektor inicjalizujący (IV), co sprawia, że ta sama wiadomość zaszyfrowana tym samym hasłem dwukrotnie da zupełnie inny wynik binarny.

### 2. Warstwa Sygnałowa (Audio DSP)
Zaszyfrowany ciąg znaków (Base64) jest zamieniany na falę dźwiękową. Wykorzystałem technikę zbliżoną do **FSK (Frequency Shift Keying)**.

* **Modulacja (Kodowanie):**
    Każdy znak ASCII jest mapowany na częstotliwość z zakresu **400 Hz – 2000 Hz**.
    $$f(znak) = MIN\_FREQ + \frac{kod\_ascii - MIN}{MAX - MIN} \cdot (MAX\_FREQ - MIN\_FREQ)$$
    Następnie generowana jest fala sinusoidalna dla wyliczonej częstotliwości przez określony czas (domyślnie 0.25s).

* **Demodulacja (Dekodowanie):**
    System dzieli plik WAV na fragmenty czasowe (okna). Dla każdego fragmentu obliczana jest **dominująca częstotliwość** przy użyciu algorytmu **FFT (Fast Fourier Transform)**. Znaleziona częstotliwość jest mapowana z powrotem na znak ASCII.

---

## Wiedza i Edukacja

Ten projekt powstał w celu zgłębienia zaawansowanych koncepcji programistycznych. Kluczowe obszary nauki obejmowały:

### Cyfrowe Przetwarzanie Sygnałów (Digital Signal Processing)
* Zrozumienie **częstotliwości próbkowania (Sample Rate)** i twierdzenia Nyquista.
* Praktyczne zastosowanie **Transformacji Fouriera (numpy.fft)** do analizy widma sygnału i detekcji tonów wiodących.
* Generowanie fal sinusoidalnych i operacje na macierzach w bibliotece **NumPy**.

### Kryptografia Stosowana
* Różnice między trybami szyfrowania (np. CBC vs ECB).
* Znaczenie **Paddingu (PKCS#7)** w algorytmach blokowych.
* Bezpieczne zarządzanie danymi binarnymi i kodowaniem Base64.

### Inżynieria Oprogramowania
* Budowa modułowej architektury aplikacji (oddzielenie logiki biznesowej od GUI).
* Tworzenie interfejsów w **PyQt6** i obsługa zdarzeń (signals & slots).
* Typowanie statyczne w Pythonie (Type Hinting) dla zwiększenia czytelności kodu.

---

## Demo i Struktura

```mermaid
graph LR
    A[Tekst Jawny] -->|Hasło + AES| B(Zaszyfrowany Base64)
    B -->|Mapowanie Hz| C{Generator Tonów}
    C -->|Zapis| D[Plik .WAV]
    D -->|Odczyt + FFT| E{Analiza Częstotliwości}
    E -->|Odszyfrowanie| F[Oryginalna Wiadomość]
