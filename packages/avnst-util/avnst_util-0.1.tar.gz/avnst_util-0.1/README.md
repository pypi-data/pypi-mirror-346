# Avnst Util

A Python utility package for clinical trial data analysis

## Features

- **Time Alignment**: Tools for aligning and comparing clinical trial event timings
- **TEAE Flag Derivation**: Utilities for determining Treatment Emergent Adverse Events
- **Data Validation**: Functions for checking missing or unknown values in clinical data

## Installation

```bash
pip install avnst_util
```

## Usage

### Time Alignment

```python
from avnst_util.time_alignment import align_time

# Align time for an event
start_time, end_time = align_time(
    date="2023-01-01",
    time="14:30",
    event_name="First Dose"
)
```

### TEAE Flag Derivation

```python
from avnst_util.teae_flag_deriver import derive_teae_flag

# Determine if an AE occurred after first dose
teae_flag = derive_teae_flag(
    first_dose_date="2023-01-01",
    first_dose_time="14:30",
    ae_start_date="2023-01-02",
    ae_start_time="09:00",
    opID="SUBJ001"
)
```

The TEAE flag returns:

- `1`: AE definitely occurred after first dose
- `0`: AE definitely occurred before first dose
- `2`: AE timing overlaps with first dose timing or timing uncertain
- `None`: Unable to determine timing

## Requirements

- Python >= 3.6
- pandas >= 1.0.0

## Development

To set up the development environment:

1. Clone the repository
2. Install development dependencies:

```bash
pip install -e .
```

## Contact

- Author: Eric Liu
- Email: txender4@gmail.com
