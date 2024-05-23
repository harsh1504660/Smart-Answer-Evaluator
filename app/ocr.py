import requests
def ocr(img):
    url = "https://pen-to-print-handwriting-ocr.p.rapidapi.com/recognize/"

    # Open the image file
    with open(img, 'rb') as file:
        # Read the image file
        image_data = file.read()

    files = {'srcImg': ('img1.png', image_data)}

    payload = {"Session": "string"}
    headers = {
        "X-RapidAPI-Key": "6f9fd15d23mshc49f619a31d5fbbp19cd9djsnf3b0da3417d9",
        "X-RapidAPI-Host": "pen-to-print-handwriting-ocr.p.rapidapi.com"
    }

    response = requests.post(url, data=payload, files=files, headers=headers)

    return response.json()['value']

"""res = ocr('uploads\studentimage.jpg')
print('RAW')
print(res)
print('PROCESSED')
print(prep(res))"""