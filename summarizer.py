# summarizer.py
from typing import List, Dict
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Load ViT5 summarization model từ VietAI
MODEL_ID = "VietAI/vit5-base-vietnews-summarization"
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID)

def summarize_segments(segments: List[Dict[str, str]]) -> str:
    text = " ".join([seg["text"] for seg in segments])
    input_text = "summarize: " + text
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(
        inputs,
        max_length=256,
        min_length=30,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary