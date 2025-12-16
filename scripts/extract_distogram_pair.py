import os
import numpy as np
import pickle
import pandas as pd
import argparse

def save_distogram_to_csv(file_path, res_a, res_b, temperature=1.0):
    """
    Extracts distogram probabilities for a specific residue pair and saves to CSV.

    Args:
        file_path (str): Path to the .npz or .pkl file.
        res_a (int): Residue index A (1-based biological indexing).
        res_b (int): Residue index B (1-based biological indexing).
        temperature (float): Scaling factor for softmax (default 1.0).
    """
    
    # 1. Define AlphaFold Bin Centers
    # 64 bins from 2.0A to 22.0A
    bin_edges = np.arange(2.0, 22.1875 + 0.3125, 0.3125)[:65]
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    # 2. Load File
    logits = None
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    try:
        if file_path.endswith(".npz"):
            data = np.load(file_path, allow_pickle=True)
            logits = data.get('logits', None)
            if logits is None:
                dgram = data.get('distogram', None)
                if isinstance(dgram, dict) and 'logits' in dgram:
                    logits = dgram['logits']
                elif isinstance(dgram, np.ndarray):
                    logits = dgram
                    
        elif file_path.endswith((".pkl", ".pickle")):
            with open(file_path, "rb") as f:
                data = pickle.load(f)
                if 'logits' in data:
                    logits = data['logits']
                elif 'distogram' in data:
                    dgram = data['distogram']
                    if isinstance(dgram, dict) and 'logits' in dgram:
                        logits = dgram['logits']
                    elif isinstance(dgram, np.ndarray):
                        logits = dgram
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    if logits is None:
        print("Error: Could not locate 'logits' or 'distogram' in file.")
        return

    # 3. Process Logits to Probabilities
    # Apply temperature scaling
    scaled_logits = logits / temperature
    
    # Numerically stable softmax
    exp_logits = np.exp(scaled_logits - np.max(scaled_logits, axis=-1, keepdims=True))
    probs = exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)

    # 4. Extract Specific Residue Pair
    # Convert 1-based input to 0-based index
    idx_a = res_a - 1
    idx_b = res_b - 1

    try:
        # Extract the probability distribution (64 bins) for this pair
        pair_probs = probs[idx_a, idx_b, :]
    except IndexError:
        print(f"Error: Residue indices {res_a} or {res_b} are out of bounds for protein length {probs.shape[0]}.")
        return

    # 5. Save to CSV
    # Create DataFrame
    df = pd.DataFrame({
        'Distance_Angstrom': bin_centers,
        'Probability': pair_probs
    })

    # Generate output filename (same name, .csv extension)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_dir = os.path.dirname(file_path)
    # If file is in current dir, output_dir might be empty string
    if output_dir == '':
        output_dir = '.'
        
    output_filename = os.path.join(output_dir, f"{base_name}_res{res_a}_{res_b}.csv")

    df.to_csv(output_filename, index=False)
    print(f"Successfully saved distogram data to: {output_filename}")

# --- Example Usage Block ---
if __name__ == "__main__":
    # You can change these variables to test directly
    input_file = "example_prediction.pkl" 
    residue_1 = 50
    residue_2 = 60

    # Or uncomment the lines below to run via command line:
    # python script.py my_file.pkl 50 60
    import sys
    if len(sys.argv) >= 4:
         save_distogram_to_csv(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    else:
        print("Usage: python script.py <file_path> <res_a> <res_b>")