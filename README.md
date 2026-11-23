# 100-App API & MCP Buildability Research

## Executive summary

This project evaluates 100 applications across 10 categories and demonstrates a working research workflow using the Composio SDK and Composio MCP.

### Deliverables and measured status

- 100 applications catalogued across 10 categories.
- 500 saved web-search result records retained in `data/search_results.json`.
- Composio session creation, MCP initialization, tool discovery and a Keenable web-search call were successfully demonstrated during development.
- The MCP research agent ran over the 100-app catalogue and reused saved search results; it did not independently verify all 100 vendors.
- A searchable HTML case study, an 81-app evidence-review report, CSV datasets and source code are included.

### Evidence status (100 rows)

| Status | Rows | Meaning |
|---|---:|---|
| `verified_official_docs` | 5 | Stronger first-party documentation review was completed for the row. |
| `partially_verified_official_docs` | 14 | Some API/authentication claims have first-party support; other fields remain qualified. |
| `page_inspected_partial_claims_verified` | 43 | At least one first-party page was opened and specific claims were verified; remaining fields still require validation. |
| `official_sources_reviewed_needs_page_validation` | 36 | First-party documentation trails identified, but no readable page-level validation completed in this pass. |
| `source_gap_manual_research_required` | 2 | Fanbasis and Sherlock need additional first-party source discovery. |

**Do not claim that all 100 applications are fully verified.** Page-inspected records verify only specific claims listed in their evidence notes; they are not comprehensive audits of every field. The 56 MCP references counted in the 81-app review are search-snippet signals, not 56 confirmed production-ready account integrations. Absence of a discovered MCP source is not proof that none exists.

## Key cross-category findings

1. API availability is not equivalent to buildability. Credential provisioning, scopes, account permissions, plan eligibility, rate limits, pagination, webhooks and read/write coverage determine practical feasibility.
2. MCP is an additional integration surface, not a guarantee of complete product coverage. Tool inventory, authentication, vendor ownership and destructive-write controls must be checked per product.
3. OAuth is generally better suited to multi-tenant, user-delegated integrations. Static API keys and personal tokens are simpler for single-account prototypes but require careful rotation, least privilege and secure storage.
4. Advertising, finance, enrichment and enterprise platforms can gate production access through developer review, partner programmes, paid plans, usage credits or account eligibility.
5. The catalogue includes different product types: hosted SaaS, consumer apps, APIs, local CLIs and agent-native tools. A local CLI may be automatable without a hosted API; a consumer UI does not imply a supported public API.

## Repository structure

- `data/apps_research.csv` — current working research matrix.
- `data/apps_research_final.csv` — synchronized final snapshot of the current matrix.
- `data/apps_research_draft.csv` — preliminary automated draft.
- `data/search_results.json` — saved web-search results.
- `outputs/case_study.html` — searchable 100-app case study.
- `outputs/analysis_81.html` — evidence review and cross-category analysis for the 81 formerly draft rows.
- `outputs/verification_progress.html` — verification status overview.
- `outputs/analysis_81_summary.json` — machine-readable 81-app review counts.
- `outputs/page_inspection_log.csv` — rapid page-inspection findings.
- `outputs/page_inspection_summary.json` — inspection counts and limitations.
- `src/mcp_research_agent.py` — Composio MCP research pipeline.
- `src/inspect_mcp.py` — MCP connection/tool inspection.
- `src/research_agent.py` — original direct Keenable research pipeline.
- `src/audit_search_results.py`, `src/populate_evidence.py`, `src/draft_research_matrix.py` — data preparation and audit scripts.

## Setup (macOS)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Add your own credentials to `.env` locally. Never commit or share `.env`, API keys, access tokens or MCP session URLs.

## Reproduce the saved workflow

```bash
python src/composio_session_check.py
python src/mcp_research_agent.py
```

The MCP agent requires valid local Composio credentials and the configured Keenable tool connection. It reuses existing results where present. The saved 500-result dataset is included; do not rerun network searches just to reproduce the submission.

## Method and limitations

For each application, the target dimensions are purpose, authentication, credential access model, API type/breadth, MCP/agent tooling, buildability, blockers and evidence. First-party vendor documentation is preferred. Search-result snippets and links are discovery leads; claims must be checked against the full documentation page before being treated as verified.

No live production API integration was tested against all 100 vendors. Buildability verdicts are qualitative and depend on customer tenant, permissions, plan, rate limits and intended use case. Vendor API/MCP availability and commercial terms can change.

## Final submission checklist

- [x] 100-app catalogue and 10 categories.
- [x] Saved 500-result research dataset.
- [x] Composio SDK/MCP workflow demonstrated.
- [x] CSV research matrix and HTML case study.
- [x] First-pass cross-category analysis.
- [ ] Page-level validation of the 79 official-source trails.
- [ ] Resolve Fanbasis and Sherlock source gaps.
- [ ] Confirm current vendor plans, limits, scopes and MCP tool permissions before production recommendations.


## Two-minute reviewer case study and publishing

The single-page reviewer-facing case study is `index.html` (also copied to `outputs/product_ops_case_study.html`). It includes the headline findings, 100-app searchable matrix, agent workflow, demonstrated Composio/MCP proof, human checkpoints, verification coverage and limitations.

### Publish a live page with GitHub Pages

1. Create or use a public GitHub repository for this project.
2. Upload the project contents, including `index.html`, `data/`, `outputs/`, `src/`, `requirements.txt` and this README. Do not upload `.env`.
3. In the repository, open **Settings → Pages**.
4. Choose **Deploy from a branch**, select `main` and `/ (root)`, then save.
5. Wait for GitHub Pages to publish; copy the generated URL into the assignment submission.

The public repository URL and live Pages URL are intentionally not fabricated in this package; they must be created from the user's GitHub account. The HTML is already prepared as the root `index.html` for this deployment path.