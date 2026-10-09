import React from "react";

export default function Footer() {
  return (
    <footer className="site-footer">
      <div className="site-footer__rule" />
      <div className="site-footer__grid">
        <div>
          <p className="site-footer__label">Model</p>
          <p>Custom CNN &amp; MobileNetV2 transfer learning</p>
        </div>
        <div>
          <p className="site-footer__label">Dataset</p>
          <p>PlantVillage — 54,305 images, 38 classes</p>
        </div>
        <div>
          <p className="site-footer__label">Stack</p>
          <p>TensorFlow/Keras · OpenCV · Django REST · React</p>
        </div>
      </div>
      <p className="site-footer__note">
        Minor Project — Tribhuvan University, Institute of Engineering. Predictions
        are a decision-support aid, not a substitute for a plant pathologist.
      </p>
    </footer>
  );
}
