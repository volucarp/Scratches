import pandas as pd
from collections import deque

def compute_position_age(dollar_position: pd.Series, total_return: pd.Series) -> pd.Series:
    """
    Compute the weighted average age of a stock position using FIFO methodology.
    
    Args:
        dollar_position: Series of dollar values indexed by datetime
        total_return: Series of total returns (adjusted for splits/dividends)
    
    Returns:
        Series of position ages in days
    """
    # Precompute cumulative return factors
    cum_ret = pd.Series(1.0, index=dollar_position.index)
    for i in range(1, len(dollar_position)):
        cum_ret.iloc[i] = cum_ret.iloc[i-1] * (1 + total_return.iloc[i])
    
    # Initialize storage for active lots
    long_lots = deque()  # (date, original_dollar_amount)
    short_lots = deque()  # (date, original_dollar_amount)
    
    # Initialize result series
    age_series = pd.Series(0.0, index=dollar_position.index)
    
    # Process each day
    for i, date in enumerate(dollar_position.index):
        # First day: entire position is cash flow
        if i == 0:
            cf = dollar_position.iloc[0]
            if cf > 0:
                long_lots.append((date, cf))
            elif cf < 0:
                short_lots.append((date, -cf))
        # Subsequent days
        else:
            prev_dollar = dollar_position.iloc[i-1]
            ret = total_return.iloc[i]
            expected = prev_dollar * (1 + ret)
            cf = dollar_position.iloc[i] - expected
            
            # Process cash flow
            if cf > 0:  # Inflow (buy/long or cover/short)
                remaining = cf
                # Cover short positions first (FIFO)
                while remaining > 0 and short_lots:
                    d, A0 = short_lots[0]
                    F = cum_ret.loc[date] / cum_ret.loc[d]
                    current_value = A0 * F
                    
                    if current_value <= remaining:
                        remaining -= current_value
                        short_lots.popleft()
                    else:
                        A0_reduced = A0 - remaining / F
                        short_lots[0] = (d, A0_reduced)
                        remaining = 0
                # Add remaining as long position
                if remaining > 0:
                    long_lots.append((date, remaining))
                    
            elif cf < 0:  # Outflow (sell/long or new short)
                remaining = -cf
                # Reduce long positions first (FIFO)
                while remaining > 0 and long_lots:
                    d, A0 = long_lots[0]
                    F = cum_ret.loc[date] / cum_ret.loc[d]
                    current_value = A0 * F
                    
                    if current_value <= remaining:
                        remaining -= current_value
                        long_lots.popleft()
                    else:
                        A0_reduced = A0 - remaining / F
                        long_lots[0] = (d, A0_reduced)
                        remaining = 0
                # Add remaining as short position
                if remaining > 0:
                    short_lots.append((date, remaining))
        
        # Calculate weighted average age
        total_abs_value = 0.0
        weighted_age_sum = 0.0
        
        # Process long positions
        for d, A0 in long_lots:
            F = cum_ret.loc[date] / cum_ret.loc[d]
            current_value = A0 * F
            age_days = (date - d).days
            total_abs_value += current_value
            weighted_age_sum += current_value * age_days
        
        # Process short positions
        for d, A0 in short_lots:
            F = cum_ret.loc[date] / cum_ret.loc[d]
            current_value = A0 * F
            age_days = (date - d).days
            total_abs_value += current_value
            weighted_age_sum += current_value * age_days
        
        # Compute final age
        if total_abs_value > 0:
            age_series.loc[date] = weighted_age_sum / total_abs_value
    
    return age_series


## Run test Cases
if __name__ == "__main__":
    import pandas as pd
    import numpy as np

    # Sample data
    dates = pd.date_range(start="2023-01-01", periods=3)
    dollar_position = pd.Series([1000, 1100, 1200], index=dates)
    total_return = pd.Series([0.0, 0.1, 0.05], index=dates)

    # Compute position age
    age_series = compute_position_age(dollar_position, total_return)
    print(age_series)
