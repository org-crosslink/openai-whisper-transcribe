import whisper
import sys
import warnings
import os

# Warningを出力させたいならコメントアウトする
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# デフォルトの作業ディレクトリ（Dockerのマウントポイントと一致）
DEFAULT_WORKDIR = "/app"

# コマンドライン引数の処理
args = sys.argv[1:]

# 文字起こし対象ファイルのパスを取得する
audio_path = next(arg for arg in args if not arg.startswith("-"))

# 入力ファイルを絶対パスに変換（相対パスの場合、自動的に/appを補完）
if not os.path.isabs(audio_path):
    audio_path = os.path.join(DEFAULT_WORKDIR, audio_path)

# turboモデルを読み込み（キャッシュ済み）
model = whisper.load_model("turbo")

# Whisperのテキスト変換の実行
result = model.transcribe(audio_path, temperature=0.5, language="ja", verbose=False)

# 出力をファイルに保存
output_lines = []
for i, segment in enumerate(result['segments']):
    # セグメントの開始時間と終了時間を取得
    start_time = segment['start']
    end_time = segment['end']

    # タイムスタンプ形式の変換
    def format_timestamp(seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02}:{seconds:02}"

    # 空白時間を挿入
    if i > 0:
        previous_end = result['segments'][i - 1]['end']
        # 1秒以上の空白がある場合は無音時間として記録
        if start_time - previous_end > 1.0:  
            output_lines.append(f"{format_timestamp(previous_end)} - {format_timestamp(start_time)}: [無音時間]")

    # セグメント内容を追加
    output_lines.append(f"{format_timestamp(start_time)} - {format_timestamp(end_time)}: {segment['text']}")

# 無音時間の行を除外
filtered_lines = [line for line in output_lines if "[無音時間]" not in line]

# ファイル保存
output_text = "\n".join(filtered_lines)
output_file = "transcription.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(output_text)

print(f"Transcription saved to {output_file}")