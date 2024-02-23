<h1 align="center">
  <br>
  <a href="リンク先のURL"><img src="https://github.com/kohseim/AquaMind/blob/main/images/logo_black.png?raw=true" alt="AquaMind" width="500"></a>
  <br>
  AquaMind
  <br>
</h1>

<h4 align="center">You can view our creation on this <a href="" target="_blank">site</a>.</h4>

<p align="center">
  <a href=>
    <img src="https://badge.fury.io/js/electron-markdownify.svg"
         alt="Gitter">
  </a>
  <a href=><img src="https://badges.gitter.im/amitmerchant1990/electron-markdownify.svg"></a>
  <a href=>
      <img src="https://img.shields.io/badge/SayThanks.io-%E2%98%BC-1EAEDB.svg">
  </a>
  <a href=>
    <img src="https://img.shields.io/badge/$-donate-ff69b4.svg?maxAge=2592000&amp;style=flat">
  </a>
</p>

<p align="center">
  <a href="#overview">Overview</a> •
  <a href="#environment">Environment</a> •
  <a href="#datasets">Dataset</a> •
  <a href="#Feature Engineering">Feature Engineering</a> •
  <a href="#models">Models</a> •
  <a href="#related">Related</a> •
  <a href="#acknowledgement">Acknowledgement</a>
</p>

## Overview

## Environment

### Quick Start

### Docker

### Library

### For Developers

 - Type Checker
 ```bash
poetry run mypy <ファイルのパス>
```
 - Formatter
```bash
poetry run black <ファイルのパス>
```
 - Code Checker
```bash
poetry run flake8 <ファイルのパス>
```


## Dataset

### Dataset Overview

### Dataset Structure

| Column               | Description (English)                                                                                                          | 説明 (日本語)                                                                                               |
|----------------------|--------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|
| id                   | Corresponds to the file name of the satellite image data.                                                                      | 衛星画像データのファイル名に対応します                                                                       |
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


## Feature Engineering

### Feature Engineering Plan

- **Categorical Variables**  
Create binary features for all absolute quantity features `'sand', 'coral_algae', 'rock', 'seagrass', 'microalgal_mats', 'rubble'`.

- **Geospatial × Domain**  
(`'latitude_min'` + `'latitude_max'` )/2 × `'seagrass'`  
(`'longitude_min'` + `'longitude_max'` )/2 × `'seagrass_rate'`  
(`'latitude_min'` + `'latitude_max'` )/2 × `'coral_algae'`  
(`'longitude_min'` + `'longitude_max'` )/2 × `'coral_algae'`  
(`'latitude_min'` + `'latitude_max'` )/2 × `'rock'`  
(`'longitude_min'` + `'longitude_max'` )/2 × `'rock'`  
(`'latitude_min'` + `'latitude_max'` )/2 × `'microalgal_mats'`  
(`'longitude_min'` + `'longitude_max'` )/2 × `'microalgal_mats'`  
(`'latitude_min'` + `'latitude_max'` )/2 × `'rubble'`  
(`'longitude_min'` + `'longitude_max'` )/2 × `'rubble'`

- **Exponential Transform**  
Take the exponential of `'seagrass'` and `'seagrass_rate'`.

- **Geospatial × Image**  
(`'latitude_min'` + `'latitude_max'` )/2 × Image Feature A  
(`'latitude_min'` + `'latitude_max'` )/2 × Image Feature B  
(`'longitude_min'` + `'longitude_max'` )/2 × Image Feature C  
(`'longitude_min'` + `'longitude_max'` )/2 × Image Feature D

- **Image × Absolute Quantity**  
Image Feature A × `'seagrass'`  
Image Feature B × `'seagrass'`  
Image Feature C × `'coral_algae'`  
Image Feature D × `'rock'`  
Image Feature E × `'microalgal_mats'`  
Image Feature F × `'rubble'`

- **Unsupervised Learning Features**  
KMeans clustering (3 classes) on absolute quantity  
KMeans clustering (5 classes) on absolute quantity  
KMeans clustering (5 classes) on (rate + image)  
KMeans clustering (7 classes) on (rate + image)

### Feature Sets

- A 
Geospatial + Absolute Quantity + Rate + Image + Categorical + Unsupervised

- B 
Absolute Quantity + Rate + Image + Categorical + Unsupervised

- C 
Absolute Quantity + Image

- D  
(Geospatial × Domain) + Categorical + Image

- E  
Exponential + (Image × Absolute Quantity) + Unsupervised

- F  
(Geospatial × Image) + Rate

- G  
Absolute Quantity + Rate + Image

## Models

### Our Strategy

<h1 align="center">
  <br>
  <a href="リンク先のURL"><img src="https://github.com/kohseim/AquaMind/blob/main/images/AquaMind_構想.png?raw=true"  width="1000"></a>
  <br>
</h1>

### Algorithm

Classify using majority vote from the following 13 models.

| Number | Model                                   | Feature Pattern                            |
|--------|-----------------------------------------|--------------------------------------------|
| 1      | lightgbm + optuna                       | A                                          |
| 2      | lightgbm + optuna                       | B                                          |
| 3      | lightgbm + optuna                       | C                                          |
| 4      | xgboost + optuna                        | A                                          |
| 5      | xgboost + optuna                        | B                                          |
| 6      | catboost + optuna                       | A                                          |
| 7      | catboost + optuna                       | B                                          |
| 8      | randomforest + optuna                   | B                                          |
| 9      | tabpfn                                  | A                                          |
| 10     | tabpfn                                  | G                                          |
| 11     | Ensemble{(lightgbm + optuna)*3)}       | D                                          |
| 12     | Ensemble{(lightgbm + optuna)*3)}       | E                                          |
| 13     | Ensemble{(xgboost + lightgbm + catboost) + optuna} | F                                |


### Train


## Related


## Acknowledgement

