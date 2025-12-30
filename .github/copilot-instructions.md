# LifeGameBot BlueSky Bot - AI Agent Instructions

## プロジェクト概要

Conway's Game of Lifeをシミュレートし、15分ごとにBlueSkyに自動投稿するボット。状態がループまたは固定化すると新しいrun（実行回）を初期化してGIFアニメーションを生成。

## アーキテクチャとデータフロー

### メインワークフロー ([lgbs.sh](lgbs.sh) - cron経由で15分ごと実行)

1. **状態更新**: `lg.pl` が `state.txt` を読み込み、Game of Lifeルールで次状態を計算 → `state.new`
2. **ループ検出**: `isLoop.py` が前後状態を比較し、ループ/固定化判定 → `loop.txt`
3. **分岐処理**:
   - **ループ/固定化時** (`loop.txt` に内容あり):
     - `makeGifMaker.py`: GIF生成スクリプトを出力 → `makeGif.sh`
     - `sh makeGif.sh`: ImageMagickでPNGからGIF作成
     - `announce.py`: 終了アナウンス文生成 → `post.txt`
     - `makeLogDirNextRun.py`: 次回ログディレクトリ作成
   - **通常進行時** (`loop.txt` が空):
     - `makeSVG.pl`: SVG画像生成 → `state.svg`
     - `makePNG.pl`: PNG画像生成 → `./pngs/{run:08}/{gene:08}.png`
     - `saveLog.pl`: 状態ファイルとSVGをログディレクトリに保存
     - `trans.pl`: 投稿本文生成 (絵文字変換) → `post.txt`
4. **投稿**: `post.py` が `post.txt` を読み込み、API経由で投稿
5. **状態更新**: `state.new` を `state.txt` にリネーム

## ファイル形式

### state.txt/state.new (状態ファイル)
```
0101010101    # 10行の10桁の0/1 (10x10グリッド)
1010101010
...
run	123      # run番号 (タブ区切り)
gene	45       # gene番号 (世代番号)
```
- 最終行が `init` の場合、次回実行時に新runを初期化

### loop.txt (ループ情報)
```
run	123
gene	45
loop_from	30  # ループ開始gene (gene==loop_from → frozen)
```

## 重要な規約

### パス構造
- ローカル: `./stateLogs/{run:08}/{gene:08}.txt|svg`
- リモート: `/home/ikatake/www/wetsteam/LifeGameBotBS/stateLogs/{run:08}/{gene:08}.txt|svg`
- PNG: `./pngs/{run:08}/{gene:08}.png` (GIF生成用一時ファイル)
- GIF: `/home/ikatake/www/wetsteam/LifeGameBotBS/gifs/{run:08}.gif`

### 言語混在パターン
- **Perl**: 状態シミュレーション (`lg.pl`)、画像生成 (`makeSVG.pl`, `makePNG.pl`)、ログ保存 (`saveLog.pl`)、テキスト変換 (`trans.pl`)
- **Python**: ループ検出 (`isLoop.py`)、GIF生成準備 (`makeGifMaker.py`)、投稿処理 (`post.py`, `announce.py`)、ディレクトリ作成 (`makeLogDirNextRun.py`)
- **共通モジュール**: [common.py](common.py) - `readStateFile()`, `readLoopFile()` 関数と `state_log_dir` 定数

### フォーマット規約
- 数値フォーマット: `{:08}` または `sprintf("%08d")` でゼロ埋め8桁
- ファイル区切り: タブ (`\t`) 区切り
- 出力方式: 標準出力にリダイレクト (`> output.txt`) を多用

## 開発ワークフロー

### テスト実行
```bash
sh test.sh  # lgbs.shとほぼ同じ、投稿なしでローカルテスト
```

### 認証情報
- [_key_secret_.py](_key_secret_.py): SNS API認証情報 (`ck`, `cs`, `at`, `ats`)
  - **注意**: このファイルは機密情報、コミット厳禁

### デバッグ
- ループ検出ロジック: [isLoop.py](isLoop.py) - `(1)` frozen判定、`(2)` 過去状態との比較
- 状態遷移: [lg.pl](lg.pl) - `update()` サブルーチンでGame of Lifeルール実装
- 10x10トーラスグリッド (端が繋がる): `($x ± 1 + $width) % $width`

## 外部依存

- **Perl**: File::Copy, File::Path, Compress::Zlib (PNG生成用)
- **Python**: tweepy (SNS API), sys, os (標準ライブラリ)
- **ImageMagick**: `convert` コマンド (PNG→GIF変換)
- **Cron**: 15分間隔でlgbs.sh実行を想定
