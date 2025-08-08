from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

class PDF():

    def __init__(self, nome_arquivo):
        self.doc = SimpleDocTemplate(nome_arquivo+'.pdf', pagesize=A4)
        self.estilos = getSampleStyleSheet()
        self.elementos = []

    def adicionarLivros(self, lista_livros):

        for livro in lista_livros:
            self.elementos.append(Paragraph(f"<b>Título:</b> {livro.titulo}", self.estilos["Normal"]))
            self.elementos.append(Spacer(1, 6))
            self.elementos.append(Paragraph(f"<b>Descrição:</b> {livro.descricao}", self.estilos["Normal"]))
            self.elementos.append(Spacer(1, 6))
            self.elementos.append(Paragraph(f"<b>Autor:</b> {livro.autor}", self.estilos["Normal"]))
            self.elementos.append(Spacer(1, 6))
            self.elementos.append(Paragraph(f"<b>Avaliação:</b> {livro.avaliacao}", self.estilos["Normal"]))
            self.elementos.append(Spacer(1, 6))
            self.elementos.append(Paragraph(f"<b>Quantidade de Avaliações:</b> {livro.qtdAvaliacao}", self.estilos["Normal"]))
            self.elementos.append(Spacer(1, 6))
            self.elementos.append(Paragraph(f"<b>Categoria:</b> {livro.categoria}", self.estilos["Normal"]))
            self.elementos.append(Spacer(1, 6))
            self.elementos.append(Paragraph(f"<b>Link:</b> <a href='{livro.link}'>Link do Livro</a>", self.estilos["Normal"]))
            self.elementos.append(PageBreak())  # quebra de página para o próximo livro

    def encerrarDocumento(self):
        self.doc.build(self.elementos)