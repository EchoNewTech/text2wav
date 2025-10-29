import numpy as np
import math
'''
Moduł z funkcjami pomocniczymi do kodowania i dekodowania dźwięku WAV.
Zamiana znaków na tony i odwrotnie, generowanie dźwięku.
'''
# --- PARAMETRY AUDIO ---
SAMPLE_RATE = 44100      # Częstotliwość próbkowania [Hz]
CHAR_DURATION = 0.25     # Czas trwania jednego znaku [s]
MIN_FREQ = 400.0         # Częstotliwość najniższego znaku [Hz]
MAX_FREQ = 2000.0        # Częstotliwość najwyższego znaku [Hz]
AMPLITUDE = 16000        # Amplituda dźwięku (16-bit PCM)
MIN_ASCII = 32           # Minimalny kod ASCII (' ')
MAX_ASCII = 379          # Maksymalny kod ASCII (np. '~', z rozszerzeniem)

# --- ZNAK → CZĘSTOTLIWOŚĆ ---
def char_to_freq(ch: str) -> float:
    """
    Zamienia znak na odpowiadającą częstotliwość.
    """
    code = min(max(ord(ch), MIN_ASCII), MAX_ASCII)        # ogranicz zakres kodów
    scale = (code - MIN_ASCII) / (MAX_ASCII - MIN_ASCII)  # przeskaluj do [0,1]
    freq = MIN_FREQ + scale * (MAX_FREQ - MIN_FREQ)       # przeskaluj do [MIN_FREQ, MAX_FREQ]
    return freq

# --- CZĘSTOTLIWOŚĆ → ZNAK ---
def freq_to_char(freq: float) -> str:
    """
    Zamienia częstotliwość na odpowiadający znak.
    """
    if not (MIN_FREQ <= freq <= MAX_FREQ):
        return '?'   # spoza zakresu
    scale = (freq - MIN_FREQ) / (MAX_FREQ - MIN_FREQ)      # przeskaluj do [0,1]
    code = int(round(MIN_ASCII + scale * (MAX_ASCII - MIN_ASCII)))
    return chr(min(max(code, MIN_ASCII), MAX_ASCII))       # ogranicz do zakresu

# --- GENEROWANIE TONU ---
def generate_tone(freq: float, duration: float) -> np.ndarray:
    """
    Generuje próbki dźwięku dla tonu o danej częstotliwości i czasie trwania.
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    wave_data = np.sin(2 * math.pi * freq * t)
    samples = (AMPLITUDE * wave_data).astype(np.int16)
    return samples

# --- DETEKCJA DOMINUJĄCEJ CZĘSTOTLIWOŚCI ---
def dominant_freq(signal: np.ndarray) -> float:
    """
    Znajduje dominantną częstotliwość w sygnale audio.
    Kroki:
    1. Oblicza FFT sygnału.
    2. Znajduje częstotliwość o największej amplitudzie
    3. Zwraca tę częstotliwość.
    """
    if len(signal) == 0:
        return 0.0
    fft = np.fft.fft(signal)
    mag = np.abs(fft[:len(signal)//2])   # amplituda (moduł) FFT pierwszej połowy
    freqs = np.fft.fftfreq(len(signal), 1/SAMPLE_RATE)[:len(signal)//2]
    return freqs[np.argmax(mag)]    # częstotliwość z maksymalną amplitudą