import pandas as pd
import pickle
from typing import List
from sklearn.feature_extraction import DictVectorizer
from scripts.config import CATEGORICAL_COLS, NUMERICAL_COLS, TEXT_COLS

def load_pickle(path):
    with open(path, 'rb') as f:
        file = pickle.load(f)
    return file

def save_pickle(path: str, file):
    with open(path, "wb") as f:
        pickle.dump(file, f)

def clean_data(df):
    # Clean data
    df['Price']=df['Price'].str.replace(r'\s+', '', regex=True).astype(int)
    df['Co2_emission'] = pd.to_numeric(df['Co2_emission'], errors='coerce')
    df['Fuel_consumption'] = pd.to_numeric(df['Fuel_consumption'], errors='coerce')
    df['Gearbox'] = df['Gearbox'].str.replace(r'Auto.*', 'Automatique')

    df=df.dropna()
    # Remove outliers
    to_drop = df.loc[(df['Gearbox'] == 'Automatique') & (df['Price'] >= 46499)]
    df.drop(to_drop.index, inplace=True)
    to_drop = df.loc[(df['Gearbox'] == 'Manuelle') & (df['Price'] >= 27499)]
    df.drop(to_drop.index, inplace=True)
    return df

def encode_cols(df, categorical_cols=None, numerical_cols=None):
    if categorical_cols is None:
        categorical_cols = CATEGORICAL_COLS
    if numerical_cols is None:
        numerical_cols = NUMERICAL_COLS

    # df[numerical_cols] = df[numerical_cols].fillna(-1).astype("float")
    df[categorical_cols] = df[categorical_cols].apply(lambda x: x.astype(str).str.lower())
    return df

def extract_x_y(
    df: pd.DataFrame,
    categorical_cols: List[str] = None,
    numerical_cols: List[str] = None,
    dv: DictVectorizer = None,
    with_target: bool = True,
) -> dict:
    if categorical_cols is None:
        categorical_cols = CATEGORICAL_COLS
    if numerical_cols is None:
        numerical_cols = NUMERICAL_COLS
    dicts = df[[*categorical_cols, *numerical_cols]].to_dict(orient="records")

    y = None
    if with_target:
        if dv is None:
            dv = DictVectorizer()
            dv.fit(dicts)
        y = df["Price"].values

    x = dv.transform(dicts)
    return x, y, dv

def run_encode_task(df, dv: DictVectorizer = None):
    df = encode_cols(df)
    x, y, dv = extract_x_y(df, CATEGORICAL_COLS, NUMERICAL_COLS, dv)
    return x, y, dv