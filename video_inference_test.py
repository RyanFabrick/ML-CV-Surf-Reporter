# Import the InferencePipeline object
import cv2
import os
from inference import InferencePipeline
from dotenv import load_dotenv

#loads variables from .env
load_dotenv()
api_key = os.getenv("ROBOFLOW_API_KEY")
workspace_name = os.getenv("ROBOFLOW_WORKSPACE")
workflow_id = os.getenv("ROBOFLOW_WORKFLOW_ID")

def my_sink(result, video_frame):
    if result.get("output_image"): # Display an image from the workflow response
        cv2.imshow("Workflow Image", result["output_image"].numpy_image)
        cv2.waitKey(1)
    print(result) # do something with the predictions of each frame


# initialize a pipeline object
pipeline = InferencePipeline.init_with_workflow(
    api_key=api_key,
    workspace_name=workspace_name,
    workflow_id=workflow_id,
    video_reference="C:/Users/ryanf/Downloads/Campus Point Surf Cam.mp4", # Path to video, device id (int, usually 0 for built in webcams), or RTSP stream url
    max_fps=5,
    on_prediction=my_sink
)

pipeline.start() #start the pipeline
pipeline.join() #wait for the pipeline thread to finish 