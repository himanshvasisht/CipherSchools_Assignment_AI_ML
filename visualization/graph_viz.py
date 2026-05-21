import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_centrality_chart(centrality_scores):
    """
    Renders a bar chart of dependency centrality.
    """
    if not centrality_scores:
        return None
        
    df = pd.DataFrame([
        {"File": f.split("/")[-1], "Centrality": score}
        for f, score in centrality_scores.items()
    ]).sort_values(by="Centrality", ascending=False).head(10)
    
    fig = px.bar(
        df, 
        x="Centrality", 
        y="File", 
        orientation="h",
        title="Top Centrality Files (Dependencies)",
        color="Centrality",
        color_continuous_scale="Purples",
        template="plotly_dark"
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(l=20, r=20, t=40, b=20), height=300)
    return fig

def create_risk_heatmap(reviews):
    """
    Renders a scatter/bubble plot or bar chart representing code risk.
    """
    if not reviews:
        return None
        
    df = pd.DataFrame([
        {
            "File": item["file"].split("/")[-1],
            "Risk Score": item["risk_score"],
            "Confidence": item["confidence"],
            "Verification Required": "Yes" if item["verify"] else "No"
        }
        for item in reviews
    ])
    
    fig = px.scatter(
        df,
        x="Risk Score",
        y="Confidence",
        size="Risk Score",
        color="Verification Required",
        hover_name="File",
        title="Risk vs Confidence Matrix",
        color_discrete_map={"Yes": "#EF4444", "No": "#10B981"},
        template="plotly_dark"
    )
    
    # Add a horizontal line at 40% confidence threshold
    fig.add_hline(y=40, line_dash="dash", line_color="#EF4444", annotation_text="Verification Threshold (40%)")
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=300)
    return fig
