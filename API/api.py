from fastapi import FastAPI, File, UploadFile
import numpy as np
import tensorflow as tf
from PIL import Image
import io
import uvicorn
import json

model = tf.keras.models.load_model('petal')

classes = {'daisy': 0, 'dandelion': 1, 'rose': 2, 'sunflower': 3, 'tulip': 4}


def get_key(val):
    for key, value in classes.items():
         if val == value:
             return key
 
    return "key doesn't exist"


def prepare_image(img):
    img = Image.open(io.BytesIO(img))
    img = img.resize((224, 224))
    img = np.array(img)
    img = np.expand_dims(img, 0)
    return img


def predict_result(img):
    pred = model.predict(img)
    val = np.argmax(pred, axis=1, keepdims=True)[0][0]

    return get_key(val)


app = FastAPI()


@app.post("/predict")
async def calssify_image(file: UploadFile = File(...)):
    img_bytes = file.file.read()
    img = prepare_image(img_bytes)
    return {"prediction" : predict_result(img)}

@app.get("/data")
async def get_data(prediction: str):
    f = open('data.json', encoding="utf-8")
    data = json.load(f)
    data = data[prediction]
    return {"data": data}


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)