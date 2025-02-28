"use client"
import { useState, useEffect, useCallback } from "react";
import axios from "axios";

export default function Home() {
  // State variables to store the image file, preview URLs, and parameters.
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [originalImageUrl, setOriginalImageUrl] = useState<string | null>(null);
  const [processedImageUrl, setProcessedImageUrl] = useState<string | null>(null);
  const [threshold, setThreshold] = useState<number>(127);
  const [method, setMethod] = useState<"otsu" | "adaptive" | "binary">("otsu");

  // When the user uploads an image, create a preview URL.
  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setImageFile(file);
      setOriginalImageUrl(URL.createObjectURL(file));
    }
  };

  // Function to call the backend API to process the image.
  const processImage = useCallback(async () => {
    if (!imageFile) return;

    const formData = new FormData();
    formData.append("image", imageFile);
    formData.append("threshold", threshold.toString());
    formData.append("method", method);

    try {
      // Adjust the URL if your backend is hosted elsewhere.
      const response = await axios.post("http://127.0.0.1:8000/binarize", formData, {
        responseType: "blob",
      });

      const url = URL.createObjectURL(response.data);
      setProcessedImageUrl(url);
    } catch (error) {
      console.error("Error processing image:", error);
    }
  }, [imageFile, threshold, method]);

 // Re-run image processing whenever threshold or method changes
  useEffect(() => {
    if (imageFile) {
      const timer = setTimeout(() => {
        processImage();
      }, 300); // Debounce API calls
      return () => clearTimeout(timer);
    }
  }, [threshold, method, processImage]);

  return (
    <div className="min-h-screen p-8 bg-gray-100">
      <h1 className="text-3xl font-bold mb-4">Real-Time Image Binarization</h1>
      
      {/* Image Upload */}
      <input type="file" accept="image/*" onChange={handleImageUpload} className="mb-4" />

      {/* Parameter Controls */}
      <div className="mb-4 space-y-4">
        <div>
          <label className="block mb-1" htmlFor="threshold">
            Threshold: {threshold}
          </label>
          <input
            id="threshold"
            type="range"
            min="0"
            max="255"
            value={threshold}
            onChange={(e) => setThreshold(Number(e.target.value))}
            className="w-full"
          />
        </div>
        <div>
          <label className="block mb-1" htmlFor="method">
            Binarization Method:
          </label>
          <select
            id="method"
            value={method}
            onChange={(e) => setMethod(e.target.value as "otsu" | "adaptive" | "binary")}
            className="p-2 border rounded"
          >
            <option value="otsu">Otsu</option>
            <option value="adaptive">Adaptive</option>
            <option value="binary">Binary</option>
          </select>
        </div>
      </div>

      {/* Image Display: Original and Binarized Side-by-Side */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {originalImageUrl && (
          <div>
            <h2 className="font-semibold mb-2">Original Image</h2>
            <img src={originalImageUrl} alt="Original" className="max-w-full border" />
          </div>
        )}
        {processedImageUrl && (
          <div>
            <h2 className="font-semibold mb-2">Binarized Image</h2>
            <img src={processedImageUrl} alt="Binarized" className="max-w-full border" />
          </div>
        )}
      </div>
    </div>
  );
}
