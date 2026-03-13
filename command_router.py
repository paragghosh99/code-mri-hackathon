from services.dependency_graph import analyze_repo
from services.ai_explainer import explain_scaling


def show_architecture(repo_id):

    result = analyze_repo(repo_id)

    return {
        "nodes": result["nodes"],
        "edges": result["edges"],
        "graph_edges": result["graph_edges"]
    }


def execute_command(command, repo_id):

    if command == "simulate_scaling":

        result = analyze_repo(repo_id)

        return result["scaling_analysis"]

    elif command == "analyze_dependencies":

        return analyze_repo(repo_id)

    elif command == "explain_risk":

        result = analyze_repo(repo_id)

        return result["ai_explanation"]

    elif command == "show_architecture":

        return show_architecture(repo_id)

    else:

        raise Exception("Unsupported command")