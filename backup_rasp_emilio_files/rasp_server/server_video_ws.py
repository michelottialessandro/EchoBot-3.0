import asyncio
import websockets
import cv2
import pickle
import struct
import depthai as dai
pipeline = dai.Pipeline()

# Create an Oak-D camera node
cam = pipeline.createColorCamera()
cam.setBoardSocket(dai.CameraBoardSocket.CAM_A)
cam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_720_P)

xout = pipeline.createXLinkOut()
xout.setStreamName("video")
cam.video.link(xout.input)
async def handle_websocket(websocket, path):
    # This function will be called when a new WebSocket connection is established.
    print(f"New connection from {websocket.remote_address}")

    try:
        with dai.Device(pipeline) as device:
            # Get the output queue for video frames
            video_queue = device.getOutputQueue(name="video", maxSize=1, blocking=False)

            # Start the camera
            device.startPipeline()


            while True:
        
                frame = video_queue.get()
                image_data = frame.getCvFrame()
                ret, buffer = cv2.imencode('.jpg', image_data)
                image_data = buffer.tobytes()
                await websocket.send(image_data)


    except websockets.exceptions.ConnectionClosed:
        # Handle when the connection is closed by the client
        print(f"Connection closed by {websocket.remote_address}")

# Set up the WebSocket server
start_server = websockets.serve(handle_websocket, "0.0.0.0", 10000)

print("WebSocket server is running. Listening on ws://0.0.0.0:10000")

# Run the WebSocket server indefinitely
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
