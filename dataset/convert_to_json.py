import csv
import json


# CSVファイルからJSON形式に変換する関数
def csv_to_json(csv_file_path):
    json_data = []  # JSONデータを格納するリスト

    # CSVファイルを読み込みモードで開く
    with open(csv_file_path, "r", newline="") as csvfile:
        # CSVリーダーを作成
        reader = csv.DictReader(csvfile)
        # 各行に対して処理を行う
        for row in reader:
            # 各行をJSON形式に変換してリストに追加
            json_data.append(
                {
                    "id": row["id"],
                    "latitude_min": row["latitude_min"],
                    "longitude_min": row["longitude_min"],
                    "latitude_max": row["latitude_max"],
                    "longitude_max": row["longitude_max"],
                    "probability": str(
                        float(row["probability"])
                    ),  # 浮動小数点数を文字列に変換
                }
            )

    return json_data


# CSVファイルからJSONファイルへの変換と保存
def convert_and_save(csv_file_path, json_file_path):
    # CSVからJSONに変換
    json_data = csv_to_json(csv_file_path)

    # JSONファイルに書き込みモードで開く
    with open(json_file_path, "w") as jsonfile:
        # JSONデータをファイルに書き込む
        json.dump(json_data, jsonfile, indent=4)


# CSVファイルからJSONファイルへの変換と保存
convert_and_save("inference_for_web.csv", "inference.json")
