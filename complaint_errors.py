# Re-runs the notebook's "after" setup (10 epochs) for seeds 42, 7, 2024 and
# saves every test prediction, so the complaint errors can be read post by post.
# Mirrors takemeter.ipynb sections 3-5. Run from the repo: python complaint_errors.py
import json
from pathlib import Path
import numpy as np
import pandas as pd
from datasets import Dataset
from sklearn.model_selection import train_test_split
from transformers import (AutoTokenizer, AutoModelForSequenceClassification,
                          TrainingArguments, Trainer, set_seed)

REPO = Path(__file__).parent
OUT = REPO
LABELS = ["question", "review", "psa", "complaint"]
BASE, EPOCHS, LR, BS, MAXLEN = "distilbert-base-uncased", 10, 2e-5, 16, 128

df = pd.read_csv(REPO / "labels.csv")


def split_dataset(df, seed, test_size=0.15, val_size=0.15):
    strat = lambda f: f["label"] if f["label"].value_counts().min() >= 2 else None
    rest, test = train_test_split(df, test_size=test_size, random_state=seed, stratify=strat(df))
    train, val = train_test_split(rest, test_size=val_size / (1 - test_size),
                                  random_state=seed, stratify=strat(rest))
    return [x.reset_index(drop=True) for x in (train, val, test)]


def to_ids(frame):
    lookup = {l: i for i, l in enumerate(LABELS)}
    out = frame.copy()
    out["labels"] = out["label"].astype(str).str.strip().map(lookup)
    return out[["text", "labels"]]


rows = []
for seed in [42, 7, 2024]:
    tr, va, te = split_dataset(df, seed)
    set_seed(seed)
    tok = AutoTokenizer.from_pretrained(BASE)
    model = AutoModelForSequenceClassification.from_pretrained(
        BASE, num_labels=len(LABELS),
        id2label=dict(enumerate(LABELS)), label2id={l: i for i, l in enumerate(LABELS)})
    t = lambda b: tok(b["text"], truncation=True, padding="max_length", max_length=MAXLEN)
    ds = lambda f: Dataset.from_pandas(to_ids(f)).map(t, batched=True)
    args = TrainingArguments(output_dir=str(REPO / "takemeter_out"), num_train_epochs=EPOCHS,
                             learning_rate=LR, per_device_train_batch_size=BS,
                             per_device_eval_batch_size=BS, eval_strategy="epoch",
                             save_strategy="no", logging_steps=10, seed=seed,
                             report_to="none", disable_tqdm=True)
    trainer = Trainer(model=model, args=args, train_dataset=ds(tr), eval_dataset=ds(va))
    trainer.train()
    logits = trainer.predict(ds(te)).predictions
    exp = np.exp(logits - logits.max(axis=-1, keepdims=True))
    probs = exp / exp.sum(axis=-1, keepdims=True)
    for i, row in te.iterrows():
        rows.append({"seed": seed, "text": row["text"], "gold": row["label"],
                     "note": row.get("note"),
                     "predicted": LABELS[int(probs[i].argmax())],
                     "probs": {l: round(float(p), 3) for l, p in zip(LABELS, probs[i])}})
    acc = np.mean([r["gold"] == r["predicted"] for r in rows if r["seed"] == seed])
    print(f"seed {seed}: accuracy {acc:.3f}", flush=True)

(OUT / "complaint_predictions_after.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
print("wrote", OUT / "complaint_predictions_after.json")
