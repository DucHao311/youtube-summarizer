# youtube-summarizer

- Tải whisper model: pip install git+https://github.com/openai/whisper.git 

- Requirements
pip install -r requirements.txt

- Cài đặt ffmpeg

- Liên kết model LlaMA3.1 từ HuggingFace

- Tạo thư mục lưu model:

mkdir -p /teamspace/studios/this_studio/models/llama-3.1-8b

- Tải model:

huggingface-cli download meta-llama/Meta-Llama-3.1-8B-Instruct --local-dir /teamspace/studios/this_studio/youtube_summary/llama-3.1-8b
