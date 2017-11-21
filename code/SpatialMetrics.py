import pandas as pd
import Parser


def aggregated_ar(technique_id, dataset_id):
    history = Parser.parse_rectangles(technique_id, dataset_id)
    df_mean = pd.DataFrame()
    for i, df in enumerate(history):
        df_ar = q_ar(df)
        df_ar = pd.merge(df_ar, q_weighted_ar(df))
        df_ar = pd.merge(df_ar, q_diag(df))
        df_ar = pd.merge(df_ar, q_weighted_diag(df))
        # Average the 4 metrics
        column = 't' + str(i)
        df_ar[column] = df_ar.mean(axis=1)
        df_mean = pd.concat([df_mean, df_ar[column]], axis=1, ignore_index=True)
    # Return a dataframe where each column is a revision and each row a cell
    return df_mean.T


def q_ar(df):
    df['q_ar'] = df[['w', 'h']].min(axis=1) / df[['w', 'h']].max(axis=1)
    return df[['id', 'q_ar']]


def q_weighted_ar(df):
    total_area = (df['x'] + df['w']).max() * (df['y'] + df['h']).max()

    df['q_w_ar'] = (df[['w', 'h']].min(axis=1) / df[['w', 'h']].max(axis=1)) * ((df['w'] * df['h']) / total_area)
    return df[['id', 'q_w_ar']]


def q_diag(df):
    # Find out max(width, height) of the base rectangle -- should be 1000
    max_dim = max((df['x'] + df['w']).max(), (df['y'] + df['h']).max())

    df['q_diag'] = 1 - abs(df['w'] - df['h']) / max_dim
    return df[['id', 'q_diag']]


def q_weighted_diag(df):
    # Find out max(width, height) of the base rectangle -- should be 1000
    max_dim = max((df['x'] + df['w']).max(), (df['y'] + df['h']).max())
    total_area = (df['x'] + df['w']).max() * (df['y'] + df['h']).max()

    df['q_w_diag'] = (1 - abs(df['w'] - df['h']) / max_dim) * ((df['w'] * df['h']) / total_area)
    return df[['id', 'q_w_diag']]
