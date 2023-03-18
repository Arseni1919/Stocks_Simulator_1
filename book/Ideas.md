# 

## Spikes in assets' volume

In ETFs the spikes in volume happens after the information arrived.
In stocks - spikes volume are good - it can be informative.

## Spike in price

Always brings some information.

# Cleaning the data

## On prices

- percentage change on OLHC (first price (adj price) each day - 1, then percentage change) 
- instead of close take adjusted

```
new_percentage_return = current_price / first_price - 1  # may be negative
new_percentage_return = current_price / first_price  # always positive
```

## On Volume

- moving median 3 (to remove one-time spikes)
- moving median 5 (to remove spikes)
- dollar-volume - how much money went through the market

# Indicators

- slope day start (tngns alpha) alpha is more than -.05 -> then day is positive 
- slope x minutes
- RSI
- MACD - sucks - depends too much on the price
- close price relative to high-low line inside candle (for example 60%)
- volume is high (2 std on last 30 minutes above median on last 5 minutes)
- sharp ratio - how much return (profit) divided by std $(x_{t-1} - x{t})^2$
```
indecator = (close) / (high - low)
```

(boolean indicator) - if several minutes this indicator is low (less than 20%) - then the market is falling
