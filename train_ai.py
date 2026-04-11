import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import pickle

# Generate training data (normal satellite behavior)
np.random.seed(42)
normal_data = []

# Feature: [hour, command_type, interval_seconds, is_unknown_ip]
# command_type: 0=capture, 1=transmit, 2=rotate, 3=power

# Normal: Daytime hours, slow commands, known IP
for _ in range(1000):
    hour = np.random.randint(6, 22)  # 6 AM to 10 PM
    cmd_type = np.random.randint(0, 4)
    interval = np.random.uniform(5, 30)  # 5-30 seconds between commands
    unknown_ip = 0  # known IP
    normal_data.append([hour, cmd_type, interval, unknown_ip])

# Generate some anomaly data (attacks)
for _ in range(100):
    hour = np.random.randint(0, 24)  # Any hour including 3 AM
    cmd_type = np.random.randint(0, 4)
    interval = np.random.uniform(0.1, 2)  # Very fast commands
    unknown_ip = np.random.choice([0, 1], p=[0.3, 0.7])  # Often unknown IP
    normal_data.append([hour, cmd_type, interval, unknown_ip])

df = pd.DataFrame(normal_data, columns=['hour', 'cmd_type', 'interval', 'unknown_ip'])
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(df)

with open('isolation_forest.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ AI Model Trained and Saved as 'isolation_forest.pkl")