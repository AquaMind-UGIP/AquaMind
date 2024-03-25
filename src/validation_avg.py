import pandas as pd
import os

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

import time


def pre_process_csv(df):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_values = scaler.fit_transform(
        df.iloc[:, 1].values.reshape(-1, 1)
    )  # スケーリングした値を取得
    scaled_df = pd.DataFrame(
        scaled_values, columns=["y_pred_normalized"]
    )  # スケーリングした値をDataFrameに変換
    df = pd.concat([df, scaled_df], axis=1)  # 新しい列を元のDataFrameに追加

    return df


from sklearn.metrics import f1_score


def find_optimal_threshold(true_labels, predicted_probs):
    thresholds = np.arange(0, 1.01, 0.001)  # 0から1までの0.01刻みのしきい値を作成
    best_threshold = 0
    best_score = 0

    true_labels = (true_labels >= 0.5).astype(int)
    print(true_labels.sum())

    best_sum = -1
    best_label = None

    for threshold in thresholds:
        # しきい値を用いて確率をバイナリに変換
        predicted_labels = (predicted_probs >= threshold).astype(int)

        sum = predicted_labels.sum()

        # score = accuracy_score(true_labels, predicted_labels)
        # score = f1_score(true_labels, predicted_labels)
        # score = f1_score(true_labels, predicted_labels, average="macro")
        score = f1_score(true_labels, predicted_labels, average="micro")
        # score = roc_auc_score(true_labels, predicted_labels)

        # 最適なしきい値を更新
        if score > best_score:
            best_score = score
            best_threshold = threshold
            best_sum = sum
            best_label = predicted_labels

    return best_threshold, best_score, best_sum, best_label, true_labels


if __name__ == "__main__":
    # #平均値作成
    # dfs = []
    # file_nums = 0
    # # 各CSVファイルをループで処理
    # for i in range(1, 14):
    #     if i in [9, 10]:
    #         continue
    #     # CSVファイルを読み込む
    #     df = pd.read_csv(f"output_{i}.csv", header=None).iloc[1:, :]
    #     print(df.iloc[1, :].max(), df.iloc[0, :].min())
    #     dfs.append(df)

    # data_avg = []

    # # 各CSVファイルの各行の平均値を計算
    # for i in range(len(dfs[0])):
    #     sums = []
    #     sum = 0
    #     for j in range(len(dfs)):
    #         sum += dfs[j].iloc[i, 1]
    #     avg = sum / len(dfs)
    #     data_avg.append(avg)

    # # 平均値から新たなdfを作成
    # df_avg = pd.DataFrame(data_avg)

    # # idと平均値をconcatする
    # df_avg = pd.concat([dfs[0].iloc[:, 0], df_avg], axis=1)
    # # df_avg.iloc[:, 0] = df_avg.iloc[:, 0].astype(int)
    # # print(df_avg.iloc[:, 1].max(), df_avg.iloc[:, 1].min())
    # # df_avg = pre_process_csv(df_avg)
    # df_avg.to_csv("output_avg.csv", index=False, header=False)
    # print(df_avg.iloc[:, 1].max(), df_avg.iloc[:, 1].min())
    # exit()

    # バグっているので読み込み直して正規化
    df_avg = pd.read_csv("output_avg_normalized.csv", header=None)
    df_avg = pre_process_csv(df_avg)
    true_data = pd.read_csv("dataset_valid.csv", usecols=[0, 17])
    true_data = pre_process_csv(true_data)

    # true_dataとdf_avgの2列目を取得
    true_labels = true_data.iloc[:, 2]
    print(true_labels)
    predicted_probs = df_avg.iloc[:, 2]

    # 最適なしきい値を見つける
    optimal_threshold, best_score, best_sum, best_label, truel_label = (
        find_optimal_threshold(true_labels, predicted_probs)
    )
    print("Optimal Threshold:", optimal_threshold)
    print("Best Score:", best_score)
    print("Best Sum:", best_sum)
    cm = confusion_matrix(truel_label, best_label)

    print("Confusion Matrix:")
    print(cm)

    # best_labelをDataFrameに変換して、IDを追加
    id_column = true_data.iloc[:, 0]
    true_data_position = pd.read_csv("dataset_valid.csv", usecols=[1, 2, 3, 4])
    print(true_data_position)

    probability = pd.read_csv("output_avg.csv", header=None).iloc[:, 1]

    best_label_df = pd.DataFrame(
        {
            "id": id_column,
            "longitude_min": true_data_position["latitude_min"],
            "latitude_min": true_data_position["longitude_min"],
            "longitude_max": true_data_position["latitude_max"],
            "latitude_max": true_data_position["longitude_max"],
            "probability": true_labels,
            # "probability": probability,
        }
    )

    # CSVファイルとして出力
    print(
        best_label_df["probability"].min(),
        best_label_df["probability"].max(),
        best_label_df["probability"].mean(),
        best_label_df["probability"].var(),
    )

    best_label_df.to_csv("best_label.csv", index=False)
