from globals import *


def set_xlims(ax, min_steps, max_steps):
    ax.set_xlim([min_steps, max_steps])


def subplot_actions(ax, info):
    step_count = info['step_count']
    history_asset = info['history_assets']
    history_actions = info['history_actions']
    main_asset = info['main_asset']
    main_actions = history_actions[main_asset][:step_count]
    l_buy, l_double_buy, l_sell, l_double_sell = [], [], [], []
    for i, pair_of_actions in enumerate(history_actions[main_asset][:step_count]):
        if pair_of_actions == [0, 1] or pair_of_actions == [1, 0]:
            l_buy.append(i)
        if pair_of_actions == [1, 1]:
            l_double_buy.append(i)
        if pair_of_actions == [-1, 0] or pair_of_actions == [0, -1]:
            l_sell.append(i)
        if pair_of_actions == [-1, -1]:
            l_double_sell.append(i)
    ax.scatter(l_buy, history_asset[main_asset][l_buy], c='green', marker='^', label='long order')
    ax.scatter(l_double_buy, history_asset[main_asset][l_double_buy], c='green', marker='*', label='switch to buy')
    ax.scatter(l_sell, history_asset[main_asset][l_sell], c='red', marker='v', label='short order')
    ax.scatter(l_double_sell, history_asset[main_asset][l_double_sell], c='red', marker='X', label='switch to sell')


def plot_asset_and_actions(ax, info):
    ax.cla()
    step_count = info['step_count']
    history_asset = info['history_assets']
    max_steps = info['max_steps']
    main_asset = info['main_asset']

    ax.plot(history_asset[main_asset][:step_count], c='lightblue')
    subplot_actions(ax, info)

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
    # ax.set_ylim(0, 50)


def plot_rewards(ax, info):
    ax.cla()
    step_count = info['step_count']
    max_steps = info['max_steps']
    history_cash = info['history_cash']
    history_portion_of_asset_worth = info['history_portion_of_asset_worth']
    history_portfolio_worth = info['history_portfolio_worth']
    history_actions = info['history_actions']
    main_asset = info['main_asset']

    h_cash = history_cash[:step_count]
    h_hold_w = history_portion_of_asset_worth[:step_count]
    h_port_w = history_portfolio_worth[:step_count]
    # ax.plot(h_cash, alpha=0.7, label='cash')
    # ax.plot(h_hold_w, alpha=0.7, label='holdings_worth')
    color = 'lightgreen' if h_port_w[-1] > 100 else 'brown'
    ax.plot(h_port_w, c=color, alpha=1, label='portfolio_worth')
    buy_steps = np.where(history_actions[main_asset][:step_count] == 1)
    ax.scatter(buy_steps, h_port_w[buy_steps], c='green', marker='^', label='long order')
    sell_steps = np.where(history_actions[main_asset][:step_count] == -1)
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

    # opt 1
    ax.plot(history_orders[:step_count])

    # opt 2
    h_commission_value = np.cumsum(history_orders[:step_count])
    ax.plot(h_commission_value[:step_count])
    # step_count = step_count if step_count >= 0 else max_steps - 1
    # ax.bar(np.arange(step_count), history_orders[:step_count], alpha=1)

    set_xlims(ax, 0, max_steps)
    ax.set_title('Orders')


def plot_property(ax, info):
    ax.cla()
    step_count = info['step_count']
    max_steps = info['max_steps']
    history_portion_of_asset = info['history_portion_of_asset']

    step_count = step_count if step_count >= 0 else max_steps - 1
    ax.plot(history_portion_of_asset[:step_count], c='brown', alpha=0.7)
    ax.fill_between(np.arange(step_count), np.zeros(step_count), history_portion_of_asset[:step_count],
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


def plot_algs_returns(ax, info):
    ax.cla()
    stats_dict = info['stats_dict']
    max_steps = info['max_steps']
    episode = info['episode']
    alg_index = info['alg_index']
    step = info['step']
    for alg_name, alg_stats_dict in stats_dict.items():
        returns_mean = alg_stats_dict['returns'][:episode+1, :].mean(axis=0)
        ax.plot(returns_mean, '--', alpha=0.7, label=f'{alg_name}')

        returns_std = alg_stats_dict['returns'][:episode+1, :].std(axis=0)
        # appendix = 'range:std'
        # ax.fill_between(np.arange(max_steps)[::10], returns_mean + returns_std, returns_mean - returns_std, alpha=0.2)
        std_every = 20
        ax.errorbar(np.arange(max_steps)[::std_every], returns_mean[::std_every], returns_std[::std_every],
                    linestyle='None', marker='.', alpha=0.2)

        returns_max = alg_stats_dict['returns'][:episode+1, :].max(axis=0)
        returns_min = alg_stats_dict['returns'][:episode+1, :].min(axis=0)
        appendix = 'range:min-max'
        ax.fill_between(range(max_steps), returns_max, returns_min, alpha=0.2)

        ax.legend()
        # ax.set_xlim([0, max_steps])
        ax.set_title(f'Portfolio Worth (ep: {episode + 1}, step: {step}, {appendix})')