"""
Tests for data transformation functionality.
"""
import pytest
import pandas as pd
from src.transformer import DataTransformer

@pytest.fixture
def sample_data():
    """Create sample test data"""
    dates = pd.date_range(start='2020-01-01', periods=365)
    
    mh_precip = pd.DataFrame({
        'date': dates,
        'rainfall_mm': [10.5] * 365
    })
    
    mh_temp = pd.DataFrame({
        'date': dates,
        'mean': [25.0] * 365
    })
    
    return {
        'mh_precip': mh_precip,
        'mh_temp': mh_temp
    }

def test_monthly_aggregates(sample_data):
    """Test monthly aggregation"""
    transformer = DataTransformer()
    result = transformer._calculate_monthly_aggregates(sample_data)
    
    assert 'mh_precip_monthly' in result
    assert 'mh_temp_monthly' in result
    assert len(result['mh_precip_monthly']) == 12  # 12 months

def test_seasonal_aggregates(sample_data):
    """Test seasonal aggregation"""
    transformer = DataTransformer()
    result = transformer._calculate_seasonal_aggregates(sample_data)
    
    assert 'mh_precip_kharif' in result
    assert 'mh_precip_rabi' in result
    assert isinstance(result['mh_precip_kharif'], pd.Series)
