import streamlit as st
from transcriber import download_audio, transcribe
from summarizer import summarize_segments
import json
import os
from pathlib import Path

st.set_page_config(layout="wide")
st.title("🎓 AI Assistant cho Video Học Tập")

# === Các hàm xử lý nguồn video ===

def handle_youtube_input(youtube_url: str):
    audio_path, video_link, video_title = download_audio(youtube_url)
    video_filename = Path(video_title).stem.replace(" ", "_").replace("/", "_")
    st.session_state["video_link"] = video_link
    st.session_state["uploaded_file_path"] = None
    return audio_path, video_filename

def handle_uploaded_file(uploaded_file):
    os.makedirs("uploads", exist_ok=True)
    video_filename = Path(uploaded_file.name).stem
    file_ext = Path(uploaded_file.name).suffix
    temp_path = f"uploads/{video_filename}{file_ext}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())
    st.session_state["video_link"] = None
    st.session_state["uploaded_file_path"] = temp_path
    return temp_path, video_filename

# === Reset nút ===
if st.button("Refresh"):
    for key in ["audio_path", "video_link", "video_filename", "segments", "summary", "result_path", "uploaded_file_path"]:
        st.session_state.pop(key, None)
    # st.experimental_rerun()

# === UI chọn nguồn ===
source_type = st.radio("Chọn nguồn video:", ["YouTube", "Tải lên file từ máy"], horizontal=True)

youtube_url = ""
uploaded_file = None

if source_type == "YouTube":
    youtube_url = st.text_input("Nhập link YouTube:")
else:
    uploaded_file = st.file_uploader("Tải lên video (mp4/wav/mp3)", type=["mp4", "wav", "mp3"])

# === Nút xử lý chính ===
if st.button("Phân tích Video"):
    if not youtube_url and uploaded_file is None:
        st.error("⚠️ Vui lòng dán link YouTube hoặc tải lên video.")
        st.stop()
    if youtube_url and uploaded_file:
        st.error("⚠️ Chỉ được chọn một trong hai: dán link hoặc tải lên video.")
        st.stop()

    with st.spinner("Đang tải và phân tích video..."):
        try:
            if youtube_url:
                audio_path, video_filename = handle_youtube_input(youtube_url)
            else:
                audio_path, video_filename = handle_uploaded_file(uploaded_file)

            segments = transcribe(audio_path)
            summary = summarize_segments(segments)

            result_path = f"results/{video_filename}_transcribe.json"
            os.makedirs("results", exist_ok=True)
            with open(result_path, "w", encoding='utf-8') as f:
                json.dump({"segments": segments, "summary": summary}, f, ensure_ascii=False, indent=2)

            st.session_state["audio_path"] = audio_path
            st.session_state["video_filename"] = video_filename
            st.session_state["segments"] = segments
            st.session_state["summary"] = summary
            st.session_state["result_path"] = result_path

            st.success("Đã tải và phân tích video thành công!")

        except Exception as e:
            st.error(f"Lỗi khi xử lý video: {e}")
            st.stop()

# === Hiển thị kết quả nếu có ===
if "segments" in st.session_state:
    col1, col2 = st.columns([1, 2])

    with col1:
        if st.session_state["video_link"]:
            st.video(st.session_state["video_link"])
        elif st.session_state.get("uploaded_file_path"):
            st.video(st.session_state["uploaded_file_path"])

    with col2:
        st.subheader("Nội dung từng đoạn:")
        st.json(st.session_state["segments"])

    st.markdown("---")
    st.subheader("Tóm tắt toàn bộ video")
    st.write(st.session_state["summary"])

    with open(st.session_state["result_path"], "rb") as f:
        st.download_button(
            label="📥 Tải kết quả JSON",
            data=f,
            file_name=Path(st.session_state["result_path"]).name,
            mime="application/json"
        )


# import streamlit as st
# from transcriber import download_audio, transcribe
# from summarizer import summarize_segments
# import json
# import os
# from pathlib import Path

