import pandas as pd
import numpy as np
from ampligraph.datasets import load_from_csv
from ampligraph.latent_features import ScoringBasedEmbeddingModel
from ampligraph.compat import evaluate_performance
from ampligraph.evaluation import mrr_score, hits_at_n_score

# ——— Configuration ———
TRAIN_FILE = "train.tsv"
VALID_FILE = "valid.tsv"
TEST_FILE = "test.tsv"
OUTPUT_CSV = "comparison_ag2.csv"

MODELS      = ["TransE", "DistMult", "ComplEx"]
EMBED_DIMS  = [50, 100]
NEG_SAMPLES = [5, 20]
EPOCHS      = 200
BATCHES     = 150  # number of batches per epoch

# ——— Load splits ———
X_train_raw = load_from_csv(".", TRAIN_FILE, sep="\t")
X_valid_raw = load_from_csv(".", VALID_FILE, sep="\t")
X_test_raw  = load_from_csv(".", TEST_FILE,  sep="\t")

# —– Build vocab from train —–
all_ents = np.concatenate([
    X_train_raw[:, 0].astype(str),
    X_train_raw[:, 2].astype(str)
])
mask = all_ents != 'nan'
ents = np.unique(all_ents[mask])
rels = np.unique(X_train_raw[:, 1])
ent_to_idx = {e: i for i, e in enumerate(ents)}
rel_to_idx = {r: i for i, r in enumerate(rels)}

# —– Helper to map and filter triples —–
def map_and_filter(X_raw, ent_to_idx, rel_to_idx):
    mapped = []
    for h, r, t in X_raw:
        if h in ent_to_idx and r in rel_to_idx and t in ent_to_idx:
            mapped.append([ent_to_idx[h], rel_to_idx[r], ent_to_idx[t]])
    return np.array(mapped, dtype=int)

X_train = map_and_filter(X_train_raw, ent_to_idx, rel_to_idx)
X_valid = map_and_filter(X_valid_raw, ent_to_idx, rel_to_idx)
X_test  = map_and_filter(X_test_raw,  ent_to_idx, rel_to_idx)

results = []
best_mrr   = -1.0
best_model = None
best_cfg   = None

for name in MODELS:
    for dim in EMBED_DIMS:
        for neg in NEG_SAMPLES:
            print(f"Training {name:7s} | dim={dim:<3d} | negs={neg:<2d}")
            # Instantiate model
            model = ScoringBasedEmbeddingModel(
                eta=neg,
                k=dim,
                scoring_type=name,
                seed=0
            )
            model.compile(optimizer='adam', loss='pairwise')

            # Fit model
            batch_size = max(1, X_train.shape[0] // BATCHES)
            model.fit(
                X_train,
                batch_size=batch_size,
                epochs=EPOCHS,
                verbose=False
            )

            # Evaluate on validation
            ranks = evaluate_performance(
                X_valid,
                model=model,
                filter_triples=X_train,
                corrupt_side='s,o',
                batch_size=256
            )
            mrr  = mrr_score(ranks)
            h10  = hits_at_n_score(ranks, 10)
            print(f"  → MRR={mrr:.4f}, Hits@10={h10:.4f}")

            results.append({
                "model":   name,
                "dim":     dim,
                "negs":    neg,
                "MRR":     mrr,
                "Hits@10": h10,
            })

            # Update best model
            if mrr > best_mrr:
                best_mrr   = mrr
                best_model = model
                best_cfg   = {"model": name, "dim": dim, "negs": neg}

# Save comparison results
df = pd.DataFrame(results)
df.to_csv(OUTPUT_CSV, index=False)
print("\nValidation results saved to", OUTPUT_CSV)
print(df.sort_values("MRR", ascending=False))

# Report best on validation
print(f"\nBest on validation: {best_cfg} with MRR={best_mrr:.4f}")

# Evaluate best model on test
ranks_test = evaluate_performance(
    X_test,
    model=best_model,
    filter_triples=X_train,
    corrupt_side='s,o',
    batch_size=256
)
mrr_test    = mrr_score(ranks_test)
hits10_test = hits_at_n_score(ranks_test, 10)
print(f"Test       → MRR={mrr_test:.4f}, Hits@10={hits10_test:.4f}")