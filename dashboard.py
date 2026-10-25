import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Cargar dataset
df = pd.read_csv(r"data/Software_Defect_Prediction_Dataset.csv")

buggy = df[df["defect_label"]=="Buggy"]
clean = df[df["defect_label"]=="Clean"]

# KPIs
buggy_mean_debt = buggy["technical_debt_score"].mean()
clean_mean_debt = clean["technical_debt_score"].mean()
buggy_mean_complexity = buggy["cyclomatic_complexity"].mean()
clean_mean_complexity = clean["cyclomatic_complexity"].mean()
buggy_mean_methods = buggy["method_count"].mean()
clean_mean_methods = clean["method_count"].mean()

# Gráficas
fig_hist = px.histogram(df, x="cyclomatic_complexity", color="defect_label",
                        barmode="overlay", nbins=30,
                        title="Distribución de Complejidad Ciclomática (Buggy vs Clean)")

fig_box_methods = px.box(df, x="defect_label", y="method_count", color="defect_label",
                         title="Distribución del Número de Métodos (Buggy vs Clean)",
                         points="outliers")

fig_flow = go.Figure()
fig_flow.add_trace(go.Scatter(
    x=[buggy_mean_debt, clean_mean_debt],
    y=[buggy_mean_complexity, clean_mean_complexity],
    mode="markers+lines+text",
    text=["Buggy", "Clean"],
    textposition="top center",
    marker=dict(color=["red", "green"], size=12),
    line=dict(dash="dot", color="blue"),
))
fig_flow.update_layout(title="Flujo de Métricas Promedio: Buggy → Clean",
                       xaxis_title="Puntaje de Deuda Técnica Promedio",
                       yaxis_title="Complejidad Ciclomática Promedio")

# App
app = dash.Dash(__name__)

app.layout = html.Div(style={"fontFamily": "Arial, sans-serif", "backgroundColor": "#f9f9f9"}, children=[
    html.H1("Dashboard: Métricas de Código y Bugs",
            style={"textAlign": "center", "color": "#2c3e50", "marginBottom": "40px"}),

    # KPI Cards
    html.Div([
        html.Div([
            html.H3("Deuda Técnica Promedio Buggy", style={"color": "#c0392b"}),
            html.P(f"{buggy_mean_debt:.2f}", style={"fontSize": "28px", "fontWeight": "bold"})
        ], style={"backgroundColor": "#fff", "padding": "20px", "margin": "10px", "borderRadius": "8px",
                  "boxShadow": "0 2px 5px rgba(0,0,0,0.1)", "width": "30%", "display": "inline-block", "textAlign": "center"}),

        html.Div([
            html.H3("Deuda Técnica Promedio Clean", style={"color": "#27ae60"}),
            html.P(f"{clean_mean_debt:.2f}", style={"fontSize": "28px", "fontWeight": "bold"})
        ], style={"backgroundColor": "#fff", "padding": "20px", "margin": "10px", "borderRadius": "8px",
                  "boxShadow": "0 2px 5px rgba(0,0,0,0.1)", "width": "30%", "display": "inline-block", "textAlign": "center"}),

        html.Div([
            html.H3("Promedio Métodos", style={"color": "#2980b9"}),
            html.P(f"Buggy: {buggy_mean_methods:.1f} | Clean: {clean_mean_methods:.1f}",
                   style={"fontSize": "22px", "fontWeight": "bold"})
        ], style={"backgroundColor": "#fff", "padding": "20px", "margin": "10px", "borderRadius": "8px",
                  "boxShadow": "0 2px 5px rgba(0,0,0,0.1)", "width": "30%", "display": "inline-block", "textAlign": "center"})
    ], style={"textAlign": "center", "marginBottom": "40px"}),

    # Gráfico principal
    html.Div([dcc.Graph(figure=fig_flow)], style={"marginBottom": "40px"}),

    # Gráficas secundarias
    html.Div([
        html.Div([dcc.Graph(figure=fig_hist)], style={"width": "48%", "display": "inline-block", "padding": "10px"}),
        html.Div([dcc.Graph(figure=fig_box_methods)], style={"width": "48%", "display": "inline-block", "padding": "10px"})
    ]),

    # Key Insight Card
    html.Div([
        html.H3("Key Insight", style={"color": "#34495e"}),
        html.P("Los módulos con mayor complejidad ciclomática tienen más probabilidad de contener bugs. "
               "Refactorizar reduce el riesgo aunque aumente el tamaño del código.",
               style={"fontSize": "18px", "lineHeight": "1.5"})
    ], style={"backgroundColor": "#ecf0f1", "padding": "20px", "margin": "20px", "borderRadius": "8px",
              "boxShadow": "0 2px 5px rgba(0,0,0,0.1)", "textAlign": "center"})
])

server = app.server

if __name__ == "__main__":
    app.run(debug=True)
