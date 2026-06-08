from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Ficha de Entrega - AC1 (Avaliacao Continuada 1)", 0, 1, "C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, "Documento gerado automaticamente", 0, 0, "C")

pdf = PDF()
pdf.add_page()

# Seção de Integrantes
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Integrantes do Grupo:", 0, 1)
pdf.set_font("Arial", "", 12)
pdf.cell(0, 10, "1. Luis Gustavo Palazzi Goulart", 0, 1)
pdf.ln(10)

# Links formatados
pdf.set_font("Arial", "B", 14)
pdf.cell(0, 10, "Links Necessarios (Regra Obrigatoria)", 0, 1)
pdf.ln(5)

# Link 1
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "1. Link do Board Agil:", 0, 1)
pdf.set_font("Arial", "U", 11)
pdf.set_text_color(0, 0, 255)
link1 = "https://github.com/users/Ravizeira/projects/1/views/2"
pdf.cell(0, 10, link1, 0, 1, link=link1)
pdf.set_text_color(0, 0, 0) # reset color
pdf.ln(5)

# Link 2
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "2. Link do Repositorio GitHub (Codigo-Fonte):", 0, 1)
pdf.set_font("Arial", "U", 11)
pdf.set_text_color(0, 0, 255)
link2 = "https://github.com/Ravizeira/ac1-dashboard-estoque"
pdf.cell(0, 10, link2, 0, 1, link=link2)
pdf.set_text_color(0, 0, 0)
pdf.ln(5)

# Link 3
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "3. Link do Video Demonstrativo:", 0, 1)
pdf.set_font("Arial", "", 11)
pdf.set_text_color(255, 0, 0)
pdf.cell(0, 10, "[COLE AQUI SEU LINK DO VIDEO ANTES DA ENTREGA]", 0, 1)
pdf.set_text_color(0, 0, 0)
pdf.ln(10)

pdf.set_font("Arial", "I", 10)
pdf.multi_cell(0, 8, "Atencao: Todos os membros do grupo listados acima precisam realizar a entrega individualmente no classroom anexando COPIA desta mesma ficha, sob pena de ficar com nota Zero.")

pdf.output("Entrega_AC1_Luis_Gustavo.pdf")
print("PDF gerado com sucesso!")
