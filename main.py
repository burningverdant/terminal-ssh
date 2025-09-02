from fastapi import FastAPI, Request
from pydantic import BaseModel
from vllm import LLM, SamplingParams
import uvicorn

# Load Qwen2 model
llm = LLM(model="Qwen/Qwen2-72B", tensor_parallel_size=8)  # Adjust GPU config
sampling_params = SamplingParams(temperature=0.7, max_tokens=512)

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_text(req: PromptRequest):
    # Run inference
    outputs = llm.generate([req.prompt], sampling_params)
    text = outputs[0].outputs[0].text
    return {"output": text}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
