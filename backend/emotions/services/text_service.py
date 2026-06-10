import requests

TEXT_SERVICE_URL = (
    "http://127.0.0.1:8003/predict"
)


def get_text_prediction(text):

    try:

        response = requests.post(

            TEXT_SERVICE_URL,

            json={
                "text": text
            }
        )

        print("TEXT STATUS:", response.status_code)
        print("TEXT RESPONSE:", response.text)

        return response.json()

    except Exception as e:

        return {

            "error": str(e)
        }