"""
Tests for data loading functionality.
"""
import pytest
from pathlib import Path
import pandas as pd
from src.data_loader import DataLoader

@pytest.fixture
def test_data_path():
    return Path("tests/test_data")

@pytest.fixture
def sample_data(test_data_path):
    """Create sample test data"""
    data = pd.DataFrame({
        'date': pd.date_range(start='2020-01-01', periods=100),
        'rainfall_mm': [10.5] * 100
    })
    test_data_path.mkdir(parents=True, exist_ok=True)
    data.to_csv(test_data_path / "MH_precipitation.csv", index=False)
    return data

def test_load_csv(test_data_path, sample_data):
    """Test CSV loading functionality"""
    loader = DataLoader(test_data_path)
    df = loader._load_csv("MH_precipitation.csv")
    
    assert isinstance(df, pd.DataFrame)
    assert 'date' in df.columns
    assert 'rainfall_mm' in df.columns
    assert pd.api.types.is_datetime64_any_dtype(df['date'])
    assert len(df) == len(sample_data)