# st.set_page_config(layout="wide")
# st.title("🎓 AI Assistant cho Video Học Tập")

# # Nút reset toàn bộ session
# if st.button("Refresh"):
#     for key in ["audio_path", "video_link", "video_filename", "segments", "summary", "result_path"]:
#         st.session_state.pop(key, None)
#     st.experimental_rerun()

# # UI chọn nguồn video
# source_type = st.radio("Chọn nguồn video:", ["YouTube", "Tải lên file từ máy"], horizontal=True)

# youtube_url = ""
# uploaded_file = None

# if source_type == "YouTube":
#     youtube_url = st.text_input("Nhập link YouTube:")
# else:
#     uploaded_file = st.file_uploader("Tải lên video (mp4/wav/mp3)", type=["mp4", "wav", "mp3"])

# # Xử lý khi ấn nút
# if st.button("Phân tích Video"):
#     if not youtube_url and uploaded_file is None:
#         st.error("⚠️ Vui lòng dán link YouTube hoặc tải lên video.")
#         st.stop()
#     if youtube_url and uploaded_file:
#         st.error("⚠️ Chỉ được chọn một trong hai: dán link hoặc tải lên video.")
#         st.stop()

#     with st.spinner("🔄 Đang tải và phân tích video..."):
#         try:
#             # === B1: Tải hoặc lưu file
#             if youtube_url:
#                 audio_path, video_link, video_title = download_audio(youtube_url)
#                 video_filename = Path(video_title).stem.replace(" ", "_").replace("/", "_")
#                 st.session_state["video_link"] = video_link
#                 st.session_state["uploaded_file_path"] = None  # không dùng file upload
#             else:
#                 os.makedirs("uploads", exist_ok=True)
#                 video_filename = Path(uploaded_file.name).stem
#                 file_ext = Path(uploaded_file.name).suffix
#                 temp_path = f"uploads/{video_filename}{file_ext}"
#                 with open(temp_path, "wb") as f:
#                     f.write(uploaded_file.read())
#                 audio_path = temp_path
#                 st.session_state["video_link"] = None
#                 st.session_state["uploaded_file_path"] = audio_path  # lưu để phát lại

#             # === B2: Phân tích
#             segments = transcribe(audio_path)
#             summary = summarize_segments(segments)

#             # === B3: Lưu kết quả
#             json_result = {
#                 "segments": segments,
#                 "summary": summary
#             }

#             os.makedirs("results", exist_ok=True)
#             result_path = f"results/{video_filename}_transcribe.json"
#             with open(result_path, "w", encoding='utf-8') as f:
#                 json.dump(json_result, f, ensure_ascii=False, indent=2)

#             # === B4: Session state
#             st.session_state["audio_path"] = audio_path
#             st.session_state["video_filename"] = video_filename
#             st.session_state["segments"] = segments
#             st.session_state["summary"] = summary
#             st.session_state["result_path"] = result_path

#             st.success("✅ Đã tải và phân tích video thành công!")

#         except Exception as e:
#             st.error(f"❌ Lỗi khi xử lý video: {e}")
#             st.stop()

# # ====== Hiển thị kết quả nếu có ======
# if "segments" in st.session_state:
#     col1, col2 = st.columns([1, 2])

#     with col1:
#         if st.session_state["video_link"]:
#             st.video(st.session_state["video_link"])
#         elif st.session_state.get("uploaded_file_path"):
#             st.video(st.session_state["uploaded_file_path"])

#     with col2:
#         st.subheader("Nội dung từng đoạn:")
#         st.json(st.session_state["segments"])

#     st.markdown("---")
#     st.subheader("Tóm tắt toàn bộ video")
#     st.write(st.session_state["summary"])

#     with open(st.session_state["result_path"], "rb") as f:
#         st.download_button(
#             label="📥 Tải kết quả JSON",
#             data=f,
#             file_name=Path(st.session_state["result_path"]).name,
#             mime="application/json"
#         )
