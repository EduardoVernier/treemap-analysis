import Parser
import SpatialMetrics
import TemporalMetrics
import pandas as pd



#df = Parser.parse_dataset('exo')

#SpatialMetrics.aggregated_ar('git', 'exo')

history = Parser.parse_rectangles('sqr', 'exo')
TemporalMetrics.relative_position_change_wrapper(history[1], history[2])

# import timeit
# start_time = timeit.default_timer()
# TemporalMetrics.aggregated_stab('sqr', 'exo')
# elapsed = timeit.default_timer() - start_time
# print(elapsed)

