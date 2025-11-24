# Market Impact & Optimal Execution Lab

## Overview

This repository contains a production-ready research lab for **Market Impact Analysis** and **Optimal Execution Simulation**. It provides tools to ingest or generate Limit Order Book (LOB) data, calculate microstructure features, estimate market impact models, and simulate execution strategies (TWAP, VWAP, POV, Almgren-Chriss) in an event-driven environment.

## Features

- **Data Ingestion**: Support for synthetic LOB generation and standard LOB data loading.
- **Feature Engineering**: Microstructure features (OFI, spreads, depth), volatility, and liquidity metrics.
- **Impact Modeling**: Parametric (Almgren-Chriss) and ML-based short-term price prediction.
- **Execution Simulation**: High-fidelity event-driven replay engine for realistic backtesting.
- **Strategies**: Built-in implementations of TWAP, VWAP, POV, and Optimal Execution.
- **Evaluation**: Comprehensive slippage attribution and performance reporting.

## Installation

1. Clone the repository.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Generate Data

```python
from src.data.synthetic import generate_synthetic_lob
df = generate_synthetic_lob(n_events=10000)
```

### 2. Run Simulation

See `notebooks/03_Execution_Simulation.ipynb` for a full example.

## Project Structure

- `src/`: Core source code.
- `notebooks/`: Jupyter notebooks for demonstration.
- `tests/`: Unit tests.
- `config/`: Configuration files.

## License

MIT
# MarketImpactLab
