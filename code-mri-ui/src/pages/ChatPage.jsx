import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

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

    const steps = [
      "Analyzing repository...",
      "✔ Crawling repository",
      "✔ Parsing files",
      "✔ Building dependency graph",
      "✔ Running scaling simulation",
      "✔ Generating AI explanation"
    ];

    let stepIndex = 0;

    const interval = setInterval(() => {

      setProgress((prev) => [...prev, steps[stepIndex]]);

      stepIndex++;

      if (stepIndex === steps.length) {
        clearInterval(interval);
      }

    }, 800);

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
    <div style={container}>

      <h1 style={title}>Code MRI</h1>

      <div style={inputRow}>

        <input
          placeholder="Owner ID"
          value={owner}
          onChange={(e) => setOwner(e.target.value)}
          style={input}
        />

        <input
          placeholder="Repository Name"
          value={repo}
          onChange={(e) => setRepo(e.target.value)}
          style={input}
        />

      </div>

      <div style={chatBox}>

        {messages.map((m, i) => (
          <div
            key={i}
            style={{
              ...message,
              alignSelf: m.role === "user" ? "flex-end" : "flex-start",
              background: m.role === "user" ? "#3b82f6" : "#1f2937"
            }}
          >
            {m.text}
          </div>
        ))}

        {loading && (
          <div style={progressBox}>
            {progress.map((p, i) => (
              <div key={i}>{p}</div>
            ))}
            <div style={{ marginTop: 10 }}>
              Estimated time: 2–4 minutes
            </div>
          </div>
        )}

      </div>

      <div style={commandRow}>

        <input
          placeholder="Type command..."
          value={command}
          onChange={(e) => setCommand(e.target.value)}
          style={commandInput}
        />

        <button onClick={handleSubmit} style={button}>
          Send
        </button>

      </div>

      {repoId && (
        <button onClick={openGraph} style={viewButton}>
          View Hierarchy
        </button>
      )}

    </div>
  );
}

const container = {
  width: "100%",
  height: "100vh",
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  padding: 30
};

const title = {
  marginBottom: 20
};

const inputRow = {
  display: "flex",
  gap: 10,
  marginBottom: 20
};

const input = {
  padding: 10,
  width: 200
};

const chatBox = {
  width: 700,
  height: 400,
  border: "1px solid #444",
  borderRadius: 10,
  padding: 20,
  display: "flex",
  flexDirection: "column",
  gap: 10,
  overflowY: "auto"
};

const message = {
  padding: 12,
  borderRadius: 10,
  maxWidth: "70%"
};

const commandRow = {
  display: "flex",
  marginTop: 20,
  gap: 10
};

const commandInput = {
  width: 500,
  padding: 10
};

const button = {
  padding: "10px 20px"
};

const progressBox = {
  background: "#111",
  padding: 15,
  borderRadius: 10,
  marginTop: 10
};

const viewButton = {
  marginTop: 20,
  padding: "12px 30px",
  fontSize: 16
};