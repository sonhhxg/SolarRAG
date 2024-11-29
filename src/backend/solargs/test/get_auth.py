# from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
# from datetime import date
# SECRET_KEY = str(date.today())
# jwt = Serializer(secret_key=SECRET_KEY)
# access_token = "dd5b41e6ab0311ef9fc10242ac120006"
# print(jwt.dumps(str(access_token)))
# import base64
#
# def base64_encode(text):
#     return base64.b64encode(text.encode()).decode()
#
#
# print(base64_encode("testertyuio"))
#
# from Crypto.Random import get_random_bytes
#
# aes_key = get_random_bytes(16)
# print(aes_key)
# import uvicorn
# from typing import Annotated
#
# from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import HTMLResponse
#
# app = FastAPI()
#
#
# @app.post("/files/")
# async def create_files(
#     files: Annotated[list[bytes], File(description="Multiple files as bytes")],
# ):
#     return {"file_sizes": [len(file) for file in files]}
#
#
# @app.post("/uploadfiles/")
# async def create_upload_files(
#     files: Annotated[
#         list[UploadFile], File(description="Multiple files as UploadFile")
#     ],
# ):
#     return {"filenames": [file.filename for file in files]}
#
#
# @app.get("/")
# async def main():
#     content = """
# <body>
# <form action="/files/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# </body>
#     """
#     return HTMLResponse(content=content)
#
# if __name__=='__main__':
#     uvicorn.run("get_auth:app", host="0.0.0.0", port=2234, reload=False, workers=1)

# fnm = r"C:\Users\Sikh0\Desktop\data\制度-word\3.txt"
# from PIL import Image
# img = Image.open(fnm)
# from io import BytesIO
# # buff = BytesIO()
# # buff.getvalue()
# BytesIO(binary)
# # img.save(buff, format='JPEG')
# # print(conn.put("test", "11-408.jpg", buff.getvalue()))
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
app = FastAPI()

@app.get("/download")
def download_file():
    file_path = r"C:\Users\Sikh0\Desktop\data\制度-word\6.txt"
    return FileResponse(file_path, media_type='application/octet-stream', filename="6.txt")

if __name__=='__main__':
    uvicorn.run("get_auth:app", host="0.0.0.0", port=2213, reload=False, workers=1)
