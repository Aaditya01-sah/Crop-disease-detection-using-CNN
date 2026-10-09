import React from "react";

export default function Header() {
  return (
    <header className="site-header">
      <div className="site-header__meta">
        <span>Advanced College of Engineering &amp; Management</span>
        <span className="site-header__dot">·</span>
        <span>Dept. of Electronics &amp; Computer Engineering</span>
      </div>

      <div className="site-header__title-row">
        <h1 className="site-header__title">
          Crop Disease
          <br />
          Detection
        </h1>
        <div className="site-header__accession">
          <span className="site-header__accession-label">Specimen index</span>
          <span className="site-header__accession-no">No. 038 / 26</span>
          <span className="site-header__accession-sub">14 crop species catalogued</span>
        </div>
      </div>

      <p className="site-header__sub">
        Upload a photograph of a leaf. A convolutional neural network trained on
        the PlantVillage collection identifies the species and condition, and
        returns a confidence-scored diagnosis in seconds.
      </p>
    </header>
  );
}
