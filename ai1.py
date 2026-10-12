"""Audio loading, preprocessing and feature extraction (MFCC + spectral features)."""
import io
import numpy as np
import librosa

SR = 16000          # sampling rate used everywhere
WINDOW_SEC = 3.0    # length of one analysis segment
HOP_SEC = 1.5       # step between segments (for uploaded files)


def load_audio(data: bytes) -> np.ndarray:
    """Decode WAV bytes -> mono float array at 16 kHz."""
    y, _ = librosa.load(io.BytesIO(data), sr=SR, mono=True)
    return y


def load_audio_file(path: str) -> np.ndarray:
    y, _ = librosa.load(path, sr=SR, mono=True)
    return y


def preprocess(y: np.ndarray) -> np.ndarray:
    """Trim silence at the edges and normalise volume."""
    y, _ = librosa.effects.trim(y, top_db=30)
    if len(y) == 0:
        return y
    peak = np.max(np.abs(y))
    return y / peak if peak > 0 else y


def split_segments(y: np.ndarray):
    """Yield (start_sec, end_sec, samples) windows. Short audio = one window."""
    win, hop = int(WINDOW_SEC * SR), int(HOP_SEC * SR)
    if len(y) <= win:
        yield 0.0, len(y) / SR, y
        return
    for s in range(0, len(y) - win + 1, hop):
        yield s / SR, (s + win) / SR, y[s:s + win]


def extract_features(y: np.ndarray) -> np.ndarray:
    """Fixed-length feature vector for one segment."""
    mfcc = librosa.feature.mfcc(y=y, sr=SR, n_mfcc=20)
    d1 = librosa.feature.delta(mfcc)
    d2 = librosa.feature.delta(mfcc, order=2)
    mel = librosa.power_to_db(librosa.feature.melspectrogram(y=y, sr=SR, n_mels=40))
    cent = librosa.feature.spectral_centroid(y=y, sr=SR)
    bw = librosa.feature.spectral_bandwidth(y=y, sr=SR)
    roll = librosa.feature.spectral_rolloff(y=y, sr=SR)
    flat = librosa.feature.spectral_flatness(y=y)
    zcr = librosa.feature.zero_crossing_rate(y)
    blocks = [mfcc, d1, d2, mel, cent, bw, roll, flat, zcr]
    return np.concatenate([np.r_[b.mean(axis=1), b.std(axis=1)] for b in blocks])