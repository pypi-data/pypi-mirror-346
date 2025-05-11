import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder, OneHotEncoder


def read_data_csv(path : str):
    global df
    df = pd.read_csv(path)
    return df.head()

def num_cat(df):
    global numerical_col
    global categorical_col

    numerical_col = df.select_dtypes(include=["int64", "float64"]).columns
    categorical_col = df.select_dtypes(include=["object"]).columns

    print("Numerical columns : ",numerical_col)
    print("Categorical columns : ",categorical_col)

def handling_missing_value(self):
    df = self.copy()

    missing_value_percent = (df.isnull().sum() / len(df) * 100).reset_index()
    missing_value_percent.columns = ["column", "missing_percent"]
    print(missing_value_percent)
    print("-"*40)
    drop_col = list(missing_value_percent[missing_value_percent["missing_percent"] > 50]["column"])
    df = df.drop(columns = drop_col)

    num_missing_col = [col for col in numerical_col if df[col].isnull().sum() > 0]
    cat_missing_col = [col for col in categorical_col if df[col].isnull().sum() > 0]
    
    if num_missing_col:
        num_imputer = SimpleImputer(strategy="mean")
        df[num_missing_col] = num_imputer.fit_transform(df[num_missing_col])
    
    if cat_missing_col:
        cat_imputer = SimpleImputer(strategy="most_frequent")
        df[cat_missing_col] = cat_imputer.fit_transform(df[cat_missing_col])

    print(f"Dropped columns: {drop_col}")
    print(f"Imputed numerical columns: {num_missing_col}")
    print(f"Imputed categorical columns: {cat_missing_col}")
    print("-"*40)
    
    return df.isnull().sum()

def encoder(self, encoding_type="label", ordinal_mapping=None, max_unique_for_ordinal=10):
    df = self.copy()
    
    categorical_col = df.select_dtypes(include="object").columns.tolist()

    if encoding_type == "label":
        le = LabelEncoder()
        for col in categorical_col:
            df[col] = le.fit_transform(df[col].astype(str))
        print("✅ Label encoding applied.")

    elif encoding_type == "onehot":
        df = pd.get_dummies(df, columns = categorical_col, drop_first = True)
        df = df.astype(int)
        print("✅ One-hot encoding applied.")

    elif encoding_type == "ordinal":
        if ordinal_mapping is None:
            # Generate automatic mapping
            ordinal_mapping = {}
            for col in categorical_col:
                unique_vals = df[col].dropna().unique()
                if len(unique_vals) <= max_unique_for_ordinal:
                    ordinal_mapping[col] = sorted(list(unique_vals))
            
            if not ordinal_mapping:
                raise ValueError("❌ No suitable columns found for ordinal encoding.")

            print("ℹ️ Auto-generated ordinal mapping:")
            for k, v in ordinal_mapping.items():
                print(f"   {k}: {v}")

        ordinal_cols = list(ordinal_mapping.keys())
        oe = OrdinalEncoder(categories=[ordinal_mapping[col] for col in ordinal_cols])

        df[ordinal_cols] = oe.fit_transform(df[ordinal_cols].astype(str))
        print("✅ Ordinal encoding applied.")

    else:
        raise ValueError("❌ Invalid encoding_type. Use 'label', 'onehot', or 'ordinal'.")

    return df