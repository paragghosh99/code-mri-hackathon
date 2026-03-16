import React from "react";
export default function NodeDetails({ node }) {

  if (!node) {
    return (
      <div style={{ width: 300, padding: 20 }}>
        Click a file node
      </div>
    );
  }

  return (
    <div style={{ width: 300, padding: 20, borderLeft: "1px solid #ddd" }}>

      <h3>File Info</h3>

      <p>
        <strong>Name:</strong> {node.id}
      </p>

      <p>
        <strong>Lines:</strong> {node.data.lines}
      </p>

    </div>
  );
}