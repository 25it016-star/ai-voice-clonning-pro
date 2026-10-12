"""
Train the classifier.

Put your audio in:
    data/real/   -> genuine human speech (.wav/.flac/.mp3)
    data/fake/   -> AI-cloned / synthetic speech

Run from the backend folder:   python train.py
"""
import os, glob
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
from features import load_audio_file, preprocess, split_segments, extract_features

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
EXTS = ("wav", "flac", "mp3", "ogg", "m4a")


def collect(label_dir, label):
    X, y, groups = [], [], []
    files = [f for e in EXTS for f in glob.glob(os.path.join(DATA, label_dir, f"*.{e}"))]
    for i, f in enumerate(files):
        try:
            audio = preprocess(load_audio_file(f))
            for _, _, seg in split_segments(audio):
                if len(seg) < 8000:
                    continue
                X.append(extract_features(seg)); y.append(label); groups.append(f)
        except Exception as e:
            print("skip", f, e)
        if (i + 1) % 50 == 0:
            print(f"  {label_dir}: {i + 1}/{len(files)} files")
    return X, y, groups


if __name__ == "__main__":
    Xr, yr, gr = collect("real", 0)
    Xf, yf, gf = collect("fake", 1)
    X, y, groups = np.array(Xr + Xf), np.array(yr + yf), np.array(gr + gf)
    if len(set(y)) < 2:
        raise SystemExit("Need audio in BOTH data/real and data/fake.")

    # split by FILE so segments from one file never land in both train and test
    files = np.unique(groups)
    train_f, test_f = train_test_split(files, test_size=0.2, random_state=42)
    tr = np.isin(groups, train_f)
    te = ~tr

    model = make_pipeline(StandardScaler(),
                          RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1))
    model.fit(X[tr], y[tr])

    pred = model.predict(X[te])
    prob = model.predict_proba(X[te])[:, 1]
    print("\nConfusion matrix [real, fake]:\n", confusion_matrix(y[te], pred))
    print(classification_report(y[te], pred, target_names=["real", "fake"]))
    print("ROC-AUC:", round(roc_auc_score(y[te], prob), 3))

    # retrain on everything for the final model
    model.fit(X, y)
    joblib.dump(model, os.path.join(os.path.dirname(__file__), "model.joblib"))
    print("Saved backend/model.joblib")