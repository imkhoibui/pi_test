from dash import Dash
from dash import Input, Output, dcc, html

import dash_bio as dashbio
import pandas as pd 
import argparse
import os

from helper import *
from content import *

def layout(df):
    return html.Div([
        html.H2(className='header-block',
                children='Differentially expressed genes visualization'),
        html.Div(
            className='plot-block',
            children=[
                dcc.Graph(
                    className='volcano-graph',
                    id='volcano-graph',
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
                            options=[{'label' : 'Upregulated', 'value' : 'upregulated'},
                                      {'label' : 'Downregulated', 'value' : 'downregulated'}],
                            value=['downregulated', 'upregulated']
                        )
                    ]),
                    # html.Div(
                    #     className='filter-item',
                    #     children=[
                    #     'Select the top number of most differentially expressed genes',
                    #     html.Br(),
                    #     dcc.Slider(
                    #         id='volcano-input',
                    #         min=0,
                    #         max=30,
                    #         step=5,
                    #         marks={i: {'label': str(i)} for i in range(5, 31, 5)},
                    #         value=5
                    #     ),
                    # ]),
                    html.Div(
                        className='filter-item',
                        children=[
                            dcc.Tabs(id='tab-options', value='tab-description',
                                children=[
                                    dcc.Tab(label='Description', value='tab-description'),
                                    dcc.Tab(label='Results', value='tab-result'),
                                    dcc.Tab(label='Explanation', value='tab-explanation')
                                ]),
                            html.Div(id='tab-content')
                    ])
                ]),
            ],
        ),
    ])

def callbacks(_app, df):
    @_app.callback(
        Output('volcano-graph', 'figure'),
        [Input('hl-select', 'value')]
    )

    def update_hlgenes(hl_select):
        palette = {'downregulated' : 'blue',
                   'upregulated' : 'red',
                   'insignificant' : 'grey'}
        df['color'] = df['DEG'].apply(lambda x: palette(x) if x in hl_select else 'grey')
        
        return dashbio.VolcanoPlot(
            dataframe=df,
            effect_size='log2FoldChange',
            p='pvalue',
            snp='padj',
            gene='Gene Name',
            annotation='DEG',
            col=df['DEG'].apply(lambda x: palette(x) if x in hl_select else 'grey'),
            width=600,
            height=800,
            xlabel='Log2(Fold Change)',
            ylabel='-Log10(PValue)',
            title='DEG between D2 and D4 Mock EpiAir',
        )

    @_app.callback(
        Output('tab-content', 'children'),
        Input('tab-options', 'value')
    )

    def render_content(tab):
        if tab == 'tab-description':
            return descripiton()
        elif tab == 'tab-result':
            return results()
        else:
            return explanation()
        
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

    with open("dash_app.html", "w") as f:
        f.write(app.index_string)
    app.run_server(debug=True, port=8050)

    