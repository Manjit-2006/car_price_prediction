import pandas as pd

def load_and_preprocess_data(path):
    df = pd.read_csv(path)

    # Create car age
    df["Car_Age"] = 2025 - df["Year"]

    # Drop unused columns
    df = df.drop(["Car_Name", "Year"], axis=1)

    # Features (X) and target (y)
    X = df.drop("Selling_Price", axis=1)
    y = df["Selling_Price"]

    return X, y
