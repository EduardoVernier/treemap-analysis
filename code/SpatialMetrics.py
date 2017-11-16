import pandas as pd

def q_ar(df):
    ar = df[['id']].copy()
    ar['q_ar'] = df[['w', 'h']].min(axis=1) / df[['w', 'h']].max(axis=1)
    return ar

def q_diag(df):
    # Find out max(width, height) of the base rectangle -- should be 1000
    max_dim = max((df['x'] + df['w']).max(), (df['y'] + df['h']).max())

    diag = df[['id']].copy()
    diag['q_diag'] = 1 - abs(df['w'] - df['h']) / max_dim
    return diag
