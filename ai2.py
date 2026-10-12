"""Loads the trained model (if present) and scores audio segments."""
import os
import numpy as np
import joblib
from features import preprocess, split_segments, extract_features

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.joblib")


class Detector:
    def __init__(self):
        self.model = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None

    @property
    def mode(self) -> str:
        return "trained-model" if self.model is not None else "untrained-demo"

    def _score_segment(self, seg: np.ndarray) -> float:
        feats = extract_features(seg)
        if self.model is not None:
            # class 1 = fake / cloned
            return float(self.model.predict_proba([feats])[0][1])
        # ---- DEMO FALLBACK (NOT a real detector) ----
        # Only here so the UI works before you train a model. It just uses how
        # much the MFCC deltas vary. Do NOT report results from this mode.
        delta_std = float(np.mean(feats[20 * 2 + 20 * 2: 20 * 2 + 20 * 2 + 20]))
        return float(1 / (1 + np.exp(0.25 * (delta_std - 6))))

    def analyze(self, y: np.ndarray) -> dict:
        y = preprocess(y)
        if len(y) < 8000:  # < 0.5 s of usable speech
            return {"ok": False, "error": "Audio too short or silent."}
        segments = []
        for start, end, seg in split_segments(y):
            p = self._score_segment(seg)
            segments.append({"start": round(start, 1), "end": round(end, 1),
                             "fake_prob": round(p, 3)})
        probs = [s["fake_prob"] for s in segments]
        score = float(np.mean(probs))
        return {
            "ok": True,
            "mode": self.mode,
            "score": round(score, 3),
            "risk": risk_level(score),
            "segments": segments,
        }


def risk_level(score: float) -> str:
    if score < 0.35:
        return "LOW"
    if score < 0.65:
        return "MEDIUM"
    return "HIGH"