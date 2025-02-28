from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import cv2
import numpy as np
from src.binary_thresholding import binary

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to ["http://localhost:3000"] for better security
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.post("/binarize")
async def binarize_image(
    image: UploadFile = File(...),
    threshold: int = Form(127),
    method: str = Form("otsu")
):
    # Read image data and convert to a NumPy array
    contents = await image.read()
    npimg = np.frombuffer(contents, np.uint8)
    
    # Decode image as grayscale
    img = cv2.imdecode(npimg, cv2.IMREAD_GRAYSCALE)
    
    # Process the image using the chosen binarization method
    if method == "otsu":
        # Otsu's method ignores the provided threshold value.
        _, binarized = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    elif method == "adaptive":
        binarized = cv2.adaptiveThreshold(
            img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
    else:  # 'binary' method uses a fixed threshold.
        binarized = binary(img, threshold)
    
    # Encode the binarized image to PNG format.
    success, buffer = cv2.imencode(".png", binarized)
    if not success:
        return Response(status_code=500)
    
    return Response(content=buffer.tobytes(), media_type="image/png")
