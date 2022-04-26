from fastapi import FastAPI, Request, File, Form, UploadFile, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
import os
import shutil
import json

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/")
async def index(request: Request, file: UploadFile = File(...)):
    with open(f'{file.filename}', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    with open(file.filename, 'rb') as f:
        pred = requests.post('http://127.0.0.1:5000/predict', files={"file": f})

    data = requests.get('http://127.0.0.1:5000/data', params={"prediction": pred.json()['prediction']})

    data = data.json()['data']

    os.remove(file.filename)

    return templates.TemplateResponse("response.html", {"request": request, "prediction": data['name'], 
                        "description": data['text'], "preview": data['preview'],
                        "link": data['url']})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/faq", response_class=HTMLResponse)
async def faq(request: Request):
    return templates.TemplateResponse("FAQ.html", {"request": request})
