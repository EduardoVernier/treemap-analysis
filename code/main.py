import Parser
import SpatialMetrics
import TemporalMetrics

# df = Parser.parse_dataset('exo')
sqr_exo = Parser.parse_rectangles('sqr', 'exo')
# SpatialMetrics.q_diag(sqr_exo[0])
TemporalMetrics.delta_vis(sqr_exo[0], sqr_exo[1])