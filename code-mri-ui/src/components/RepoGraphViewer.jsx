import React, { useRef, useEffect, useState } from "react";
import ReactFlow, {
  Background,
  Controls,
  MiniMap
} from "reactflow";

import "reactflow/dist/style.css";

import { fetchRepoGraph } from "../services/api";
import NodeDetails from "./NodeDetails";
import dagre from "dagre";

// const [aiExplanation, setAiExplanation] = useState(null);

function layoutGraph(nodes, edges) {
  const g = new dagre.graphlib.Graph();
  g.setDefaultEdgeLabel(() => ({}));
  g.setGraph({ rankdir: "TB" });

  nodes.forEach((node) => {
    g.setNode(node.id, { width: 150, height: 50 });
  });

  edges.forEach((edge) => {
    g.setEdge(edge.source, edge.target);
  });

  dagre.layout(g);

  const xs = nodes.map(n => g.node(n.id).x);
  const minX = Math.min(...xs);
  const maxX = Math.max(...xs);
  const centerX = (minX + maxX) / 2;
 

  return nodes.map((node) => {
    const pos = g.node(node.id);

    return {
      ...node,
      position: {
        x: pos.x - centerX,
        y: pos.y
      },
      sourcePosition: "bottom",
      targetPosition: "top"
    };
  });
}


