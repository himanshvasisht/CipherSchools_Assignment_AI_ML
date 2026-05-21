import os
import sys
import json
import time
import math
import requests
import streamlit as st
import pandas as pd

# Add workspace root and directories to python path for robust importing
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if current_dir not in sys.path:
    sys.path.append(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from backend.app_engine import run_review
from visualization.graph_viz import create_centrality_chart, create_risk_heatmap

st.set_page_config(
    page_title="Repository Intelligence & Review Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Simple & Modern Look
st.markdown("""
<style>
    .metric-card {
        background-color: #1e1e1e;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #b794f4;
    }
    .verify-badge {
        background-color: #742a2a;
        color: #feb2b2;
        padding: 8px 12px;
        border-radius: 6px;
        border: 1px solid #e53e3e;
        font-weight: bold;
        margin-bottom: 15px;
        display: inline-block;
    }
    .safe-badge {
        background-color: #1c4532;
        color: #9ae6b4;
        padding: 8px 12px;
        border-radius: 6px;
        border: 1px solid #38a169;
        font-weight: bold;
        margin-bottom: 15px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  SESSION STATE INITIALIZATION
# ─────────────────────────────────────────────────────────────────────────────
if "latest_result" not in st.session_state:
    st.session_state.latest_result = None
if "selected_idx" not in st.session_state:
    st.session_state.selected_idx = 0

# ─────────────────────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("Repository Analytics")
    st.subheader("Automated Source Code Auditor")
    st.markdown("---")

    st.markdown("### 1. Repository Configuration")
    repo_url = st.text_input(
        "GitHub Repo URL", 
        placeholder="https://github.com/owner/repo"
    )

    st.markdown("### 2. Provider Options")
    provider_choice = st.selectbox(
        "LLM Provider",
        ["Gemini", "OpenRouter", "OpenAI", "Ollama"]
    )
    
    # Render optional credential inputs depending on choice
    api_key_input = None
    if provider_choice == "OpenAI":
        api_key_input = st.text_input("OpenAI API Key", type="password", help="If left empty, will fall back to environment variables.")
    elif provider_choice == "Gemini":
        api_key_input = st.text_input("Gemini API Key", type="password", help="If left empty, will fall back to environment variables.")
    elif provider_choice == "OpenRouter":
        api_key_input = st.text_input("OpenRouter API Key", type="password", help="If left empty, will fall back to environment variables.")
    elif provider_choice == "Ollama":
        ollama_host_input = st.text_input("Ollama Host", value="http://localhost:11434")
        st.info("Ensure Ollama is running locally and model 'qwen2.5-coder:1.5b' is downloaded.")

    st.markdown("### 3. Execution Model")
    exec_mode = st.radio(
        "Execution Source",
        ["Direct Engine (Local)", "API Service (FastAPI)"],
        help="Direct Engine runs analysis locally inside Streamlit Cloud. API Service queries the FastAPI backend server."
    )

    st.markdown("### 4. Hardening & Security")
    simulate_stress = st.checkbox(
        "Simulate Stress Attack",
        value=False,
        help="Simulates a rate-limit denial-of-service stress attack to test request throttling controls."
    )

    st.markdown("---")
    analyze_clicked = st.button("Run Analysis", use_container_width=True, type="primary")

    if analyze_clicked:
        if not repo_url.strip():
            st.warning("Please enter a GitHub repository URL.")
        else:
            # Set chosen provider values in environment context dynamically
            os.environ["LLM_PROVIDER"] = provider_choice.lower()
            if api_key_input:
                if provider_choice == "OpenAI":
                    os.environ["OPENAI_API_KEY"] = api_key_input
                elif provider_choice == "Gemini":
                    os.environ["GEMINI_API_KEY"] = api_key_input
                elif provider_choice == "OpenRouter":
                    os.environ["OPENROUTER_API_KEY"] = api_key_input
            if provider_choice == "Ollama" and 'ollama_host_input' in locals():
                os.environ["OLLAMA_HOST"] = ollama_host_input

            st.session_state.latest_result = None
            st.session_state.selected_idx = 0

            with st.spinner("Cloning, scanning and parsing repository..."):
                try:
                    start_time = time.time()
                    if exec_mode == "Direct Engine (Local)":
                        result = run_review(repo_url.strip(), simulate_stress=simulate_stress)
                    else:
                        # FastAPI Mode
                        backend_url = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
                        response = requests.post(
                            f"{backend_url}/review",
                            json={"repo_url": repo_url.strip(), "simulate_stress": simulate_stress},
                            timeout=600
                        )
                        result = response.json()

                    elapsed = time.time() - start_time
                    if result.get("success"):
                        st.success(f"Analysis completed in {elapsed:.1f}s!")
                        st.session_state.latest_result = result
                    else:
                        st.error(result.get("error", "Analysis failed."))
                except Exception as e:
                    st.error(f"Error executing analysis: {e}")

# ─────────────────────────────────────────────────────────────────────────────
#  MAIN WINDOW
# ─────────────────────────────────────────────────────────────────────────────
result = st.session_state.latest_result

if not result:
    st.info("Paste a GitHub repository URL in the sidebar and click 'Run Analysis' to initiate the audit.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
#  DASHBOARD METRICS STAGES
# ─────────────────────────────────────────────────────────────────────────────
reviews = result.get("reviews", [])
total_findings = len(reviews)
avg_confidence = int(sum(r.get("confidence", 0) for r in reviews) / max(total_findings, 1))
vulnerabilities = sum(len(r.get("security", [])) for r in reviews)

st.title("📊 Repository Analysis Dashboard")
st.caption(f"Target Repository: {result.get('repo')}")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown(f'<div class="metric-card"><div style="font-size:0.8rem; color:#888;">FILES SCAN</div><div class="metric-value">{result.get("files_scanned", 0)}</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><div style="font-size:0.8rem; color:#888;">CHUNKS PROCESSED</div><div class="metric-value">{result.get("chunks", 0)}</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><div style="font-size:0.8rem; color:#888;">TOTAL FINDINGS</div><div class="metric-value">{total_findings}</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card"><div style="font-size:0.8rem; color:#888;">VULNERABILITIES</div><div class="metric-value" style="color:#e53e3e;">{vulnerabilities}</div></div>', unsafe_allow_html=True)
with col5:
    st.markdown(f'<div class="metric-card"><div style="font-size:0.8rem; color:#888;">AVG CONFIDENCE</div><div class="metric-value" style="color:#38a169;">{avg_confidence}%</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Visualizations Row
col_left, col_right = st.columns(2)
with col_left:
    heatmap = create_risk_heatmap(reviews)
    if heatmap:
        st.plotly_chart(heatmap, use_container_width=True)
with col_right:
    # Build simple centrality list for centrality chart
    centrality_map = {r["file"]: r["risk_score"] - r["confidence"]/10.0 for r in reviews} # Mock or compute
    centrality_fig = create_centrality_chart(centrality_map)
    if centrality_fig:
        st.plotly_chart(centrality_fig, use_container_width=True)

st.markdown("---")

# Audit Findings Panel
st.subheader("Audited Repository Findings")
filter_option = st.radio(
    "Filter by Confidence Threshold",
    ["Show All", "Verification Required (Low Confidence < 40%)", "High / Medium Confidence (>= 40%)"],
    horizontal=True
)

filtered_reviews = reviews
if filter_option == "Verification Required (Low Confidence < 40%)":
    filtered_reviews = [r for r in reviews if r.get("verify")]
elif filter_option == "High / Medium Confidence (>= 40%)":
    filtered_reviews = [r for r in reviews if not r.get("verify")]

if not filtered_reviews:
    st.info("No reviews matched this confidence filter.")
    st.stop()

# Layout: Split panel - Left finding selector, Right details
left_panel, right_panel = st.columns([1, 2])

with left_panel:
    st.markdown("#### Findings List")
    selected_name = st.selectbox(
        "Select Finding",
        [f"{r.get('risk_score')}/100 | {r.get('name')} ({r.get('type')})" for r in filtered_reviews],
        index=min(st.session_state.selected_idx, len(filtered_reviews) - 1)
    )
    
    # Resolve index of selected option
    selected_item = None
    for idx, r in enumerate(filtered_reviews):
        option_label = f"{r.get('risk_score')}/100 | {r.get('name')} ({r.get('type')})"
        if option_label == selected_name:
            selected_item = r
            st.session_state.selected_idx = idx
            break

with right_panel:
    if selected_item:
        st.markdown(f"### Finding Details: `{selected_item.get('name')}`")
        st.markdown(f"**Source File:** `{selected_item.get('file')}`")
        
        # Epistemic Humility Badge
        confidence = selected_item.get("confidence", 0)
        if selected_item.get("verify"):
            st.markdown(
                f'<div class="verify-badge">⚠️ VERIFY THIS (Low Confidence: {confidence}%)</div>', 
                unsafe_allow_html=True
            )
            st.warning("This review was generated with low overall confidence. Manual verification is highly recommended.")
        else:
            st.markdown(
                f'<div class="safe-badge">✓ High/Medium Confidence ({confidence}%)</div>', 
                unsafe_allow_html=True
            )

        tab_review, tab_compare, tab_security = st.tabs(
            ["Auditor Analysis", "Proposed Refactoring", "Vulnerability Scanner"]
        )

        with tab_review:
            st.markdown(selected_item.get("llm_review", "No reviews generated."))
            
        with tab_compare:
            st.markdown("### Proposed Refactoring & Patches")
            # We display the explanation part (removing code snippet if already present to avoid duplication)
            full_repair = selected_item.get("repair_suggestions", "No repair suggestions available.")
            explanation = full_repair.split("```python")[0] if "```python" in full_repair else full_repair
            st.markdown(explanation)
            
            st.markdown("---")
            col_orig, col_fix = st.columns(2)
            with col_orig:
                st.markdown("**Original Code Segment**")
                st.code(selected_item.get("code_preview", ""), language="python")
            with col_fix:
                st.markdown("**Refactored Code**")
                st.code(selected_item.get("repaired_code", ""), language="python")
            
        with tab_security:
            sec_report = selected_item.get("security", [])
            if not sec_report:
                st.success("No static analysis vulnerabilities flagged.")
            else:
                for issue in sec_report:
                    st.error(f"**{issue.get('test_id')}**: {issue.get('issue_text')}")
                    st.markdown(f"Severity: `{issue.get('issue_severity')}` | Confidence: `{issue.get('issue_confidence')}`")

# Download Results Option
st.markdown("---")
st.download_button(
    "Download Full Review JSON",
    json.dumps(result, indent=2),
    file_name=f"revue_report_{int(time.time())}.json",
    mime="application/json",
    use_container_width=True
)