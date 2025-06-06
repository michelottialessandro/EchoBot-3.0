# Face Detection

# Import required modules
import cv2
import depthai as dai
import time
import blobconverter

# Define Frame
FRAME_SIZE = (640, 400)

# Define NN model name and input size
# If you define the blob make make sure the MODEL_NAME and ZOO_TYPE are None
# DET_INPUT_SIZE = (672, 384)
# MODEL_NAME = None
# ZOO_TYPE = None
# blob_path = "models/face-detection-adas-0001.blob"

DET_INPUT_SIZE = (300, 300)
MODEL_NAME = "face-detection-retail-0004"
ZOO_TYPE = "depthai"
blob_path = None

# DET_INPUT_SIZE = (672, 384)
# MODEL_NAME = "face-detection-adas-0001"
# ZOO_TYPE = "intel"
# blob_path = None


# Start defining a pipeline
pipeline = dai.Pipeline()

# Define a source - RGB camera
cam = pipeline.createColorCamera()
cam.setPreviewSize(FRAME_SIZE[0], FRAME_SIZE[1])
cam.setInterleaved(False)
cam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
cam.setBoardSocket(dai.CameraBoardSocket.RGB)

# Convert model from OMZ to blob
if MODEL_NAME is not None:
    blob_path = blobconverter.from_zoo(
        name=MODEL_NAME,
        shaves=6,
        zoo_type=ZOO_TYPE
    )

# Define face detection NN node
face_det_nn = pipeline.createMobileNetDetectionNetwork()
face_det_nn.setConfidenceThreshold(0.75)
face_det_nn.setBlobPath(blob_path)

# Define face detection input config
face_det_manip = pipeline.createImageManip()
face_det_manip.initialConfig.setResize(DET_INPUT_SIZE[0], DET_INPUT_SIZE[1])
face_det_manip.initialConfig.setKeepAspectRatio(False)

cam.preview.link(face_det_manip.inputImage)
face_det_manip.out.link(face_det_nn.input)

# Create preview output
x_preview_out = pipeline.createXLinkOut()
x_preview_out.setStreamName("preview")
cam.preview.link(x_preview_out.input)

# Create detection output
det_out = pipeline.createXLinkOut()
det_out.setStreamName('det_out')
face_det_nn.out.link(det_out.input)


def display_info(frame, bbox, status, status_color, fps):
    # Display bounding box
    cv2.rectangle(frame, bbox, status_color[status], 2)

    # Create background for showing details
    cv2.rectangle(frame, (5, 5, 175, 100), (50, 0, 0), -1)

    # Display authentication status on the frame
    cv2.putText(frame, status, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, status_color[status])

    # Display instructions on the frame
    cv2.putText(frame, f'FPS: {fps:.2f}', (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255))


# Frame count
frame_count = 0

# Placeholder fps value
fps = 0

# Used to record the time when we processed last frames
prev_frame_time = 0

# Used to record the time at which we processed current frames
new_frame_time = 0

# Set status colors
status_color = {
    'Face Detected': (0, 255, 0),
    'No Face Detected': (0, 0, 255)
}

# Start pipeline
with dai.Device(pipeline) as device:

    # Output queue will be used to get the right camera frames from the outputs defined above
    q_cam = device.getOutputQueue(name="preview", maxSize=1, blocking=False)

    # Output queue will be used to get nn data from the video frames.
    q_det = device.getOutputQueue(name="det_out", maxSize=1, blocking=False)

    while True:
        # Get right camera frame
        in_cam = q_cam.get()
        frame = in_cam.getCvFrame()

        bbox = None

        inDet = q_det.tryGet()

        if inDet is not None:
            detections = inDet.detections

            # if face detected
            if len(detections) is not 0:
                detection = detections[0]

                # Correct bounding box
                xmin = max(0, detection.xmin)
                ymin = max(0, detection.ymin)
                xmax = min(detection.xmax, 1)
                ymax = min(detection.ymax, 1)

                # Calculate coordinates
                x = int(xmin*FRAME_SIZE[0])
                y = int(ymin*FRAME_SIZE[1])
                w = int(xmax*FRAME_SIZE[0]-xmin*FRAME_SIZE[0])
                h = int(ymax*FRAME_SIZE[1]-ymin*FRAME_SIZE[1])

                bbox = (x, y, w, h)

        # Check if a face was detected in the frame
        if bbox:
            # Face detected
            status = 'Face Detected'
        else:
            # No face detected
            status = 'No Face Detected'

        # Display info on frame
        display_info(frame, bbox, status, status_color, fps)

        # Calculate average fps
        if frame_count % 10 == 0:
            # Time when we finish processing last 100 frames
            new_frame_time = time.time()

            # Fps will be number of frame processed in one second
            fps = 1 / ((new_frame_time - prev_frame_time)/10)
            prev_frame_time = new_frame_time

        # Capture the key pressed
        key_pressed = cv2.waitKey(1) & 0xff

        # Stop the program if Esc key was pressed
        if key_pressed == 27:
            break

        # Display the final frame
        cv2.imshow("Face Cam", frame)

        # Increment frame count
        frame_count += 1

cv2.destroyAllWindows()
