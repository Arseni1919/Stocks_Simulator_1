

def mean(sample):
    return sum(sample) / len(sample)


def rsi_calc(close, time_period=6):
    # time_period looks back period to compute gains & losses
    gain_history = []  # history of gains over look back period (0 if no gain, magnitude of gain if gain)
    loss_history = []  # history of losses over look back period (0 if no loss, magnitude of loss if loss)
    avg_gain_values = []  # track avg gains for visualization purposes
    avg_loss_values = []  # track avg losses for visualization purposes
    rsi_values = []  # track computed RSI values
    last_price = 0  # current_price - last_price > 0 => gain. current_price - last_price < 0 => loss.

    for close_price in close:
        if last_price == 0:
            last_price = close_price

        gain_history.append(max(0, close_price - last_price))
        loss_history.append(max(0, last_price - close_price))
        last_price = close_price

        if len(gain_history) > time_period:  # maximum observations is equal to lookback period
            del (gain_history[0])
            del (loss_history[0])

        avg_gain = mean(gain_history)  # average gain over lookback period
        avg_loss = mean(loss_history)  # average loss over lookback period

        avg_gain_values.append(avg_gain)
        avg_loss_values.append(avg_loss)

        rs = 0
        if avg_loss > 0:  # to avoid division by 0, which is undefined
            rs = avg_gain / avg_loss
        elif avg_loss == 0 and avg_gain > 0:
            rs = 100
        else:
            rs = 50

        rsi = 100 - (100 / (1 + rs))
        rsi_values.append(rsi)
        # print(rsi_values)
    rsi_values[:time_period] = [50] * time_period
    return rsi_values


def macd_func(close, short=8, long=22):
    # Get the long EMA of the closing price
    k = close.ewm(span=short, adjust=False, min_periods=short).mean()

    # Get the short EMA of the closing price
    d = close.ewm(span=long, adjust=False, min_periods=long).mean()

    # Subtract the long EMA from the short EMA to get the MACD
    macd = k - d
    macd.fillna(0, inplace=True)

    return macd