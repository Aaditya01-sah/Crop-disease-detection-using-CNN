import React from "react";

export default function ResultCard({ result }) {
  if (!result) return null;

  const {
    display_name: displayName,
    is_healthy: isHealthy,
    confidence,
    description,
    recommendation,
    top_predictions: topPredictions = [],
  } = result;

  return (
    <section className="result-card" aria-live="polite">
      <div className={"stamp " + (isHealthy ? "stamp--healthy" : "stamp--diseased")}>
        {isHealthy ? "Healthy" : "Disease detected"}
      </div>

      <div className="result-card__body">
        <p className="result-card__eyebrow">Diagnosis</p>
        <h2 className="result-card__title">{displayName}</h2>

        <div className="result-card__confidence">
          <span className="result-card__confidence-label">Model confidence</span>
          <span className="result-card__confidence-value">
            {confidence.toFixed(1)}%
          </span>
        </div>
        <div className="confidence-bar">
          <div
            className="confidence-bar__fill"
            style={{ width: `${Math.min(confidence, 100)}%` }}
          />
        </div>

        <p className="result-card__description">{description}</p>

        <div className="result-card__recommendation">
          <span className="result-card__recommendation-label">
            {isHealthy ? "Guidance" : "Recommended action"}
          </span>
          <p>{recommendation}</p>
        </div>

        {topPredictions.length > 1 && (
          <div className="result-card__top">
            <p className="result-card__top-label">Other close matches</p>
            <ul className="top-list">
              {topPredictions.map((p, idx) => (
                <li key={idx} className="top-list__row">
                  <span className="top-list__name">{p.display_name}</span>
                  <span className="top-list__value">{p.confidence.toFixed(1)}%</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </section>
  );
}
