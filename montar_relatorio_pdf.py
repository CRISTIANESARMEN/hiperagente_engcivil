from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def gerar_pdf(texto_relatorio):
    c = canvas.Canvas("relatorio_obra.pdf", pagesize=A4)
    largura, altura = A4

    c.setFont("Helvetica", 12)
    linhas = texto_relatorio.split('\n')
    y = altura - 50
    for linha in linhas:
        c.drawString(50, y, linha)
        y -= 15
        if y < 50:
            c.showPage()
            y = altura - 50
    # Inserir gráfico
    c.drawImage("grafico_custos.png", 50, y - 250, width=500, height=200)
    c.save()
