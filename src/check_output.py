import pandas as pd
import matplotlib.pyplot as plt
import os

# CSVファイルが格納されたディレクトリ
# CSVファイルのリストを取得

# サブプロットの行数と列数
rows = 5
cols = 2

# サブプロットのインデックス
subplot_index = 1

# フィギュアのサイズを設定
plt.figure(figsize=(15, 15))

for i in range(1, 1):
    # CSVファイルを読み込む
    if i in [9, 10]:
        continue
    file_name = f"output_{i}"
    df = pd.read_csv(f"{file_name}.csv", header=None)

    # サブプロットを追加
    plt.subplot(rows, cols, subplot_index)

    # プロット
    plt.plot(df.iloc[:, 0], df.iloc[:, 1], marker="o")

    # ラベル設定
    plt.xlabel(df.columns[0])
    plt.ylabel(df.columns[1])
    plt.title("{}".format(file_name))  # ファイル名をタイトルに設定

    # グリッド線追加
    plt.grid(True)

    subplot_index += 1

# サブプロット間の余白を調整
plt.tight_layout()

# グラフ表示
plt.show()
