from imp import reload
from fastapi import FastAPI, File, UploadFile
import numpy as np
import tflite_runtime.interpreter as tflite
from PIL import Image
import io
import json


model = tflite.Interpreter("Model/lite/model.tflite")
model.allocate_tensors()

input_details = model.get_input_details()
output_details = model.get_output_details()

classes = {'daisy': 0, 'dandelion': 1, 'rose': 2, 'sunflower': 3, 'tulip': 4}


def get_key(val):
    for key, value in classes.items():
         if val == value:
             return key
 
    return "key doesn't exist"


def prepare_image(img):
    img = Image.open(io.BytesIO(img))
    img = img.resize((128,128))
    img = np.array(img)
    img = np.expand_dims(img, 0)
    img = np.float32(img)
    return img


def predict_result(img):
    model.set_tensor(input_details[0]['index'], img)
    model.invoke()
    output_data = model.get_tensor(output_details[0]['index'])

    argmax = np.argmax(output_data, axis=1)

    return get_key(argmax[0])


# app initioalization
app = FastAPI()


@app.post("/predict")
async def calssify_image(file: UploadFile = File(...)):
    img_bytes = file.file.read()
    img = prepare_image(img_bytes)
    return {"prediction" : predict_result(img)}


@app.get("/data")
async def get_data(prediction: str):
    f = open('API/data.json', encoding="utf-8")
    data = json.load(f)
    data = data[prediction]
    return {"data": data}


@app.get("/")
async def root():
    return {"message": "API is running"}