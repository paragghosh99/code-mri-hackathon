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

    const rfEdges = data.graph_edges.map((e, i) => ({
      id: `e${i}`,
      source: e.source,
      target: e.target
    }));

    const nodeSet = new Set();

    data.graph_edges.forEach((e) => {
      nodeSet.add(e.source);
      nodeSet.add(e.target);
    });

    const rfNodes = Array.from(nodeSet).map((id) => ({
      id,
      data: { label: id },
      position: { x: 0, y: 0 }
    }));

    const layoutedNodes = layoutGraph(rfNodes, rfEdges);

    setNodes(layoutedNodes);
    setEdges(rfEdges);

    setTimeout(() => {
      reactFlowInstance.current?.fitView({ padding: 0.05 });
    }, 0);
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
        style={{ width: "100%", height: "100%" }}
      >

        {scalingAnalysis && (
            <div
              onWheel={(e) => e.stopPropagation()}
              style={{
                position: "absolute",
                top: 20,
                right: 20,
                width: 340,
                zIndex: 10,
                maxHeight: "60vh",
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
                    {aiExplanation}
                  </div>
                </>
              )}
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
        <Background />

      </ReactFlow>
    </div>
  );
}