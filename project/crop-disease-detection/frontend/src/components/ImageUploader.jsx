import React, { useCallback, useRef, useState } from "react";

const ACCEPTED_TYPES = ["image/jpeg", "image/jpg", "image/png", "image/webp"];

function CornerTicks() {
  return (
    <>
      <span className="mount-corner mount-corner--tl" />
      <span className="mount-corner mount-corner--tr" />
      <span className="mount-corner mount-corner--bl" />
      <span className="mount-corner mount-corner--br" />
    </>
  );
}

export default function ImageUploader({ onFileSelected, previewUrl, loading, onSubmit, onClear }) {
  const [isDragOver, setIsDragOver] = useState(false);
  const [localError, setLocalError] = useState("");
  const inputRef = useRef(null);

  const handleFiles = useCallback(
    (fileList) => {
      const file = fileList && fileList[0];
      if (!file) return;
      if (!ACCEPTED_TYPES.includes(file.type)) {
        setLocalError("Please upload a JPEG, PNG, or WEBP image.");
        return;
      }
      if (file.size > 10 * 1024 * 1024) {
        setLocalError("Image is larger than 10MB. Please choose a smaller file.");
        return;
      }
      setLocalError("");
      onFileSelected(file);
    },
    [onFileSelected]
  );

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    handleFiles(e.dataTransfer.files);
  };

  return (
    <section className="mount">
      <div className="mount__ruleline">
        <span>Fig. A — leaf sample</span>
        <span>224 × 224 px, RGB, normalized</span>
      </div>

      <div
        className={
          "mount__dropzone" +
          (isDragOver ? " mount__dropzone--drag" : "") +
          (previewUrl ? " mount__dropzone--filled" : "")
        }
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragOver(true);
        }}
        onDragLeave={() => setIsDragOver(false)}
        onDrop={handleDrop}
        onClick={() => !previewUrl && inputRef.current?.click()}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => {
          if ((e.key === "Enter" || e.key === " ") && !previewUrl) {
            inputRef.current?.click();
          }
        }}
        aria-label="Upload a leaf photo"
      >
        <CornerTicks />

        {previewUrl ? (
          <div className="mount__preview-wrap">
            <img src={previewUrl} alt="Uploaded leaf" className="mount__preview-img" />
            {loading && (
              <div className="scan-overlay" aria-hidden="true">
                <div className="scan-overlay__line" />
              </div>
            )}
          </div>
        ) : (
          <div className="mount__placeholder">
            <svg
              width="40"
              height="40"
              viewBox="0 0 40 40"
              fill="none"
              aria-hidden="true"
            >
              <path
                d="M20 6C11 6 5 14 5 22c0 6 5 10 10 8-1-6 2-13 8-16 3 6 1 13-4 16 8 1 15-5 15-14C34 12 28 6 20 6Z"
                stroke="var(--leaf)"
                strokeWidth="1.6"
                strokeLinejoin="round"
              />
              <path d="M20 6c3 8 3 16-3 26" stroke="var(--leaf)" strokeWidth="1.2" />
            </svg>
            <p className="mount__placeholder-title">
              Drop a leaf photograph here
            </p>
            <p className="mount__placeholder-sub">or click to browse — JPEG, PNG, WEBP up to 10MB</p>
          </div>
        )}

        <input
          ref={inputRef}
          type="file"
          accept={ACCEPTED_TYPES.join(",")}
          onChange={(e) => handleFiles(e.target.files)}
          hidden
        />
      </div>

      {localError && <p className="mount__error">{localError}</p>}

      <div className="mount__actions">
        {previewUrl && !loading && (
          <>
            <button className="btn btn--ghost" type="button" onClick={onClear}>
              Choose a different photo
            </button>
            <button className="btn btn--primary" type="button" onClick={onSubmit}>
              Diagnose this leaf
            </button>
          </>
        )}
        {previewUrl && loading && (
          <button className="btn btn--primary btn--busy" type="button" disabled>
            Analyzing sample…
          </button>
        )}
        {!previewUrl && (
          <button
            className="btn btn--primary"
            type="button"
            onClick={() => inputRef.current?.click()}
          >
            Select a leaf photo
          </button>
        )}
      </div>
    </section>
  );
}
