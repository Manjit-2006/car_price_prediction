import joblib
import pandas as pd

model = joblib.load("car_price_model.pkl")

# Example input — change these values to test
data = {
    "Present_Price": [6.5],
    "Kms_Driven": [45000],
    "Fuel_Type": ["Petrol"],
    "Seller_Type": ["Dealer"],
    "Transmission": ["Manual"],
    "Owner": [0],
    "Car_Age": [5]
}

df = pd.DataFrame(data)

prediction = model.predict(df)
print("Estimated Selling Price:", prediction[0])
