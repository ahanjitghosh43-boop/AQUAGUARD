import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Dataset
df = pd.read_csv("dataset/water_potability.csv")

# Display first 5 rows
print("\nFirst 5 Rows:")
print(df.head())

# Dataset Shape
print("\nDataset Shape:")
print(df.shape)

# Dataset Information
print("\nDataset Information:")
print(df.info())

# Statistical Description
print("\nStatistical Description:")
print(df.describe())

# Missing Values
print("\nMissing Values:")
print(df.isnull().sum())

# Target Column Distribution
print("\nPotability Distribution:")
print(df["Potability"].value_counts())

# Plot Potability Distribution
sns.countplot(x="Potability", data=df)
plt.title("Water Potability Distribution")
plt.xlabel("Potability (0 = Not Potable, 1 = Potable)")
plt.ylabel("Number of Samples")
plt.show()

# Correlation Heatmap
plt.figure(figsize=(10, 7))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Feature Correlation Heatmap")
plt.show()