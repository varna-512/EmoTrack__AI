from fastapi import FastAPI, UploadFile, File

from fastapi.middleware.cors import CORSMiddleware

import shutil

from realtime_predict import predict_emotion


app = FastAPI()


# CORS

app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        "http://localhost:3000"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


@app.get("/")
def home():

    return {
        "message": "Voice Emotion Service Running"
    }


@app.post("/predict")
async def predict_audio(

    audio: UploadFile = File(...)
):

    file_path = "temp_audio.wav"


    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(

            audio.file,

            buffer
        )


    result = predict_emotion(
        file_path
    )

    return result