export async function fetchRepoGraph(repoId) {
  const response = await fetch(`http://localhost:8000/repo-graph/${repoId}`);
  return response.json();
}