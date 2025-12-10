#  Functional Data Processing Project (Functional-data-processing)

This repository contains two distinct implementations for a data processing pipeline: one built using a **functional programming style** and the other developed using an **imperative programming style**.

The goal of this project is to analyze retail store sales data (`retail_store_sales.csv`) and demonstrate the differences, advantages, and structure of both programming paradigms when applied to common data manipulation tasks.

---

##  Getting Started

To run or contribute to this project, you will need to clone the repository and install the necessary dependencies (e.g., Python, Pandas, etc.).

### Prerequisites

* Python (version 3.x recommended)
* Required libraries (install via pip):
    ```bash
    pip install pandas numpy
    ```

### Cloning the Repository

```bash
git clone [https://github.com/alaa-anx/Functional-data-processing.git](https://github.com/aliaa-anx/Functional-data-processing.git)
cd Functional-data-processing

The core logic of the project is separated into two top-level directories based on programming paradigm:

| **Directory** | **Description** | **Status** |
| :--- | :--- | :--- |
| **`functional_style/`** | Contains all code written in a **functional, immutable, and declarative** style. This includes data transformation functions and the primary pipeline notebook. | **Complete** |
| **`imperative_style/`** | Reserved for code written in an **imperative, state-changing, and sequential** style. | **Work in Progress** |
| `retail_store_sales.csv` | The raw dataset used for analysis. | N/A |

### Functional Component Details

| **File / Folder** | **Purpose** |
| :--- | :--- |
| `functional_style/pipeline.ipynb` | The main Jupyter Notebook demonstrating the execution of the entire data pipeline and analysis using functional composition. |
| `functional_style/transformation/` | Contains the core Python scripts (`.py` files) that define the atomic, pure functions used for data cleaning and feature engineering. |
| `functional_style/data_analysis.py` | Contains the final analysis or aggregation logic for the functional pipeline. |
| `functional_style/tests.py` | Unit tests to ensure the purity and correctness of the functional transformation scripts. |

---