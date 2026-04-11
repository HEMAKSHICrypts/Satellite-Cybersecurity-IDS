import pandas as pd
import numpy as np
import pickle
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Load trained model
with open('isolation_forest.pkl', 'rb') as f:
    model = pickle.load(f)

# Create test data with known labels
np.random.seed(123)
test_data = []

# NORMAL test samples (500)
for _ in range(500):
    hour = np.random.randint(6, 22)
    cmd_type = np.random.randint(0, 4)
    interval = np.random.uniform(5, 30)
    unknown_ip = 0
    test_data.append([hour, cmd_type, interval, unknown_ip, 0])

# ATTACK test samples (100)
for _ in range(100):
    hour = np.random.randint(0, 24)
    cmd_type = np.random.randint(0, 4)
    interval = np.random.uniform(0.1, 2)
    unknown_ip = 1
    test_data.append([hour, cmd_type, interval, unknown_ip, 1])

df_test = pd.DataFrame(test_data, columns=['hour', 'cmd_type', 'interval', 'unknown_ip', 'is_attack'])

X_test = df_test[['hour', 'cmd_type', 'interval', 'unknown_ip']]
y_test = df_test['is_attack']

# Predict
predictions = model.predict(X_test)
predictions_binary = [0 if x == 1 else 1 for x in predictions]

# Calculate metrics
accuracy = accuracy_score(y_test, predictions_binary)

print("=" * 60)
print("🔬 AI MODEL EVALUATION REPORT - PROOF OF ACCURACY")
print("=" * 60)
print(f"\n📊 Test Data: {len(df_test)} samples")
print(f"   - Normal Commands: {sum(y_test==0)} samples")
print(f"   - Attack Commands: {sum(y_test==1)} samples")
print("\n" + "=" * 60)
print(f"✅ ACCURACY: {accuracy * 100:.2f}%")
print("=" * 60)

print("\n📋 CLASSIFICATION REPORT:")
print(classification_report(y_test, predictions_binary, target_names=['NORMAL', 'ATTACK']))

print("\n📊 CONFUSION MATRIX:")
print("                 Predicted")
print("              NORMAL   ATTACK")
tn, fp, fn, tp = confusion_matrix(y_test, predictions_binary).ravel()
print(f"Actual Normal     {tn:4d}    {fp:4d}")
print(f"Actual Attack     {fn:4d}    {tp:4d}")

print("\n🎯 KEY METRICS SUMMARY:")
print(f"   ✓ Detection Rate: {(tp/(tp+fn))*100:.2f}% (Attacks caught)")
print(f"   ✓ False Alarm Rate: {(fp/(fp+tn))*100:.2f}% (Normals flagged as attack)")
print(f"   ✓ Precision: {tp/(tp+fp)*100:.2f}%")
print(f"   ✓ Recall: {tp/(tp+fn)*100:.2f}%")
print(f"   ✓ F1-Score: {2 * (tp/(tp+fp)) * (tp/(tp+fn)) / ((tp/(tp+fp)) + (tp/(tp+fn))) * 100:.2f}%")