# openai-whisper
## 概要
OpenAIのWhisperモデルを使用して音声ファイルを文字起こしするDocker環境を構築します。

## 必要な環境/ファイル
- Docker（メモリ6GB割り当て）
- ffmpeg（Docker内にインストールされるため、ローカルには不要）
- 録音データ（webm, wav）

## 使い方
以下でdockerイメージをビルドして、録音データを入力させる。
処理後に音声データを文字起こししたファイル「transcription.txt」が生成される。

```
$ docker build -t openai-whisper-transcribe .
$ docker run --rm -v $(pwd):/app openai-whisper-transcribe /app/録音データ.webm
```

## 備考
- modelはデフォルトのsmall以上を推奨ですが、実行環境によっては時間がかかりすぎる場合があるのでその場合は以下を参照して調整してください
- コンテナ割り当てメモリが6GBを確保できない場合は、modelを変更してください（mediumなら5GB, それ以下なら2GBのメモリ割り当てが必要です）
- 処理時間がかかりすぎる場合はmodelの変更を検討してください
