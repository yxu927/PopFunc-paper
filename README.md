# PopFunc-paper

**PopFunc-paper** is the companion repository for the manuscript:

> **Bayesian model-averaging of parametric coalescent models for phylodynamic inference**  
> _Yuan Xu, Kylie Chen, Walter Xie, Alexei J. Drummond, et al._

This repository contains all simulation data, real datasets, and analysis scripts needed to reproduce the results presented in the paper. We also demonstrate how to integrate these scripts with the **[PopFunc](https://github.com/LinguaPhylo/PopFunc)** codebase, which implements the Bayesian model-averaging framework for multiple parametric coalescent models (e.g., constant, exponential, logistic, Gompertz, and their expansion variants).

---

## Requirements

1. PopFunc  
   - Clone or download from [GitHub](https://github.com/LinguaPhylo/PopFunc). Follow its README to install or compile the plugin within your local BEAST2 setup.

2. BEAST2 (v2.7 or later)
   - [Official repository](https://github.com/CompEvol/beast2).  
   - Java 17 is recommended for the most recent BEAST2 releases.
  

3. Python 3.8+
   - Libraries such as `numpy`, `pandas`, `matplotlib`, `seaborn` (for plotting).

4. R language, tracerR from the github [TraceR](https://github.com/walterxie/TraceR) and packages:

```
readr
tools
ape
expm
ggtree
ggplot2
```
  
## Simulated Data

Under `data/simX/`, you will find multiple subfolders (e.g., `sim1`, `sim2`, etc.) each containing:

- XML files for BEAST2 analyses (e.g., `*.xml`).
- Ground-truth logs (e.g., `*_true.log` ) containing the “true” parameters used when simulating the data.  
- True trees (e.g., `*_true.trees`) if they are used for coverage or calibration checks.


Under the **PopFunc-paper** repository, you will find the following subfolders: `BMA_simulation/`, `cons-exp-cons/`, `gompertz_f0/`, `gompertz_t50/`, `logistic/`.

Each folder contains a `data/` subdirectory with the corresponding simulated datasets.

Note, `gompertz_t50/` and `gompertz_f0/` is structured like (`nooperator/`, `operator/`, `gt16/`), illustrating three different situations.

Beast analysis XML files are in sub-directories `../data/*.xml` for each dataset.


**Generating Figures (simulation data)**

To produce the necessary plots for data analysis:

Coverage plots: run `calc_tree_stats.py` from the scripts sub-directory.

Tree statistics plots: run `JC69_plot_coverage.py` from the scripts sub-directory.



## Real Dataset

1.We provide a real-world **HCV dataset** in **NEXUS** format under the file [`hcv.nexus`](https://github.com/yxu927/PopFunc-paper/blob/main/real/hcv/data/hcv.nexus). 
This file contains 63 HCV sequences (NTAX=63) each of length 411 nucleotides (NCHAR=411).


2.We also provide an **L86 dataset** in **FASTA** format, located in [`L86/L86.fasta`](https://github.com/yxu927/PopFunc-paper/blob/main/real/L86/data/L86meta.fasta). 


- Each dataset (HCV or L86) has its own `.xml` file for BEAST2.
- When you run BEAST2 on these `.xml` files, the resulting log (`*.log`) files are stored under `../beast/`.

- The file `BMA.R` provides the R script referenced in the paper for processing a single BMA log file and computing both posterior probabilities and log Bayes factors. To run this script:

In `BMA.R`, locate the line:

```r
log_file_path <- "../*.log"

```

and replace `../*.log` with the actual path to your BMA log file (e.g., `../hcv.log`).

Then open an R session or use Rscript from the command line:

```r
Rscript BMA.R

```

**Using `demographic.py` for BMA-Based Demographic Plots**

The script `demographic.py` in the `scripts` directory generates demographic-history plots after BMA analysis. To use it:


   In `demographic.py`, find the line:
   ```python
   data = pd.read_csv('../output_results.csv')

   ```

and replace `../output_results.csv` with the path to your actual CSV file.
And also find the line:

 ```python
plt.savefig('../*.png', format='png', dpi=600, bbox_inches='tight')

```

and change `../*.png` to the desired output path.










