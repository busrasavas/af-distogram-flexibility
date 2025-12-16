import pickle
from pathlib import Path
import argparse
import os

# === Load perturbation pattern from .pkl file ===
def extract_pattern_from_pkl(pkl_path):
    with open(pkl_path, "rb") as f:
        data = pickle.load(f)
    return data.get("X_msa_indexes", [])

# === Load MSA from .a3m ===
def load_msa(msa_path):
    lines = Path(msa_path).read_text().splitlines()
    return [(lines[i], lines[i+1]) for i in range(0, len(lines), 2)]

# === Create ungapped → gapped index map ===
def ungapped_to_gapped_map(seq):
    mapping = {}
    idx = 0
    for i, c in enumerate(seq):
        if c != '-':
            mapping[idx] = i
            idx += 1
    return mapping

# === Apply perturbation and save ===
def apply_perturbation(msa, ungapped_positions, output_path):
    ref_seq = msa[0][1]
    ref_map = ungapped_to_gapped_map(ref_seq)
    gapped_positions = [ref_map[p] for p in ungapped_positions if p in ref_map]

    modified = [msa[0]]  # keep reference unmodified
    for header, seq in msa[1:]:
        seq_chars = list(seq)
        for pos in gapped_positions:
            if pos < len(seq_chars):
                seq_chars[pos] = 'X'
        modified.append((header, ''.join(seq_chars)))

    with open(output_path, "w") as f:
        for h, s in modified:
            f.write(h + "\n" + s + "\n")
    print(f"✅ Saved perturbed MSA to {output_path}")

# === Main ===
def main():
    parser = argparse.ArgumentParser(description="Generate perturbed MSA from a3m and pkl.")
    parser.add_argument("msa_file", type=str, help="Path to input .a3m MSA file")
    parser.add_argument("pkl_file", type=str, help="Path to input .pkl file containing X_msa_indexes")
    args = parser.parse_args()

    msa_file = args.msa_file
    pkl_file = args.pkl_file

    base_name = os.path.splitext(os.path.basename(pkl_file))[0]
    output_file = f"{base_name}_perturbed_msa.a3m"

    perturbed_columns = extract_pattern_from_pkl(pkl_file)
    msa = load_msa(msa_file)
    apply_perturbation(msa, perturbed_columns, output_file)

if __name__ == "__main__":
    main()
