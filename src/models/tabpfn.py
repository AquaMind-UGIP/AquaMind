import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score
from tabpfn import TabPFNClassifier
from typing import List, Tuple


def train_tabpfn_stratified_kfold(
    X: pd.DataFrame,
    y: pd.Series,
    columns_feature: List[str],
    n_splits: int = 5,
    N_ensemble_configurations: int = 32,
) -> Tuple[List[TabPFNClassifier], List[float]]:
    """
    Stratified k-foldクロスバリデーションを使用してTabPFNモデルを訓練する関数。
    非均衡データを考慮して、各クラスの割合を保持する。

    引数:
    - X: pandas DataFrame, 特徴量データ。
    - y: pandas Series, 目的変数データ。
    - columns_feature: list, 特徴量のカラム名のリスト。
    - n_splits: int, クロスバリデーションの分割数。
    - N_ensemble_configurations: int, アンサンブル設定の数。

    戻り値:
    - Tuple[List[TabPFNClassifier], List[float]]: 訓練済みTabPFNモデルのリストと各foldの精度スコアのリスト。
    """
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    models: List[TabPFNClassifier] = []
    scores: List[float] = []

    for train_index, test_index in skf.split(X, y):
        X_train, X_test = (
            X.iloc[train_index][columns_feature],
            X.iloc[test_index][columns_feature],
        )
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        classifier = TabPFNClassifier(
            device="cpu", N_ensemble_configurations=N_ensemble_configurations
        )
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)

        score = accuracy_score(y_test, y_pred)
        scores.append(score)
        models.append(classifier)

    return models, scores
