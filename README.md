SIRA (Smart Incident Report Analyzer)

About the Application:
SIRA is a modular Python data engineering tool built to process, clean, and standardize raw incident report logs using a structured architecture (src/data_loader.py and src/preprocessing.py).

Data Quality Issues Discovered:
Duplicates: Redundant rows artificially inflating the dataset.

Missing Data: Empty cells (NaN) hidden within text and categorical fields.

Inconsistent Casing: Mismatched capitalization creating fragmented, redundant categories.

Bad Formatting: Dates stored as generic text strings instead of proper temporal objects.

How They Were Identified:
Anomalies were flagged interactively in eda_investigation.ipynb using core Pandas operations: .shape for dimensions, .isnull().sum() for missing values, .duplicated() for repeats, and .unique() for categorical text checks.

Steps Taken to Clean the Data:
Deduplication: Dropped duplicate entries, safely trimming the dataset from 1,000 down to 957 unique rows.

Normalizing Casing - Converted text features to lowercase to unify overlapping categories.

Handling NaNs - Assigned explicit placeholders (like "Unknown") to protect rows from total deletion.

Type Casting - Converted string-based date columns into structured datetimes.

Why These Approaches Were Chosen:
Reproducibility - A modular pipeline ensures new incoming logs are cleaned identically.

Efficiency - Vectorized Pandas commands maximize execution speed over manual loops.

Data Integrity - Strategic imputation preserves neighboring data signals instead of blindly wiping out incomplete rows.