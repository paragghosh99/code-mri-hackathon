# 📚 Code MRI
AI Architecture Scanner for GitHub Repositories

Live Demo  
https://code-mri-hackathon.vercel.app/

---

## 🚀 Features

- GitHub repository architecture scanning  
- Automatic repository crawling and analysis  
- Python dependency extraction via static import analysis  
- Directed dependency graph construction (NetworkX)  
- Architecture visualization through dependency graphs  
- Graph-based scaling simulation using coupling and centrality metrics  
- Detection of architectural bottlenecks and scaling risks  
- Identification of high-impact modules and dependency hotspots  
- Gemini 2.5 Flash AI architecture reasoning  
- AI-generated scaling recommendations  
- Firestore-backed repository metadata storage  
- In-memory dependency graph caching for fast repeated analysis  
- AI explanation caching to minimize LLM latency  
- FastAPI backend with modular service architecture  
- Async repository analysis with background execution  
- Multimodal architecture analysis support (Gemini multimodal pipeline)  
- Browser automation pipeline for future repository visual inspection  
- Cloud-ready architecture designed for Vertex AI deployment  
- React frontend for interactive architecture scanning  
- Vercel deployment for instant demo access

---

# 🧠 What Code MRI Does

Modern software repositories contain hidden architectural risks that only surface when systems scale.

Code MRI performs an **AI-powered architecture scan** of any GitHub repository and detects:

- Hidden dependency bottlenecks  
- High coupling modules  
- Centralized components that limit scalability  
- Missing caching layers  
- Database concentration risks  

It builds a **dependency graph of the repository**, runs a **scaling simulation using graph theory**, and uses **Gemini 2.5 Flash** to generate architecture insights.

Think of it as an **MRI scan for software architecture**.

---

# 🌐 Live Demo

Open the demo:

https://code-mri-hackathon.vercel.app/

Enter a public GitHub repository:
`Owner`: **paragghosh99**
`Repo`: **task_app_auth_testing**


Code MRI will:

1. Crawl the repository
2. Extract Python dependencies
3. Build the architecture graph
4. Run scaling simulations
5. Generate AI architecture insights

---

# 🧪 Reproducible Testing (For Judges)

Follow these steps to test the system.

## Step 1

Open the demo:

https://code-mri-hackathon.vercel.app/

---

## Step 2

Enter a public GitHub repository.

Example:
`Owner`: **paragghosh99**
`Repo`: **task_app_auth_testing**

---

## Step 3

Submit the request.

If the repository has never been analyzed before, Code MRI will start background analysis.

---

## Step 4

Wait ~20–40 seconds.

The system will:

- fetch repository structure from GitHub
- parse Python files
- extract import dependencies
- build a dependency graph
- compute scaling risk metrics
- generate AI explanations

---

## Step 5

The UI will display:

- dependency graph
- most connected modules
- scaling risk signals
- AI-generated architecture explanation

---

## Step 6

Reload the same repository.

The result loads **instantly** due to:

- dependency graph caching
- AI explanation caching

---

# 🧩 Problem This Project Solves

Developers often discover architecture flaws **only after systems are under production load**.

Common failures include:

- tightly coupled modules
- centralized services becoming bottlenecks
- missing caching layers
- single database access points

These issues are difficult to detect manually in large repositories.

Code MRI automatically analyzes repositories and **predicts scaling risks before they become outages**.

---

# 🏗 System Architecture

                ┌──────────────────────────┐
                │        React UI          │
                │  (Owner + Repo Input)    │
                └──────────────┬───────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     FastAPI API     │
                    │       main.py       │
                    └─────────┬───────────┘
                              │
                              ▼
                  ┌─────────────────────┐
                  │ Repository Analyzer │
                  │    repo_analyzer    │
                  └─────────┬───────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │ GitHub API   │
                     │ Repo Tree    │
                     └──────┬───────┘
                            ▼
                 ┌─────────────────────┐
                 │ File Downloader     │
                 │ Python Source Files │
                 └─────────┬───────────┘
                           ▼
               ┌─────────────────────────┐
               │ Structure Extractor     │
               │ Import Dependency Scan  │
               └─────────┬───────────────┘
                         ▼
                 ┌──────────────────┐
                 │ Firestore DB     │
                 │ repo_analysis    │
                 └─────────┬────────┘
                           ▼
                 ┌──────────────────┐
                 │ Dependency Graph │
                 │ Graph Metrics    │
                 └─────────┬────────┘
                           ▼
                ┌────────────────────┐
                │ Gemini 2.5 Flash   │
                │ Architecture AI    │
                └─────────┬──────────┘
                          ▼
                 ┌──────────────────┐
                 │ Scaling Risk     │
                 │ Recommendations  │
                 └──────────────────┘

