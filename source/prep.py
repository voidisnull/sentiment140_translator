import pandas as pd
import html


def extract_labels_and_text(rawData: str, featureSet: str) -> None:
    """
    Extracts the desired feature columns and labels
    from the raw data save it to Training.csv

    """
    df = pd.read_csv(rawData, encoding="latin1", header=None)
    df.columns = ["Polarity", "Tweet ID", "Time", "Query", "User", "Tweet"]

    # Pre-processing data
    df["Tweet"] = df["Tweet"].astype(str).str.replace(r"@[\w_]+", "USER", regex=True)
    df["Tweet"] = df["Tweet"].astype(str).str.replace(r"http\S+", "URL", regex=True)
    df["Tweet"] = df["Tweet"].astype(str).str.strip()
    df["Polarity"] = df["Polarity"].apply(lambda x: 1 if x == 4 else 0)

    # Resolving html syntax sequences
    df["Tweet"] = df["Tweet"].apply(html.unescape)

    df.to_csv(featureSet, index=False, columns=["Polarity", "Tweet"], header=False)


def split_data_into_chunks(
    featureSet: str, langSpecificDir: str, chunk_size: int = 10000
) -> None:
    """
    Splits the Training.csv dataset into smaller chunks
    i.e. of 10,000 rows each
    """
    df = pd.read_csv(featureSet, header=None)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    chunks = [df[i : i + chunk_size] for i in range(0, len(df), chunk_size)]

    for i, chunk in enumerate(chunks):
        chunk.to_csv(f"{langSpecificDir}/{i + 1}.csv", index=False, header=False)


if __name__ == "__main__":
    extract_labels_and_text()
    split_data_into_chunks()
