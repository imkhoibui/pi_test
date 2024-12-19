def cal_genes(df):
    if df[df.padj < 0.05]:
        if df[df.log2FoldChange < -0.585]:
            df['DEG'] = 'Downregulated'
        elif df[df.log2FoldChange >= 0.585]:
            df['DEG'] = 'Upregulated'
        else:
            df['DEG'] = 'Not significant'
    return df


def highlight_genes(df, modes):
    for mode in modes:
        hl_genes = df[df['DEG'] == mode]['Gene Name']
    return hl_genes