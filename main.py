import json

import pika
from fastapi import FastAPI
import uvicorn
from starlette.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()


class Current(BaseModel):
    current: float
    recorded_time: str


@app.get("/")
async def hello():
    return JSONResponse(content="Server Works!", status_code=200)


@app.post("/add_data")
async def add_data(current: Current):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='62.72.21.79', port=5673))
    channel = connection.channel()

    channel.queue_declare(queue="rpi", durable=True)

    channel.basic_publish(exchange='',
                          routing_key='rpi',
                          body=json.dumps({"current": current.current,
                                           "recorded_time": current.recorded_time}).encode('utf-8'))

    connection.close()

    return JSONResponse(content="Record added successfully!", status_code=200)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0')
