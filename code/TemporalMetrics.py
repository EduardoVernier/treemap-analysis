import pandas as pd
import numpy as np
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


def q_1_minus_ratio(df):
    # Create a df with columns delta_vis and delta_data
    df['q_ratio'] = (1 - df['delta_vis']) / (1 - df['delta_data'])
    df['q_ratio'] = df['q_ratio'].fillna(1)
    return df[['q_ratio']]

def q_ratio(df):
    # Create a df with columns delta_vis and delta_data
    df['q_ratio'] = df['delta_data'] / df[['delta_data', 'delta_vis']].max(axis=1)
    df['q_ratio'] = df['q_ratio'].fillna(1)
    return df[['q_ratio']]


def q_weighted_ratio(df):
    # Create a df with columns delta_vis, delta_data, and relative_weight
    N = len(df)
    df['q_w_ratio'] = (1 - (N * df['weight'] * df['delta_vis'])) / (1 - df['delta_data'])
    return df[['q_w_ratio']]


def q_mod(df):
    df['q_mod'] = 1 - abs(df['delta_vis'] - df['delta_data'])
    return df[['q_mod']]


def q_weighted_mod(df):
    df['q_w_mod'] = df['weight'] * (1 - abs(df['delta_vis'] - df['delta_data']))
    return df[['q_w_mod']]


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

    df = pd.merge(df1, df2, how='outer', left_index=True, right_index=True)
    df.columns = ['x1', 'y1', 'w1', 'h1', 'x2', 'y2', 'w2', 'h2']
    df['delta_vis'] = df.apply(lambda r: corner_travel(*list(r)) / norm, axis=1)
    return df[['delta_vis']]


def delta_data_by_area(df1, df2):
    base_width = (df1['x'] + df1['w']).max()
    base_height = (df1['y'] + df1['h']).max()
    # Normalize by base area
    norm = base_height * base_width

    df = pd.merge(df1, df2, how='outer', left_index=True, right_index=True)
    df.columns = ['x1', 'y1', 'w1', 'h1', 'x2', 'y2', 'w2', 'h2']
    df['delta_data'] = df.apply(lambda r: area_change(*list(r)) / norm, axis=1)
    return df[['delta_data']]

# Given by the average of the two areas
def relative_weight(df1, df2):
    # Normalize by base area
    base_width1 = (df1['x'] + df1['w']).max()
    base_height1 = (df1['y'] + df1['h']).max()
    area1 = base_height1 * base_width1

    base_width2 = (df2['x'] + df2['w']).max()
    base_height2 = (df2['y'] + df2['h']).max()
    area2 = base_height2 * base_width2

    df = pd.merge(df1, df2, how='outer', left_index=True, right_index=True)
    df.columns = ['x1', 'y1', 'w1', 'h1', 'x2', 'y2', 'w2', 'h2']
    df['weight'] = df.apply(lambda r: relative_weight_mean(*list(r), area1, area2), axis=1)
    return df[['weight']]


# If the precision of rectangles is good enough, this shouldn't be necessary
def delta_data_by_tree(df1, df2):
    pass


def point_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def corner_travel(*args):
    x1, y1, w1, h1, x2, y2, w2, h2 = args
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
    x1, y1, w1, h1, x2, y2, w2, h2 = args
    if math.isnan(w1):
        return w2 * h2
    elif math.isnan(w2):
        return w1 * h1
    else:
        return abs(w1 * h1 - w2 * h2)


def relative_weight_mean(*args):
    x1, y1, w1, h1, x2, y2, w2, h2, area1, area2 = args
    if math.isnan(w1):
        return ((w2 * h2) / area2) / 2
    elif math.isnan(w2):
        return ((w1 * h1) / area1) / 2
    else:
        return ((w1 * h1) / area1 + (w2 * h2) / area2) / 2


