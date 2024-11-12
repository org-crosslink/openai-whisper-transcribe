import whisper
import sys
import os

# smallモデルを読み込み
model = whisper.load_model("small")

# 音声ファイルのパス
audio_path = sys.argv[1]

# Whisperのテキスト変換の実行
result = model.transcribe(audio_path, temperature=0.5, language="ja", verbose=True)

# 出力をファイルに保存
output_text = "\n".join([segment['text'] for segment in result['segments']])
output_file = "transcription.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(output_text)

print(f"Transcription saved to {output_file}")