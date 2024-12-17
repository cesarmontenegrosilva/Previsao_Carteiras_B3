import yfinance as yf
import pandas as pd
import io
from google.cloud import storage
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

tickers = [
    'AMBP3.SA', 'LIGT3.SA', 'EMBR3.SA', 'SYNE3.SA', 'MRFG3.SA', 'BRFS3.SA',
    'JBSS3.SA', 'CVCB3.SA', 'PETR4.SA', 'VALE3.SA', 'ELET3.SA', 'BBDC4.SA',
    'BBAS3.SA', 'ITUB4.SA', 'ABEV3.SA', 'MGLU3.SA', 'WEGE3.SA', 'CMIG4.SA',
    '^BVSP'
]

# Lê o caminho das credenciais do arquivo .env
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if not credentials_path:
    raise ValueError("A variável de ambiente GOOGLE_APPLICATION_CREDENTIALS não foi definida no arquivo .env")

# Ajusta a variável de ambiente para as credenciais do Google Cloud
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

# Defina as datas desejadas
start_date = "2023-12-01"
end_date = "2024-12-13"  # Ajuste conforme necessário

# Nome do bucket do GCS
bucket_name = "fiap-augusto"

# Cria cliente do GCS
client = storage.Client()
bucket = client.bucket(bucket_name)

for ticker in tickers:
    # Baixa dados do Yahoo Finance
    df = yf.download(ticker, start=start_date, end=end_date)
    
    # Converte DataFrame em CSV na memória (buffer)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer)
    csv_buffer.seek(0)
    
    # Prepara nome do arquivo no GCS
    file_name = f"{ticker.replace('^', '_')}.csv"
    blob_path = f"tickers/{ticker}/{file_name}"
    
    # Cria o blob (objeto no bucket)
    blob = bucket.blob(blob_path)
    # Faz upload direto do buffer
    blob.upload_from_string(csv_buffer.getvalue(), content_type='text/csv')
    
    print(f"Dados de {ticker} carregados em: gs://{bucket_name}/{blob_path}")