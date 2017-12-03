import Parser
import SpatialMetrics
import TemporalMetrics
import pandas as pd
import matplotlib.pyplot as plt


#df = Parser.parse_dataset('exo')

#SpatialMetrics.aggregated_ar('git', 'exo')

# history = Parser.parse_rectangles('app', 'exo')
# print(TemporalMetrics.relative_position_change_wrapper(history[0], history[1]))

# import timeit
# start_time = timeit.default_timer()
# TemporalMetrics.aggregated_stab('sqr', 'exo')
# elapsed = timeit.default_timer() - start_time
# print(elapsed)

technique_list = Parser.list_techniques()
nrow = 7
ncol = 2
fig, axs = plt.subplots(nrow, ncol, sharex=True, sharey=True)
fig.delaxes(axs[6, 1])
fig.tight_layout()
for i, ax in enumerate(fig.axes):
    ax.set_title(technique_list[i].upper())

    data = []
    history = Parser.parse_rectangles('sqr', 'exo')
    for i in range(1, len(history)):
        df = TemporalMetrics.delta_vis(history[i - 1], history[i])
        df = pd.merge(df, TemporalMetrics.delta_data_by_area(history[i - 1], history[i]), left_index=True, right_index=True)
        df = pd.merge(df, TemporalMetrics.relative_weight(history[i - 1], history[i]), left_index=True, right_index=True)

        df_stab = TemporalMetrics.q_ratio(df)
        df_stab = pd.merge(df_stab, TemporalMetrics.q_weighted_ratio(df), left_index=True, right_index=True)

        column = 't' + str(i)
        data.append(df_stab.mean(axis=1))