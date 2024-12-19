def cal_genes(df):
    df['DEG'] = 'Insignificant'
    df.loc[(df['padj'] < 0.05) & (df['log2FoldChange'] < -0.585), 'DEG'] = 'Downregulated'
    df.loc[(df['padj'] < 0.05) & (df['log2FoldChange'] > 0.585), 'DEG'] = 'Upregulated'
    return df


def set_style():
    return dict(family='Verdana', color='blue')