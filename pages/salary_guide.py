"""
Salary Guide - Market salary information and negotiation tips
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils.salary_guide import (
    get_salary_range, get_negotiation_tips, get_all_roles,
    get_market_trends, calculate_compensation_increase
)

def show_salary_guide():
    """Display salary guide page"""
    st.markdown('<h1>💰 Salary Guide</h1>', unsafe_allow_html=True)

    st.markdown("""
        <div class="card" style="margin-bottom: 20px;">
            <div class="card-title">Market Intelligence</div>
            <div style="color: #D1D5DB; padding: 10px 0;">
                Research salary ranges, market trends, and negotiation strategies for your role.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Input section
    col1, col2, col3 = st.columns(3)

    with col1:
        role = st.selectbox(
            "Select Your Role",
            options=get_all_roles(),
            format_func=lambda x: x.replace("_", " ").title()
        )

    with col2:
        level = st.selectbox(
            "Experience Level",
            options=["entry_level", "mid_level", "senior"],
            format_func=lambda x: {
                "entry_level": "Entry Level (0-2 years)",
                "mid_level": "Mid Level (2-5 years)",
                "senior": "Senior (5+ years)"
            }.get(x, x)
        )

    with col3:
        if st.button("📊 Get Salary Info", use_container_width=True):
            st.session_state.show_salary_info = True

    st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

    # Display salary info if requested
    if st.session_state.get("show_salary_info", True):
        # Get salary data
        salary_range = get_salary_range(role, level)

        # Salary range cards
        st.markdown('<h2>Salary Range</h2>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
                <div class="card">
                    <div class="card-title">Minimum</div>
                    <div class="card-value">${salary_range['min']:,}</div>
                    <div class="card-desc">Base salary</div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div class="card hero-card">
                    <div class="card-title">Average</div>
                    <div class="card-value">${salary_range['avg']:,}</div>
                    <div class="card-desc">Market average</div>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
                <div class="card">
                    <div class="card-title">Maximum</div>
                    <div class="card-value">${salary_range['max']:,}</div>
                    <div class="card-desc">Top tier</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

        # Salary progression chart
        st.markdown('<h2>📈 Salary Progression by Level</h2>', unsafe_allow_html=True)

        progression_data = {}
        for lv in ["entry_level", "mid_level", "senior"]:
            sal = get_salary_range(role, lv)
            progression_data[lv] = sal["avg"]

        levels = [
            "Entry Level\n(0-2 years)",
            "Mid Level\n(2-5 years)",
            "Senior\n(5+ years)"
        ]
        salaries = [progression_data["entry_level"], progression_data["mid_level"], progression_data["senior"]]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=levels,
            y=salaries,
            marker=dict(color=['#9CA3AF', '#3B82F6', '#4ADE80']),
            text=[f"${s:,}" for s in salaries],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Salary: $%{y:,.0f}<extra></extra>'
        ))

        fig.update_layout(
            title="",
            xaxis_title="",
            yaxis_title="Average Salary ($)",
            plot_bgcolor="#111827",
            paper_bgcolor="#0B0F19",
            font=dict(color="#ffffff"),
            height=400,
            showlegend=False,
            yaxis=dict(tickformat="$,.0f")
        )

        st.plotly_chart(fig, use_container_width=True, theme="streamlit")

        st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

        # Negotiation tips
        tips = get_negotiation_tips(role)
        st.markdown('<h2>🤝 Negotiation Tips</h2>', unsafe_allow_html=True)

        for i, tip in enumerate(tips, 1):
            st.markdown(f"""
                <div class="card">
                    <div style="color: #D1D5DB; line-height: 1.6;">
                        <b>Tip {i}:</b> {tip}
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

        # Salary calculator
        st.markdown('<h2>💹 Salary Calculator</h2>', unsafe_allow_html=True)

        current_salary = st.number_input(
            "Your Current Salary ($)",
            min_value=0,
            value=int(salary_range["avg"]),
            step=5000
        )

        if current_salary > 0:
            comp_info = calculate_compensation_increase(current_salary, role, level)

            if not comp_info.get("error"):
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"""
                        <div class="card">
                            <div class="card-title">Market Average</div>
                            <div class="card-value">${comp_info['market_avg']:,}</div>
                            <div class="card-desc">vs your current</div>
                        </div>
                    """, unsafe_allow_html=True)

                with col2:
                    increase_pct = comp_info['increase_percent']
                    color = "#4ADE80" if increase_pct > 0 else "#9CA3AF"
                    st.markdown(f"""
                        <div class="card" style="border-color: {color};">
                            <div class="card-title">Potential Increase</div>
                            <div class="card-value" style="color: {color};">+{increase_pct:.0f}%</div>
                            <div class="card-desc">${comp_info['increase_amount']:,.0f}/year</div>
                        </div>
                    """, unsafe_allow_html=True)

    st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

    # Market trends
    st.markdown('<h2>📊 Market Trends</h2>', unsafe_allow_html=True)

    trends = get_market_trends()
    roles_list = list(trends.keys())[:10]  # Top 10
    salaries_list = [trends[r] for r in roles_list]

    fig = px.bar(
        x=salaries_list,
        y=roles_list,
        orientation='h',
        labels={'x': 'Average Salary ($)', 'y': 'Role'},
        color=salaries_list,
        color_continuous_scale=['#6B7280', '#3B82F6', '#4ADE80'],
        text=[f'${s:,}' for s in salaries_list],
        title=""
    )

    fig.update_layout(
        plot_bgcolor="#111827",
        paper_bgcolor="#0B0F19",
        font=dict(color="#ffffff"),
        height=400,
        showlegend=False,
        xaxis=dict(tickformat="$,.0f"),
        hovermode="y"
    )

    fig.update_traces(hovertemplate='<b>%{y}</b><br>Avg Salary: $%{x:,.0f}<extra></extra>')

    st.plotly_chart(fig, use_container_width=True, theme="dark")
