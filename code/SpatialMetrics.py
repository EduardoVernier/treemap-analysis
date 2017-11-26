import pandas as pd
import Parser


def q_ar(df):
    df['q_ar'] = df[['w', 'h']].min(axis=1) / df[['w', 'h']].max(axis=1)
    return df[['id', 'q_ar']]


def q_weighted_ar(df):
    total_area = (df['x'] + df['w']).max() * (df['y'] + df['h']).max()

    df['q_w_ar'] = (df[['w', 'h']].min(axis=1) / df[['w', 'h']].max(axis=1)) * ((df['w'] * df['h']) / total_area)
    return df[['id', 'q_w_ar']]


# We won't be using these in the paper.
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
