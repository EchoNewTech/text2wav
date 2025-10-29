import wave
import numpy as np
from audio_utils import (
    SAMPLE_RATE, CHAR_DURATION, MIN_FREQ, MAX_FREQ, AMPLITUDE,
    char_to_freq, freq_to_char, generate_tone, dominant_freq
)
'''
Moduł do kodowania tekstu do pliku WAV i dekodowania pliku WAV do tekstu.
Używa tonów o różnych częstotliwościach do reprezentacji znaków ASCII.
'''
def text_to_wav(text: str, filename: str) -> None:
    '''
    Zamienia tekst na dźwięk i zapisuje do pliku WAV.
    Każdy znak reprezentowany jest przez ton o określonej częstotliwości.
    '''
    if not text:
        raise ValueError("Brak tekstu do zapisania.")

    # Dla każdego znaku generujemy odpowiedni ton
    samples = [generate_tone(char_to_freq(ch), CHAR_DURATION) for ch in text]

    # Łączymy wszystkie próbki w całość
    audio = np.concatenate(samples)

    # Zapis do pliku WAV (mono, 16-bit, zadane SAMPLE_RATE)
    with wave.open(filename, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(audio.tobytes())

    print(f"[SUCCESS] Plik WAV został zapisany jako: {filename}")

def wav_to_text(filename: str) -> str:
    '''
    Odczytuje plik WAV i zamienia dźwięk na tekst.
    Każdy ton odpowiada jednemu znakowi ASCII.
    '''
    try:
        # Otwórz plik WAV do odczytu
        with wave.open(filename, "rb") as w:
            # Jeśli parametry pliku są nietypowe – ostrzeżenie
            if w.getnchannels() != 1 or w.getsampwidth() != 2 or w.getframerate() != SAMPLE_RATE:
                print("[WARN] Plik nie jest mono, 16-bit, 44100 Hz.")
            frames = w.readframes(w.getnframes())
    except wave.Error as e:
        print(f"[ERROR] Nie można otworzyć pliku WAV: {e}")
        return ""

    # Zamiana ramek bajtowych na próbki numpy (16-bitowe)
    samples = np.frombuffer(frames, dtype=np.int16)
    chunk_size = int(SAMPLE_RATE * CHAR_DURATION)
    chars = []

    # Przetwarzaj każdą porcję/próbkę odpowiadającą jednemu znakowi
    for i in range(0, len(samples), chunk_size):
        chunk = samples[i:i + chunk_size]
        if len(chunk) < chunk_size // 2:
            continue  # pomiń jeśli próbka za krótka (np. na końcu pliku)
        freq = dominant_freq(chunk)      # wyznacz dominantę częstotliwości
        ch = freq_to_char(freq)          # zamień częstotliwość na znak
        chars.append(ch)

    # Złóż znaki w wiadomość
    message = ''.join(chars)
    return message
