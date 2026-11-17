# 💧 AQUAGUARD
### Machine Learning Based Water Quality Prediction System

AQUAGUARD is a Machine Learning-based application that predicts whether water is potable or not potable using nine important water quality parameters.

## 🚀 Features

- Water Potability Prediction
- Machine Learning Model Integration
- Multiple Model Comparison
- Input Validation and Error Handling
- Prediction Confidence
- Permanent Prediction History
- Prediction Statistics Dashboard
- Pie Chart Visualization
- Export Prediction History to CSV
- Clear Prediction History
- Modern GUI using CustomTkinter

## 🧪 Water Quality Parameters

The application uses the following nine parameters:

1. pH
2. Hardness
3. Solids
4. Chloramines
5. Sulfate
6. Conductivity
7. Organic Carbon
8. Trihalomethanes
9. Turbidity

## 🤖 Machine Learning Models

The project explores and compares:

- Logistic Regression
- Decision Tree
- Random Forest

The best-performing model is selected based on F1 Score.

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- CustomTkinter
- Joblib

## 📂 Project Structure

```text
AQUAGUARD/
│
├── dataset/
│   └── water_potability.csv
│
├── models/
│   └── best_water_model.pkl
│
├── results/
│   ├── model_comparison.csv
│   ├── accuracy_comparison.png
│   ├── performance_comparison.png
│   └── prediction_history.csv
│
├── main.py
├── model_training.py
├── model_evaluation.py
├── prediction.py
├── eda.py
├── requirements.txt
└── readme.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_LINK
```

### 2. Open the Project Folder

```bash
cd AQUAGUARD
```

### 3. Install Required Libraries

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python main.py
```

## 📊 Application Workflow

1. Enter the nine water quality parameters.
2. Click the Predict Water Quality button.
3. The trained Machine Learning model generates a prediction.
4. View the prediction result and confidence.
5. Check prediction statistics and the pie chart.
6. View previously saved prediction history.
7. Export history as a CSV file when required.

## ⚠️ Disclaimer

AQUAGUARD provides Machine Learning-based predictions for educational and demonstration purposes. It is not a substitute for laboratory water testing or official drinking water safety certification.

## 👨‍💻 Developer

**Ahanjit Ghosh**

B.Tech – Computer Science and Engineering (AI & ML)

## ⭐ Support

If you find this project interesting, consider giving the repository a star!