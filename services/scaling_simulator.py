import networkx as nx


def normalize(value, max_value):
    if max_value == 0:
        return 0
    return min(value / max_value, 1)


def detect_cache_layer(G):
    keywords = ["cache", "redis", "memcache", "lru_cache"]

    for node in G.nodes:
        name = node.lower()
        if any(k in name for k in keywords):
            return True
    return False


def detect_db_modules(G):
    keywords = ["db", "database", "sql", "session", "model"]

    db_nodes = []

    for node in G.nodes:
        name = node.lower()
        if any(k in name for k in keywords):
            db_nodes.append(node)

    return db_nodes


def compute_coupling(G):

    in_degrees = dict(G.in_degree())

    if not in_degrees:
        return 0, None

    max_node = max(in_degrees, key=in_degrees.get)
    max_degree = in_degrees[max_node]

    score = normalize(max_degree, len(G.nodes))

    return score, max_node


def compute_centrality_risk(G):

    centrality = nx.degree_centrality(G)

    if not centrality:
        return 0, None

    max_node = max(centrality, key=centrality.get)
    max_value = centrality[max_node]

    return max_value, max_node


def compute_db_risk(G):

    db_nodes = detect_db_modules(G)

    if not db_nodes:
        return 0, None

    if len(db_nodes) == 1:
        return 0.8, db_nodes[0]

    return 0.3, db_nodes


def run_scaling_simulation(G):

    signals = []

    # ---- coupling ----
    coupling_score, coupling_node = compute_coupling(G)

    if coupling_score > 0.4:
        signals.append(f"High coupling around module: {coupling_node}")

    # ---- centrality ----
    centrality_risk, central_node = compute_centrality_risk(G)

    if centrality_risk > 0.4:
        signals.append(f"High centrality module: {central_node}")

    # ---- db concentration ----
    db_risk, db_node = compute_db_risk(G)

    if db_risk > 0.6:
        signals.append("Single database access layer detected")

    # ---- caching ----
    cache_present = detect_cache_layer(G)

    if not cache_present:
        signals.append("No caching module detected")

    # ---- overall score ----
    overall = (
        0.4 * coupling_score +
        0.3 * db_risk +
        0.3 * centrality_risk
    )

    if not cache_present:
        overall += 0.1

    overall = min(overall, 1)

    return {
        "coupling_score": round(coupling_score, 2),
        "db_risk": round(db_risk, 2),
        "overall_scaling_risk": round(overall, 2),
        "signals": signals
    }