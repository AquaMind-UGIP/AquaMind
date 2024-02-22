import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import log_loss
from typing import List, Dict, Tuple


def train_xgboost_stratified_kfold(
    X: pd.DataFrame,
    y: pd.Series,
    columns_feature: List[str],
    target_binary: List[str],  # この実装では使用しないが、型情報を含める
    param: Dict[str, any],
    n_splits: int = 5,
) -> Tuple[List[xgb.Booster], List[float]]:
    """
    Stratified k-foldクロスバリデーションを使用してXGBoostモデルを訓練する関数。
    非均衡データを考慮して、各クラスの割合を保持する。

    引数:
    - X: pandas DataFrame, 特徴量データ。
    - y: pandas Series, 目的変数データ。
    - columns_feature: list, 特徴量のカラム名のリスト。
    - target_binary: list, 目的変数のカラム名のリスト（この関数では使用しないが、一貫性のために残す）。
    - param: dict, XGBoostモデルのパラメータ。
    - n_splits: int, クロスバリデーションの分割数。

    戻り値:
    - Tuple[List[xgb.Booster], List[float]]: 訓練済みXGBoostモデルのリストと各foldのlog lossスコアのリスト。
    """
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    models: List[xgb.Booster] = []
    scores: List[float] = []

    for train_index, test_index in skf.split(X, y):
        X_train, X_test = (
            X.iloc[train_index][columns_feature],
            X.iloc[test_index][columns_feature],
        )
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        dtrain = xgb.DMatrix(X_train, label=y_train)
        dtest = xgb.DMatrix(X_test, label=y_test)

        bst: xgb.Booster = xgb.train(
            param,
            dtrain,
            num_boost_round=param.get("num_boost_round", 100),
            evals=[(dtrain, "train"), (dtest, "eval")],
            early_stopping_rounds=param.get("early_stopping_rounds", 10),
            verbose_eval=param.get("verbose_eval", 50),
        )

        y_pred = bst.predict(dtest)
        score: float = log_loss(y_test, y_pred)
        scores.append(score)
        models.append(bst)

    return models, scores
