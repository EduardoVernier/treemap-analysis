import Parser
import SpatialMetrics

# df = Parser.parse_dataset('exo')
sqr_exo = Parser.parse_rectangles('sqr', 'exo')
SpatialMetrics.q_diag(sqr_exo[0])