from src.transform import Transformer, balance_dataset
import pandas as pd


def test_map_gender_to_int():
    transformer = Transformer()
    df = pd.DataFrame({"Gender": ["Male", "Female", "Female", "Male"]})

    expected_df = pd.DataFrame({"Gender": [1, 0, 0, 1]})

    transformed_df = transformer._map_gender_to_int(df)

    pd.testing.assert_frame_equal(transformed_df, expected_df)


def test_impute_mode_columns_fills_missing_with_most_frequent_value():
    transformer = Transformer()
    df = pd.DataFrame({"Geography": ["France", "France", "Spain", None]})

    transformed_df = transformer._impute_mode_columns(df)

    assert transformed_df["Geography"].isna().sum() == 0
    assert transformed_df.loc[3, "Geography"] == "France"


def test_impute_median_columns_fills_missing_with_median():
    transformer = Transformer()
    df = pd.DataFrame({"Age": [20.0, 30.0, 40.0, None]})

    transformed_df = transformer._impute_median_columns(df)

    assert transformed_df["Age"].isna().sum() == 0
    assert transformed_df.loc[3, "Age"] == 30.0


def test_cast_binary_numeric_columns_to_int():
    transformer = Transformer()
    df = pd.DataFrame({"HasCrCard": [1.0, 0.0, 1.0], "IsActiveMember": [0.0, 1.0, 1.0]})

    transformed_df = transformer._cast_binary_numeric_columns(df)

    assert transformed_df["HasCrCard"].dtype == int
    assert transformed_df["IsActiveMember"].dtype == int


def test_one_hot_encoding_drops_original_column_and_adds_dummies():
    transformer = Transformer()
    df = pd.DataFrame({"Geography": ["France", "Spain", "Germany", "France"]})

    transformed_df = transformer._one_hot_encoding(df)

    assert "Geography" not in transformed_df.columns
    # drop="first" means one fewer dummy column than categories
    assert len(transformed_df.columns) == 2


def create_df_balance():
    return pd.DataFrame(
        {
            "CreditScore": [600, 650, 700, 750, 800, 850],
            "Geography": [
                "France",
                "Spain",
                "France",
                "Spain",
                "France",
                "Spain",
            ],
            "Exited": [1, 0, 1, 0, 1, 0],
        }
    )


def test_balance_dataset():
    df_balance = create_df_balance()

    balanced_df = balance_dataset(df_balance, target_column="Exited")

    class_counts = balanced_df["Exited"].value_counts()
    assert class_counts[0] == class_counts[1]
    assert len(balanced_df) == len(df_balance)


def test_balance_with_unequal_classes():
    df_unequal = pd.DataFrame(
        {
            "CreditScore": [600, 650, 700, 750, 800],
            "Geography": ["France", "Spain", "France", "Spain", "France"],
            "Exited": [0, 0, 1, 0, 1],
        }
    )

    balanced_df = balance_dataset(df_unequal, target_column="Exited")

    class_counts = balanced_df["Exited"].value_counts()
    assert class_counts[0] == class_counts[1]
