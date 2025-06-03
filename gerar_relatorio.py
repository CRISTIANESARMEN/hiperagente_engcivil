from fastapi import FastAPI
import openai
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = FastAPI()
openai.api_key = "SUA_API_KEY_OPENAI"

# Configuração Google Sheets
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open("Dados da Obra").sheet1

def obter_dados_planilha():
    dados = sheet.get_all_records()
    texto = ""
    for linha in dados:
        texto += f"Etapa: {linha['Etapa']}\nPrevisto: {linha['Data Prevista']}\nRealizado: {linha['Data Realizada']}\nCusto Previsto: R$ {linha['Custo Previsto']}\nCusto Realizado: R$ {linha['Custo Realizado']}\nObservações: {linha['Observações']}\n\n"
    return texto

@app.get("/gerar-relatorio")
def gerar_relatorio():
    dados_obra = obter_dados_planilha()
    prompt = f"""
    Você é um assistente para engenheiro civil. Com base nos dados abaixo, crie um relatório técnico detalhado.

    {dados_obra}

    Relatório:
    """
    resposta = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=700
    )
    texto_relatorio = resposta['choices'][0]['message']['content']
    return {"relatorio": texto_relatorio}
