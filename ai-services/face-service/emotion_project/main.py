from fastapi import FastAPI, UploadFile, File

from fastapi.middleware.cors import CORSMiddleware

import shutil

from predict import predict_face_emotion


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
        "message": "Face Emotion Service Running"
    }


@app.post("/predict")
async def predict_image(

    image: UploadFile = File(...)
):

    file_path = "temp_face.jpg"


    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(

            image.file,

            buffer
        )


    result = predict_face_emotion(
        file_path
    )

    return result