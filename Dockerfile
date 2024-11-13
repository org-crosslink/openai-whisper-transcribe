# ベースイメージとしてPython 3.8を使用
FROM python:3.8-slim

# 必要なライブラリをインストール
RUN apt-get update && \
    apt-get install -y ffmpeg git libffi-dev && \
    rm -rf /var/lib/apt/lists/*

# Whisperと依存ライブラリをインストール
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir git+https://github.com/openai/whisper.git

# turboモデルをキャッシュに保存
RUN python -c "import whisper; whisper.load_model('turbo')"

# 作業ディレクトリの設定
WORKDIR /app

# Whisperスクリプトを追加
COPY transcribe.py /app/transcribe.py

# エントリポイントの設定
ENTRYPOINT ["python", "/app/transcribe.py"]