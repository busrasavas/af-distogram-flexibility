<img src="logo.png" alt="AF-distogram Logo" width="600"/>


Here we explore **flexibility signals** embedded in **AlphaFold distograms**, with a special focus on **cryo-EM** interpretation.  

This repository supports the manuscript:
[**"Exploring the Potential of AlphaFold Distograms for Predicting Binding-induced Hinge Motions"**](https://www.biorxiv.org/content/10.1101/2025.07.25.666757v3)  
Authors: Büşra Savaş, Ayşe Berçin Barlas, Ezgi Karaca  

---

## 🔬 Research Background

AlphaFold’s distograms encode inter-residue distance distributions that often contain conformational information not visible in the final coordinate predictions. In this project, we investigate how these distograms capture binding-induced hinge motions using the AK2:AIFM1 complex as a test case. We compare distogram outputs across multiple AlphaFold versions (AF2.0 (AF2-ptm), AF2.1, AF2.2, AF2.3, AF3), different enhanced sampling strategies (MinnieFold, AF_cluster, AFsample2, AF3sample2, AF3_cluster), and evaluate their correspondence with molecular dynamics simulations. We also compare structural outputs from AF2- and AF3-based enhanced sampling methods with generative approaches such as BioEmu, Chai-1, and Boltz-2 in terms of sampled hinge distances.

---

## 📂 Folder Structure
```
data*/                                        
├── distograms/                               # Generated distograms per tool and targets
├── pdbs/                                     # Structural predictions and calculated distance measurements, access via Zenodo.
├── msas/                                     # MSA files (.a3m) used in distogram generation
├── md/                                       # Molecular dynamics based reference distances

scripts/
├── dist-calc-two-res.py                      # Extracts pairwise distances from PDB files
├── distogram-figures-main-figures.ipynb      # Plotting scripts for manuscript main figures
├── distogram-figures-supp-figures.ipynb      # Plotting scripts for manuscript supplementary figures
└── column_masking.py                         # Generates perturbed MSAs from AFsample2 .pkl outputs and the original MSA
```
* Large files omitted from the repo; available via[Zenodo.](https://zenodo.org/records/16364512).
  
**Visualize hinge motion distograms**

Use the provided Jupyter notebook to reproduce key figures in the manuscript, such as distogram plotting:
```
plot_all_distograms_in_directory(
    "/path/to/distograms",
    res_i=res_i,
    res_j=res_j,
    title=f"AK2 Distogram: Residue {res_i} vs {res_j}"
)
```
**Analyze custom pairwise distances**

Extract pairwise distance distributions for any residue pair (e.g., 230–233):
```
python dist-calc-two-res.py --input_pdb /path/to/pdb --residue1 230 --residue2 233
```

**🧠 Citing This Work**

If you find this repository useful, please consider citing our paper.

**📧 Contact**

For questions or contributions, feel free to contact:

Ezgi Karaca
📩 ezgi.karaca@ibg.edu.tr
