import os
import json
import pandas as pd
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Paths where the model and validation data will be located
model_path = "/opt/ml/processing/model/model.tar.gz"
validation_data_path = "/opt/ml/processing/output/validation/validation.csv"

# Load the trained model
def load_model(model_path):
    import tarfile
    with tarfile.open(model_path) as tar:
        tar.extractall(path=".")
    model = joblib.load("model.joblib")  # Update based on the model type and format
    return model

# Load the validation data
def load_validation_data(validation_data_path):
    # Load the data into a pandas DataFrame
    data = pd.read_csv(validation_data_path)
    
    # The first column is treated as the target
    y_val = data.iloc[:, 0]  # First column as target
    X_val = data.iloc[:, 1:]  # All other columns as features
    
    return X_val, y_val

# Evaluate the model
def evaluate_model(model, X_val, y_val):
    # Predict using the trained model
    y_pred = model.predict(X_val)

    # Calculate accuracy
    accuracy = accuracy_score(y_val, y_pred)

    # Generate classification report
    report = classification_report(y_val, y_pred, output_dict=True)

    return accuracy, report

# Save the evaluation report to a JSON file
def save_evaluation_report(report, output_dir):
    evaluation_path = os.path.join(output_dir, "evaluation.json")
    with open(evaluation_path, "w") as f:
        json.dump(report, f)

if __name__ == "__main__":
    # Load model and validation data
    model = load_model(model_path)
    X_val, y_val = load_validation_data(validation_data_path)

    # Evaluate the model
    accuracy, report = evaluate_model(model, X_val, y_val)

    # Save evaluation metrics
    evaluation_output_dir = "/opt/ml/processing/evaluation"
    os.makedirs(evaluation_output_dir, exist_ok=True)

    # Save accuracy
    accuracy_report = {"accuracy": accuracy}
    save_evaluation_report(accuracy_report, evaluation_output_dir)

    # Save detailed classification report
    save_evaluation_report(report, evaluation_output_dir)
