import React, { useEffect, useState } from "react";
import "./App.css";
import Header from "./components/Header";
import ImageUploader from "./components/ImageUploader";
import ResultCard from "./components/ResultCard";
import Footer from "./components/Footer";
import { predictDisease } from "./api/predictApi";

export default function App() {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    return () => {
      if (previewUrl) URL.revokeObjectURL(previewUrl);
    };
  }, [previewUrl]);

  const handleFileSelected = (selectedFile) => {
    setFile(selectedFile);
    setResult(null);
    setError("");
    setPreviewUrl(URL.createObjectURL(selectedFile));
  };

  const handleClear = () => {
    setFile(null);
    setPreviewUrl(null);
    setResult(null);
    setError("");
  };

  const handleSubmit = async () => {
    if (!file) return;
    setLoading(true);
    setError("");
    try {
      const data = await predictDisease(file);
      setResult(data);
    } catch (err) {
      const backendMessage = err?.response?.data?.details;
      setError(
        backendMessage ||
          "Couldn't reach the diagnosis service. Make sure the Django backend is running and try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <div className="page__inner">
        <Header />

        <main className="layout">
          <ImageUploader
            onFileSelected={handleFileSelected}
            previewUrl={previewUrl}
            loading={loading}
            onSubmit={handleSubmit}
            onClear={handleClear}
          />

          <div className="layout__result">
            {error && (
              <div className="notice notice--error" role="alert">
                <p className="notice__title">Diagnosis unavailable</p>
                <p>{error}</p>
              </div>
            )}

            {!result && !error && (
              <div className="notice notice--idle">
                <p className="notice__title">Awaiting a sample</p>
                <p>
                  Results — predicted species, condition, confidence score, and
                  recommended action — will appear here once a leaf photo is
                  analyzed.
                </p>
              </div>
            )}

            <ResultCard result={result} />
          </div>
        </main>

        <Footer />
      </div>
    </div>
  );
}
