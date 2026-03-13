import React from "react";
import RepoGraphViewer from "./components/RepoGraphViewer";

function App() {
  const repoId = "paragghosh99_task_app_auth_testing";

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

export default App;