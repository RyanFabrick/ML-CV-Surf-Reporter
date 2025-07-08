import cv2
import os
from inference import InferencePipeline
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("ROBOFLOW_API_KEY")
workspace_name = os.getenv("ROBOFLOW_WORKSPACE")
workflow_id = os.getenv("ROBOFLOW_WORKFLOW_ID")

video_path = "C:/Users/ryanf/Desktop/EXAMPLE VIDEO.mp4"

# Open video to get size and fps
cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS) or 5  # fallback to 5 if fps not available
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
cap.release()

# Prepare VideoWriter - saving to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
output_file = os.path.join(desktop_path, "output.mp4")
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

def my_sink(result, video_frame):
    vis_image = result.get("detection_visualization")
    if vis_image:
        frame = vis_image.numpy_image
        cv2.imshow("Workflow Image", frame)
        cv2.waitKey(1)
        out.write(frame)  # save frame to video file
    else:
        frame = video_frame.image
        cv2.imshow("Workflow Image", frame)
        cv2.waitKey(1)

pipeline = InferencePipeline.init_with_workflow(
    api_key=api_key,
    workspace_name=workspace_name,
    workflow_id=workflow_id,
    video_reference=video_path,
    max_fps=5,
    on_prediction=my_sink
)

try:
    pipeline.start()
    pipeline.join()
finally:
    out.release()
    cv2.destroyAllWindows()
