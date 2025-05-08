# NanoGO Basecaller

<p align="center">
  <img src="https://raw.githubusercontent.com/phac-nml/nanogo/main/extra/nanogo_logo.svg" alt="NanoGo Logo" width="300" height="auto"/>
</p>

<p align="center">
  <strong>Oxford Nanopore Data Processing Made Simple</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/build-passing-brightgreen?style=for-the-badge&logo=gitlab&logoColor=white&logoWidth=40&color=green" alt="Build Status">
  <img src="https://img.shields.io/badge/coverage-58.6%25-brightgreen?style=for-the-badge&logo=codecov&logoColor=white&logoWidth=40&color=green" alt="Coverage">
  <img src="https://img.shields.io/badge/python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white&logoWidth=40&color=blue" alt="Python Versions">
  <img src="https://img.shields.io/pypi/dm/nanogo-basecaller?style=for-the-badge&logo=pypi&logoColor=white&logoWidth=30&color=orange" alt="PyPI Downloads">
  <img src="https://img.shields.io/badge/license-GNU%20GPL%20v3-blue?style=for-the-badge&logo=gnu&logoColor=white&logoWidth=40&color=blue" alt="License">
</p>

---

## Overview

**NanoGO Basecaller** is a specialized command-line tool designed for efficient processing of Oxford Nanopore Technologies (ONT) sequencing data. It integrates seamlessly with **Dorado**, ONT’s latest high-performance basecalling software, and supports both standard and duplex basecalling. Whether you are a seasoned bioinformatician or a newcomer to ONT data, NanoGO Basecaller offers:

- **Simple setup**: Automatic installation of Dorado and other dependencies
- **High-performance basecalling**: GPU acceleration and multi-threading support
- **Flexible workflows**: Interactive and scripted command-line modes
- **Demultiplexing**: On-the-fly barcode separation with intuitive output organization

---

## Quick Start

1. **Set up a Conda environment (Recommended)**:
   ```bash
   conda create -n nanogo-basecaller "python=3.10" -y
   conda activate nanogo-basecaller
   ```

2. **Install NanoGO Basecaller**:
   ```bash
   pip install nanogo-basecaller
   ```

3. **Install Dorado** (if not already installed):
   ```bash
   nanogo install-dorado  # Automatically handles latest version
   ```
   > *Use `--user` to install locally without sudo, or `--force` to overwrite an existing installation.*

4. **Run the basecaller**:
   ```bash
   nanogo basecaller -i /path/to/FAST5_or_POD5 -o /path/to/output
   ```
   You will be guided through model selection, demultiplexing, and hardware preferences.

That’s all it takes to start basecalling ONT data with **NanoGO**!

---

## Table of Contents

