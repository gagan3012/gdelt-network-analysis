import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import networkx as nx

st.set_page_config(
page_title="Ex-stream-ly Cool App",
page_icon="🧊",
layout="wide")
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file:
    df = pd.read_csv(uploaded_file)

labels = {i: i for i in dict(G.nodes).keys()}
    G = nx.from_pandas_edgelist(df, 'a_name', 'b_name', edge_attr='COUNT')

layt = nx.spring_layout(G, dim=3, seed=18)
N = list(G.nodes())
E = list(G.edges())

Xn=[layt[k][0] for k in (N)]# x-coordinates of nodes
Yn=[layt[k][1] for k in (N)]# y-coordinates
Zn=[layt[k][2] for k in (N)]# z-coordinates
Xe=[]
Ye=[]
Ze=[]
for e in E:
    Xe+=[layt[e[0]][0],layt[e[1]][0], None]# x-coordinates of edge ends
    Ye+=[layt[e[0]][1],layt[e[1]][1], None]
    Ze+=[layt[e[0]][2],layt[e[1]][2], None]

trace1=go.Scatter3d(x=Xe,
               y=Ye,
               z=Ze,
               mode='lines',
               line=dict(color='rgb(125,125,125)', width=1),
               hoverinfo='none'
               )

trace2=go.Scatter3d(x=Xn,
               y=Yn,
               z=Zn,
               mode='markers',
               name='Persons',
               marker=dict(symbol='circle',
                             size=6,
                             color=df['COUNT'],
                             colorscale='Viridis',
                             line=dict(color='rgb(50,50,50)', width=0.5),
                           colorbar=dict(
                thickness=15, title="COUNT", xanchor="left", titleside="right"
            ),
                             ),
               text=N,
               hoverinfo='all',
               )


axis=dict(showbackground=False,
          showline=False,
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title=''
          )

layout = go.Layout(
         title="Network Analysis of GDELT data",
         width=1000,
         height=1000,
         showlegend=False,
         scene=dict(
             xaxis=dict(axis),
             yaxis=dict(axis),
             zaxis=dict(axis),
        ),
     margin=dict(
        t=100
    ),
    hovermode='closest',
    annotations=[
           dict(
           showarrow=False,
            text="Data source: GDELT",
            xref='paper',
            yref='paper',
            x=0,
            y=0.1,
            xanchor='left',
            yanchor='bottom',
            font=dict(
            size=14
            )
            )
        ],    )

data=[trace1, trace2]
fig=go.Figure(data=data, layout=layout)

st.plotly_chart(fig, use_container_width=True)
