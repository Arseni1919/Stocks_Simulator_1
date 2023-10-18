from globals import *


def main():
    st.set_page_config(page_title='Main', initial_sidebar_state="auto",
                       menu_items=None)

    st.markdown("""
    # Assets

    ## Stocks and ETF on Stocks

    - VIXY - SP500 volatility index.
    There are options inside(spy is down hard -> vixy is up).
    Volume is interesting and comparison with SPY.

    - SPY - SP500

    - IVV - SP500 (same holdings as SPY - for volume)

    - VOO - SP500 (same holdings as SPY - for volume)

    - AAPL (stock)
    - MSFT (stock)
    - GOOG (stock)
    - GOOGL (stock)
    - AMZN (stock)
    - FB (stock)
    - NFLX (stock)
    - TSLA (stock)

    - QQQ - (Nasdaq100 - this is an index) - this is a very big ETF
    It has a very high correlation with SP500

    - DIA - Dow Jones index.
    Counts as more stable/conservative. 
    High correlation with SPY.
    They require revenue and stability.

    ## ETF on Corporate Bonds

    On corp rate influence the following things: fed rate, stock price and duration.
    Corp bonds are dangerous but not as stocks.
    (If company dies - first to receive the money are the bond holders.)

    - VCSH - Corp bonds 1-3 years. It is huge. Follows the index perfectly. Very tradable.

    To cover all the range of durations:
    - IGSB - corporate Bond 1-5 years.
    - VCIT - Corp bonds 5-10 years (6 in average).

    - LQD - Corporate Bond 9(+-) years. Huge and long duration.

    Stock is influencing the bond besides the FED rate.
    More dangerous and profitable than Gov. Bond.
    If company's stock does not good the IGSB, LQD, VCIT and VCSH are dive.
    Stocks are bad for a long time <-> Bond is down.
    Fed rate grows -> Bond is going down.
    Fed rate declines -> Bond is going up.

    Spread: is the difference between the yield of corp bond and gov bond.
    Corp bond is 5% and gov bond is 4% -> the spread is 1%.
    You will demand a bigger spread for more dangerous companies.
    We look on the change of the spread.

    Fly to safety - a market condition when people sell risky assets (stocks and corp bond) and buy gov bonds.
    Crawl to Adventure - the opposite.

    ## ETF on Governmental (Treasury) Bonds

    - SHY - short-term gov bonds (1-3 years). Comparable to VCSH.
    If VCSH is going down very hard and SHY is stable -> there market is falling and will continue to fall.
    (IEI - gov bonds 1-3 years. 4 time smaller than LQD - we have no data.)

    - IEF - gov bonds 7-10 years. 2 time smaller than LQD. Comparable with LQD.

    - GOVT - all the gov bods 6(+-) years. Comparable with VCIT and LQD. 
    The biggest gov bonds there are in the market for now.
    The duration can change with the time. It is dependent on the decisions of US governments.

    - TLT - long gov bonds (20+ years). Huge. If something happens with *rate* - it will move drastically.

    # Commodities (Schora)

    - IAU - gold.
    - GLD - gold. 2 times bigger than IAU. Huge.

    # Vocabulary

    - raw data - data from API 
    - corrected data - to fill al the holes in data
    - scaled data - the day-based cumulative percentage change of assets for price. Volume is not changed.
    - normalized data - according to some standard
    - standardized data - according to standard normal distribution $N(0, 1)$
    - after-split data - to correct all the data according to the split
    - indicator - any transformation on raw data (parameterized)
    - boolean indicator - transformation on raw data that outputs a boolean value per time unit (parameterized)
    - strategy - outputs the decisions of buy/sell/hold.
    - full strategy - outputs the decisions of buy/sell/hold and in which proportions to execute the action.
    - backtester on one day - compares strategies on one day.
    - backtester on some timeframe - compares strategies on specified timeframe.



    """)


if __name__ == '__main__':
    main()
