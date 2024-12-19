from dash import Dash
from dash import Input, Output, dcc, html

import dash_bio as dashbio
import pandas as pd 
import argparse
import os

from helper import *


def layout(df):
    return html.Div([
        html.H2('Differentially expressed genes visualization'),
        html.Div(
            className='plot-block',
            children=[
                dcc.Graph(
                    id='volcano-graph',
                    figure=dashbio.VolcanoPlot(
                        dataframe=df,
                        effect_size='log2FoldChange',
                        p='pvalue',
                        snp='padj',
                        gene='Gene Name',
                        annotation='Gene Name',
                        width=600,
                        height=800,
                    )
                ),
                html.Div([
                    'Select the genes you wish to highlight',
                    html.Br(),
                    dcc.Checklist(
                        id='hl_select',
                        options=['Upregulated', 'Downregulated'],
                        value=['Upregulated']
                    )
                ]),
                html.Div([
                    'Select the top number of most differentially expressed genes',
                    html.Br(),
                    dcc.RangeSlider(
                        id='volcano-input',
                        min=5,
                        max=50,
                        step=5,
                        marks={i: {'label': str(i)} for i in range(5, 51, 5)},
                        value=[5,5]
                    ),
                ]),
            ],
        ),
    ])

def callbacks(_app, df):
    @_app.callback(
        Output('volcano-graph', 'figure'),
        Input('volcano-input', 'value')
    )
    def update_volcanoplot(effects):
        return dashbio.VolcanoPlot(
            dataframe=df,
            effect_size='log2FoldChange',
            p='pvalue',
            snp='padj',
            gene='Gene Name',
            annotation='Gene Name',
            width=600,
            height=800,
        )
    
    @_app.callback(
        Output(),
        Input(),
    )
    def update_hlgenes(effects):
        return


def run_app(data_path):
    df = pd.read_excel(data_path)
    df = cal_genes(df)
    app = Dash(__name__)
    app.layout = layout(df)
    callbacks(app, df)
    return app

if __name__ == "__main__":
    data_path = 'data/Set_1_D4_Mock_EpiAir_vs_Set_1_D2_Mock_EpiAir_DESeq_results.xlsx'
    app = run_app(data_path)
    app.run_server(debug=True, port=8050)