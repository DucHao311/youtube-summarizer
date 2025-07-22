import whisper
import yt_dlp
import os
import uuid

def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'downloads/{str(uuid.uuid4())}.%(ext)s',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        audio_path = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")
        # return audio_path, f"https://www.youtube.com/watch?v={info['id']}"
        return audio_path, f"https://www.youtube.com/watch?v={info['id']}", info['title']

def transcribe(audio_path, model_size='medium'):   #turbo
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path)

    segments = result["segments"]
    if not segments:
        return []

    # Gom các segment nhỏ thành câu hoàn chỉnh kết thúc bằng dấu chấm "."
    merged_segments = []
    current_text = ""
    start_time = segments[0]["start"]

    for seg in segments:
        current_text += " " + seg["text"].strip()
        if current_text.strip().endswith("."):
            merged_segments.append({
                "start": round(start_time, 2),
                "end": round(seg["end"], 2),
                "text": current_text.strip()
            })
            current_text = ""
            start_time = seg["end"]

    # Thêm đoạn cuối nếu chưa có dấu chấm
    if current_text.strip():
        merged_segments.append({
            "start": round(start_time, 2),
            "end": round(segments[-1]["end"], 2),
            "text": current_text.strip()
        })

    return merged_segments


# def transcribe(audio_path, model_size='medium', max_duration=20.0):   #turbo
#     model = whisper.load_model(model_size)
#     result = model.transcribe(audio_path)

#     segments = [
#         {
#             "start": round(seg["start"], 2),
#             "end": round(seg["end"], 2),
#             "text": seg["text"].strip()
#         } for seg in result["segments"]
#     ]

#     # Gộp các segment thành từng đoạn dài tối đa max_duration giây
#     if not segments:
#         return []

#     merged = []
#     current = {
#         "start": segments[0]["start"],
#         "end": segments[0]["end"],
#         "text": segments[0]["text"]
#     }

#     for seg in segments[1:]:
#         duration = seg["end"] - current["start"]
#         if duration <= max_duration:
#             current["end"] = seg["end"]
#             current["text"] += " " + seg["text"]
#         else:
#             merged.append(current)
#             current = {
#                 "start": seg["start"],
#                 "end": seg["end"],
#                 "text": seg["text"]
#             }

#     merged.append(current)
#     return merged