- [NanoGO Basecaller](#nanogo-basecaller)
  - [Overview](#overview)
  - [Quick Start](#quick-start)
  - [Table of Contents](#table-of-contents)
  - [Key Features](#key-features)
  - [Detailed Installation](#detailed-installation)
    - [System Requirements](#system-requirements)
    - [Step-by-Step Installation](#step-by-step-installation)
    - [Installing from Source](#installing-from-source)
    - [Installing Dorado](#installing-dorado)
      - [1. Using the Built-In Installer (Recommended)](#1-using-the-built-in-installer-recommended)
      - [2. Manual Installation](#2-manual-installation)
  - [Usage](#usage)
    - [Interactive Mode](#interactive-mode)
    - [Command-Line Mode](#command-line-mode)
  - [Workflow](#workflow)
  - [Command-Line Options](#command-line-options)
  - [Input and Output Structure](#input-and-output-structure)
    - [Input Directory](#input-directory)
    - [Output Directory](#output-directory)
    - [File Naming Convention](#file-naming-convention)
  - [Troubleshooting](#troubleshooting)
  - [License](#license)
  - [Support and Contact](#support-and-contact)

---

## Key Features

- **Dorado Integration**  
  Automatically installs and manages **Dorado** (v0.6.0+) for standard or duplex basecalling. No manual setup required.

- **Fast and Scalable**  
  Utilizes **GPU acceleration** and automatic resource detection to speed up large datasets. Supports **multi-GPU** configurations.

- **Interactive or Scripted**  
  A single command-line interface supports either guided (interactive) runs or scripted executions for automation.

- **On-the-Fly Demultiplexing**  
  Built-in barcode detection to produce organized output directories by barcode. Unclassified reads are also tracked.

- **Robust Conversion and Management**  
  Automatically converts FAST5 to POD5 format. Handles model selection, model downloads, and version checks.

- **Error Handling**  
  Offers comprehensive logging, graceful recovery, and easy debugging through user-friendly error messages.

---

## Detailed Installation

### System Requirements

- **Python**: 3.8 to 3.10 (3.11+ is currently unsupported)  
- **Operating System**: Linux or Windows Subsystem for Linux (WSL 2)  
- **CPU**: Minimum 4 cores recommended  
- **RAM**: 16GB+ recommended (32GB+ for larger datasets)  
- **Storage**: SSD recommended for high I/O workloads  
- **GPU** (Optional but Recommended):  
  - NVIDIA GPU with CUDA support for best performance  
  - Supports multiple GPUs for parallel jobs  

### Step-by-Step Installation

1. **Create a Conda environment**:
   ```bash
   conda create -n nanogo-basecaller "python=3.10" -y
   conda activate nanogo-basecaller
   ```

2. **Install NanoGO Basecaller using pip**:
   ```bash
   pip install nanogo-basecaller
   ```

3. **Verify the NanoGO CLI**:
   ```bash
   nanogo --help
   ```
   This should display help text and list available subcommands.

### Installing from Source

If you prefer to work with the latest source code:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/phac-nml/nanogo-basecaller.git
   cd nanogo-basecaller
   ```
2. **Install in development mode**:
   ```bash
   pip install -e .
   ```

### Installing Dorado

#### 1. Using the Built-In Installer (Recommended)

```bash
nanogo install-dorado
```
- Detects existing installations  
- Downloads and verifies the latest Dorado version  
- Installs to your virtual environment or system path  

Use `--user` to install locally (no sudo) or `--force` to overwrite any existing installation.

#### 2. Manual Installation

If automatic installation fails:
1. Download Dorado from [Oxford Nanopore’s CDN](https://cdn.oxfordnanoportal.com/software/analysis/).
2. Extract the tarball:
   ```bash
   tar -xzf dorado-x.y.z-linux-x64.tar.gz
   ```
3. Copy binaries and libraries to a directory in your PATH (e.g., `~/.local/bin` and `~/.local/lib`).
4. Add these directories to your system PATH or LD_LIBRARY_PATH as needed.

---

## Usage

### Interactive Mode

Run the basecaller without any arguments to enter interactive mode:
```bash
nanogo basecaller
```
You will be prompted to:
1. Select or confirm the input directory  
2. Choose a Dorado basecalling model  
3. Specify demultiplexing options (if relevant)  
4. Set GPU or CPU usage (auto-detected by default)

### Command-Line Mode

For direct or automated executions:
```bash
nanogo basecaller -i /path/to/reads -o /path/to/output [options]
```
Examples:
```bash
# Use GPU (auto-detected), standard basecalling
nanogo basecaller -i data/ -o results/

# Enable duplex basecalling
nanogo basecaller -i data/ -o results/ --duplex
```

---

## Workflow

1. **Version Check** – Verifies Dorado and POD5 versions.  
2. **Input Scanning** – Locates FAST5/POD5 files.  
3. **Configuration** – Selects basecalling model, sets up demultiplexing.  
4. **Preparation** – Converts FAST5 to POD5 if necessary; downloads models.  
5. **Basecalling** – Executes **Dorado** (standard/duplex) generating BAM or FASTQ files.  
6. **Demultiplexing** – Splits reads by barcode into subfolders.  
7. **Output Structuring** – Moves final outputs into well-defined directory tree.

---

## Command-Line Options

<details>
<summary><strong>Basecalling Options</strong></summary>

- **`-b, --basecaller`** – Enable specifying basecaller software (Dorado enabled by default).  
- **`-d, --duplex`** – Activates duplex basecalling mode.  
- **`-m, --model <model_name>`** – Manually specify a Dorado model.  
- **`--ignore <pattern>`** – Skip files matching the pattern (e.g., `_failed.pod5`).  
</details>

<details>
<summary><strong>Device Options</strong></summary>

- **`--device {auto,cpu,gpu}`** – Select processing device (default: auto-detect).  
- **`--gpu-device <ID>`** – Specify which GPU device to use (default: 0).  
</details>

<details>
<summary><strong>Advanced Options</strong></summary>

- **`--check-version`** – Check for the latest Dorado version (default: enabled).  
- **`--threads <N>`** – Specify number of CPU threads (default: auto-detect).  
- **`--chunk-size <SIZE>`** – Control chunking for basecalling.  
- **`--modified-bases`** – Enable modified base detection (requires a compatible model).  
</details>

---

## Input and Output Structure

### Input Directory

NanoGO expects an organized directory with raw ONT data:

```
/path/to/reads
├─ Sample_A
│  ├─ A_01.fast5
│  └─ A_02.fast5
├─ Sample_B
│  ├─ B_01.pod5
│  ├─ B_02.fast5
└─ ...
```
- Each subfolder is treated as a separate run or sample.  
- FAST5 or POD5 files are automatically detected.

### Output Directory

NanoGO creates a structured output folder:
```
/path/to/output
├─ temp_data
│  ├─ basecalling_model/
│  ├─ sample_sheet.csv
│  └─ sublist_# folders/ (processing chunks)
└─ final_output
   ├─ barcode01/
   ├─ barcode02/
   └─ unclassified/
```
- **temp_data**: Intermediate files, logs, partial BAM/FASTQ outputs  
- **final_output**: Fully demultiplexed and basecalled reads, separated by barcode  

### File Naming Convention

```
{flow_cell_id}_{run_id}_{model_hash}_{kit_hash}_{file_count}.fastq
```
1. **flow_cell_id** – From ONT metadata  
2. **run_id** – First 8 characters of run identifier  
3. **model_hash** – Short hash of the Dorado model used  
4. **kit_hash** – Short hash identifying the barcoding kit  
5. **file_count** – Incremental count to avoid conflicts  

This scheme ensures clarity, uniqueness, and traceability of all output files.

---

## Troubleshooting

1. **Installation Issues**  
   - *Compiler errors*: `conda install -c conda-forge gcc_linux-64 gxx_linux-64`  
   - *Missing Dorado*: Run `nanogo install-dorado` or manually install. Check your PATH.

2. **Runtime Errors**  
   - *No CUDA device*: Ensure NVIDIA drivers are installed, or use `--device cpu`.  
   - *Memory errors*: Lower chunk size or increase system RAM.  
   - *PySAM wheel issues*: Try `pip install --only-binary=:all: pysam`.

3. **Path or Permission Problems**  
   - Use `--user` or run with appropriate permissions (sudo) if installing system-wide.  
   - Update your `PATH` and `LD_LIBRARY_PATH` if installing Dorado manually.

---

## License

NanoGO Basecaller is distributed under the **GNU General Public License v3.0**. Refer to the [GNU GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.html) for the full terms and conditions.

---

## Support and Contact

- **Primary Contact**: [Gurasis Osahan](mailto:gurasis.osahan@phac-aspc.gc.ca), National Microbiology Laboratory  
- **Issue Tracking**: Use the GitHub [Issues](https://github.com/phac-nml/nanogo-basecaller/issues) page for bug reports or feature requests  
- **Documentation**: Additional references and usage examples are in the `docs/` directory  

*Maintained by the National Microbiology Laboratory, Public Health Agency of Canada.*  
*Ensuring public health through advanced genomics.*

---

> **Thank you for using NanoGO Basecaller!**  
> We continuously improve our tools to deliver efficient and robust ONT data processing. Feel free to reach out with any feedback or suggestions.