---

# ⚙️ Key Engineering Ideas

## 🧱 Dependency Graph Construction

The repository is converted into a **directed dependency graph** using NetworkX.

Nodes represent source files.  
Edges represent import dependencies.

This graph becomes the foundation for architecture analysis.

---

## 📊 Graph-Based Scaling Simulation

Code MRI simulates scaling risks using graph theory metrics.

The simulation measures:

- module coupling
- degree centrality
- database concentration
- caching presence

These signals are combined into an **overall scaling risk score**.

---

## 🤖 AI Architecture Reasoning

Gemini 2.5 Flash generates explanations for the detected risks.

The AI receives:

- graph metrics
- scaling signals
- architecture structure

and produces human-readable recommendations.

The Gemini client supports both:

- AI Studio
- Vertex AI

and can switch between them via configuration.

---

## ⚡ Async Repository Analysis

Repository crawling runs asynchronously so the API remains responsive while analysis occurs.

When a repository has not been analyzed before, the system launches a **background analysis task**.

---

## 🧠 Intelligent Caching

Two levels of caching dramatically improve performance.

### 📦 Graph Cache

Dependency graphs are stored in memory so repeated requests do not rebuild the graph.

### AI Explanation Cache

AI responses are stored in:
`ai_cache/{repo_id}.json`


This prevents repeated LLM calls and reduces latency.

---

# 🧩 Multimodal AI Support

The system includes a **multimodal architecture pipeline** that can analyze:

- architecture diagrams
- UI screenshots
- repository visuals

using Gemini multimodal APIs.

This capability exists in the codebase but is disabled in the demo to minimize latency.

When enabled, the system uses a browser automation loop to capture repository context and feed it into Gemini.

---

# 📂 Project Structure

root/
├ gemini_client.py
├ main.py
├ action_models.py
├ prompts.py
├ pydantic_models.py
├ repo_analyzer.py
├ temp_file.py

sources/
├ file_parser.py
├ firestore.py
├ structure_extractor.py

services/
├ ai_explainer.py
├ dependency_graph.py
├ repo_graph_route.py
├ scaling_simulation.py

helper/
├ get_current_folder.py
├ github_api.py

ai_cache/
└ cached AI explanations

---

# 🔌 API Endpoints

- Health check: `GET /health`
- AI text generation: `POST /generate`
- Multimodal repository analysis: `POST /analyze`
- Action planning endpoint: `POST /plan`
- Repository command API: `POST /command`
- Dependency graph API: `GET /repo-graph/{repo_id}`

- Example repo_id: `owner_repoName`
- Example: `paragghosh99_task_app_auth_testing`

---

# 📦 Tech Stack

## 🎨 Frontend

- React  
- Vercel
- Vite
- JavaScript

## 🧠 Backend

1. FastAPI  
2. Python  
3. NetworkX
4. Playwright

## 🤖 AI

1. Gemini 2.5 Flash  
2. Vertex AI / AI Studio

## 🗄 Data

1. Google Firestore

---

# 🔮 Future Work

Code MRI can evolve into a full **AI architecture assistant**.

Potential extensions include:

- CI integration for architecture scanning
- IDE plugins
- automated refactoring suggestions
- architecture drift detection
- multimodal architecture diagram understanding

---

# 🎯 Why This Matters

Software systems fail not because of syntax errors but because of **architecture decisions that do not scale**.

Code MRI helps developers detect these problems **before they reach production**.

Instead of debugging outages, teams can **scan architecture risks early**.