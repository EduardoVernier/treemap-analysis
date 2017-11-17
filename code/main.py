import Parser
import SpatialMetrics
import TemporalMetrics
import pandas as pd

# df = Parser.parse_dataset('exo')
sqr_exo = Parser.parse_rectangles('sqr', 'exo')
# SpatialMetrics.q_diag(sqr_exo[0])
TemporalMetrics.q_ratio(sqr_exo[0], sqr_exo[1])
