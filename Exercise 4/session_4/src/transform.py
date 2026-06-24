import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from metadata import (
    COLUMNS_TO_DROP,
    MODE_IMPUTE_COLUMNS,
    MEDIAN_IMPUTE_COLUMNS,
    GENDER_MAPPING,
    BINARY_NUMERIC_COLUMNS,
    ONE_HOT_ENCODE_COLUMNS,
)


class Transformer:
    def __init__(self):
        self.drop_columns = COLUMNS_TO_DROP
        self.mode_impute_columns = MODE_IMPUTE_COLUMNS
        self.median_impute_columns = MEDIAN_IMPUTE_COLUMNS
        self.gender_mapping = GENDER_MAPPING
        self.binary_numeric_columns = BINARY_NUMERIC_COLUMNS
        self.one_hot_encoding_columns = ONE_HOT_ENCODE_COLUMNS

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.drop(columns=self.drop_columns)
        df = self._impute_mode_columns(df)
        df = self._impute_median_columns(df)
        df = self._map_gender_to_int(df)
        df = self._cast_binary_numeric_columns(df)
        df = self._one_hot_encoding(df)

        return df

    def _impute_mode_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in self.mode_impute_columns:
            if col in df.columns:
                df[col] = df[col].fillna(df[col].mode()[0])
        return df

    def _impute_median_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in self.median_impute_columns:
            if col in df.columns:
                df[col] = df[col].fillna(df[col].median())
        return df

    def _map_gender_to_int(self, df: pd.DataFrame) -> pd.DataFrame:
        df["Gender"] = df["Gender"].map(self.gender_mapping)
        return df

    def _cast_binary_numeric_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in self.binary_numeric_columns:
            if col in df.columns:
                df[col] = df[col].astype(int)
        return df

    def _one_hot_encoding(self, df: pd.DataFrame) -> pd.DataFrame:
        encoder = OneHotEncoder(drop="first", sparse_output=False).set_output(
            transform="pandas"
        )
        encoder.fit(df[self.one_hot_encoding_columns])
        encoded_df = encoder.transform(df[self.one_hot_encoding_columns])
        df = df.drop(columns=self.one_hot_encoding_columns)
        df = pd.concat([df.reset_index(drop=True), encoded_df.reset_index(drop=True)], axis=1)

        return df


def balance_dataset(df: pd.DataFrame, target_column: str) -> pd.DataFrame:
  
    df_majority = df[df[target_column] == 0].copy()
    df_minority = df[df[target_column] == 1].copy()


    min_size = len(df_minority)

   
    df_majority_balanced = df_majority.sample(n=min_size, random_state=42)

  
    df_balanced = pd.concat([df_majority_balanced, df_minority])

    
    df_balanced = df_balanced.sample(frac=1, random_state=42).reset_index(drop=True)

    return df_balanced
