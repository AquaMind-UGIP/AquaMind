import os
import rasterio
import numpy as np
from matplotlib import pyplot as plt
import re
import cv2


def extract_haar_like_features(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Haar-like特徴量を抽出するためのカスケード分類器を読み込む
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    cascade_classifier = cv2.CascadeClassifier(cascade_path)

    # 画像から顔を検出する
    faces = cascade_classifier.detectMultiScale(img_gray)

    # Haar-like特徴量を抽出した結果を格納するリスト
    features = []

    # 検出された各顔領域についてHaar-like特徴量を抽出する
    for x, y, w, h in faces:
        # 顔領域を切り取る
        face_roi = img_gray[y : y + h, x : x + w]

        # Haar-like特徴量を抽出する
        haar_features = cv2.HaarEvaluator.evaluate(img_gray, face_roi)

        # 抽出した特徴量をリストに追加する
        features.append(haar_features)

    return features


def extract_hog_features(img):
    # HOG特徴量抽出器を初期化
    win_size = (64, 64)  # ウィンドウサイズ
    block_size = (16, 16)  # ブロックサイズ
    block_stride = (8, 8)  # ブロックストライド
    cell_size = (8, 8)  # セルサイズ
    num_bins = 9  # ヒストグラムのビンの数
    hog = cv2.HOGDescriptor(win_size, block_size, block_stride, cell_size, num_bins)

    # HOG特徴量を計算
    hog_features = hog.compute(img)

    return hog_features


def extract_sift_features(image):
    # SIFT特徴量抽出器を初期化
    sift = cv2.SIFT_create()

    # 画像からSIFT特徴量を検出および記述
    keypoints, descriptors = sift.detectAndCompute(image, None)

    return keypoints, descriptors


if __name__ == "__main__":
    current_directory = os.path.dirname(__file__)
    target_directory = os.path.join(current_directory, "..", "..", "dataset", "img_tif")

    # ディレクトリ内のすべてのファイルを取得
    files = sorted([f for f in os.listdir(target_directory) if f.endswith(".tif")])
    files.sort(key=lambda x: int(re.search(r"\d+", x).group()))

    # ディレクトリ内のすべての画像ファイルに対して処理を繰り返す
    for idx, file in enumerate(files):
        # TIFファイルの場合のみ処理を行う
        if file.endswith(".tif"):
            # 画像ファイルのパス
            img_path = os.path.join(target_directory, file)

            # Rasterioを使って画像を開く
            with rasterio.open(img_path) as src:
                # バンド4, 3, 2を読み込む
                band_r = src.read(4)
                band_g = src.read(3)
                band_b = src.read(2)

                # それぞれのバンドの範囲を0から1に正規化する
                band_r = band_r / band_r.max()
                band_g = band_g / band_g.max()
                band_b = band_b / band_b.max()

                # RGB画像を作成する
                rgb_img = np.dstack((band_r, band_g, band_b))
            bgr_img = cv2.cvtColor((rgb_img * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
            height, width, _ = bgr_img.shape
            resized_image = cv2.resize(bgr_img, (width * 10, height * 10))

            # 画像からHaar-like特徴量を抽出する
            # haar_features = extract_haar_like_features(resized_image)
            # print(idx, haar_features)

            # 画像からHOG特徴量を抽出する
            # hog_features = extract_hog_features(resized_image)
            # print(idx, np.sum(hog_features != 0), len(hog_features))

            # 画像からSIFT特徴量を抽出する
            # SIFT特徴量を抽出
            # sift_keypoints, sift_descriptors = extract_sift_features(resized_image)
            # print(idx, sift_descriptors)
