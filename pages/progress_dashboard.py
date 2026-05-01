"""
Progress Dashboard - Track resume analysis history and improvements
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils.progress_tracker import (
    get_score_history, get_improvement_percentage, get_score_trend_data, get_statistics
)
from datetime import datetime
import csv
import io

def show_progress_dashboard():
    """Display progress dashboard"""
    st.markdown('<h1>📊 Progress Dashboard</h1>', unsafe_allow_html=True)

    user_id = st.session_state.user_id

    # Get data
    history = get_score_history(user_id)
    improvement = get_improvement_percentage(user_id)
    trend_data = get_score_trend_data(user_id, limit=12)
    stats = get_statistics(user_id)

    # Top metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
            <div class="card">
                <div class="card-title">Total Analyses</div>
                <div class="card-value">{}</div>
                <div class="card-desc">Resumes reviewed</div>
            </div>
        """.format(stats['total_analyses']), unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="card">
                <div class="card-title">Average Score</div>
                <div class="card-value">{}</div>
                <div class="card-desc">/10</div>
            </div>
        """.format(stats['avg_score']), unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="card">
                <div class="card-title">Best Score</div>
                <div class="card-value">{}</div>
                <div class="card-desc">/10</div>
            </div>
        """.format(stats['max_score']), unsafe_allow_html=True)

    with col4:
        improvement_text = f"+{improvement['improvement']}%" if improvement['improvement'] > 0 else f"{improvement['improvement']}%"
        color = "#4ADE80" if improvement['improvement'] >= 0 else "#EF4444"
        st.markdown(f"""
            <div class="card" style="border-color: {color};">
                <div class="card-title">Improvement</div>
                <div class="card-value" style="color: {color};">{improvement_text}</div>
                <div class="card-desc">vs first score</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

    # Score trend chart
    if trend_data:
        st.markdown('<h2>📈 Score Trend</h2>', unsafe_allow_html=True)

        scores = [d['score'] for d in trend_data]
        dates = [d['date'] for d in trend_data]
        roles = [d['role'] for d in trend_data]

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=dates,
            y=scores,
            mode='lines+markers',
            name='Score',
            line=dict(color='#3B82F6', width=3),
            marker=dict(size=10, color='#3B82F6'),
            fill='tozeroy',
            fillcolor='rgba(59, 130, 246, 0.1)',
            hovertemplate='<b>%{text}</b><br>Date: %{x}<br>Score: %{y}/10<extra></extra>',
            text=roles
        ))

        # Add threshold line
        fig.add_hline(y=7, line_dash="dash", line_color="gray", annotation_text="Good (7+)")

        fig.update_layout(
            title="",
            xaxis_title="Date",
            yaxis_title="Score (/10)",
            hovermode="x unified",
            plot_bgcolor="#111827",
            paper_bgcolor="#0B0F19",
            font=dict(color="#ffffff"),
            yaxis=dict(range=[0, 10]),
            height=400
        )

        st.plotly_chart(fig, use_container_width=True, theme="dark")
    else:
        st.info("📤 No analyses yet. Upload a resume to get started!")

    st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

    # Analysis history table
    st.markdown('<h2>📋 Analysis History</h2>', unsafe_allow_html=True)

    if history:
        # Create display data
        display_data = []
        for record in history:
            display_data.append({
                "Date": record['timestamp'].split(' ')[0],
                "Time": record['timestamp'].split(' ')[1][:5] if len(record['timestamp'].split(' ')) > 1 else "",
                "Role": record.get('target_role', 'General'),
                "Score": f"{record['score']}/10",
                "File": record.get('filename', 'Unknown')
            })

        st.dataframe(display_data, use_container_width=True, hide_index=True)

        # Export button
        csv_data = io.StringIO()
        writer = csv.DictWriter(csv_data, fieldnames=["Date", "Time", "Role", "Score", "File"])
        writer.writeheader()
        writer.writerows(display_data)

        st.download_button(
            label="📥 Download as CSV",
            data=csv_data.getvalue(),
            file_name="resumeiq_analysis_history.csv",
            mime="text/csv",
            key="download_history"
        )
    else:
        st.info("No analyses recorded yet.")

    st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

    # Score distribution
    if history and len(history) > 1:
        st.markdown('<h2>📊 Score Distribution</h2>', unsafe_allow_html=True)

        scores = [r['score'] for r in history]

        fig = go.Figure(data=[
            go.Histogram(
                x=scores,
                nbinsx=10,
                marker=dict(color='#3B82F6'),
                hovertemplate='Score: %{x}<br>Count: %{y}<extra></extra>'
            )
        ])

        fig.update_layout(
            title="",
            xaxis_title="Score (/10)",
            yaxis_title="Frequency",
            plot_bgcolor="#111827",
            paper_bgcolor="#0B0F19",
            font=dict(color="#ffffff"),
            height=300,
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True, theme="dark")
