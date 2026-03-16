import React from "react";
import "../style.css";

export default function AiOrb({ processing, completed }) {

  let className = "ai-orb";

  if (processing) className += " orb-processing";
  if (completed) className += " orb-complete";

  return (
    <div className="orb-container">

      <div className={className}>

        <div className="orb-wave"></div>
        <div className="orb-wave orb-wave-2"></div>

      </div>

    </div>
  );
}