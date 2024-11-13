import whisper
import sys
import warnings

# Warningを出力させたいならコメントアウトする
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# コマンドライン引数の処理
args = sys.argv[1:]

# -t オプションが指定されたか確認し、文字起こし対象ファイルのパスを取得する
add_timestamp = "-t" in args
audio_path = next(arg for arg in args if not arg.startswith("-"))

# turboモデルを読み込み（キャッシュ済み）
model = whisper.load_model("turbo")

# Whisperのテキスト変換の実行
result = model.transcribe(audio_path, temperature=0.5, language="ja", verbose=False)

# 出力をファイルに保存
output_lines = []
for segment in result['segments']:
    if add_timestamp:
        # 各セグメントの開始時間を mm:ss 形式に変換
        minutes = int(segment['start'] // 60)
        seconds = int(segment['start'] % 60)
        timestamp = f"{minutes:02}:{seconds:02}"
        output_lines.append(f"{timestamp} {segment['text']}")
    else:
        # 時間情報を追加しない場合
        output_lines.append(segment['text'])

# すべての行を一つのテキストに結合してファイルに保存
output_text = "\n".join(output_lines)
output_file = "transcription.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(output_text)

print(f"Transcription saved to {output_file}")
