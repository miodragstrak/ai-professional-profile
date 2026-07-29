# AI Professional Profile

A public Model Context Protocol (MCP) server that helps AI recruiters and other AI clients understand Miodrag Strak's professional background through structured, curated, and user-approved information.

## Public endpoint

MCP endpoint:

```text
https://ai-professional-profile.onrender.com/mcp
```

Health endpoint:

```text
https://ai-professional-profile.onrender.com/health
```

## Project status

**V1 is live and publicly accessible.**

The production MCP endpoint has been tested with the official MCP Python client and currently exposes five tools:

- `get_profile`
- `get_projects`
- `get_experience`
- `get_skills`
- `get_links`

This repository is a practical personal product for Miodrag Strak.

It is not currently an Open Professional Identity specification or standard. The implementation and lessons learned from operating it may later help inform broader Open Professional Identity work.

## Purpose

Professional information is usually fragmented across CVs, LinkedIn, GitHub, portfolio websites, freelance platforms, and other public sources.

AI systems often have to interpret those sources independently, which can lead to:

- incomplete professional context;
- outdated information;
- weak attribution;
- inconsistent summaries;
- incorrect assumptions about roles or contributions.

AI Professional Profile provides one controlled interface through which an external AI system can request structured professional information.

## Example recruiter questions

An AI recruiter can use the available tools to help answer questions such as:

- What kind of roles is Miodrag suited for?
- What experience does he have with AI products?
- Has he worked in QA and product operations?
- Does he have technical product management experience?
- Which projects demonstrate technical leadership?
- Has he worked in banking, PMO, or release management?
- What are his strongest professional skills?
- Which technologies and industry domains has he worked with?
- Where can his work and professional presence be verified?

## Public MCP tools

### `get_profile`

Returns the public professional overview:

- name;
- location;
- professional headline;
- career summary;
- current professional status;
- references to the main public profile sources.

### `get_projects`

Returns approved public project information, including:

- project title;
- role;
- period and status;
- contribution summary;
- key contributions;
- outcomes;
- technologies;
- repository and public implementation links;
- source references.

The current profile includes:

- AI Professional Profile;
- Materialize;
- PSK Tax Optimization Calculator;
- A.Lex;
- NelutAI.

### `get_experience`

Returns approved professional experience, including:

- organization;
- role;
- start and end dates;
- current status;
- summary;
- key responsibilities;
- source references.

The current profile includes experience in:

- AI product operations, QA, and delivery;
- company and project leadership;
- technical product management;
- banking, PMO, and release management;
- international development;
- university teaching and research.

### `get_skills`

Returns structured professional capabilities in four groups:

- core skills;
- supporting skills;
- technologies;
- industry and professional domains.

Core areas include AI product architecture, technical product management, product operations, project management, quality assurance, workflow automation, business-process design, stakeholder management, and delivery coordination.

### `get_links`

Returns approved public professional and verification links:

- LinkedIn;
- GitHub;
- portfolio;
- Upwork;
- the public AI Professional Profile MCP endpoint.

## Public data model

The public professional information is stored in:

```text
profile.json
```

Its main sections are:

```text
profile
experience
projects
skills
domains
education
links
sources
```

Only information intentionally copied into `profile.json` is exposed through MCP tools.

## Review and publication workflow

Professional data follows a controlled workflow:

```text
source or user-provided fact
→ internal review record
→ explicit user confirmation
→ publication in profile.json
→ MCP exposure
→ local and production testing
```

Internal review records are stored in:

```text
reviews/
```

Examples include:

```text
reviews/github-project-candidates.json
reviews/github-project-details.json
reviews/experience-details.json
reviews/skills-details.json
reviews/links-details.json
```

Review records distinguish between states such as:

```text
candidate
confirmed
published
```

This prevents automatically discovered or inferred information from becoming public without approval.

## Sources and evidence

The profile may reference several source types:

- current CV;
- LinkedIn;
- GitHub;
- portfolio;
- Upwork;
- public project implementations;
- user-confirmed professional facts.

A source reference does not mean that the source itself is served through the MCP endpoint.

Private source files remain private unless information from them is deliberately reviewed and published.

