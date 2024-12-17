# README

## Visão Geral do Projeto

Este projeto visa coletar dados de 18 ativos pre selecionados da B3, no período de 01/12/2023 até 16/12/2024 e inserir GCP, a partir do Google Cloud Storage (GCS), construir carteiras de investimento baseadas em critérios específicos (maior rentabilidade, menor volatilidade e menor correlação), e treinar um modelo LSTM para prever o comportamento dessas carteiras nos próximos 60 dias. 
O tratamento dos dados, criação das carteiras, construção e treinamento da LSTM são feitos dentro da GCP, através da aplicação VERTEX AI, utilizando o notebook do Colab. Além disso, o projeto carrega os resultados de volta para GCS e para o Google BigQuery dentro da GCP, o que possibilita a construção da visualização dos resultados, através de um dashboard no Looker Studio (aqui fora da GCP, mas conectando aos dados do BigQuery da GCP).

## Links

1 - Repositório Github: https://github.com/cesarmontenegrosilva/Previsao_Carteiras_B3.git

2 - LOOKER STUDIO Dashboard: https://lookerstudio.google.com/u/0/reporting/b4ddffe1-8bf7-4c8c-995c-244e8a2fa081/page/p_hlc7j9nxnd

3 - Link video YouTube: 


## Objetivos

1. **Coleta e Pré-Processamento de Dados:**
   - Obter dados históricos de diversos ativos da B3 (este código é rodade localmente, e pode ser colocado no Windows Task Schedule, para que seja executado diariamente), armazenando os dados dos ativos no GCS, em arquivos .csv.
   - Preparar os dados (cálculo de retornos, remoção de outliers, ajuste de períodos), tudo isso já feito dentro do GCP.

2. **Construção de Carteiras de Investimento:**
   - **Carteira de Maior Rentabilidade:** Selecionar os 5 ativos com maior retorno acumulado.
   - **Carteira de Menor Volatilidade:** Selecionar os 5 ativos com menor desvio padrão nos retornos.
   - **Carteira de Menor Correlação:** Selecionar os 5 ativos com menor correlação média entre si.
   
   **Importante:** O índice de mercado (^BVSP) não é incluído em nenhuma das carteiras; ele serve apenas como referência.

3. **Treinamento de um Modelo LSTM:**
   - Treinar um modelo LSTM para prever o retorno diário futuro (passo a passo) de cada carteira.
   - Estender as previsões por 60 dias, obtendo assim cenários futuros estimados.

4. **Armazenamento e Visualização:**
   - Salvar as previsões e as composições de carteira no GCS.
   - Carregar os CSVs resultantes no BigQuery, criando tabelas acessíveis via SQL.
   - Visualização dos dados históricos, as previsões de 60 dias e a composição das carteiras em um dashboard do Looker Studio.

## Fluxo de Trabalho

1. **Execução do Código (Local):**
   - O código pode ser executado localmente.
   - A partir da inserção dos dados no GCS um trigger aciona o notebook no Vertex AI, para o tratamento dos dados criação   das carteiras e treinamento do modelo.
   - Ele lerá arquivos CSV do GCS (dados já disponíveis dos ativos).

2. **Cálculos e Modelagem:**
   - A partir dos retornos diários, são definidas as carteiras sem incluir o índice ^BVSP.
   - Uma LSTM é treinada para cada carteira, prevendo o retorno do próximo dia.
   - Ao repetir a previsão iterativamente por 60 dias, gera-se um horizonte futuro de retornos estimados.

3. **Resultados e Salvamento:**
   - Criação do `comparison_df` (dados históricos cumulativos) e do `predictions_df` (previsões cumulativas para 60 dias).
   - Criação do `assets_df` contendo a lista de ativos de cada carteira.
   - Salvamento dos DataFrames em CSV no GCS.
   - Salvamento do gráfico interativo (HTML) e PNG no GCS.

4. **Carregamento no BigQuery:**
   - Os CSVs de previsões e composição de carteiras são carregados no BigQuery.
   - Agora os dados estão prontos para visualização no Looker Studio.

5. **Visualização no Looker Studio:**
   - Conecção do Looker Studio ao BigQuery.
   - Foram criadas duas páginas. .
   - A primeira exibe as previsões das três carteiras para os próximos 60 dias e uma tabela com a composição de cada carteira.
   - A segunda exibe o comportamento histórico das três carteiras p e uma tabela com a composição de cada carteira.

## Tecnologias Utilizadas

- **Python:** Linguagem principal.
- **Pandas, NumPy:** Manipulação e análise de dados.
- **TensorFlow/Keras:** Treinamento do modelo LSTM.
- **Plotly:** Geração de gráficos interativos (HTML/PNG).
- **Google Cloud Storage:** Armazenamento dos dados (entrada e saída).
- **BigQuery:** Armazenamento tabular dos resultados, pronto para dashboards.
- **Vertex AI (opcional):** Ambiente gerenciado para executar notebooks na nuvem.
- **Looker Studio (Data Studio):** Criação de dashboards interativos.

## Passo a Passo para Reproduzir

1. **Configurar o Ambiente:**
   - Criar um projeto GCP.
   - Ativar APIs do BigQuery e Storage.
   - Criar um bucket no GCS e um dataset no BigQuery.
   
2. **Executar o Código:**
   - Ajustar `bucket_name` e `dataset_id` conforme seu ambiente.
   - Executar o código Python (localmente).
   - O código fará:
     - Coleta de dados da B3.
     - Inserção dos dados no GCS.
     - Leitura de dados do GCS.
     - Cálculo das carteiras sem incluir o ^BVSP.
     - Treinamento LSTM, previsões futuras.
     - Salvamento de CSVs no GCS.
     - Carga dos CSVs no BigQuery.
     - Salvamento do gráfico (HTML e PNG) no GCS.

3. **Criar Dashboard no Looker Studio:**
   - Criação de um novo relatório no LS.
   - Conecção ao BigQuery, selecionando o dataset e as tabelas (`previsoes_carteiras`, `carteiras_ativos`,`comparison_df`).
   - Criação de gráficos de linha (time series) para histórico e previsão.
   - Criação de tabelas para visualizar a composição de cada carteira.

## Resultados Esperados

- **Dashboard Interativo:**  
  Visualização dos dados históricos das carteiras e do mercado, além das previsões de 60 dias, tudo em um só lugar.
  
- **Composição das Carteiras:**  
  Tabela mostrando quais ativos compõem cada uma das carteiras (maior rentabilidade, menor volatilidade, menor correlação).

- **Análise de Tendências Futuras:**
  Com a LSTM, observar a tendência projetada das carteiras em relação ao mercado, ajudando na tomada de decisão.

## Próximos Passos

- Ajustar hiperparâmetros do modelo LSTM para melhorar a precisão.
- Expandir a análise para incluir mais ativos ou outros indicadores.
- Criar pipelines automatizados para atualização diária das previsões.

