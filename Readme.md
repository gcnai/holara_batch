# Holaraで一括ダウンロードできないのを何とかするスクリプト

## 使い方

1. F12 を押してデベロッパーコンソールを開いてNetworkタブを出しっぱなしにする。
2. 画像を生成する。
3. "Save all as HAR with content"でHAR形式で保存する。
4. HARファイルをmain.pyにぶちこむ。

## できること

Networkタブを開いた状態で生成した画像をローカルに吐き出す。その際にpromptなど情報をPNGのメタデータに組み込む。

## 動作環境

- 動いた: vivaldi
- 多分動く: Chrome
- 動かない: Firefox
  - jsonのテキストの最大長が1Mしかない

## Usage

```shell
python main.py holara.ai.har
```
