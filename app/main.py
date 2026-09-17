from __future__ import annotations

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from .content import generate_content
from .models import PublishJob
from .platforms import PLATFORMS
from .render import render_video
from .trends import discover_trends


class GenerateRequest(BaseModel):
    trend_index: int = Field(default=0, ge=0, le=29)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="AutoPost AI", version="0.1.0", lifespan=lifespan)


@app.get("/", response_class=HTMLResponse)
async def dashboard():
    return HTMLResponse('''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AutoPost AI</title><style>body{font-family:Inter,system-ui,sans-serif;max-width:1100px;margin:40px auto;padding:0 20px;background:#0b1020;color:#eef2ff}button{padding:12px 16px;border:0;border-radius:10px;background:#7c3aed;color:white;cursor:pointer}.card{background:#141b31;padding:18px;border-radius:14px;margin:14px 0}small{color:#9ca3af}pre{white-space:pre-wrap}</style></head><body><h1>AutoPost AI</h1><p>Trend discovery → AI script → short-video render → platform queue.</p><button onclick="loadTrends()">Find trending topics</button><div id="app"></div><script>async function loadTrends(){const r=await fetch('/api/trends');const d=await r.json();document.getElementById('app').innerHTML=d.map((x,i)=>`<div class=card><b>${i+1}. ${x.title}</b><br><small>${x.source} · score ${x.score}</small><br><br><button onclick="generate(${i})">Generate short</button></div>`).join('')}async function generate(i){const r=await fetch('/api/generate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({trend_index:i})});const d=await r.json();document.getElementById('app').innerHTML='<div class=card><h2>'+d.content.title+'</h2><p><b>Hook:</b> '+d.content.hook+'</p><pre>'+d.content.script+'</pre><p>'+d.content.hashtags.join(' ')+'</p><small>Render: '+d.video_path+'</small><p>Publishing remains approval-gated in this MVP.</p></div>'}</script></body></html>''')


@app.get("/api/trends")
async def trends():
    items = await discover_trends()
    return [item.__dict__ for item in items]


@app.post("/api/generate")
async def generate(request: GenerateRequest):
    items = await discover_trends()
    if request.trend_index >= len(items):
        raise HTTPException(status_code=404, detail="Trend not available")
    trend = items[request.trend_index]
    content = await generate_content(trend.title, trend.source_url)
    video_path = render_video(content)
    return {"trend": trend.__dict__, "content": content.__dict__, "video_path": video_path}


@app.get("/api/platforms")
async def platforms():
    return {name: {"status": "adapter-ready"} for name in PLATFORMS}


@app.post("/api/queue/{platform}")
async def queue(platform: str):
    if platform not in PLATFORMS:
        raise HTTPException(status_code=404, detail="Unsupported platform")
    job = PublishJob(content_id="latest", platform=platform)
    return job.__dict__
