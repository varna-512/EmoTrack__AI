import requests


FACE_SERVICE_URL = (
    "http://127.0.0.1:8002/predict"
)


def get_face_prediction(image_file):

    try:

        files = {

            "image": (

                image_file.name,

                image_file,

                "image/jpeg"
            )
        }

        response = requests.post(

            FACE_SERVICE_URL,

            files=files
        )
       
        print("FACE STATUS:", response.status_code)
        print("FACE RESPONSE:", response.text)



        return response.json()

    except Exception as e:

        return {

            "error": str(e)
        }
    