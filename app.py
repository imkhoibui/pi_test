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
                    className='volcano-graph',
                    id='volcano-graph',
                    figure=dashbio.VolcanoPlot(
                        dataframe=df,
                        effect_size='log2FoldChange',
                        p='pvalue',
                        snp='padj',
                        gene='Gene Name',
                        annotation='DEG',
                        highlight_color='#119DFF',
                        width=600,
                        height=800,
                        xlabel='Log2(Fold Change)',
                        ylabel='-Log10(PValue)',
                        title='DEG between D2 and D4 Mock EpiAir'
                    )
                ),
                html.Div(
                    className='filter-block',
                    children=[
                    html.Div(
                        className='filter-item',
                        children=[
                        'Select the genes you wish to highlight',
                        html.Br(),
                        dcc.Checklist(
                            id='hl-select',
                            options=['Upregulated', 'Downregulated'],
                            value=['Upregulated', 'Downregulated']
                        )
                    ]),
                    html.Div(
                        className='filter-item',
                        children=[
                        'Select the top number of most differentially expressed genes',
                        html.Br(),
                        dcc.RangeSlider(
                            id='volcano-input',
                            min=0,
                            max=50,
                            step=5,
                            marks={i: {'label': str(i)} for i in range(5, 51, 5)},
                            value=[0,5]
                        ),
                    ]),
                ]),
            ],
        ),
    ])

def callbacks(_app, df):
    @_app.callback(
        Output('volcano-graph', 'figure'),
        [Input('volcano-input', 'value'),
         Input('hl-select', 'value')]
    )

    def update_hlgenes(hl_range, hl_select):
        min_r, max_r = hl_range

        hl_genes = []
        for mode in hl_select:
            hl_genes += df[df['DEG'] == mode]['Gene Name'].to_list()

        return dashbio.VolcanoPlot(
            dataframe=df,
            effect_size='log2FoldChange',
            p='pvalue',
            snp='padj',
            gene='Gene Name',
            annotation='DEG',
            highlight=hl_genes,
            highlight_color='#119DFF',
            width=600,
            height=800,
            xlabel='Log2(Fold Change)',
            ylabel='-Log10(PValue)',
            title='DEG between D2 and D4 Mock EpiAir'
        )


def run_app(data_path):
    df = pd.read_excel(data_path)
    df = cal_genes(df)

    app = Dash(__name__)
    app.layout = layout(df)
    callbacks(app, df)
    return app

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path')
    args = parser.parse_args()

    # data_path = 'data/Set_1_D4_Mock_EpiAir_vs_Set_1_D2_Mock_EpiAir_DESeq_results.xlsx'
    app = run_app(args.data_path)
    app.run_server(debug=True, port=8050)