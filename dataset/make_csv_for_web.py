import csv


# 関数定義: CSVファイルのパスを受け取り、各行の1列目とインデックスを比較する
def compare_index_with_value(csv_file_path):
    # CSVファイルを読み込みモードで開く
    with open(csv_file_path, "r", newline="") as csvfile:
        # CSVリーダーを作成
        reader = csv.reader(csvfile)
        # ヘッダー行をスキップ
        next(reader)
        # インデックスを初期化
        index = 0
        # 各行に対して処理を行う
        for row in reader:
            # 行から1列目の値を取得
            value = row[0]
            # インデックスと1列目の値を比較し、一致しているかどうかを確認
            if str(index) == value:
                # print(f"Index {index} matches value {value}")
                pass
            else:
                print(f"Index {index} does not match value {value}")
            # インデックスをインクリメント
            index += 1


# 関数定義: 2つのCSVファイルから指定された列を取得して結合し、新しいCSVファイルを作成する
def merge_csv_files(file1_path, file2_path, output_file_path):
    # 正規化のために事前処理
    data = []
    with open(file2_path, "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # ヘッダー行をスキップ
        for idx, row in enumerate(reader):
            if idx == 0:
                continue
            data.append(float(row[1]))  # 2列目のデータをfloat型に変換してリストに追加
    # 最小値と最大値を取得
    min_value = min(data)
    max_value = max(data)

    # 新しいCSVファイルを書き込みモードで開く
    with open(output_file_path, "w", newline="") as outfile:
        # CSVライターを作成
        writer = csv.writer(outfile)

        # ファイル1を読み込みモードで開く
        with open(file1_path, "r", newline="") as file1:
            # CSVリーダーを作成
            reader1 = csv.reader(file1)
            # ファイル2を読み込みモードで開く
            with open(file2_path, "r", newline="") as file2:
                # CSVリーダーを作成
                reader2 = csv.reader(file2)

                # 2つのファイルから順番に行を読み込み、結合して新しいCSVファイルに書き込む
                for index, (row1, row2) in enumerate(zip(reader1, reader2)):
                    # 2つの行から2列目と3列目を取得
                    if index == 0:
                        column2_3_file1 = [
                            "id",
                            "latitude_min",
                            "longitude_min",
                            "latitude_max",
                            "longitude_max",
                        ]
                        column2_file2 = "probability"
                    else:
                        column2_3_file1 = row1[0:5]
                        column2_file2 = row2[1]
                    print(column2_file2)

                    # ファイル1の2列目が負の場合は0に変換
                    if index > 0:
                        if float(column2_file2) < 0:
                            column2_file2 = "0"

                        # 新しい行を作成してCSVファイルに書き込む
                        new_probability = (float(column2_file2) - min_value) / (
                            max_value - min_value
                        )
                    else:
                        new_probability = column2_file2
                    new_row = column2_3_file1 + [new_probability]
                    writer.writerow(new_row)


# 関数の呼び出し: CSVファイルのパスを指定して比較を行う
# compare_index_with_value("inference.csv")


# 関数の呼び出し: 2つのCSVファイルから2列目と3列目を取得して新しいCSVファイルを作成
merge_csv_files("dataset_valid.csv", "inference.csv", "inference_for_web.csv")
