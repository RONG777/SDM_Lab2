import pandas as pd
from rdflib import Graph, Literal
from sklearn.model_selection import train_test_split

TTL_FILE   = "research_ontology.ttl"   # tu ABox en TTL
MAX_LIT_LEN= 200                  # filtrado de literales
SEED       = 42
MIN_COUNT   = 3    # Umbral mínimo para mantener relación en estratificación

def load_triples(ttl_path):
    g = Graph()
    g.parse(ttl_path, format="ttl")
    rows = []
    for s, p, o in g:
        if isinstance(o, Literal) and len(str(o)) > MAX_LIT_LEN:
            continue
        rows.append((str(s), str(p), str(o)))
    return pd.DataFrame(rows, columns=["head","relation","tail"])

def make_splits(df):
    counts = df["relation"].value_counts()
    df["stratify_rel"] = df["relation"].apply(
        lambda r: r if counts[r] >= MIN_COUNT else "rare"
    )
    # Split train vs temp (80/20)
    train, temp = train_test_split(
        df,
        test_size=0.2,
        random_state=SEED,
        stratify=df["stratify_rel"]
    )
    # Split temp en valid/test 50/50 -> 10/10 total
    counts_temp = temp["relation"].value_counts()
    temp["stratify_rel"] = temp["relation"].apply(
        lambda r: r if counts_temp[r] >= MIN_COUNT else "rare"
    )
    valid, test = train_test_split(
        temp,
        test_size=0.5,
        random_state=SEED,
        stratify=temp["stratify_rel"]
    )
    for split in (train, valid, test):
        split.drop(columns="stratify_rel", inplace=True)
    return train, valid, test

if __name__ == "__main__":
    df = load_triples(TTL_FILE)
    train, valid, test = make_splits(df)
    train.to_csv("train.tsv", sep="\t", index=False, header=False)
    valid.to_csv("valid.tsv", sep="\t", index=False, header=False)
    test.to_csv("test.tsv",  sep="\t", index=False, header=False)
    print(f"Total triples: {len(df)}  →  train={len(train)}, valid={len(valid)}, test={len(test)}")