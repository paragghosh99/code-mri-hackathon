# In-memory cache
GRAPH_CACHE = {}

from google.cloud import firestore
from services.ai_explainer import explain_scaling
import networkx as nx
from services.scaling_simulator import run_scaling_simulation
from pathlib import Path
import json

db = firestore.Client()

def load_repo_files(repo_id):

    doc = db.collection("repo_analysis").document(repo_id).get()

    print("doc exists:", doc.exists)

    if not doc.exists:
        return []

    data = doc.to_dict()

    print("fields:", data.keys())

    return data.get("files", [])


def build_dependency_graph(files):

    G = nx.DiGraph()

    # collect all repo files
    repo_file_names = {f["file"] for f in files}

    for f in files:

        filename = f["file"]
        imports = f.get("imports", [])
        lines = f.get("lines", 0)

        G.add_node(filename, lines=lines)

        for imp in imports:

            # normalize import name → module.py
            imp_file = imp.split(".")[-1] + ".py"

            if imp_file in repo_file_names:
                G.add_edge(filename, imp_file)

    return G


def most_connected_files(G):

    return sorted(
        G.degree(),
        key=lambda x: x[1],
        reverse=True
    )


def affected_files(G, target_file):

    if target_file not in G:
        return []

    return list(G.predecessors(target_file))


def transitive_impact(G, target_file):

    if target_file not in G:
        return []

    return list(nx.ancestors(G, target_file))


def analyze_repo(repo_id):

    # 1️⃣ Get graph from cache or build it
    if repo_id in GRAPH_CACHE:
        G = GRAPH_CACHE[repo_id]

    else:
        files = load_repo_files(repo_id)

        if not files:
            return {
                "nodes": 0,
                "edges": 0,
                "top_files": []
            }

        G = build_dependency_graph(files)

        # store in cache
        GRAPH_CACHE[repo_id] = G

    # 2️⃣ Run analysis (always runs now)
    top = most_connected_files(G)[:5]

    simulation = run_scaling_simulation(G)

    AI_CACHE = Path("ai_cache")
    AI_CACHE.mkdir(exist_ok=True)

    cache_file = AI_CACHE / f"{repo_id}.json"

    if cache_file.exists():

        with open(cache_file) as f:
            ai_explanation = json.load(f)

    else:

        ai_explanation = explain_scaling(simulation)

        with open(cache_file, "w") as f:
            json.dump(ai_explanation, f)

    graph_edges = [
        {"source": u, "target": v}
        for u, v in G.edges()
    ]

    return {
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "top_files": top,
        "graph_edges": graph_edges,
        "scaling_analysis": simulation,
        "ai_explanation": ai_explanation
    }