import joblib
import pandas as pd
import numpy as np

# Load the exact feature list the model expects
features = joblib.load('models/features.joblib')

# Generate 10 rows of random numeric data
np.random.seed(42)
data = np.random.randint(0, 1000, size=(10, len(features)))

# Create a DataFrame
df = pd.DataFrame(data, columns=features)

# Save to CSV
df.to_csv('sample_test.csv', index=False)
print("sample_test.csv generated successfully with 10 rows and exact features!")
