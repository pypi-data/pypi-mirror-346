# OutDatedLabs - Secure Machine Learning Training Package

A Python package for secure machine learning model training using the ML training server.

## Installation

```bash
pip install outdatedLabs
```

## Quick Start

```python
from outdatedLabs import SecureModel

# Create a linear regression model
model = SecureModel.linearRegression()

# Optionally set a custom server URL
model.set_server_url("http://your-server:8000")

# Train the model
model.fit(
    dataset_hash="your_dataset_hash",
    features=["feature1", "feature2"],
    target="target_column"
)

# Make predictions
predictions = model.predict(X)

# Get training metrics
metrics = model.get_metrics()
print(metrics)
```

## Features

- Secure model training using encrypted datasets
- Support for linear regression models
- Progress tracking with tqdm
- Comprehensive error handling and logging
- Easy-to-use interface
- Configurable server URL

## API Reference

### SecureModel

The main class for secure model training.

#### Methods

- `linearRegression(server_url: str = "http://localhost:8000") -> SecureModel`
  - Create a new linear regression model instance
  
- `set_server_url(server_url: str) -> SecureModel`
  - Set a custom URL for the ML training server
  
- `fit(dataset_hash: str, features: List[str] = None, target: str = None, params: Dict[str, Any] = None) -> SecureModel`
  - Train the model using the specified dataset
  
- `predict(X: Union[pd.DataFrame, List[List[float]]]) -> List[float]`
  - Make predictions using the trained model
  
- `score(X: Union[pd.DataFrame, List[List[float]]], y: List[float]) -> Dict[str, float]`
  - Calculate model performance metrics
  
- `get_metrics() -> Dict[str, Any]`
  - Get training metrics

## Requirements

- Python 3.7+
- requests
- joblib
- pandas
- scikit-learn
- tqdm

## License

MIT License 