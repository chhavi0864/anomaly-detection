import pandas as pd
import os

def generate_balanced_sample(input_csv, output_csv, total_rows=5000):
    print(f"Loading dataset from '{input_csv}'...")
    print("(This might take a minute depending on the size of the original dataset)")
    
    try:
        # Read the original massive dataset
        df = pd.read_csv(input_csv)
    except FileNotFoundError:
        print(f"❌ Error: Could not find '{input_csv}'.")
        print("Please ensure you have downloaded the real CICIDS dataset and updated the path.")
        return
        
    # Clean column names (strip leading/trailing whitespaces)
    df.columns = df.columns.str.strip()
    
    # Check for the Label column
    label_col = 'Label'
    if label_col not in df.columns:
        print(f"❌ Error: Could not find '{label_col}' column.")
        print(f"Available columns: {list(df.columns)}")
        return
        
    print("\nSeparating Normal and Anomalous traffic...")
    # In CICIDS2017, normal traffic is usually marked as 'BENIGN'
    normal_df = df[df[label_col] == 'BENIGN']
    anomaly_df = df[df[label_col] != 'BENIGN']
    
    print(f"Found {len(normal_df)} Normal records and {len(anomaly_df)} Anomaly records in the original data.")
    
    # Determine how many rows to pull from each category for a balanced split
    half_rows = total_rows // 2
    
    # Safely sample without exceeding available row counts
    n_anomalies_to_sample = min(half_rows, len(anomaly_df))
    n_normal_to_sample = total_rows - n_anomalies_to_sample
    
    print(f"Sampling {n_normal_to_sample} Normal rows and {n_anomalies_to_sample} Anomaly rows...")
    
    sampled_anomaly = anomaly_df.sample(n=n_anomalies_to_sample, random_state=42)
    sampled_normal = normal_df.sample(n=n_normal_to_sample, random_state=42)
    
    # Combine the samples and shuffle them (frac=1 shuffles the whole dataframe)
    balanced_df = pd.concat([sampled_normal, sampled_anomaly]).sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Since our API expects just the raw features to predict on, 
    # we don't technically need the Label column for the API test file, 
    # but we will keep it because the API automatically drops extra columns anyway!
    balanced_df.to_csv(output_csv, index=False)
    
    print(f"\n✅ Successfully generated balanced test set with {len(balanced_df)} rows!")
    print(f"Saved to: '{output_csv}'\n")
    print("--- Data Breakdown in the new Test File ---")
    print(balanced_df[label_col].value_counts())

if __name__ == '__main__':
    # -------------------------------------------------------------------
    # Configuration
    # -------------------------------------------------------------------
    
    # Path to your massive original CICIDS2017 dataset
    INPUT_DATASET = 'combinenew.csv' 
    
    # Path where you want to save the new balanced test file
    OUTPUT_DATASET = 'balanced_test_data.csv'
    
    # How many total rows do you want in the test file? (e.g., 1000, 5000, 10000)
    TOTAL_ROWS = 5000 
    
    # Run the generator
    generate_balanced_sample(INPUT_DATASET, OUTPUT_DATASET, total_rows=TOTAL_ROWS)
