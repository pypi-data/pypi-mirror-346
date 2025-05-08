# longer-limbs
Wrapper for SciKit-learn tree-based estimators providing linear regression fallback for inputs outside of training data range.

## Instructions

Install longer-limbs with:

```bash
pip install longer-limbs
```

Longer-limbs wraps SciKit-learn's `GradientBoostingRegressor()`. It offers identical `.fit()` and `.predict()` methods. To adapt code which currently uses pure SciKit-learn, change the import of `GradientBoostingRegressor()` from:

```python
from sklearn.ensemble import GradientBoostingRegressor
```

to:

```python
from longer_limbs.regressors import GradientBoostingRegressor
```

## Usage

See the [example regression notebook](https://github.com/gperdrizet/longer-limbs/blob/main/examples/regression.ipynb) for usage demonstration and comparison to SciKit-learn.