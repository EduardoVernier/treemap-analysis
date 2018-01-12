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



history = Parser.parse_rectangles('ssv', 'exo')
i = 86
df = TemporalMetrics.delta_vis(history[i - 1], history[i])
df = pd.merge(df, TemporalMetrics.delta_data_by_area(history[i - 1], history[i]), left_index=True, right_index=True)
df = pd.merge(df, TemporalMetrics.relative_weight(history[i - 1], history[i]), left_index=True, right_index=True)

df_stab = TemporalMetrics.q_ratio(df)
df_stab = pd.merge(df_stab, TemporalMetrics.q_weighted_ratio(df), left_index=True, right_index=True)
df_stab
