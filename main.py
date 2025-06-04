from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializar cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# Modelo para o corpo da requisição
class Etapa(BaseModel):
    nome: str
    data_prevista: str
    data_realizada: str
    custo_previsto: float
    custo_realizado: float
    observacoes: str = ""

class DadosObra(BaseModel):
    etapas: list[Etapa]

@app.post("/gerar-relatorio")
async def gerar_relatorio(dados: DadosObra):
    try:
        # Montar texto formatado
        texto_dados = ""
        for etapa in dados.etapas:
            texto_dados += (
                f"Etapa: {etapa.nome}\n"
                f"Data Prevista: {etapa.data_prevista}\n"
                f"Data Realizada: {etapa.data_realizada}\n"
                f"Custo Previsto: R$ {etapa.custo_previsto}\n"
                f"Custo Realizado: R$ {etapa.custo_realizado}\n"
                f"Observações: {etapa.observacoes}\n\n"
            )

        prompt = (
            "Você é um assistente técnico para engenheiro civil. "
            "Baseado nos dados da obra abaixo, gere um relatório detalhado, "
            "incluindo análise do andamento, custos e sugestões:\n\n"
            + texto_dados
            + "\nRelatório:\n"
        )

        response = client.chat.completions.create(
            model="gpt-4o",  # use o modelo correto
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=700,
        )

        return {"relatorio": response.choices[0].message.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from openai import OpenAI
# import os

# # Criar cliente da OpenAI
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# app = FastAPI()

# # Modelo de dados que o endpoint vai receber
# class Etapa(BaseModel):
#     nome: str
#     data_prevista: str
#     data_realizada: str
#     custo_previsto: float
#     custo_realizado: float
#     observacoes: str = ""

# class DadosObra(BaseModel):
#     etapas: list[Etapa]

# @app.post("/gerar-relatorio")
# async def gerar_relatorio(dados: DadosObra):
#     try:
#         # Montar texto estruturado para o prompt
#         texto_dados = ""
#         for etapa in dados.etapas:
#             texto_dados += (
#                 f"Etapa: {etapa.nome}\n"
#                 f"Data Prevista: {etapa.data_prevista}\n"
#                 f"Data Realizada: {etapa.data_realizada}\n"
#                 f"Custo Previsto: R$ {etapa.custo_previsto}\n"
#                 f"Custo Realizado: R$ {etapa.custo_realizado}\n"
#                 f"Observações: {etapa.observacoes}\n\n"
#             )

#         prompt = (
#             "Você é um assistente técnico para engenheiro civil. "
#             "Baseado nos dados da obra abaixo, gere um relatório detalhado, "
#             "incluindo análise do andamento, custos e sugestões:\n\n"
#             + texto_dados
#             + "\nRelatório:\n"
#         )

#         response = client.chat.completions.create(
#             model="gpt-4o",
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.7,
#             max_tokens=700
#         )

#         texto_relatorio = response.choices[0].message.content
#         return {"relatorio": texto_relatorio}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))




# # from fastapi import FastAPI, HTTPException
# # from pydantic import BaseModel
# # import openai
# # import os

# # # Configurar chave da API da OpenAI (melhor usar variável ambiente)
# # openai.api_key = os.getenv("OPENAI_API_KEY")

# # app = FastAPI()

# # # Modelo de dados que o endpoint vai receber
# # class DadosObra(BaseModel):
# #     etapas: list

# # # Cada etapa do projeto terá esses campos
# # class Etapa(BaseModel):
# #     nome: str
# #     data_prevista: str
# #     data_realizada: str
# #     custo_previsto: float
# #     custo_realizado: float
# #     observacoes: str = ""

# # @app.post("/gerar-relatorio")
# # async def gerar_relatorio(dados: DadosObra):
# #     try:
# #         # Montar texto estruturado para o prompt
# #         texto_dados = ""
# #         for etapa in dados.etapas:
# #             texto_dados += (
# #                 f"Etapa: {etapa['nome']}\n"
# #                 f"Data Prevista: {etapa['data_prevista']}\n"
# #                 f"Data Realizada: {etapa['data_realizada']}\n"
# #                 f"Custo Previsto: R$ {etapa['custo_previsto']}\n"
# #                 f"Custo Realizado: R$ {etapa['custo_realizado']}\n"
# #                 f"Observações: {etapa.get('observacoes', '')}\n\n"
# #             )

# #         prompt = (
# #             "Você é um assistente técnico para engenheiro civil. "
# #             "Baseado nos dados da obra abaixo, gere um relatório detalhado, "
# #             "incluindo análise do andamento, custos e sugestões:\n\n"
# #             + texto_dados
# #             + "\nRelatório:\n"
# #         )

# #         response = openai.ChatCompletion.create(
# #             model="gpt-4o-mini",
# #             messages=[{"role": "user", "content": prompt}],
# #             temperature=0.7,
# #             max_tokens=700,
# #         )

# #         texto_relatorio = response["choices"][0]["message"]["content"]
# #         return {"relatorio": texto_relatorio}

# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))




# # # from fastapi import FastAPI
# # # import openai
# # # import gspread
# # # from oauth2client.service_account import ServiceAccountCredentials

# # # app = FastAPI()
# # # openai.api_key = "SUA_API_KEY_OPENAI"

# # # # Configuração Google Sheets
# # # scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
# # # creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
# # # client = gspread.authorize(creds)
# # # sheet = client.open("hiperagentesengcivil").sheet1

# # # def obter_dados_planilha():
# # #     dados = sheet.get_all_records()
# # #     texto = ""
# # #     for linha in dados:
# # #         texto += f"Etapa: {linha['Etapa']}\nPrevisto: {linha['Data Prevista']}\nRealizado: {linha['Data Realizada']}\nCusto Previsto: R$ {linha['Custo Previsto']}\nCusto Realizado: R$ {linha['Custo Realizado']}\nObservações: {linha['Observações']}\n\n"
# # #     return texto

# # # @app.get("/gerar-relatorio")
# # # def gerar_relatorio():
# # #     dados_obra = obter_dados_planilha()
# # #     prompt = f"""
# # #     Você é um assistente para engenheiro civil. Com base nos dados abaixo, crie um relatório técnico detalhado.

# # #     {dados_obra}

# # #     Relatório:
# # #     """
# # #     resposta = openai.ChatCompletion.create(
# # #         model="gpt-4o-mini",
# # #         messages=[{"role": "user", "content": prompt}],
# # #         temperature=0.7,
# # #         max_tokens=700
# # #     )
# # #     texto_relatorio = resposta['choices'][0]['message']['content']
# # #     return {"relatorio": texto_relatorio}
