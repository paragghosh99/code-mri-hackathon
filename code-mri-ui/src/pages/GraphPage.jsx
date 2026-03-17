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
    <div className="graph-page">

      <h1 className="graph-title">Code MRI</h1>

      <div className="graph-container">
        <RepoGraphViewer repoId={repoId} />
      </div>

    </div>
  );
}