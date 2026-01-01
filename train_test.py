from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
import joblib

from data_preprocessing import load_and_preprocess_data
from regression_model import build_model

# Load data
X, y = load_and_preprocess_data("car.csv")

# Categorical columns in your dataset
cat_cols = ["Fuel_Type", "Seller_Type", "Transmission"]

# Build model
model = build_model(cat_cols)

# Train / test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)

print("R2 Score:", r2_score(y_test, y_pred))
print("MAE:", mean_absolute_error(y_test, y_pred))

# Save trained model
joblib.dump(model, "car_price_model.pkl")
print("Model saved as car_price_model.pkl")