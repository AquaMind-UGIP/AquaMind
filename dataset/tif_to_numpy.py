import numpy as np
import matplotlib.pyplot as plt
import tifffile as tiff
import os
import pandas as pd
import cv2

# 画像の読み込み
img = tiff.imread("/Users/andohikaru/Desktop/YAM/YAM/dataset/img_tif/265.tif")

# チャンネル数の確認
if img.shape[2] == 16:
    # 16チャンネルの場合の処理
    # 例えば、16チャンネルをRGBに変換して表示するなど
    # 以下は最初の3チャンネルを取り出してRGB画像に変換する例です
    img_rgb = img[:, :, :3]  # 最初の3チャンネルを取り出す
    img_rgb = np.clip(img_rgb, 0, 1)  # 0から1の範囲にクリッピング
    plt.imshow(img_rgb)
    plt.show()
else:
    # 通常の3チャンネルまたは4チャンネルの場合の処理
    img_array = np.array(img)
    plt.imshow(img_array)
    plt.show()
