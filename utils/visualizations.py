import plotly.express as px
import plotly.graph_objects as go

def bar_indicator(df, x_col, y_col, color_col=None, title=""):
    """
    Bar chart for comparison
    """
    fig = px.bar(
        df, x=x_col, y=y_col, color=color_col or x_col,
        text=y_col, title=title,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(yaxis=dict(range=[0, df[y_col].max()*1.2]), title=dict(x=0.5))
    return fig

def line_indicator(df, x_col, y_col, color_col=None, title=""):
    """
    Line chart for trends
    """
    fig = px.line(df, x=x_col, y=y_col, color=color_col, title=title, markers=True)
    fig.update_layout(yaxis=dict(range=[0, df[y_col].max()*1.2]), title=dict(x=0.5))
    return fig

def heatmap_correlation(df, cols, title="Correlation Heatmap"):
    """
    Heatmap for correlation between selected indicators
    """
    corr = df[cols].corr()
    fig = go.Figure()
    fig.add_trace(go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale='Viridis',
        zmin=-1,
        zmax=1,
        colorbar=dict(title="Correlation"),
        hovertemplate='Indicator X: %{y}<br>Indicator Y: %{x}<br>Correlation: %{z:.2f}<extra></extra>'
    ))

    # Add annotations
    for i, row in enumerate(corr.values):
        for j, val in enumerate(row):
            fig.add_annotation(
                x=corr.columns[j],
                y=corr.columns[i],
                text=f"{val:.2f}",
                showarrow=False,
                font=dict(color="white" if abs(val) > 0.5 else "black")
            )

    fig.update_layout(title=title, xaxis=dict(tickangle=-45), width=900, height=900)
    return fig
