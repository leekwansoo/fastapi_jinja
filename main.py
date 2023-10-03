import uvicorn
from fastapi import FastAPI, File, UploadFile, Request, Form, Depends, Header
from fastapi.templating import Jinja2Templates
import base64
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, Response, StreamingResponse
from fastapi.concurrency import run_in_threadpool
from schemas import AwesomeForm
from models.firebase_db import store_userdata, store_imagedata
from models.firebase_storage import storeimage
import os

from pathlib import Path
import glob
from io import BytesIO

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# convert list into tuple
def convert_list_tuple(list):
    return tuple(list)

CHUNK_SIZE = 1024*1024

# Image List Table
headings = ("Image_Name", "Display", "Delete")
data = () 

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request} )

@app.get("/getimage")
def list_file(request: Request):

    files = os.listdir("static/images")


    return templates.TemplateResponse("list_image.html", {"request": request, "files":files})

app.get("/imagelist")
def main(request: Request):
    imagefiles = ("24_09.jpg", "28_18.jpg")
    for file in glob.glob(".jpg"):
        imagefiles.append(file)
    for file in glob.glob(".png"):
        imagefiles.append(file)
    return templates.TemplateResponse("imagelist.html", {"request": request, "headings": headings, "data": imagefiles})


@app.get("/getimage/{id}")
async def read_files(request: Request, id: str, q: str | None = None):
    print(id)
    file_type= id.split(".")[1]
    print(file_type)
    file_path = Path("static/images/" + id)    
    with open(file_path, "rb") as contents:
       
        if  file_type == "jpg":
            base64_encoded_image = contents
            return templates.TemplateResponse("display_image.html", {"request": request,  "myImage": base64_encoded_image})
            #base64_encoded_image = base64.b64encode(contents).decode("utf-8")
            #return templates.TemplateResponse("display_image.html", {"request": request,  "myImage": base64_encoded_image})
        else:
            print(file_type)
            return templates.TemplateResponse("display_video.html", {"request": request,  "myImage": file_path})

@app.get("/getvideo")
def list_file(request: Request):

    files = os.listdir("static/videos")
    file_path = files[0]

    return templates.TemplateResponse("list_video.html", {"request": request, "files":files, "myImage": file_path})

@app.get("/getvideo/{id}")
async def read_files(request: Request, id: str, q: str | None = None):
    file_type= id.split(".")[1]
    mediatype ='video/'+ file_type
    print(mediatype)
    file_path = Path("static/videos/" + id)

    return FileResponse(file_path)

@app.get("/videolist")
def main(request: Request):
    path ="static/videos"
    files = os.listdir(path)
    
    print(files)
    files = convert_list_tuple(files)
    return templates.TemplateResponse("videolist.html", {"request": request, "headings": headings, "data": files}) 

@app.get("/video")
async def video_endpoint():
    video_path = Path("static/videos/images01.mp4")
    return FileResponse(video_path)

@app.get("/upload")
def main(request: Request):
    print("ok")
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/upload")
def upload(request: Request, file: UploadFile = File(...)):
    try:
        #location = storeimage(file_path)
        file_name = file.filename
        file_type = file_name.split(".")[1]
        
        contents = file.file.read()
        file_path = f'static/images' + file.filename
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
        #location = storeimage(file_path)
    #base64_encoded_image = base64.b64encode(contents).decode("utf-8")

    if  file_type == "jpg":
        base64_encoded_image = base64.b64encode(contents).decode("utf-8")
        location ="file_path"
        store_imagedata(file_name, location)
        return templates.TemplateResponse("display_image.html", {"request": request,  "myImage": base64_encoded_image})

    else:
        print(file_type)
        return templates.TemplateResponse("display_video.html", {"request": request,  "myImage": file_path})

@app.get('/basic', response_class=HTMLResponse)
def get_basic_from(request: Request):
    return templates.TemplateResponse("basic_form.html", {"request": request})

@app.post('/basic', response_class=HTMLResponse)
def post_basic_from(request: Request, username: str = Form(...), password: str = Form(...), file: UploadFile = File(...)):
    print(f'username: {username}')
    print(f'password: {password}')
    print(file)
    return templates.TemplateResponse("basic_form.html", {"request": request})

@app.get('/awesome', response_class=HTMLResponse)
def get_from(request: Request):
    return templates.TemplateResponse("awesome_form.html", {"request": request})

@app.post('/awesome', response_class=HTMLResponse)
def post_from(request: Request, form_data: AwesomeForm = Depends(AwesomeForm.as_form)):
    print(form_data)
    return templates.TemplateResponse("awesome_form.html", {"request": request})


@app.get("/items/{id}", response_class= HTMLResponse)
async def read_items(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})

 


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port = 8000, reload=True)