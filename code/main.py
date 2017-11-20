import Parser
import SpatialMetrics
import TemporalMetrics
import pandas as pd



#df = Parser.parse_dataset('exo')

#SpatialMetrics.aggregated_ar('git', 'exo')

#history = Parser.parse_rectangles('sqr', 'exo')
#TemporalMetrics.q_weighted_ratio(history[0], history[1])

TemporalMetrics.aggregated_stab('sqr', 'exo')