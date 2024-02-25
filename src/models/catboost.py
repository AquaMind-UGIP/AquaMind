import numpy as np
import pandas as pd
from catboost import CatBoostClassifier, Pool
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import log_loss
from typing import List, Dict, Tuple


def train_catboost_stratified_kfold(
    X: pd.DataFrame,
    y: pd.Series,
    columns_feature: List[str],
    target_binary: List[str],  # この実装では使用しないが、型情報を含める
    param: Dict[str, any],
    n_splits: int = 5,
) -> Tuple[List[CatBoostClassifier], List[float]]:
    """
    Stratified k-foldクロスバリデーションを使用してCatBoostモデルを訓練する関数。
    非均衡データを考慮して、各クラスの割合を保持する。

    引数:
    - X: pandas DataFrame, 特徴量データ。
    - y: pandas Series, 目的変数データ。
    - columns_feature: list, 特徴量のカラム名のリスト。
    - target_binary: list, 目的変数のカラム名のリスト（この関数では使用しないが、一貫性のために残す）。
    - param: dict, CatBoostモデルのパラメータ。
    - n_splits: int, クロスバリデーションの分割数。

    戻り値:
    - Tuple[List[CatBoostClassifier], List[float]]: 訓練済みCatBoostモデルのリストと各foldのlog lossスコアのリスト。
    """
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    models: List[CatBoostClassifier] = []
    scores: List[float] = []

    for train_index, test_index in skf.split(X, y):
        X_train, X_test = (
            X.iloc[train_index][columns_feature],
            X.iloc[test_index][columns_feature],
        )
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        train_pool = Pool(X_train, y_train)
        test_pool = Pool(X_test, y_test)

        model = CatBoostClassifier(**param)
        model.fit(
            train_pool,
            eval_set=test_pool,
            # verbose=50,
            # early_stopping_rounds=100,
            use_best_model=True,
        )

        y_pred = model.predict_proba(X_test)[:, 1]
        score = log_loss(y_test, y_pred)
        scores.append(score)
        models.append(model)

    return models, scores
