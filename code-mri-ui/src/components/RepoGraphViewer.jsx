import React from "react";
import { useEffect, useState } from "react";
import ReactFlow, {
  Background,
  Controls,
  MiniMap
} from "reactflow";
import { ReactFlowProvider } from "reactflow";

import "reactflow/dist/style.css";

import { fetchRepoGraph } from "../services/api";
import NodeDetails from "./NodeDetails";
import dagre from "dagre";


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

  return nodes.map((node) => {
    const pos = g.node(node.id);

    return {
      ...node,
      position: {
        x: pos.x - 75,
        y: pos.y - 25
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

  useEffect(() => {
    loadGraph();
  }, [repoId]);

  async function loadGraph() {

    const data = await fetchRepoGraph(repoId);

    setScalingAnalysis(data.scaling_analysis);

    console.log("API response:", data);

    if (!data || !data.top_files) return;

    const rfNodes = data.top_files.map((file, i) => ({
        id: file[0],
        data: {
        label: `${file[0]} (${file[1]})`,
        lines: file[1]
        },
        position: { x: i * 300 - 300, y: 200 }
    }));

    setNodes(rfNodes);
    const rfEdges = data.graph_edges.map((e, i) => ({
    id: `e${i}`,
    source: e.source,
    target: e.target
    }));

    setEdges(rfEdges);
    }

  function onNodeClick(event, node) {
    setSelectedNode(node);
  }

    return (
        <div style={{ width: "100vw", height: "100vh" }}>
            <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodeClick={onNodeClick}
            fitView
            fitViewOptions={{ padding: 0.3 }}
            style={{ width: "100%", height: "100%" }}
            >
                {scalingAnalysis && (
                <div
                    style={{
                    position: "absolute",
                    top: 20,
                    right: 20,
                    background: "#111",
                    color: "white",
                    padding: 15,
                    borderRadius: 8,
                    width: 250
                    }}
                >
                    <h4>Scaling Risk</h4>

                    <p>
                    Score: {scalingAnalysis.overall_scaling_risk}
                    </p>

                    <ul>
                    {scalingAnalysis.signals.map((s, i) => (
                        <li key={i}>{s}</li>
                    ))}
                    </ul>
                </div>
                )}
            <MiniMap />
            <Controls />
            <Background />
            </ReactFlow>
        </div>
        );
}