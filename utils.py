
import json

import numpy as np
import pandas as pd
import sklearn
from sklearn.compose import make_column_transformer
from sklearn.linear_model import PoissonRegressor
from sklearn.metrics import make_scorer, mean_poisson_deviance
from sklearn.model_selection import KFold, cross_validate
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Lets exposure weights reach both the model fit and the validation score
sklearn.set_config(enable_metadata_routing=True)

RANDOM_STATE = 42
MIN_DRIVING_AGE = 16
TRADITIONAL_COLS = [
    "Insured.age", "Insured.sex", "Car.age", "Marital", "Car.use",
    "Credit.score", "Region", "Annual.miles.drive", "Years.noclaims", "Territory",
]


def load_data(path="telematics_syn-032021.csv", drop_columns_path="drop_columns.json"):
    """Clean the data and return X, claim counts and exposure in years."""
    df = pd.read_csv(path)
    df = df[df["Insured.age"] - df["Years.noclaims"] >= MIN_DRIVING_AGE].copy()
    df["Territory"] = df["Territory"].astype("category")

    X = df.drop(columns=["NB_Claim", "AMT_Claim", "Duration",
                         "Pct.drive.sun", "Pct.drive.wkday", "Pct.drive.wkend"])
    if drop_columns_path:
        X = X.drop(columns=json.load(open(drop_columns_path)))
    return X, df["NB_Claim"], df["Duration"] / 366


def build_pipeline(cat_cols, alpha=0.0):
    """Encode, scale and fit, all refitted inside each fold."""
    encoder = make_column_transformer(
        (OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=False), cat_cols),
        remainder="passthrough",
        verbose_feature_names_out=False,
    )
    return make_pipeline(
        encoder,
        StandardScaler().set_fit_request(sample_weight=False),
        PoissonRegressor(alpha=alpha, max_iter=1000).set_fit_request(sample_weight=True),
    )


def cv_deviance(pipe, X, y, exposure):
    """Exposure weighted Poisson deviance for each fold (lower is better)."""
    scorer = make_scorer(mean_poisson_deviance, greater_is_better=False).set_score_request(sample_weight=True) # this line makes the mean poisson deviance become negative
    cv = cross_validate(
        pipe, X, y / exposure,
        cv=KFold(5, shuffle=True, random_state=RANDOM_STATE),
        scoring=scorer,
        params={"sample_weight": exposure},
    )
    return -cv["test_score"] # flip the sign back to positive


def evaluate(X, y, exposure, alphas=np.logspace(-4, 2, 13)):
    """Try every alpha by CV and return the best alpha and its fold scores."""
    cat_cols = X.select_dtypes(include=["object", "category"]).columns.tolist()
    best_alpha, best_folds = None, None
    for alpha in alphas:
        folds = cv_deviance(build_pipeline(cat_cols, alpha), X, y, exposure)
        if best_folds is None or folds.mean() < best_folds.mean():
            best_alpha, best_folds = alpha, folds
    return best_alpha, best_folds