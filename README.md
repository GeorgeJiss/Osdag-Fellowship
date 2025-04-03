# Osdag-Fellowship

# Bolted Lap Joint Design

This repository contains Python modules for designing bolted lap joints and performing unit tests to validate the design.

## Objective

The primary goal of this repository is to develop a comprehensive and precise unit test for the bolted lap joint design module, as part of the Osdag Fellowship screening task. The test is designed to be both concise and robust, ensuring thorough validation of all specified prompts.


## Project Structure

```
├── bolted_lap_joint_design.py  # Main design module
├── test_unit.py                 # Unit test module using pytest
├── is800_2007.py                # Module implementing IS 800:2007 design methods
├── README.md                    # Documentation
```

## Features
- Implements IS 800:2007 code for bolted lap joint design.
- Computes the required number of bolts based on input parameters.
- Ensures minimum two-bolt requirement for various loads and plate thicknesses.
- Unit tests using `pytest` to validate the design rules.

## Installation
Ensure you have Python installed along with required dependencies:
```sh
pip install pytest
```

## Usage
Run the design module with sample inputs:
```sh
python bolted_lap_joint_design.py
```

Run the unit tests:
```sh
pytest test_unit.py
```


### Unit Test Output
To verify the correctness of the design:
```sh
pytest -v test_unit.py
```


## Report

Link for the overleaf latex report of the whole screening task:

```sh
https://www.overleaf.com/read/rvhnnqnsfkfr#d6621b
```