#####################################################
# Relative Position Change Metric from 'Stable Treemaps via Local Moves' 2017
#  - Contains a list of the rectangles in the current and in the new iteration. Only those rectangles present in both are there
#    a object in the list should contain "x1","x2","y1","y2" values
def relative_position_change_wrapper(df1, df2):
    df = pd.merge(df1, df2, how='inner', left_index=True, right_index=True)  # Retain only rows in both sets
    df.columns = ['x1', 'y1', 'w1', 'h1', 'x2', 'y2', 'w2', 'h2']
    df['w1'] = df['x1'] + df['w1']
    df['h1'] = df['y1'] + df['h1']

    df['w2'] = df['x2'] + df['w2']
    df['h2'] = df['y2'] + df['h2']

    # Coords from 1st revision and coords from 2nd revision
    df.columns = ['x11', 'y11', 'x12', 'y12', 'x21', 'y21', 'x22', 'y22']

    df = get_relative_score(df)
    return df[['delta_vis']]


def get_relative_score(df):
    N = len(df)
    df['delta_vis'] = pd.Series(np.zeros(N), index=df.index)

    revision_stability = 0
    for i, r1 in df.iterrows():
        item_stability = 0
        for j, r2 in df.iterrows():
            if i != j:
                old_percentage = getRelativePositions(r1['x11'], r1['x12'], r1['y11'], r1['y12'],
                                                      r2['x11'], r2['x12'], r2['y11'], r2['y12'])
                new_percentage = getRelativePositions(r1['x21'], r1['x22'], r1['y21'], r1['y22'],
                                                      r2['x21'], r2['x22'], r2['y21'], r2['y22'])
                pair_stability = getQuadrantStability(old_percentage, new_percentage)
                item_stability += pair_stability
                revision_stability += pair_stability
        r1['delta_vis'] = item_stability / (N - 1)

    # revision_stability = revision_stability / (pow(N, 2) - N)
    return df


def getQuadrantStability(percentagesOld, percentagesNew):
    stability = 1
    for i in range(0, 8):
        oldPercentage = percentagesOld[i]
        newPercentage = percentagesNew[i]
        stability -= abs(oldPercentage - newPercentage) / 2
    return stability


# gets the relative positions per quadrant from r1 to r2
def getRelativePositions(x11, x12, y11, y12, x21, x22, y21, y22):
    E = 0
    NE = 0
    N = 0
    NW = 0
    W = 0
    SW = 0
    S = 0
    SE = 0

    if (x21 >= x12):
        # Strictly east
        if (y21 < y11):
            # at least partially in NE
            # get the percentage that r2 is in NE
            NE = (y11 - y21) / (y22 - y21)
            NE = min(1, NE)

        if (y22 > y12):
            # at least partiall in SE
            SE = (y22 - y12) / (y22 - y21)
            SE = min(1, SE)

            # remainder is in east
            E = 1 - NE - SE
    elif (x22 <= x11):
        # strictly west
        if (y21 < y11):
            # at least partially in NW
            # get the percentage that r2 is in NW
            NW = (y11 - y21) / (y22 - y21)
            NW = min(1, NW)

        if (y22 > y12):
            # at least partiall in SW
            SW = (y22 - y12) / (y22 - y21)
            SW = min(1, SW)

            # remainder is in west
            W = 1 - NW - SW
    elif (y22 <= y11):
        # strictly North
        if (x21 < x11):
            # at least partially in NW
            # get the percentage that r2 is in NW
            NW = (x11 - x21) / (x22 - x21)
            NW = min(1, NW)

        if (x22 > x12):
            # at least partiall in SW
            NE = (x22 - x12) / (x22 - x21)
            NE = min(1, NE)

            # remainder is in west
            N = 1 - NW - NE
    else:
        # strictly south
        if (x21 < x11):
            # at least partially in SW
            # get the percentage that r2 is in NW
            SW = (x11 - x21) / (x22 - x21)
            SW = min(1, SW)

        if (x22 > x12):
            # at least partiall in SE
            SE = (x22 - x12) / (x22 - x21)
            SE = min(1, SE)

            # remainder is in west
            S = 1 - SW - SE

    quadrant = []
    quadrant.append(E)
    quadrant.append(NE)
    quadrant.append(N)
    quadrant.append(NW)
    quadrant.append(W)
    quadrant.append(SW)
    quadrant.append(S)
    quadrant.append(SE)
    return quadrant

# test code
# array =  getRelativePositions(0,10,10,20,-10,0,0,30)

# print (array)

