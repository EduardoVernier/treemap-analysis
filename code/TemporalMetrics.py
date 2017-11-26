import pandas as pd
import math
from scipy import stats

import Parser


# def aggregated_stab(technique_id, dataset_id):
#     history = Parser.parse_rectangles(technique_id, dataset_id)
#     df_mean = pd.DataFrame()
#     pearson_list = []
#     weighted_pearson_list = []
#     for i in range(1, len(history)):
#         df = delta_vis(history[i - 1], history[i])
#         df = pd.merge(df, delta_data_by_area(history[i - 1], history[i]))
#         df = pd.merge(df, relative_weight(history[i - 1], history[i]))

#         df_stab = q_ratio(df)
#         df_stab = pd.merge(df_stab, q_weighted_ratio(df))
#         df_stab = pd.merge(df_stab, q_mod(df))
#         df_stab = pd.merge(df_stab, q_weighted_mod(df))

#         pearson_list.append(max(pearson(df)[0], 0))
#         weighted_pearson_list.append(max(weighted_pearson(df), 0))

#         column = 't' + str(i)
#         df_stab[column] = df_stab.mean(axis=1)
#         df_mean = pd.concat([df_mean, df_stab[column]], axis=1, ignore_index=True)
#     # Return a dataframe where each row is a revision and each column a cell,
#     # list of Pearson correlation coef., and weighted Pearson coefs.
#     return df_mean.T, pearson_list, weighted_pearson_list


def q_ratio(df):
    # Create a df with columns delta_vis and delta_data
    df['q_ratio'] = (1 - df['delta_vis']) / (1 - df['delta_data'])
    return df[['id', 'q_ratio']]


def q_weighted_ratio(df):
    # Create a df with columns delta_vis, delta_data, and relative_weight
    df['q_w_ratio'] = df['weight'] * (1 - df['delta_vis']) / (1 - df['delta_data'])
    return df[['id', 'q_w_ratio']]


def q_mod(df):
    df['q_mod'] = 1 - abs(df['delta_vis'] - df['delta_data'])
    return df[['id', 'q_mod']]


def q_weighted_mod(df):
    df['q_w_mod'] = df['weight'] * (1 - abs(df['delta_vis'] - df['delta_data']))
    return df[['id', 'q_w_mod']]


def pearson(df):
    return stats.pearsonr(df['delta_vis'], df['delta_data'])


# https://en.wikipedia.org/wiki/Pearson_correlation_coefficient#Weighted_correlation_coefficient
def weighted_pearson(df):
    x = df['delta_data'].values
    y = df['delta_vis'].values
    weights = df['weight'].values

    n_items = len(x)
    weight_sum = sum(weights)

    # Compute vector x and y weighted means
    x_weighted_mean = sum(weights[i] * x[i] for i in range(n_items)) / weight_sum
    y_weighted_mean = sum(weights[i] * x[i] for i in range(n_items)) / weight_sum

    # Compute weighted covariance
    xy_weighted_covariance = sum(weights[i] * (x[i] - x_weighted_mean) * (y[i] - y_weighted_mean) for i in range(n_items)) / weight_sum
    xx_weighted_covariance = sum(weights[i] * (x[i] - x_weighted_mean) * (x[i] - x_weighted_mean) for i in range(n_items)) / weight_sum
    yy_weighted_covariance = sum(weights[i] * (y[i] - y_weighted_mean) * (y[i] - y_weighted_mean) for i in range(n_items)) / weight_sum

    weighted_correlation = xy_weighted_covariance / math.sqrt(xx_weighted_covariance * yy_weighted_covariance)
    return weighted_correlation


def delta_vis(df1, df2):
    base_width = (df1['x'] + df1['w']).max()
    base_height = (df1['y'] + df1['h']).max()
    # Normalize by 4 * hypotenuse
    norm = 4 * math.sqrt(base_width ** 2 + base_height ** 2)

    df = pd.merge(df1, df2, on='id', how='outer')
    df.columns = ['id', 'x1', 'y1', 'w1', 'h1', 'x2', 'y2', 'w2', 'h2']
    df['delta_vis'] = df.apply(lambda r: corner_travel(*list(r)) / norm, axis=1)
    return df[['id', 'delta_vis']]


def delta_data_by_area(df1, df2):
    base_width = (df1['x'] + df1['w']).max()
    base_height = (df1['y'] + df1['h']).max()
    # Normalize by base area
    norm = base_height * base_width

    df = pd.merge(df1, df2, on='id', how='outer')
    df.columns = ['id', 'x1', 'y1', 'w1', 'h1', 'x2', 'y2', 'w2', 'h2']
    df['delta_data'] = df.apply(lambda r: area_change(*list(r)) / norm, axis=1)
    return df[['id', 'delta_data']]


# Given by the average of the two areas
def relative_weight(df1, df2):
    # Normalize by base area
    base_width1 = (df1['x'] + df1['w']).max()
    base_height1 = (df1['y'] + df1['h']).max()
    area1 = base_height1 * base_width1

    base_width2 = (df2['x'] + df2['w']).max()
    base_height2 = (df2['y'] + df2['h']).max()
    area2 = base_height2 * base_width2

    df = pd.merge(df1, df2, on='id', how='outer')
    df.columns = ['id', 'x1', 'y1', 'w1', 'h1', 'x2', 'y2', 'w2', 'h2']
    df['weight'] = df.apply(lambda r: relative_weight_mean(*list(r), area1, area2), axis=1)
    return df[['id', 'weight']]


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


def relative_weight_mean(*args):
    _, x1, y1, w1, h1, x2, y2, w2, h2, area1, area2 = args
    if math.isnan(w1):
        return ((w2 * h2) / area2) / 2
    elif math.isnan(w2):
        return ((w1 * h1) / area1) / 2
    else:
        return ((w1 * h1) / area1 + (w2 * h2) / area2) / 2
