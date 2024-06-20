import cv2
from flask import Flask, Response
import depthai as dai

app = Flask(__name__)
#camera = cv2.VideoCapture(0)  # 0 represents the default camera, change it if needed

pipeline = dai.Pipeline()

# Create an Oak-D camera node
cam = pipeline.createColorCamera()
cam.setBoardSocket(dai.CameraBoardSocket.CAM_A)
cam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_720_P)

xout = pipeline.createXLinkOut()
xout.setStreamName("video")
cam.video.link(xout.input)


def generate_frames():
    with dai.Device(pipeline) as device:
        # Get the output queue for video frames
        video_queue = device.getOutputQueue(name="video", maxSize=1, blocking=False)
        device.startPipeline()
        while True:
            frame = video_queue.get()
            image_data = frame.getCvFrame()
            ret, buffer = cv2.imencode('.jpg', image_data)
            image_data = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + image_data + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=10000,debug=False)
