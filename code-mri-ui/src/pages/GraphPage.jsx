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
      <div className="title-block">
        <h1 className="landing-title">Code MRI</h1>
        
     </div>

     <div className="graph-page">
        <RepoGraphViewer repoId={repoId} />
    </div>
    </div>
  );
}