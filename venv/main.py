import uvicorn
from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional
from pydantic import BaseModel
import os
app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

headings = ("Name", "Role", "Salary")
data = (
    ("Rolf", "Software Engineer", "$48,000.00"),
    ("Smith", "Mechanical Engineer", "$44,000.00"),
    ("Bob", "Hardware Engineer", "$42,000.00"),
)

tasks = ['task 1', 'task 2', 'task 3']

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/videolist', response_class=HTMLResponse)
def list_file(request: Request):

    files = os.listdir("static/videos")
    file_path = files[0]

    return templates.TemplateResponse("list_video.html", {"request": request, "files":files, "myImage": file_path})

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    print(id)
    return templates.TemplateResponse("item.html", {"request": request, "id": id})

@app.get("/form")
def form(request: Request):
    result = ""
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})

@app.post("/form")
def form(request: Request, text: str=Form(...)):
    
    result = ['Hello', 'Hi', 'Bye'] # to simplify the example
    return templates.TemplateResponse('form.html', context={'request': request, 'result': tuple(result)})

@app.get("/uploadimage")
def form(request: Request):
    result = ""
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})

@app.post("/uploadimage")
def form(request: Request, text: str=Form(...)):
    
    result = ['Hello', 'Hi', 'Bye'] # to simplify the example
    return templates.TemplateResponse('form.html', context={'request': request, 'result': tuple(result)})


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request})

@app.get("/")
def table(request: Request):
    result = {"headings":headings, "data": data}
    print(result)
    return templates.TemplateResponse("table.html", {"request": request, "headings": headings, "data": data})
   
if __name__ == "__main__":
    uvicorn.run("main:app", host = "0.0.0.0", port = 8000, reload=True)