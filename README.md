# Minimum Hamming Distance Estimation using LSH

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)

Estimates the minimum Hamming distance between binary vectors using Locality-Sensitive Hashing (LSH) for efficient approximation.

## 🔍 Problem Statement
Calculating the exact minimum Hamming distance (number of differing bits between binary vectors) is computationally expensive for large datasets. This project provides:
- An LSH-based approximation (`min_hamming_LSH.py`)
- Scientific validation tools (`comparison.py`, `min_hamming.py`) to verify accuracy

## ✨ Key Features
- **LSH-optimized comparison**: Reduces pairwise computations via bit-position grouping (in `min_hamming_LSH.py`).
- **Rigorous validation**: Compare against brute-force method with accuracy metrics (in `comparison.py`).
- **Multiple evaluation runs**: Ensures consistent approximation through repeated sampling.
- **Customizable input**: Generate vectors of any length/count via command-line arguments.

## 🛠️ Getting Started

### Prerequisites
- **Python 3.7+** (check with `python --version`)
- **pip** (Python package manager)

### Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/bar-kalandarov/min-hamming-LSH.git
   cd min-hamming-LSH
   ```

2. **Install dependencies**:
   ```bash
   pip install numpy
   ```

## 💻 Usage

### Core LSH Implementation
```bash
python min_hamming_LSH.py --vectors 1000 --length 32 --iterations 10
```

Example Output:
```text
Minimum Hamming distance is 12
V1: [1,0,0,0,1,...]
V2: [1,0,1,0,1,...]
```

### Accuracy Validation
```bash
python comparison.py --vectors 1000 --length 32 --iterations 10 --samples 100
```
Example Output:
```text
Hit rate is 99.00%
Avg. relative error is 0.37%
```

### Arguments for Both Scripts:
| Flag           | Description                                        | Required |
|----------------|----------------------------------------------------|----------|
| `--vectors`    | Number of binary vectors to generate               | Yes      |
| `--length`     | Bit-length of each vector                          | Yes      |
| `--iterations` | Number of LSH iterations                           | Yes      |
| `--samples`    | (comparison.py only) Number of datasets to compare | Yes      |

## ⚙️ How It Works
1. **LSH Approximation** (`min_hamming_LSH.py`):
   - Groups vectors by randomly sampled bit positions
   - Compares only within groups 

2. **Validation Suite** (`comparison.py`):
   - Runs brute-force (`min_hamming.py`) and LSH methods in parallel
   - Calculates:
     - **Hit Rate**: % of exact matches
     - **Relative Error**: Average deviation when not matching

    
## 📊 Benchmark Results

Performance of LSH vs. brute-force on different datasets:

| Vectors | Length | Iterations | Samples | Hit Rate | Avg. Error |
|--------|--------|------------|---------|----------|------------|
| 1,000  | 32     | 1          | 100     | 50%      | 22%        |
| 1,000  | 32     | 5          | 100     | 93%      | 2%         |
| 1,000  | 32     | 10         | 100     | 98%      | 0.5%       |



## 📚 Dependencies
- `numpy` (for vector generation)
- Python built-ins: `argparse`, `math`, `collections`, `itertools`

