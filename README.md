# openai-whisper
## 概要
OpenAIのWhisperモデルを使用して音声ファイルを文字起こしするDocker環境を構築します。

## 必要な環境/ファイル
- Docker
- ffmpeg（Docker内にインストールされるため、ローカルには不要）
- 録音データ（webm, wav）

## 使い方
以下でdockerイメージをビルドして、録音データを入力させる。
処理後に音声データを文字起こししたファイル「transcription.txt」が生成される。

```
$ docker build -t openai-whisper-transcribe .
$ docker run --rm -v $(pwd):/app openai-whisper-transcribe /app/録音データ.webm
$ ls transcription.txt
```

## 備考
- modelはデフォルトのsmall以上を推奨ですが、実行環境によっては時間がかかりすぎる場合があるのでその場合は以下を参照して調整してください
- 処理時間がかかりすぎる場合は以下を検討してください
    - modelを変更する
        - tiny、base、small、medium、large の順で高精度ですが、必要になる計算リソースも多くなるので時間もかかります
    - 話者分離版(speaker_separated)を使わない
        - 話者分離版は重いのでこれを無効にすることで大幅に速度改善が期待できます
- 処理が完了したのに文字起こしがされない場合は指定modelと実行環境のメモリ量を確認してください
    - base > コンテナメモリ割り当て2GB
    - small > コンテナメモリ割り当て4GB
    - medium > コンテナメモリ割り当て6GB
