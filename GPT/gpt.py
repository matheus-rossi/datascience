import streamlit as st
import pandas as pd
import altair as alt


def create_histogram(column, df, df_min, df_max, df_step):
    chart = alt.Chart(df, width=700).mark_bar().encode(
        alt.X(column, bin=alt.Bin(extent=[df_min, df_max], step=df_step)),
        y='count()',
        tooltip=[column, 'count()']
    ).interactive()
    return chart


def main():
    st.sidebar.title('Análise de Tempos')
    st.sidebar.markdown('Notebook desenvolvido para auxiliar a análise de tempos na gestão dos postos de trabalho')
    st.sidebar.header('Instruções')
    st.sidebar.markdown('1 Anexar arquivos')
    st.sidebar.markdown('2 Escolher colunas com dados')
    st.sidebar.markdown('3 Ajustar histograma se necessário')
    st.markdown('## Anexar arquivo')
    file = st.file_uploader('Clique abaixo para importar seu arquivo', type='csv')
    if file is not None:
        df = pd.read_csv(file)
        st.markdown('## Linhas a serem visualizadas')
        slider = st.slider('Selecione o intervalo', 5, 100)
        st.dataframe(df.head(slider))
        st.markdown('## Coluna com os tempos a serem analisados')
        selected_time_column = st.selectbox('Coluna que contém os tempos dos códigos', df.columns)
        st.markdown('## Coluna com os códigos a serem analisados')
        selected_group_column = st.selectbox('Coluna que contém a informação dos códigos', df.columns)
        st.markdown('## Produto ou parada a ser analisada')
        option_cods = sorted(df[selected_group_column].unique())
        select = st.selectbox('Escolha o código a ser analisado:', option_cods)
        df_cod_filtered = df[df[selected_group_column] == select]
        st.table(df_cod_filtered.groupby(selected_group_column)[selected_time_column].describe())
        st.markdown('## Favor revisar os parâmetros abaixo, para uma análise mais assertiva dos dados:')
        df_min_column = int(df_cod_filtered[selected_time_column].min())
        df_max_column = int(df_cod_filtered[selected_time_column].max())
        df_min_value = st.number_input('Limite inferior do histograma:', min_value=0, value=0)
        df_max_value = st.number_input('Limite superior do histograma:', min_value=df_min_column, value=df_max_column, max_value=df_max_column)
        st.markdown('### O step representa como os dados são agrupados, quanto menor o valor, mais colunas existirão:')
        df_step_value = st.number_input('Steps do histograma:', min_value=1, value=1)
        st.write(create_histogram(selected_time_column, df_cod_filtered, df_min_value, df_max_value, df_step_value))



if __name__ == '__main__':
    main()
