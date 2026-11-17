import pandas as pd
import joblib

# Load Trained Model
model = joblib.load("models/best_water_model.pkl")

print("\n===================================")
print("       AQUAGUARD WATER PREDICTION")
print("===================================")

# Take User Input
print("\nEnter Water Quality Parameters:\n")

ph = float(input("Enter pH: "))
hardness = float(input("Enter Hardness: "))
solids = float(input("Enter Solids: "))
chloramines = float(input("Enter Chloramines: "))
sulfate = float(input("Enter Sulfate: "))
conductivity = float(input("Enter Conductivity: "))
organic_carbon = float(input("Enter Organic Carbon: "))
trihalomethanes = float(input("Enter Trihalomethanes: "))
turbidity = float(input("Enter Turbidity: "))

# Create Input DataFrame
input_data = pd.DataFrame([{
    "ph": ph,
    "Hardness": hardness,
    "Solids": solids,
    "Chloramines": chloramines,
    "Sulfate": sulfate,
    "Conductivity": conductivity,
    "Organic_carbon": organic_carbon,
    "Trihalomethanes": trihalomethanes,
    "Turbidity": turbidity
}])

# Make Prediction
prediction = model.predict(input_data)

# Display Result
print("\n===================================")
print("           PREDICTION RESULT")
print("===================================")

if prediction[0] == 1:
    print("Water Status: POTABLE")
    print("The water is predicted as suitable for drinking.")
else:
    print("Water Status: NOT POTABLE")
    print("The water is predicted as unsuitable for drinking.")

print("\n===================================")
print("Thank you for using AQUAGUARD!")
print("===================================")