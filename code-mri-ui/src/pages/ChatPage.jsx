import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import AiOrb from "../components/AiOrb";
import "../style.css";

export default function ChatPage() {

  const navigate = useNavigate();

  const [owner, setOwner] = useState("");
  const [repo, setRepo] = useState("");
  const [command, setCommand] = useState("");

  const [messages, setMessages] = useState([]);

  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState([]);

  const [repoId, setRepoId] = useState(null);

  async function handleSubmit() {

    if (!owner || !repo || !command) return;

    setMessages((prev) => [
      ...prev,
      { role: "user", text: command }
    ]);

    setLoading(true);
    setProgress([]);

    const steps = [
      "Crawling repository...",
      "Parsing files...",
      "Building dependency graph...",
      "Running scaling simulation...",
      "Generating AI explanation..."
    ];

    let stepIndex = 0;

    const interval = setInterval(() => {

      setProgress([steps[stepIndex]]);

      stepIndex++;

      if (stepIndex === steps.length) {
        clearInterval(interval);
      }

    }, 1200);

    try {

      const response = await fetch("http://localhost:8000/command", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          owner,
          repo,
          command
        })
      });

      const data = await response.json();

      console.log("API response:", data);

      setRepoId(data.repo_id || `${owner}_${repo}`);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: `Command executed: ${data.command_executed}
Confidence: ${data.confidence}

Repository analysis complete.`
        }
      ]);

    } catch (err) {

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "Error analyzing repository."
        }
      ]);

    }

    setLoading(false);
    setCommand("");
  }

  function openGraph() {

    navigate("/graph", {
      state: {
        repoId: repoId
      }
    });

  }

  return (
    <div className="landing-container">

      <div className="title-block">
        <h1 className="landing-title">Code MRI</h1>
        <div className="landing-subtitle">
            AI Architecture Intelligence
        </div>
     </div>

      

      <AiOrb
        processing={loading}
        completed={!loading && repoId}
      />

      <div className="status-message">
        {progress.length > 0
            ? (repoId && !loading
                ? "Analysis completed"
                : progress[progress.length - 1])
            : ""}
        </div>

        <div className="repo-command-row">

            <input
                placeholder="Owner"
                value={owner}
                onChange={(e) => setOwner(e.target.value)}
                className="repo-input"
            />

            <input
                placeholder="Repository"
                value={repo}
                onChange={(e) => setRepo(e.target.value)}
                className="repo-input"
            />

            <button onClick={handleSubmit} className="send-button">
                Send
            </button>

            </div>

      {/* <div className="command-area">

        <input
          placeholder="Type command..."
          value={command}
          onChange={(e) => setCommand(e.target.value)}
          className="command-input"
        />

        <button onClick={handleSubmit} className="send-button">
          Send
        </button>

      </div> */}

      {repoId && (
        <button onClick={openGraph} className="view-button">
          View Hierarchy
        </button>
      )}
      <div className="command-box">

        <input
            placeholder="Type command..."
            value={command}
            onChange={(e) => setCommand(e.target.value)}
            className="command-input"
        />

        </div>

    </div>
  );
}