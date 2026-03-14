import React from "react";
import { useLocation } from "react-router-dom";
import RepoGraphViewer from "../components/RepoGraphViewer";

export default function GraphPage() {

  const location = useLocation();

  const repoId = location.state?.repoId;

  if (!repoId) {
    return <div style={{padding:40}}>No repository selected</div>;
  }

  return (
    <div style={{ width: "100%", height: "100vh" }}>
      <h2 style={{ padding: "10px", margin: 0 }}>
        Code MRI – Architecture Viewer
      </h2>

      <div style={{ height: "calc(100vh - 50px)" }}>
        <RepoGraphViewer repoId={repoId} />
      </div>
    </div>
  );
}