import axios from "axios";

// Set REACT_APP_API_BASE_URL in a .env file to point at a deployed backend;
// defaults to the local Django dev server described in section 3.2.3.
const API_BASE_URL =
  process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:8000/api";

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

/**
 * Uploads a leaf image to POST /api/predict/ and returns the parsed
 * prediction payload (predicted_class, confidence, description, ...).
 */
export async function predictDisease(imageFile) {
  const formData = new FormData();
  formData.append("image", imageFile);

  const response = await client.post("/predict/", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
}

export async function checkHealth() {
  const response = await client.get("/health/");
  return response.data;
}

export default client;
