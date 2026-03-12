from services.dependency_graph import (
    load_repo_files,
    build_dependency_graph,
    most_connected_files,
    affected_files,
    transitive_impact,
    analyze_repo
)

files = load_repo_files("fastapi_fastapi")

print(len(files))

if files:
    print(files[0])

files = load_repo_files("fastapi_fastapi")

print("files:", len(files))

G = build_dependency_graph(files)

print("nodes:", G.number_of_nodes())
print("edges:", G.number_of_edges())

top = most_connected_files(G)

print("top connected:", most_connected_files(G)[:5])

print("affected by starlette:", affected_files(G, "starlette"))

print("transitive impact:", transitive_impact(G, "starlette"))

result = analyze_repo("fastapi_fastapi")

print(result)