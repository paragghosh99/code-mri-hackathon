from google.cloud import firestore
import networkx as nx

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

    for f in files:

        filename = f["file"]
        imports = f.get("imports", [])
        lines = f.get("lines", 0)

        G.add_node(filename, lines=lines)

        for imp in imports:
            G.add_edge(filename, imp)

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

    files = load_repo_files(repo_id)

    if not files:
        return {
            "nodes": 0,
            "edges": 0,
            "top_files": []
        }

    G = build_dependency_graph(files)

    top = most_connected_files(G)[:5]

    return {
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "top_files": top
    }