export default function RepoGraphViewer({ repoId }) {

  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [selectedNode, setSelectedNode] = useState(null);
  const [scalingAnalysis, setScalingAnalysis] = useState(null);
  const [aiExplanation, setAiExplanation] = useState(null);
  const [isPanelOpen, setIsPanelOpen] = useState(true);

  const reactFlowInstance = useRef(null);

  useEffect(() => {
    loadGraph();
  }, [repoId]);


  async function loadGraph() {

    const data = await fetchRepoGraph(repoId);

    console.log("API response:", data);

    if (!data || !data.graph_edges) return;

    setScalingAnalysis(data.scaling_analysis);
    setAiExplanation(data.ai_explanation);

    // const rfEdges = data.graph_edges.map((e, i) => ({
    //   id: `e${i}`,
    //   source: e.source,
    //   target: e.target
    // }));
    const rfEdges = data.graph_edges.map((e) => ({
      id: `${e.source}-${e.target}`,
      source: e.source,
      target: e.target
    }));

    // const nodeSet = new Set();

    // data.graph_edges.forEach((e) => {
    //   nodeSet.add(e.source);
    //   nodeSet.add(e.target);
    // });

    // // 
    // const rfNodes = Array.from(nodeSet).map((fullPath) => {

    //   const filename = fullPath.split("/").pop();

    //   return {
    //     id: fullPath,              // unique id
    //     data: { label: filename }, // readable label
    //     position: { x: 0, y: 0 }
    //   };
    // });
    
    const rfNodes = (data.graph_nodes || []).map((node) => {
      const fullPath = node.id;

      const filename = fullPath.split("/").pop();

      return {
        id: fullPath,
        data: { label: filename },
        position: { x: 0, y: 0 }
      };
    });
    console.log("graph_nodes length:", data.graph_nodes?.length);
    console.log("graph_edges length:", data.graph_edges?.length);
    console.log("API response:", JSON.stringify(data, null, 2));

    // const layoutedNodes = layoutGraph(rfNodes, rfEdges);
    // const layoutedNodes =
    // rfEdges.length > 0 ? layoutGraph(rfNodes, rfEdges) : rfNodes;
    const layoutedNodes =
    rfEdges.length > 0
      ? layoutGraph(rfNodes, rfEdges)
      : rfNodes.map((n, i) => ({
          ...n,
          position: {
            x: (i % 4) * 250,
            y: Math.floor(i / 4) * 150
          }
        }));

    setNodes(layoutedNodes);
    setEdges(rfEdges);

    setTimeout(() => {
      reactFlowInstance.current?.fitView({
      padding: 0.2,
      duration: 400
    });
    }, 400);
  }


  function onNodeClick(event, node) {
    setSelectedNode(node);
  }


  return (
    <div style={{ width: "100%", height: "100%" }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodeClick={onNodeClick}
        onInit={(instance) => {
          reactFlowInstance.current = instance;
        }}
        style={{ width: "100%", height: "100%", background: "transparent" }}
      >

        {scalingAnalysis && isPanelOpen && (
          <div
            onWheel={(e) => e.stopPropagation()}
            style={{
              position: "absolute",

              top: 110,          // below header
              right: 20,
              bottom: 200,      // above minimap

              width: 340,
              zIndex: 10,

              overflowY: "auto",

              padding: "18px 20px",
              background: "rgba(27,27,27,0.9)",
              border: "1px solid #333",
              borderRadius: 12,
              boxShadow: "0 6px 18px rgba(0,0,0,0.45)",
              backdropFilter: "blur(4px)",
              textAlign: "left",
              color: "#e5e7eb"
            }}
          >
            {/* 🔴 MINIMIZE BUTTON */}
            <button
              onClick={() => setIsPanelOpen(false)}
              title="Close panel"
              style={{
                position: "sticky",
                top: 0,
                marginLeft: "auto",

                width: 28,
                height: 30,
                fontsize: 14,

                borderRadius: "8px",
                border: "1px solid rgba(255,255,255,0.15)",

                background: "rgba(255,255,255,0.08)",
                color: "#e5e7eb",

                display: "flex",
                alignItems: "center",
                justifyContent: "center",

                cursor: "pointer",
                fontSize: 18,
                fontWeight: "600",

                backdropFilter: "blur(6px)",
                transition: "all 0.2s ease"
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = "rgba(255,255,255,0.18)";
                e.currentTarget.style.color = "#fff";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = "rgba(255,255,255,0.08)";
                e.currentTarget.style.color = "#e5e7eb";
              }}
            >
              ✕
            </button>

            <h4 style={{ margin: "0 0 10px", fontSize: 16 }}>
              Scaling Risk
            </h4>

            <p style={{ margin: "0 0 10px", color: "#9ca3af" }}>
              Score:
              <strong style={{ color: "#fff" }}>
                {" "}{scalingAnalysis.overall_scaling_risk}
              </strong>
            </p>

            <ul style={{ marginBottom: 16, paddingLeft: 18 }}>
              {scalingAnalysis.signals.map((s, i) => (
                <li key={i}>{s}</li>
              ))}
            </ul>

            {aiExplanation && (
              <>
                <h4 style={{ margin: "10px 0", fontSize: 16 }}>
                  AI Architecture Insight
                </h4>

                <div
                  style={{
                    fontSize: 14,
                    lineHeight: 1.5,
                    whiteSpace: "pre-line",
                    color: "#d1d5db"
                  }}
                >
                  {aiExplanation.explanation}
                </div>

                <h4 style={{ marginTop: 10 }}>Recommendations</h4>

                <ul style={{ paddingLeft: 18 }}>
                  {aiExplanation.recommendations?.map((r, i) => (
                    <li key={i}>{r}</li>
                  ))}
                </ul>
              </>
            )}
          </div>
        )}

        {scalingAnalysis && !isPanelOpen && (
          <div
            onClick={() => setIsPanelOpen(true)}
            style={{
              position: "absolute",
              right: 30,
              bottom: 200,

              width: 56,
              height: 56,
              borderRadius: "50%",

              background: "radial-gradient(circle, #1f2937, #020617)",
              
              display: "flex",
              alignItems: "center",
              justifyContent: "center",

              cursor: "pointer",
              zIndex: 10,

              color: "#60a5fa",
              fontWeight: "bold",

              transition: "all 0.25s ease",

              animation: "orbPulse 2.5s ease-in-out infinite"
            }}

            onMouseEnter={(e) => {
              e.currentTarget.style.animation = "none";
              e.currentTarget.style.transform = "scale(1.1)";
              e.currentTarget.style.boxShadow = `
                0 0 18px rgba(59,130,246,0.9),
                0 0 40px rgba(59,130,246,0.5),
                inset 0 0 12px rgba(0,0,0,0.9)
              `;
            }}

            onMouseLeave={(e) => {
              e.currentTarget.style.transform = "scale(1)";
              e.currentTarget.style.boxShadow = `
                0 0 12px rgba(59,130,246,0.6),
                0 0 24px rgba(59,130,246,0.3),
                inset 0 0 10px rgba(0,0,0,0.8)
              `;
            }}

            onMouseDown={(e) => {
              e.currentTarget.style.transform = "scale(0.95)";
            }}

            onMouseUp={(e) => {
              e.currentTarget.style.transform = "scale(1.1)";
            }}
          >
          <span style={{ fontSize: 12, opacity: 0.8 }}>AI</span>
          </div>
        )}

        <MiniMap
          style={{
            position: "absolute",
            right: 20,
            bottom: 40,
            width: 180,
            height: 120,
            background: "#1b1b1b",
            border: "1px solid #333",
            borderRadius: 10,
            boxShadow: "0 4px 12px rgba(0,0,0,0.4)"
          }}
          nodeColor={() => "#6fa8ff"}
          maskColor="rgba(0,0,0,0.4)"
        />
        <Controls
          style={{
            left: 20,
            bottom: 40,
            background: "#1b1b1b",
            border: "1px solid #333",
            borderRadius: 10,
            boxShadow: "0 4px 12px rgba(0,0,0,0.4)"
          }}
        />
        <Background color="#2a3b5c" gap={30} size={1}/>

      </ReactFlow>
    </div>
  );
}