from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor

def build_model(cat_cols):
    preprocess = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(drop="first"), cat_cols)
        ],
        remainder="passthrough"
    )

    model = Pipeline(steps=[
        ("preprocess", preprocess),
        ("rf", RandomForestRegressor(n_estimators=200, random_state=42))
    ])

    return model