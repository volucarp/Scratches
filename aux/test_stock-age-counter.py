import pytest
import pandas as pd
from datetime import datetime, timedelta
from .stock_age_counter import compute_position_age  # Import your function


# Helper function to create date range
def create_dates(days):
    return pd.date_range(start="2023-01-01", periods=days)


def test_zero_return_buy_sell():
    """
    Zero Daily Return - Simple Buy and Sell
    --------------------------------------
    Date        | Dollar_Position | Total_Return | Expected_Age
    2023-01-01  | 1000            | 0.0          | 0.0
    2023-01-02  | 500             | 0.0          | 1.0
    2023-01-03  | 0               | 0.0          | 0.0
    
    Day 1: New $1000 position (age=0)
    Day 2: Sell $500 → remaining $500 position (age=1)
    Day 3: Close position → age=0
    """
    dates = create_dates(3)
    position = pd.Series([1000, 500, 0], index=dates)
    returns = pd.Series([0, 0, 0], index=dates)
    
    age = compute_position_age(position, returns)
    assert age.iloc[0] == 0
    assert age.iloc[1] == 1.0
    assert age.iloc[2] == 0.0  # Position closed

def test_50pct_return_buy_hold():
    """
    50% Daily Return - Buy and Hold
    -------------------------------
    Date        | Dollar_Position | Total_Return | Expected_Age
    2023-01-01  | 1000            | 0.0          | 0.0
    2023-01-02  | 1500            | 0.5          | 1.0
    2023-01-03  | 2250            | 0.5          | 2.0
    
    Day 1: New $1000 position (age=0)
    Day 2: Grows to $1500 (age=1)
    Day 3: Grows to $2250 (age=2)
    """
    dates = create_dates(3)
    position = pd.Series([1000, 1500, 2250], index=dates)
    returns = pd.Series([0, 0.5, 0.5], index=dates)
    
    age = compute_position_age(position, returns)
    assert age.iloc[0] == 0
    assert age.iloc[1] == 1.0
    assert age.iloc[2] == 2.0

def test_long_to_short_transition():
    """
    Long to Short Transition (4 days)
    ---------------------------------
    Date        | Dollar_Position | Total_Return | Expected_Age
    2023-01-01  | 1000            | 0.0          | 0.0
    2023-01-02  | -1000           | 0.0          | 0.0
    2023-01-03  | -1500           | 0.5          | 1.0
    2023-01-04  | 0               | 0.0          | 0.0
    
    Day 1: $1000 long (age=0)
    Day 2: Sell $2000 → $1000 long closed, $1000 short opened (age=0)
    Day 3: Position grows to -$1500 (age=1)
    Day 4: Position closed (age=0)
    """
    dates = create_dates(4)
    position = pd.Series([1000, -1000, -1500, 0], index=dates)
    returns = pd.Series([0, 0, 0.5, 0], index=dates)
    
    age = compute_position_age(position, returns)
    assert age.iloc[0] == 0
    assert age.iloc[1] == 0.0
    assert age.iloc[2] == 1.0
    assert age.iloc[3] == 0.0  # Position closed

def test_short_to_long_transition():
    """
    Short to Long Transition (4 days)
    ---------------------------------
    Date        | Dollar_Position | Total_Return | Expected_Age
    2023-01-01  | -1000           | 0.0          | 0.0
    2023-01-02  | 1000            | 0.0          | 0.0
    2023-01-03  | 1500            | 0.5          | 1.0
    2023-01-04  | 0               | 0.0          | 0.0
    
    Day 1: $1000 short (age=0)
    Day 2: Buy $2000 → $1000 short covered, $1000 long opened (age=0)
    Day 3: Position grows to $1500 (age=1)
    Day 4: Position closed (age=0)
    """
    dates = create_dates(4)
    position = pd.Series([-1000, 1000, 1500, 0], index=dates)
    returns = pd.Series([0, 0, 0.5, 0], index=dates)
    
    age = compute_position_age(position, returns)
    assert age.iloc[0] == 0
    assert age.iloc[1] == 0.0
    assert age.iloc[2] == 1.0
    assert age.iloc[3] == 0.0  # Position closed

def test_fifo_aging_multiple_lots():
    """
    FIFO Aging with Multiple Lots
    ----------------------------
    Date        | Dollar_Position | Total_Return | Expected_Age
    2023-01-01  | 1000            | 0.0          | 0.0
    2023-01-02  | 2000            | 0.0          | 0.5
    2023-01-03  | 500             | 0.0          | 1.0
    2023-01-04  | 0               | 0.0          | 0.0
    
    Day 1: $1000 long (age=0)
    Day 2: Add $1000 → positions: $1000@day1 (age=1), $1000@day2 (age=0)
            Weighted age = (1000*1 + 1000*0)/2000 = 0.5
    Day 3: Sell $1500 → Remaining: $500@day2 (age=1)
    Day 4: Position closed (age=0)
    """
    dates = create_dates(4)
    position = pd.Series([1000, 2000, 500, 0], index=dates)
    returns = pd.Series([0, 0, 0, 0], index=dates)
    
    age = compute_position_age(position, returns)
    assert age.iloc[0] == 0
    assert age.iloc[1] == 0.5
    assert age.iloc[2] == 1.0
    assert age.iloc[3] == 0.0  # Position closed

def test_extreme_return_position_flip():
    """
    Extreme Return with Position Flip
    ---------------------------------
    Date        | Dollar_Position | Total_Return | Expected_Age
    2023-01-01  | 1000            | 0.0          | 0.0
    2023-01-02  | -2000           | 1.0          | 0.0
    2023-01-03  | 0               | 0.0          | 0.0
    
    Day 1: $1000 long (age=0)
    Day 2: 
      - Position grows 100% → $2000 long (age=1)
      - Sell $4000 → close $2000 long, open $2000 short (age=0)
    Day 3: Position closed (age=0)
    """
    dates = create_dates(3)
    position = pd.Series([1000, -2000, 0], index=dates)
    returns = pd.Series([0, 1.0, 0], index=dates)
    
    age = compute_position_age(position, returns)
    assert age.iloc[0] == 0
    assert age.iloc[1] == 0.0
    assert age.iloc[2] == 0.0  # Position closed