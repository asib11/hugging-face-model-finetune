from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter()


MODEL_PATH = Path(__file__).resolve().parents[1] / "AIModels" / "llama"

# part 1: tokenizer and model loading text --> input token --> model --> output token --> text

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    device_map="auto", 
    dtype=torch.float16
)

#part 2: return schema

class ChatRequest(BaseModel):
    prompt: str

@router.post("/chat-llama")
def chat(request: ChatRequest):

    #Porcess input messages
    messages = [{"role": "user", "content": request.prompt}]

    #input message -- input token
    input_token = tokenizer.apply_chat_template(
        messages, 
        add_special_tokens=True,
        return_dict=True, 
        return_tensors="pt"
    ).to(model.device)

    output_token = model.generate(**input_token, max_new_tokens=128)

    result = tokenizer.decode(output_token[0][input_token["input_ids"].shape[1]:], skip_special_tokens=True)

    return {"content": result}