import pandas as pd
import math


def q_ratio(df1, df2):
    # Create a df with columns delta_vis and delta_data
    df = delta_vis(df1, df2).copy()
    df = pd.merge(df, delta_data_by_area(df1, df2))
    df['q_ratio'] = (1 - df['delta_vis']) / (1 - df['delta_data'])
    return df


def q_mod(df1, df2):
    pass


def delta_vis(df1, df2):
    base_width = (df1['x'] + df1['w']).max()
    base_height = (df1['y'] + df1['h']).max()
    # Normalize by 4 * hypotenuse
    norm = 4 * math.sqrt(base_width ** 2 + base_height ** 2)

    df = pd.merge(df1, df2, on='id', how='outer')
    df.columns = ['id', 'x1', 'y1', 'w1', 'h1', 'x2', 'y2', 'w2', 'h2']
    dv = df[['id']].copy()
    dv['delta_vis'] = df.apply(lambda r: corner_travel(*list(r)) / norm, axis=1)
    return dv


def delta_data_by_area(df1, df2):
    base_width = (df1['x'] + df1['w']).max()
    base_height = (df1['y'] + df1['h']).max()
    # Normalize by base area
    norm = base_height * base_width

    df = pd.merge(df1, df2, on='id', how='outer')
    df.columns = ['id', 'x1', 'y1', 'w1', 'h1', 'x2', 'y2', 'w2', 'h2']
    dd = df[['id']].copy()
    dd['delta_data'] = df.apply(lambda r: area_change(*list(r)) / norm, axis=1)
    return dd


# If the precision of rectangles is good enough, this shouldn't be necessary
def delta_data_by_tree(df1, df2):
    pass


def point_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def corner_travel(*args):
    _, x1, y1, w1, h1, x2, y2, w2, h2 = args
    if math.isnan(w1):
        # 2 times the hypotenuse -- growth from center
        return 2 * math.sqrt(w2 ** 2 + h2 ** 2)
    elif math.isnan(w2):
        return 2 * math.sqrt(w1 ** 2 + h1 ** 2)
    else:
        return point_distance(x1, y1, x2, y2)   \
            + point_distance(x1 + w1, y1, x2 + w2, y2)   \
            + point_distance(x1, y1 + h1, x2, y2 + h2)   \
            + point_distance(x1 + w1, y1 + h1, x2 + w2, y2 + h2)


def area_change(*args):
    _, x1, y1, w1, h1, x2, y2, w2, h2 = args
    if math.isnan(w1):
        return w2 * h2
    elif math.isnan(w2):
        return w1 * h1
    else:
        return abs(w1 * h1 - w2 * h2)
