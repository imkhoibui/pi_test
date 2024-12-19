from dash import html

def descripiton():
    return html.P('The Volcano plot on the left demonstrates two DEGs, Downregulated'
                  'gene PHACTR3 and upregulated gene CXCL5. The remaining genes show'
                  'no significance between two samples, indicated by its padj and l2fc values')


def results():
    return html.P('A genes is considered differentially expressed between two'
                  'or more samples when it satisfies the following conditions:'
                  '1. The gene has padj < 0.05'
                  '2. The gene has l2fc < -0.585 or > 0.585'
                  'Filtering the gene lists, the data shows that there is only'
                  '1 gene which upregulated and 1 gene which is downregulated.'
                  'To make sure the padj is correct, a FDR test has been employed'
                  'using statsmodels library in Python but the padj result is'
                  'the same.')


def explanation():
    return html.P('DEG helps identify, as the name suggests, differentially'
            'expressed genes between two or more samples. The data provided'
            'include D2 and D4 of the EpiAir treatment. DEG has already been'
            'performed using DESeq2 from Bioconductor. Visualization is done'
            'Plotly and deployed with Github pages.')


