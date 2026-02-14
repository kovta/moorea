#!/usr/bin/env python
import torch
from transformers import AutoTokenizer, AutoModel

print("Loading model...")
model = AutoModel.from_pretrained("google/siglip-so400m-patch14-384")
tokenizer = AutoTokenizer.from_pretrained("google/siglip-so400m-patch14-384")
model.eval()

print("Testing text features...")
texts = ['a beautiful dress']
tokens = tokenizer(texts, padding=True, return_tensors="pt")

try:
    with torch.no_grad():
        output = model.get_text_features(**tokens)
    print(f"SUCCESS! Output shape: {output.pooler_output.shape}")
except Exception as e:
    print(f"FAILED! Error: {e}")
    import traceback
    traceback.print_exc()
