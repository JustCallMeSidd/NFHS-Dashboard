import streamlit as st
from utils.data_loader import load_nfhs_data, get_column_info
from utils.visualizations import bar_indicator, heatmap_correlation, line_indicator
from utils.rag_qa import generate_answer

st.set_page_config(page_title="NFHS Health Dashboard", layout="wide")

# Custom CSS for modern styling with #016B61 background
st.markdown("""
    <style>
    /* Main background - CHANGED TO #016B61 */
    .stApp {
        background: #016B61;
    }
    
    /* Header container */
    .header-container {
        background: linear-gradient(135deg, #014d45 0%, #016B61 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        margin-bottom: 2rem;
        text-align: center;
        border: 2px solid rgba(255,255,255,0.1);
    }
    
    /* Title styling */
    .main-title {
        color: black !important;
        font-size: 3.5rem;
        font-weight: 800;
        margin: 1rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        letter-spacing: -1px;
    }
    
    .subtitle {
        color: rgba(255,255,255,0.95);
        font-size: 1.3rem;
        font-weight: 400;
        margin-top: 0.5rem;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #014d45 0%, #013a35 100%);
    }
    
    [data-testid="stSidebar"] h2 {
        color: black !important;
    }
    
    [data-testid="stSidebar"] label {
        color: black !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox, [data-testid="stSidebar"] .stMultiSelect {
        background-color: rgba(255,255,255,0.95);
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(90deg, #014d45 0%, #01857a 100%);
        color: black !important;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 2rem 0 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        border: 2px solid rgba(255,255,255,0.1);
    }
    
    /* Stats cards */
    .stat-card {
        background: rgba(255,255,255,0.95);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        border-left: 5px solid #01857a;
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.4);
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #016B61;
        margin: 0;
    }
    
    .stat-label {
        font-size: 1rem;
        color: #6c757d;
        margin-top: 0.5rem;
    }
    
    /* Info boxes */
    .info-box {
        background: rgba(0,0,0,0.95);
        border-left: 4px solid #01857a;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 3px 15px rgba(0,0,0,0.3);
    }
    
    /* Question box */
    .question-box {
        background: rgba(255,255,255,0.95);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 25px rgba(0,0,0,0.3);
        border: 2px solid rgba(1,107,97,0.3);
    }
    
    /* Answer box */
    .answer-box {
        background: linear-gradient(135deg, #e8f5f4 0%, #c8e6e4 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #01857a;
        margin-top: 1rem;
        box-shadow: 0 3px 15px rgba(0,0,0,0.2);
    }
    
    /* Chart containers */
    .chart-container {
        background: rgba(255,255,255,0.95);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        margin: 1rem 0;
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #014d45 0%, #01857a 100%);
        color: black !important;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(0,0,0,0.4);
    }
    
    /* Horizontal rule */
    hr {
        border-color: rgba(255,255,255,0.2);
    }
    
    /* Footer styling */
    .footer-text {
        color: rgba(255,255,255,0.9) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header with logo and title
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.png", width=200)
    st.markdown('<h1 class="main-title">NFHS Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Comprehensive Health Indicators & Analytics Platform</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Load data
df = load_nfhs_data()
column_info = get_column_info()

# Sidebar Filters
st.sidebar.markdown("## 🎯 Filters & Options")
st.sidebar.markdown("---")
states = st.sidebar.multiselect("🗺️ Select States/UTs", df['states_uts'].unique(), default=["India"])
area_options = df['area'].unique()
area = st.sidebar.selectbox("📍 Select Area", area_options)

# Filter dataframe
filtered_df = df[df['area']==area]
if states:
    filtered_df = filtered_df[filtered_df['states_uts'].isin(states)]

# Key metrics at the top
st.markdown("---")
metric_cols = st.columns(4)
with metric_cols[0]:
    st.markdown("""
        <div class="stat-card">
            <p class="stat-value">{}</p>
            <p class="stat-label">📊 States Selected</p>
        </div>
    """.format(len(states) if states else 0), unsafe_allow_html=True)

with metric_cols[1]:
    st.markdown("""
        <div class="stat-card">
            <p class="stat-value">{}</p>
            <p class="stat-label">📈 Total Indicators</p>
        </div>
    """.format(len(df.columns) - 2), unsafe_allow_html=True)

with metric_cols[2]:
    st.markdown("""
        <div class="stat-card">
            <p class="stat-value">{}</p>
            <p class="stat-label">🌐 Total Records</p>
        </div>
    """.format(len(filtered_df)), unsafe_allow_html=True)

with metric_cols[3]:
    st.markdown("""
        <div class="stat-card">
            <p class="stat-value">{}</p>
            <p class="stat-label">📍 Area Type</p>
        </div>
    """.format(area), unsafe_allow_html=True)

# Show top indicators
st.markdown('<div class="section-header">📌 Top Indicators Overview</div>', unsafe_allow_html=True)
st.markdown('<div class="info-box">Displaying key health indicators across selected regions for comparative analysis.</div>', unsafe_allow_html=True)
top_cols = df.columns[2:20]  # demo: first 20 indicators
st.dataframe(filtered_df[['states_uts'] + list(top_cols)].round(2), use_container_width=True)

# Multi-state comparison bar charts
st.markdown('<div class="section-header">📊 Multi-State Comparison</div>', unsafe_allow_html=True)
st.markdown('<div class="info-box">Interactive visualizations comparing health indicators across different states and union territories.</div>', unsafe_allow_html=True)

for col in top_cols[:5]:  # first 5 top indicators
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig = bar_indicator(filtered_df, x_col='states_uts', y_col=col, title=f"{col} Comparison")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Heatmap correlation
st.markdown('<div class="section-header">🔗 Correlation Heatmap of Top Indicators</div>', unsafe_allow_html=True)
st.markdown('<div class="info-box">Explore relationships and correlations between different health indicators to identify patterns and insights.</div>', unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
fig = heatmap_correlation(filtered_df, top_cols, title="Correlation Across States")
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Line charts for trends
st.markdown('<div class="section-header">📈 Trend Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="info-box">Analyze trends and patterns in health indicators over time and across regions.</div>', unsafe_allow_html=True)

for col in top_cols[:3]:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig = line_indicator(filtered_df, x_col='states_uts', y_col=col, title=f"{col} Trend Comparison")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# RAG Question Answering
st.markdown('<div class="section-header">💡 AI-Powered Insights</div>', unsafe_allow_html=True)
st.markdown('<div class="question-box">', unsafe_allow_html=True)
st.markdown("### Ask a Question about NFHS Data")
st.markdown("Get instant answers powered by AI based on the current dataset filters.")
question = st.text_input("Enter your question here:", placeholder="e.g., What is the average maternal mortality rate?")
if question:
    with st.spinner('🤔 Analyzing data and generating answer...'):
        context = filtered_df.to_string()
        answer = generate_answer(question, context)
    st.markdown(f'<div class="answer-box"><strong>💬 Answer:</strong><br/>{answer}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <p class='footer-text' style='font-size: 0.9rem;'>📊 NFHS Health Dashboard | Powered by Streamlit & AI</p>
        <p class='footer-text' style='font-size: 0.8rem;'>Data sourced from National Family Health Survey (NFHS)</p>
    </div>
""", unsafe_allow_html=True)