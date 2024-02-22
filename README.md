<h1 align="center">
  <br>
  <a href="リンク先のURL"><img src="https://github.com/kohseim/AquaMind/blob/main/images/logo_black.png?raw=true" alt="AquaMind" width="500"></a>
  <br>
  AquaMind
  <br>
</h1>

<h4 align="center">You can view our creation on this <a href="" target="_blank">site</a>.</h4>

<p align="center">
  <a href="https://badge.fury.io/js/electron-markdownify">
    <img src="https://badge.fury.io/js/electron-markdownify.svg"
         alt="Gitter">
  </a>
  <a href="https://gitter.im/amitmerchant1990/electron-markdownify"><img src="https://badges.gitter.im/amitmerchant1990/electron-markdownify.svg"></a>
  <a href="https://saythanks.io/to/bullredeyes@gmail.com">
      <img src="https://img.shields.io/badge/SayThanks.io-%E2%98%BC-1EAEDB.svg">
  </a>
  <a href="https://www.paypal.me/AmitMerchant">
    <img src="https://img.shields.io/badge/$-donate-ff69b4.svg?maxAge=2592000&amp;style=flat">
  </a>
</p>

<p align="center">
  <a href="#overview">Overview</a> •
  <a href="#datasets">Dataset</a> •
  <a href="#EDA">EDA</a> •
  <a href="#models">Models</a> •
  <a href="#related">Related</a> •
  <a href="#acknowledgement">Acknowledgement</a>
</p>

## Overview


## Dataset

### Dataset Overview

### Dataset Structure

| Column               | Description (English)                                                                                                          | 説明 (日本語)                                                                                               |
|----------------------|--------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|
| id                   | Corresponds to the file name of the satellite image data.                                                                      | 衛星画像データのファイル名に対応します。                                                                         |
| latitude_min         | The y-coordinate (latitude) of the bottom left corner of a 100m x 100m rectangle in the target area (around Ishigaki Island coast). | 対象の範囲（石垣島の海岸あたり）を100m×100mの矩形に区切りながら処理している。その矩形の左下のy座標（緯度）              |
| longitude_min        | The x-coordinate (longitude) of the bottom left corner of the rectangle.                                                       | 上記と同様に矩形の左下のx座標（経度）                                                                    |
| latitude_max         | The y-coordinate (latitude) of the top right corner of the rectangle.                                                          | 上記と同様に矩形の右上のy座標（緯度）                                                                       |
| longitude_max        | The x-coordinate (longitude) of the top right corner of the rectangle.                                                         | 上記と同様に矩形の右上のx座標（経度）                                                                       |
| sand                 | The number of pixels of sand distributed within the rectangle, as surveyed by the [Allen Coral Atlas](https://allencoralatlas.org/). | [Allen Coral Atlas](https://allencoralatlas.org/)で調査した、矩形内に分布するsandのピクセル数                           |
| coral_algae          | The number of pixels of coral/algae within the rectangle.                                                                       | 矩形内に分布するcoral/algaeのピクセル数                                                                      |
| rock                 | The number of pixels of rock within the rectangle.                                                                              | 矩形内に分布するrockのピクセル数                                                                             |
| seagrass             | The number of pixels of seagrass within the rectangle.                                                                          | 矩形内に分布するseagrassのピクセル数。                                                                         |
| microalgal_mats      | The number of pixels of microalgal mats within the rectangle.                                                                   | 矩形内に分布するmicroalgal matsのピクセル数                                                                  |
| rubble               | The number of pixels of rubble within the rectangle.                                                                            | 矩形内に分布するrubbleのピクセル数                                                                        |
| sand_rate            | The proportion of sand within the rectangle, as surveyed by the [Allen Coral Atlas](https://allencoralatlas.org/).              | [Allen Coral Atlas](https://allencoralatlas.org/)で調査した、矩形内に分布するsandの割合                           |
| coral_algae_rate     | The proportion of coral/algae within the rectangle.                                                                             | 矩形内に分布するcoral/algaeの割合                                                                            |
| rock_rate            | The proportion of rock within the rectangle.                                                                                    | 矩形内に分布するrockの割合                                                                                   |
| seagrass_rate        | The proportion of seagrass within the rectangle.                                                                                | 矩形内に分布するseagrassの割合。                                                                                |
| microalgal_mats_rate | The proportion of microalgal mats within the rectangle.                                                                         | 矩形内に分布するmicroalgal matsの割合。                                                                         |
| rubble_rate          | The proportion of rubble within the rectangle.                                                                                  | 矩形内に分布するrubbleの割合。                                                                                  |
| seagrass_overlap     | The percentage of the rectangle's area that overlaps with seagrass distribution areas obtained from the [OCEAN DATA VIEWER](https://data.unep-wcmc.org/). | [OCEAN DATA VIEWER](https://data.unep-wcmc.org/)で取得した海草の分布の領域に対して、100m×100mの矩形の面積の内何


## EDA (Exploratory Data Analysis)


## Models


## Related


## Acknowledgement

