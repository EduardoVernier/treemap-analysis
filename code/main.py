import Parser
import SpatialMetrics
import TemporalMetrics
import pandas as pd



#df = Parser.parse_dataset('exo')

#SpatialMetrics.aggregated_ar('git', 'exo')

#history = Parser.parse_rectangles('sqr', 'exo')
#TemporalMetrics.q_weighted_ratio(history[0], history[1])

# import timeit
# start_time = timeit.default_timer()
# # f
# elapsed = timeit.default_timer() - start_time
# print(elapsed)

TemporalMetrics.aggregated_stab('sqr', 'exo')
