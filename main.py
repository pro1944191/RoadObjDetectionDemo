from typing import List
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException, File, UploadFile, Body, Request, WebSocket, WebSocketDisconnect
from models import Gender, Role, User
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from predictionModel import YoloModel
import json
from websockets.exceptions import ConnectionClosed
import asyncio
import cv2

# Create instance of the application
app = FastAPI(title="YOLOv8 Traffic Detection")
camera = cv2.VideoCapture("./web/img/video_dataset_completo.mp4")
yolo = YoloModel()
# Example JSON database file
DATABASE_FILE = "data.json"

# Example database list for user database -> Is a list of Users
#id=uuid4(
db: List[User] = [
    User(id=uuid4(), first_name="Francesco", last_name="Pro", gender=Gender.male, roles=[Role.admin,Role.user]),
    User(id=uuid4(), first_name="Alice", last_name="Fiorentini", gender=Gender.female, roles=[Role.user])
]

app.mount('/web', StaticFiles(directory='web', html=True), name='web')

# Define a Pydantic model for your data
class Item(BaseModel):
    channel: str
    description: str = None

# -------- ASGI ------------#
# Sometimes we need asynchronous computation
# @app.get("/route")
# async def root():
#   result = await function_to_call()
#   return result
# -------- ASGI ------------#

# Create an index route
@app.get("/", response_class=HTMLResponse)
def index():
    #return {"result": "Hello 🔥 APP2"}
    with open("./web/index.html") as file:
    #with open("./web/sock.html") as file:
    
        #return file.read()
        return HTMLResponse(content=file.read(), status_code=200)

# Take the uploaded file to detect
@app.post("/upload_image")
def upload(file: UploadFile = File(...)):
    #return {"message": f"Successfuly uploaded "}
    imagePath = "./web/img/" + file.filename

    try:
        contents = file.file.read()
        with open("./web/img/" + file.filename, "wb") as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    
    if file.content_type.split("/")[0] == "image":
        yolo.predict(imagePath)
    #elif file.content_type.split("/")[0] == "video":
        #yolo.predictVideo(imagePath)


    return JSONResponse({"message": f"Successfuly uploaded {file.filename}"})

@app.get("/show_prediction", response_class=HTMLResponse)
async def show_prediction():
    with open("./web/result.html") as file:
        #return file.read()
        return HTMLResponse(content=file.read(), status_code=200)

@app.get("/show_predictionVideo", response_class=HTMLResponse)
async def show_predictionVideo():
    with open("./web/resultVideo.html") as file:
        #return file.read()
        return HTMLResponse(content=file.read(), status_code=200)

@app.websocket("/ws")
async def get_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                frame_bb = yolo.predictVideoLive(frame)
                ret, buffer = cv2.imencode('.jpg', frame)
                await websocket.send_text("some text")
                await websocket.send_bytes(buffer.tobytes())
            #await asyncio.sleep(0.03)
    except (WebSocketDisconnect, ConnectionClosed):
        print("Client disconnected")
"""
# Create a route to visualize all users 
@app.get("/api/v1/users")
async def fetch_users():
    return db

# Create a route to insert a user
@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"user_id":user.id}
"""


"""    
# Create a route to read items
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    items = read_data_from_db()
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

# Create a route to create items
@app.post("/items/")
async def create_item(item: Item):
    items = read_data_from_db()
    items.append(item.model_dump())
    write_data_to_db(items)
    return item

# Helper function to read data from the JSON database
def read_data_from_db():
    try:
        with open(DATABASE_FILE, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    return data

# Helper function to write data to the JSON database
def write_data_to_db(data):
    with open(DATABASE_FILE, "w") as file:
        json.dump(data, file, indent=2)

# Run the application with uvicorn
# Example: uvicorn main:app --reload
"""