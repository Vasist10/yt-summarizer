import os
from transformers import pipeline
from dotenv import load_dotenv

load_dotenv()

def summarize_with_huggingface(text, chunk_size=1000, overlap=200):
    print("⏳ Loading summarization model from Hugging Face...")

    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise ValueError("❌ Hugging Face token not found. Please set HF_TOKEN in your .env file.")

    summarizer = pipeline(
        "summarization",
        model="facebook/bart-large-cnn",
        tokenizer="facebook/bart-large-cnn",
        token=hf_token  # ✅ Correct way to use token
    )

    summaries = []
    start = 0
    text = text.replace('\n', ' ').strip()

    print("🔄 Splitting text into chunks...")
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]

        try:
            summary = summarizer(chunk, max_length=150, min_length=40, do_sample=False)[0]['summary_text']
            summaries.append(summary)
        except Exception as e:
            print(f"⚠️ Failed to summarize chunk ({start}:{end}): {e}")
        
        start += chunk_size - overlap

    print("🧠 Merging partial summaries into final summary...")
    final_summary_input = " ".join(summaries)

    try:
        final_summary = summarizer(final_summary_input, max_length=300, min_length=100, do_sample=False)[0]['summary_text']
    except Exception as e:
        print(f"⚠️ Final summary failed: {e}")
        final_summary = final_summary_input  # fallback to concatenated summaries

    return final_summary
