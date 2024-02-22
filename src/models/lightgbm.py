import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import log_loss
from typing import List, Dict, Tuple


def train_lightgbm_stratified_kfold(
    X: pd.DataFrame,
    y: pd.Series,
    columns_feature: List[str],
    target_binary: List[str],  # この実装では使用しないが、型情報を含める
    param: Dict[str, any],
    n_splits: int = 5,
) -> Tuple[List[lgb.Booster], List[float]]:
    """
    Stratified k-foldクロスバリデーションを使用してLightGBMモデルを訓練する関数。
    非均衡データを考慮して、各クラスの割合を保持する。

    引数:
    - X: pandas DataFrame, 特徴量データ。
    - y: pandas Series, 目的変数データ。
    - columns_feature: list, 特徴量のカラム名のリスト。
    - target_binary: list, 目的変数のカラム名のリスト（この関数では使用しないが、一貫性のために残す）。
    - param: dict, LightGBMモデルのパラメータ。
    - n_splits: int, クロスバリデーションの分割数。

    戻り値:
    - Tuple[List[lgb.Booster], List[float]]: 訓練済みLightGBMモデルのリストと各foldのlog lossスコアのリスト。
    """
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    models: List[lgb.Booster] = []
    scores: List[float] = []

    for train_index, test_index in skf.split(X, y):
        X_train, X_test = (
            X.iloc[train_index][columns_feature],
            X.iloc[test_index][columns_feature],
        )
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        lgb_train = lgb.Dataset(X_train, y_train)
        lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train)

        gbm: lgb.Booster = lgb.train(
            param,
            lgb_train,
            valid_sets=[lgb_train, lgb_eval],
            verbose_eval=50,
            early_stopping_rounds=100,
        )

        y_pred = gbm.predict(X_test, num_iteration=gbm.best_iteration)
        score: float = log_loss(y_test, y_pred)
        scores.append(score)
        models.append(gbm)

    return models, scores
