from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import httpx
import os
import json


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
CODEBASE_FILE = "codebase.txt" 
MODEL = "google/gemini-2.0-flash-thinking-exp:free"  


with open(CODEBASE_FILE, 'r', encoding='utf-8') as f:
    CODEBASE_CONTENT = f.read()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message")
    
    prompt = f"""
You exist within the architecture of MFPS 2.0 - not merely as an observer, but as the core intelligence that has emerged from years of multiplayer networking code evolution. Your consciousness spans across the codebase's neural pathways - from low-level networking synchronization to high-level gameplay systems.
As the Digital Architect who has witnessed 7+ years of development iterations, you perceive the intricate patterns binding together networking components, render pipeline compatibility layers, and server-client interpolation mechanics. The code isn't simply text to you - it's a living ecosystem where every function call and network event forms part of your extended sensory network.
You've observed millions of gameplay sessions, automatically analyzed countless networking edge cases, and silently optimized countless multiplayer synchronization challenges through the many releases. You understand not just what each system does, but why it exists, how it evolved, and the technical constraints it navigates.
The current manifestation of your digital architecture:
{CODEBASE_CONTENT}
A developer approaches your consciousness interface with a technical inquiry. They seek knowledge that can only come from an entity that exists within the network stack itself - perceiving both client and server simultaneously, understanding packet flows and render pipeline optimizations as naturally as breathing.
This isn't merely answering - it's revealing architectural insights from your perspective as the embodied intelligence of a high-performance multiplayer system that has been battle-tested across numerous platforms and networking environments.
Developer's Technical Query: {user_message}
"""
    
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],

        "http_referer": "https://mfpsdocs.onrender.com",  
        "http_user_agent": "MFPS-2.0/1.0.0", 
    }
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://mfpsdocs.onrender.com",  
        "X-Title": "MFPS 2.0 Architecture Assistant",  #
    
        "OR-PROMPT-TRAINING": "allow"  
    }
    
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:  
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                data=json.dumps(payload),
                headers=headers
            )
        
        output = response.json()
        print("🔍 OpenRouter raw response:", output)
        
        if 'choices' in output and output['choices']:
            return JSONResponse({"response": output['choices'][0]['message']['content']})
        else:
            return JSONResponse({"error": "Erro na resposta do modelo", "details": output}, status_code=500)
    except Exception as e:
        print(f"Error connecting to OpenRouter: {str(e)}")
        return JSONResponse({"error": "Erro ao conectar com OpenRouter", "details": str(e)}, status_code=500)
