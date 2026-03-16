const API_BASE = "https://code-mri-service-94165953450.us-central1.run.app";
// const API_BASE = "http://localhost:8000";

export async function fetchRepoGraph(repoId) {

  const response = await fetch(`${API_BASE}/repo-graph/${repoId}`);

  if (!response.ok) {
    throw new Error("Failed to fetch repo graph");
  }

  return await response.json();
}