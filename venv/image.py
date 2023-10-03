import uvicorn
from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional
from pydantic import BaseModel
import base64
import os
import glob
import pathlib

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory = "templates")
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []

# convert list into tuple
def convert_list_tuple(list):
    return tuple(list)

# Image List Table
headings = ("Image_Name", "Display", "Delete")
data = ()
   

""" upload file and save it to local """ 

@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    
    with open(file.filename, "wb") as f:
        f.write(file.file.read())
    return {"filename": file.filename}

''' create html page to show uploaded file '''
@app.get("/")
async def root():
    html_content = """
    <html>
        <head>
            <title>Upload File</title>
        </head>
        <body>
            <h1>Upload File</h1>
            <form action="/upload-file/" method="post" enctype="multipart/form-data">
                <input type="file" name="file" />
                <input type="submit" />
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/upload_image")
def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
  
@app.post("/upload")
def upload(request: Request, file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        
        with open(file.filename, "wb") as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
        
    base64_encoded_image = base64.b64encode(contents).decode("utf-8")

    return templates.TemplateResponse("display.html", {"request": request,  "myImage": base64_encoded_image})

@app.get("/imagelist")
def main(request: Request):
    path ="static/images"
    files = os.listdir(path)
    imagefiles = []
    
    files_jpg = glob.glob("*.jpg")
    imagefiles = [[i] for i in files_jpg] # convert each element as a independent list
    """
    files_png = glob.glob("*.png")
    for file in files_png:
        imagefiles.append(files_png)
        """
    print(imagefiles)
    imagefiles = convert_list_tuple(imagefiles)
    return templates.TemplateResponse("imagelist.html", {"request": request, "headings": headings, "data": imagefiles})

if __name__ == "__main__":
    uvicorn.run("image:app", host = "0.0.0.0", port = 8000, reload=True)