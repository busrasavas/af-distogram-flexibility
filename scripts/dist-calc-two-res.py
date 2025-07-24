import pymol
import os
import csv
import argparse

# Initialize PyMOL in command-line mode
pymol.finish_launching(['pymol', '-cq'])

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Measure distance between two CB atoms of specified residues.")
parser.add_argument('--input_pdb', type=str, required=True, help='Input PDB file name')
parser.add_argument('--residue1', type=int, required=True, help='Residue number 1')
parser.add_argument('--residue2', type=int, required=True, help='Residue number 2')
parser.add_argument('--chain1', type=str, default='A', help='Chain ID for residue 1 (default: A)')
parser.add_argument('--chain2', type=str, default='A', help='Chain ID for residue 2 (default: A)')
parser.add_argument('--output_csv', type=str, default='measurements.csv', help='Output CSV file')

args = parser.parse_args()

# Load the structure
pymol.cmd.load(args.input_pdb)

# Hardcoded to select CB atoms only
selection1 = f"chain {args.chain1} and resi {args.residue1} and name CB"
selection2 = f"chain {args.chain2} and resi {args.residue2} and name CB"

# Measure distance
distance = pymol.cmd.distance("distance", selection1, selection2)

# Prepare header and data
header = ["PDB file", "Residue 1", "Residue 2", "Chain 1", "Chain 2", "Atom", "Distance"]
data = [os.path.basename(args.input_pdb), args.residue1, args.residue2, args.chain1, args.chain2, "CB", distance]

# Write to CSV
write_header = not os.path.exists(args.output_csv)

with open(args.output_csv, "a", newline="") as csv_file:
    writer = csv.writer(csv_file)
    if write_header:
        writer.writerow(header)
    writer.writerow(data)

# Clean up and exit
pymol.cmd.delete("all")
pymol.cmd.quit()

