"""Add recorded chapter captions to the real browser video (requires FFmpeg on PATH)."""

import json
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
output = root / "data/runs/demo"
recording = json.loads((output / "recording.json").read_text(encoding="utf-8"))


def timestamp(seconds):
    ticks = round(seconds * 100)
    return f"{ticks // 360000}:{ticks // 6000 % 60:02}:{ticks // 100 % 60:02}.{ticks % 100:02}"


captions = """[Script Info]
ScriptType: v4.00+
PlayResX: 1440
PlayResY: 1000

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Microsoft YaHei,26,&H00FFFFFF,&H00FFFFFF,&H001A170B,&H001A170B,0,0,0,0,100,100,0,0,1,0,0,2,24,24,12,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
chapters = recording["chapters"]
for index, chapter in enumerate(chapters):
    start = 0 if index == 0 else chapter["start"]
    stop = chapters[index + 1]["start"] if index + 1 < len(chapters) else 180
    text = chapter["text"].replace("\n", r"\N")
    captions += f"Dialogue: 0,{timestamp(start)},{timestamp(stop)},Default,,0,0,0,,{text}\n"
(output / "captions.ass").write_text(captions, encoding="utf-8")
subprocess.run(
    [
        "ffmpeg", "-y", "-i", recording["video"],
        "-vf", "pad=iw:1000:0:0:color=0x0B171A,subtitles=data/runs/demo/captions.ass,tpad=stop_mode=clone:stop_duration=1",
        "-t", "180", "-r", "15", "-c:v", "libx264", "-crf", "23",
        "-preset", "fast", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        str(output / "battery-copilot-demo.mp4"),
    ],
    cwd=root, check=True,
)
