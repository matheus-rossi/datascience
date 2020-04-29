import streamlit as st
import pandas as pd
import altair as alt


def create_histogram(column, df):
    chart = alt.Chart(df, width=700).mark_bar().encode(
        alt.X(column, bin=alt.Bin(extent=[0, 271], step=5)),
        y='count()',
        tooltip=[column, 'count()']
    ).interactive()
    return chart


def main():
    st.title('Análise de Tempos GPT')
    st.subheader('Notebook desenvolvido para auxiliar a análise de dados da gestão de posto de trabalho.')
    file = st.file_uploader('Clique abaixo para importar seu arquivo', type='csv')
    if file is not None:
        df = pd.read_csv(file)
        slider = st.slider('Linhas a serem visualizadas', 5, 100)
        st.dataframe(df.head(slider))
        option_cods = sorted(df['COD'].unique())
        select = st.selectbox('Escolha o código a ser analisado:', option_cods)
        df_cod_filtered = df[df['COD'] == select]
        st.table(df_cod_filtered.groupby('COD')['TEMPO (MIN)'].describe())
        st.write(create_histogram('TEMPO (MIN)', df_cod_filtered))


if __name__ == '__main__':
    main()
