import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Model Comparison Results
df = pd.read_csv("results/model_comparison.csv")

print("\n===== MODEL PERFORMANCE COMPARISON =====\n")
print(df.to_string(index=False))

# Display Best Model
best_model = df.loc[df["F1 Score"].idxmax()]

print("\n===== BEST PERFORMING MODEL =====")
print("Model:", best_model["Model"])
print("Accuracy:", round(best_model["Accuracy"] * 100, 2), "%")
print("Precision:", round(best_model["Precision"] * 100, 2), "%")
print("Recall:", round(best_model["Recall"] * 100, 2), "%")
print("F1 Score:", round(best_model["F1 Score"] * 100, 2), "%")

# Model Accuracy Comparison
plt.figure(figsize=(9, 5))
sns.barplot(data=df, x="Model", y="Accuracy")

plt.title("Model Accuracy Comparison")
plt.ylabel("Accuracy")
plt.xlabel("Machine Learning Algorithms")
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig("results/accuracy_comparison.png")
plt.show()

# Performance Metrics Comparison
metrics = ["Accuracy", "Precision", "Recall", "F1 Score"]

df_melted = df.melt(
    id_vars="Model",
    value_vars=metrics,
    var_name="Metric",
    value_name="Score"
)

plt.figure(figsize=(10, 6))
sns.barplot(
    data=df_melted,
    x="Metric",
    y="Score",
    hue="Model"
)

plt.title("Machine Learning Model Performance")
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig("results/performance_comparison.png")
plt.show()

print("\nGraphs Saved Successfully!")