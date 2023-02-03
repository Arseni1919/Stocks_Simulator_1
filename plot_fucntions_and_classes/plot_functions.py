from globals import *


def set_xlims(ax, min_steps, max_steps):
    ax.set_xlim([min_steps, max_steps])


def plot_asset_and_actions(ax, info):
    ax.cla()
    step_count = info['step_count']
    history_asset = info['history_assets']
    history_actions = info['history_actions']
    max_steps = info['max_steps']
    main_asset = info['main_asset']

    ax.plot(history_asset[main_asset][:step_count], c='lightblue')
    buy_steps = np.where(history_actions[:step_count] == 1)
    ax.scatter(buy_steps, history_asset[main_asset][buy_steps], c='green', marker='^', label='long order')
    sell_steps = np.where(history_actions[:step_count] == -1)
    ax.scatter(sell_steps, history_asset[main_asset][sell_steps], c='red', marker='v', label='short order')

    if 'w1' in info:
        ts = pd.Series(history_asset[main_asset][0:step_count])
        data = ts.rolling(window=info['w1']).mean().to_numpy()
        ax.plot(data, label=f"w: {info['w1']}")

        ts = pd.Series(history_asset[main_asset][0:step_count])
        data = ts.rolling(window=info['w2']).mean().to_numpy()
        ax.plot(data, label=f"w: {info['w2']}")

    ax.legend()
    set_xlims(ax, 0, max_steps)

    if info is not None:
        episode = info['episode']
        step = info['step']
        ax.set_title(f"{episode=} | {step=}")


def plot_volume(ax, info):
    ax.cla()
    step_count = info['step_count']
    history_volume = info['history_volume']
    max_steps = info['max_steps']
    main_asset = info['main_asset']

    step_count = step_count if step_count >= 0 else max_steps - 1
    ax.bar(np.arange(step_count), history_volume[main_asset][:step_count], alpha=0.2)
    ax.set_ylim(0, 50)


def plot_rewards(ax, info):
    ax.cla()
    step_count = info['step_count']
    max_steps = info['max_steps']
    history_cash = info['history_cash']
    history_holdings_worth = info['history_holdings_worth']
    history_portfolio_worth = info['history_portfolio_worth']
    history_actions = info['history_actions']

    h_cash = history_cash[:step_count]
    h_hold_w = history_holdings_worth[:step_count]
    h_port_w = history_portfolio_worth[:step_count]
    ax.plot(h_cash, alpha=0.7, label='cash')
    ax.plot(h_hold_w, alpha=0.7, label='holdings_worth')
    color = 'lightgreen' if h_port_w[-1] > 100 else 'orange'
    ax.plot(h_port_w, c=color, alpha=1, label='portfolio_worth')
    buy_steps = np.where(history_actions[:step_count] == 1)
    ax.scatter(buy_steps, h_port_w[buy_steps], c='green', marker='^', label='long order')
    sell_steps = np.where(history_actions[:step_count] == -1)
    ax.scatter(sell_steps, h_port_w[sell_steps], c='red', marker='v', label='short order')
    # ax.plot(np.cumsum(h_rewards_fee), '--', c='gray', alpha=0.7, label='with fees')
    set_xlims(ax, 0, max_steps)
    ax.legend()
    ax.set_title('Cumulative Rewards')


def plot_commissions(ax, info):
    ax.cla()
    step_count = info['step_count']
    max_steps = info['max_steps']
    history_commission_value = info['history_commission_value']
    h_commission_value = np.cumsum(history_commission_value[:step_count])
    ax.plot(h_commission_value[:step_count])
    # ax.plot(history_commission_value[:step_count])
    step_count = step_count if step_count >= 0 else max_steps - 1
    ax.bar(np.arange(step_count), history_commission_value[:step_count], alpha=1)
    set_xlims(ax, 0, max_steps)
    ax.set_title('Commisions')


def plot_orders(ax, info):
    ax.cla()
    step_count = info['step_count']
    max_steps = info['max_steps']
    history_orders = info['history_orders']
    # h_commission_value = np.cumsum(history_orders[:step_count])
    # ax.plot(h_commission_value[:step_count])
    ax.plot(history_orders[:step_count])
    # step_count = step_count if step_count >= 0 else max_steps - 1
    # ax.bar(np.arange(step_count), history_orders[:step_count], alpha=1)
    set_xlims(ax, 0, max_steps)
    ax.set_title('Orders')


def plot_property(ax, info):
    ax.cla()
    step_count = info['step_count']
    max_steps = info['max_steps']
    history_holdings = info['history_holdings']

    step_count = step_count if step_count >= 0 else max_steps - 1
    ax.plot(history_holdings[:step_count], c='brown', alpha=0.7)
    ax.fill_between(np.arange(step_count), np.zeros(step_count), history_holdings[:step_count],
                    color='coral', alpha=0.5)
    # ax.set_yticks([-1, 0, 1])
    # ax.set_yticklabels(['Short', 'Hold', 'Long'])
    set_xlims(ax, 0, max_steps)
    ax.set_title('In Hand')


def plot_variance(ax, info):
    ax.cla()
    step_count = info['step_count']
    max_steps = info['max_steps']
    history_asset = info['history_assets']

    ts = pd.Series(history_asset[1:step_count] - history_asset[0:step_count-1])
    for window in [10, 40, 70, 100]:
        data = ts.rolling(window=window).std().to_numpy()
        ax.plot(data, label=f'w:{window}')
    set_xlims(ax, 0, max_steps)
    ax.legend()
    ax.set_title('Asset Residuals')


def plot_average(ax, info):
    ax.cla()
    step_count = info['step_count']
    max_steps = info['max_steps']
    history_asset = info['history_assets']
    main_asset = info['main_asset']

    ts = pd.Series(history_asset[main_asset][0:step_count])
    for window in [10, 40, 70, 100]:
        data = ts.rolling(window=window).mean().to_numpy()
        ax.plot(data, label=f'w:{window}')
    set_xlims(ax, 0, max_steps)
    ax.legend()
    ax.set_title('Asset Average')
