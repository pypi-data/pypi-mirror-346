# NUTMEG-Cython

A Cython-optimized implementation of the NUTMEG algorithm for crowdsourced data analysis.

## Installation

You can install the package using pip:

```bash
pip install nutmeg-cython
```

## Usage

```python
from nutmeg import NUTMEG

# Initialize the model
model = NUTMEG(n_restarts=10, n_iter=50)

# Fit the model to your data
# data should be a pandas DataFrame with columns: 'worker', 'task', 'label', 'subpopulation'
model.fit(data)

# Get predictions
predictions = model.labels_
```

## Development

To build the package locally:

```bash
python setup.py build_ext --inplace
```

## License

MIT License 