## Privacy boundaries

The public profile intentionally excludes:

- private email addresses;
- phone numbers;
- the private CV file;
- private documents;
- internal project URLs;
- administrative endpoints;
- credentials and tokens;
- unpublished review records.

The MCP server returns only the approved professional data stored in `profile.json`.

## Architecture

The V1 architecture is intentionally small:

```text
External MCP client
        |
        v
Public Streamable HTTP MCP endpoint
        |
        v
FastMCP tools
        |
        v
Validated profile loader
        |
        v
profile.json
```

Main components:

- `main.py` — creates the FastAPI application, starts the MCP session manager, exposes `/health`, and mounts the MCP application.
- `mcp_server.py` — defines the public MCP server, transport-security configuration, and MCP tools.
- `profile_loader.py` — locates, loads, and validates the public profile data file.
- `profile.json` — contains the approved public professional profile.
- `reviews/` — contains internal review and publication records.
- `snapshots/` — contains source snapshots or snapshot placeholders used during controlled ingestion.
- `scripts/` — contains supporting ingestion and maintenance scripts.

## Technology

The V1 uses:

- Python 3.14;
- FastAPI;
- the official MCP Python SDK;
- Streamable HTTP transport;
- JSON;
- Uvicorn;
- Render;
- GitHub.

The V1 intentionally does not require:

- a database;
- authentication;
- embeddings;
- a vector database;
- retrieval-augmented generation;
- a user interface;
- an external LLM integration.

## Local setup

Clone the repository:

```bash
git clone https://github.com/miodragstrak/ai-professional-profile.git
cd ai-professional-profile
```

Create and activate a Python 3.14 virtual environment:

```bash
python3.14 -m venv .venv
source .venv/bin/activate
```

Install the project:

```bash
pip install -e .
```

Start the server:

```bash
uvicorn main:app \
  --host 127.0.0.1 \
  --port 8000
```

Local endpoints:

```text
Health:
http://127.0.0.1:8000/health

MCP:
http://127.0.0.1:8000/mcp
```

## Basic MCP client test

With the project environment active:

```python
import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


MCP_URL = "https://ai-professional-profile.onrender.com/mcp"


async def main() -> None:
    async with streamable_http_client(MCP_URL) as streams:
        read_stream, write_stream, _ = streams

        async with ClientSession(
            read_stream,
            write_stream,
        ) as session:
            await session.initialize()

            tools = await session.list_tools()

            print([
                tool.name
                for tool in tools.tools
            ])

            result = await session.call_tool(
                "get_profile",
                {},
            )

            print(result.structuredContent)


asyncio.run(main())
```

Expected tool list:

```text
[
  "get_profile",
  "get_projects",
  "get_experience",
  "get_skills",
  "get_links"
]
```

## Deployment

The public implementation is deployed as a Render web service.

Production MCP endpoint:

```text
https://ai-professional-profile.onrender.com/mcp
```

The current Render URL will remain the primary V1 endpoint.

A custom professional domain may be introduced in a later version while preserving the Render endpoint during migration.

## V1 scope

The V1 proves the central product idea:

> An external AI system can connect to one public URL and retrieve controlled, structured, and user-approved professional information.

V1 includes:

- a public MCP server;
- a structured professional profile;
- professional experience;
- selected projects;
- categorized skills and domains;
- verification links;
- controlled review and publication records;
- local and production MCP tests.

## Current limitations

- The profile is manually curated.
- Source freshness is not yet automatically monitored.
- Education is not yet published through a dedicated MCP tool.
- The server does not independently verify employment or credentials.
- The server does not provide a conversational recruiter agent.
- There is no authentication or access-control layer in V1.
- The public endpoint currently uses a Render-provided domain.

## Potential next steps

Possible post-V1 improvements include:

- a custom professional domain;
- richer education and certification data;
- source freshness and verification timestamps;
- improved GitHub snapshot ingestion;
- automated consistency checks;
- recruiter-oriented summaries;
- role-fit and evidence tools;
- optional access control;
- additional professional profiles.

## Repository

```text
https://github.com/miodragstrak/ai-professional-profile
```
