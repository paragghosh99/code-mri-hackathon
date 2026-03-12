import React from "react";
import RepoGraphViewer from "./components/RepoGraphViewer";

function App() {
  const repoId = "paragghosh99_task_app_auth_testing";

  return (
    <div style={{ height: "100vh" }}>
      <h2 style={{ padding: "10px" }}>
        Code MRI – Architecture Viewer
      </h2>

      <RepoGraphViewer repoId={repoId} />
    </div>
  );
}

export default App;