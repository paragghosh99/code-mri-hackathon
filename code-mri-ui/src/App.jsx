import React from "react";
import { Routes, Route } from "react-router-dom";

import ChatPage from "./pages/ChatPage";
import GraphPage from "./pages/GraphPage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<ChatPage />} />
      <Route path="/graph" element={<GraphPage />} />
    </Routes>
  );
}

export default App;