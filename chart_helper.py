import pandas as pd
import plotly.express as px


def suggest_chart(df: pd.DataFrame):
    """
    Looks at a query result DataFrame and decides:
    1. Whether a chart makes sense at all
    2. What type of chart fits best
    Returns a Plotly figure, or None if no chart is appropriate.
    """
    if df is None or df.empty:
        return None

    # Need at least 2 columns and more than 1 row to make a meaningful chart
    if df.shape[1] < 2 or df.shape[0] < 2:
        return None

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    non_numeric_cols = df.select_dtypes(exclude="number").columns.tolist()

    # No numeric column at all -> nothing to plot
    if not numeric_cols:
        return None

    x_col = non_numeric_cols[0] if non_numeric_cols else df.columns[0]
    y_col = numeric_cols[0]

    # --- Detect if x-axis looks like a date/time column ---
    is_date_like = "date" in x_col.lower()

    if is_date_like:
        fig = px.line(df, x=x_col, y=y_col, title=f"{y_col} over {x_col}", markers=True)

    # --- Few categories (<=6) with one numeric column -> pie chart works well ---
    elif len(non_numeric_cols) == 1 and df[x_col].nunique() <= 6:
        fig = px.pie(df, names=x_col, values=y_col, title=f"{y_col} by {x_col}")

    # --- Default: bar chart, good for rankings/comparisons ---
    else:
        fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")

    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        height=400
    )

    return fig