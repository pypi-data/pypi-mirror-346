# TiledImage

大きな画像を効率的に扱うための Python ライブラリです。メモリ使用量を抑えながら、大きな画像をタイル（小さな断片）に分割して管理します。

## 特徴

- 大きな画像をタイルに分割して管理
- ファイルシステム上でのキャッシュ機能
- メモリ効率の良い画像処理
- コンテキストマネージャ（`with`文）による簡単な使用

## インストール

```bash
pip install tiledimage
```

## 基本的な使い方

### 画像の分割（PNG → PNGs）

```python
from tiledimage import CachedImage
import cv2

# 画像を読み込み
img = cv2.imread("large_image.png")

# タイル化して保存
with CachedImage(
    mode="new",
    dir="output.pngs",
    tilesize=(64, 64),
    cachesize=10,
    bgcolor=(255, 255, 255),  # 背景色（白）
    fileext="jpg"
) as tiled:
    tiled.put_image((0, 0), img)  # 画像を配置
```

### 画像の結合（PNGs → PNG）

```python
from tiledimage import CachedImage
import cv2

# タイル化された画像を読み込み
with CachedImage(mode="inherit", dir="input.pngs") as tiled:
    # 全体の画像を取得
    full_image = tiled.get_image()
    # 保存
    cv2.imwrite("combined_image.png", full_image)
```

### コマンドラインツール

画像の分割：

```bash
pngs2 input.png output.pngs
```

画像の結合：

```bash
2pngs input.pngs output.png
```

## API リファレンス

### CachedImage

メインのクラス。タイル化された画像を管理します。

```python
CachedImage(
    mode,           # "new" または "inherit"
    dir="image.pngs",  # タイルの保存ディレクトリ
    tilesize=128,   # タイルのサイズ（整数またはタプル）
    cachesize=10,   # キャッシュサイズ
    fileext="png",  # タイルのファイル形式
    bgcolor=(0,0,0), # 背景色
    hook=None,      # タイル書き換え時のフック関数
    disposal=False  # 終了時にディレクトリを削除するか
)
```

#### 主要メソッド

- `put_image(pos, img, linear_alpha=None)`: 画像を配置
- `get_image()`: 全体の画像を取得
- `write_info()`: 情報を保存（通常は自動的に呼ばれる）

### TiledImage

基本的なタイル画像クラス。キャッシュ機能はありません。

```python
TiledImage(
    tilesize=128,   # タイルのサイズ
    bgcolor=(100,100,100)  # 背景色
)
```

## 開発者向け情報

### テスト

```bash
make test
```

### ビルド

```bash
make build
```

### デプロイ

```bash
make deploy
```

## ライセンス

MIT License

## 作者

Masakazu Matsumoto (vitroid@gmail.com)
