# -*- coding: utf-8 -*-
"""Gera o PDF de norte de apresentacao do Compilador MACSLang."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable, Preformatted, ListFlowable, ListItem
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

OUT = os.path.join(os.path.dirname(__file__), "Guia_Apresentacao_MACSLang.pdf")

# Fontes com suporte a acentuação (PT-BR)
pdfmetrics.registerFont(TTFont("ArialPT", r"C:\Windows\Fonts\arial.ttf"))
pdfmetrics.registerFont(TTFont("ArialPT-Bold", r"C:\Windows\Fonts\arialbd.ttf"))
pdfmetrics.registerFont(TTFont("ArialPT-Italic", r"C:\Windows\Fonts\ariali.ttf"))
pdfmetrics.registerFont(TTFont("ArialPT-BoldItalic", r"C:\Windows\Fonts\arialbi.ttf"))
pdfmetrics.registerFontFamily(
    "ArialPT",
    normal="ArialPT",
    bold="ArialPT-Bold",
    italic="ArialPT-Italic",
    boldItalic="ArialPT-BoldItalic",
)
FONT = "ArialPT"
FONT_B = "ArialPT-Bold"
FONT_I = "ArialPT-Italic"

# Cores
AZUL = HexColor("#1a365d")
AZUL_MED = HexColor("#2c5282")
AZUL_CLARO = HexColor("#ebf4ff")
CINZA = HexColor("#4a5568")
CINZA_CLARO = HexColor("#f7fafc")
VERDE = HexColor("#276749")
LARANJA = HexColor("#c05621")
BORDA = HexColor("#cbd5e0")

PAGE_W, PAGE_H = A4


def header_footer(canvas, doc):
    canvas.saveState()
    # topo
    canvas.setFillColor(AZUL)
    canvas.rect(0, PAGE_H - 14 * mm, PAGE_W, 14 * mm, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont(FONT_B, 9)
    canvas.drawString(1.8 * cm, PAGE_H - 9 * mm, "Compilador MACSLang — Guia de Apresentação A3")
    canvas.setFont(FONT, 8)
    canvas.drawRightString(PAGE_W - 1.8 * cm, PAGE_H - 9 * mm, "Teoria da Computação e Compiladores")
    # rodape
    canvas.setFillColor(CINZA_CLARO)
    canvas.rect(0, 0, PAGE_W, 12 * mm, fill=1, stroke=0)
    canvas.setFillColor(CINZA)
    canvas.setFont(FONT, 8)
    canvas.drawString(1.8 * cm, 5 * mm, "UniBH — Entrega: 25/11/2026")
    canvas.drawRightString(PAGE_W - 1.8 * cm, 5 * mm, f"Página {doc.page}")
    canvas.restoreState()


def build_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="CapaTitulo",
        fontName=FONT_B,
        fontSize=22,
        leading=28,
        textColor=AZUL,
        alignment=TA_CENTER,
        spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name="CapaSub",
        fontName=FONT,
        fontSize=12,
        leading=16,
        textColor=CINZA,
        alignment=TA_CENTER,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name="H1",
        fontName=FONT_B,
        fontSize=14,
        leading=18,
        textColor=AZUL,
        spaceBefore=14,
        spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name="H2",
        fontName=FONT_B,
        fontSize=11,
        leading=14,
        textColor=AZUL_MED,
        spaceBefore=10,
        spaceAfter=5,
    ))
    styles.add(ParagraphStyle(
        name="Body",
        fontName=FONT,
        fontSize=9.5,
        leading=13,
        textColor=black,
        alignment=TA_JUSTIFY,
        spaceAfter=5,
    ))
    styles.add(ParagraphStyle(
        name="BulletItem",
        fontName=FONT,
        fontSize=9.5,
        leading=13,
        textColor=black,
        leftIndent=10,
        spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        name="Fala",
        fontName=FONT_I,
        fontSize=9,
        leading=12,
        textColor=VERDE,
        leftIndent=8,
        rightIndent=8,
        spaceBefore=4,
        spaceAfter=6,
        backColor=HexColor("#f0fff4"),
        borderPadding=6,
    ))
    styles.add(ParagraphStyle(
        name="CodeBlock",
        fontName="Courier",
        fontSize=8,
        leading=11,
        textColor=HexColor("#1a202c"),
        backColor=CINZA_CLARO,
        leftIndent=4,
        spaceBefore=4,
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name="Cell",
        fontName=FONT,
        fontSize=8.5,
        leading=11,
        textColor=black,
    ))
    styles.add(ParagraphStyle(
        name="CellBold",
        fontName=FONT_B,
        fontSize=8.5,
        leading=11,
        textColor=AZUL,
    ))
    styles.add(ParagraphStyle(
        name="Small",
        fontName=FONT,
        fontSize=8,
        leading=10,
        textColor=CINZA,
        alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        name="BoxTitle",
        fontName=FONT_B,
        fontSize=10,
        leading=13,
        textColor=AZUL,
        spaceAfter=3,
    ))
    return styles


def box_table(title, body_paras, styles, width=16.5 * cm):
    """Caixa com titulo e conteudo."""
    inner = [Paragraph(title, styles["BoxTitle"])] + body_paras
    data = [[inner]]
    t = Table(data, colWidths=[width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), AZUL_CLARO),
        ("BOX", (0, 0), (-1, -1), 0.8, AZUL_MED),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def fala(texto, styles):
    return Paragraph(f'<b>Fale assim:</b> “{texto}”', styles["Fala"])


def hr():
    return HRFlowable(width="100%", thickness=0.6, color=BORDA, spaceBefore=4, spaceAfter=8)


def build():
    styles = build_styles()
    doc = SimpleDocTemplate(
        OUT,
        pagesize=A4,
        leftMargin=1.7 * cm,
        rightMargin=1.7 * cm,
        topMargin=2.0 * cm,
        bottomMargin=1.6 * cm,
        title="Guia de Apresentacao — Compilador MACSLang",
        author="Grupo A3 UniBH",
    )
    story = []
    P = lambda t, s="Body": Paragraph(t, styles[s])
    B = lambda t: Paragraph(f"• {t}", styles["BulletItem"])

    # ========== CAPA ==========
    story.append(Spacer(1, 2.2 * cm))
    story.append(P("NORTE DE APRESENTAÇÃO", "CapaTitulo"))
    story.append(P("Compilador MACSLang — Trabalho A3", "CapaTitulo"))
    story.append(Spacer(1, 0.4 * cm))
    story.append(hr())
    story.append(P("UC: Teoria da Computação e Compiladores", "CapaSub"))
    story.append(P("Professor: Otaviano Martins Monteiro", "CapaSub"))
    story.append(P("Entrega e apresentação: 25/11/2026 · Valor: 20 pontos", "CapaSub"))
    story.append(Spacer(1, 0.8 * cm))

    story.append(box_table(
        "Objetivo deste guia",
        [
            P("Roteiro para explicar o projeto em sala: o que o compilador faz, "
              "o papel de cada arquivo, como as 4 fases se conectam e o que "
              "demonstrar ao vivo. Use as caixas verdes (“Fale assim”) como fala pronta."),
        ],
        styles,
    ))

    story.append(Spacer(1, 1.0 * cm))
    story.append(P(
        "<b>Em uma frase:</b> o compilador lê um programa escrito em MACSLang "
        "(arquivo <font face='Courier'>.macs</font>), analisa e traduz para "
        "assembly x86-64 Windows (<font face='Courier'>.s</font>), que o GCC "
        "transforma em executável.",
        "Body",
    ))

    story.append(PageBreak())

    # ========== 1. O QUE PEDIRAM ==========
    story.append(P("1. O que o enunciado pediu", "H1"))
    story.append(hr())
    story.append(P(
        "Desenvolver um <b>compilador</b> para a linguagem <b>MACSLang</b> "
        "(imperativa e estruturada), em linguagem compilada (C), com as fases "
        "abaixo em módulos separados. Não é necessário IR nem otimização."
    ))

    dados = [
        [P("<b>Fase</b>", "CellBold"), P("<b>Arquivo</b>", "CellBold"), P("<b>Resultado</b>", "CellBold")],
        [P("1. Léxico", "Cell"), P("lexico.c", "Cell"), P("Tokens (IF, NUMERO, IDENTIFICADOR…)", "Cell")],
        [P("2. Sintático", "Cell"), P("parser.c + ast.c", "Cell"), P("AST (árvore do programa)", "Cell")],
        [P("3. Semântico", "Cell"), P("semantica.c", "Cell"), P("Validação de escopos e tipos", "Cell")],
        [P("4. Geração de código", "Cell"), P("codegen.c", "Cell"), P("Assembly x86-64 (.s)", "Cell")],
        [P("Orquestrador", "Cell"), P("main.c", "Cell"), P("Liga as 4 fases em sequência", "Cell")],
    ]
    t = Table(dados, colWidths=[4.2 * cm, 4.5 * cm, 7.8 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("BACKGROUND", (0, 1), (-1, 1), CINZA_CLARO),
        ("BACKGROUND", (0, 3), (-1, 3), CINZA_CLARO),
        ("BACKGROUND", (0, 5), (-1, 5), CINZA_CLARO),
        ("BOX", (0, 0), (-1, -1), 0.6, BORDA),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, BORDA),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.35 * cm))
    story.append(fala(
        "O professor pediu quatro fases em módulos separados. Nós fizemos em C: "
        "léxico, parser com AST, semântica e geração de código x86 para Windows.",
        styles,
    ))

    # ========== 2. PIPELINE ==========
    story.append(P("2. Como o fluxo acontece (pipeline)", "H1"))
    story.append(hr())
    story.append(Preformatted(
        "  arquivo.macs\n"
        "       |\n"
        "       v\n"
        "  [lexico.c]  ---- tokens ---->  [parser.c]  ---- AST ---->  [semantica.c]\n"
        "                                                                  |\n"
        "                                                                  v  (AST ok)\n"
        "                                                           [codegen.c]\n"
        "                                                                  |\n"
        "                                                                  v\n"
        "                                                              saida.s\n"
        "                                                                  |\n"
        "                                                              gcc / link\n"
        "                                                                  |\n"
        "                                                                  v\n"
        "                                                           programa.exe",
        styles["CodeBlock"],
    ))
    story.append(P(
        "Cada fase <b>consome</b> a saída da anterior. O <font face='Courier'>main.c</font> "
        "abre o arquivo, chama as funções na ordem e grava o <font face='Courier'>.s</font>."
    ))
    story.append(fala(
        "Não é interpretador: a gente gera assembly, o GCC monta e liga, e sai um .exe de verdade.",
        styles,
    ))

    # ========== 3. ARQUIVO POR ARQUIVO ==========
    story.append(P("3. O que cada arquivo faz", "H1"))
    story.append(hr())

    # main
    story.append(P("3.1 main.c — Orquestrador", "H2"))
    story.append(B("Lê argumentos: arquivo <font face='Courier'>.macs</font>, <font face='Courier'>-o saida.s</font>, <font face='Courier'>--ast</font>, <font face='Courier'>--no-codegen</font>."))
    story.append(B("Chama: <font face='Courier'>lexico_iniciar</font> → <font face='Courier'>parse_programa</font> → <font face='Courier'>analisar_semantica</font> → <font face='Courier'>gerar_codigo</font>."))
    story.append(B("Opcionalmente imprime a AST (útil na demo)."))
    story.append(fala(
        "O main só amarra as fases. Se der erro no léxico, parser ou semântica, paramos antes de gerar código.",
        styles,
    ))

    # tokens
    story.append(P("3.2 tokens.h — Dicionário léxico ↔ parser", "H2"))
    story.append(P(
        "Define números para cada “palavra” da linguagem: <font face='Courier'>IF=1</font>, "
        "<font face='Courier'>WHILE=4</font>, <font face='Courier'>FUNC=40</font>, "
        "<font face='Courier'>NUMERO=36</font>, etc. O léxico devolve esses códigos; "
        "o parser decide o que fazer com cada um."
    ))
    story.append(fala(
        "O tokens.h é o contrato entre as duas primeiras fases. WHILE é token próprio, "
        "separado do FOR — isso evita misturar laços.",
        styles,
    ))

    # lexico
    story.append(P("3.3 lexico.c (+ lexico.h, analiselexica.l) — Análise léxica", "H2"))
    story.append(P(
        "Lê o arquivo <b>caractere a caractere</b> e transforma em tokens. "
        "Ignora espaços e comentários <font face='Courier'>//</font>. "
        "Reconhece operadores (<font face='Courier'>==</font>, <font face='Courier'>&&</font>…), "
        "números, strings, chars, identificadores e palavras reservadas "
        "(<font face='Courier'>if</font>, <font face='Courier'>while</font>, "
        "<font face='Courier'>func</font>, <font face='Courier'>var</font>…)."
    ))
    story.append(B("<font face='Courier'>analiselexica.l</font> = especificação no estilo Flex (documentação)."))
    story.append(B("<font face='Courier'>lexico.c</font> = implementação manual em C (não depende do Flex na máquina da apresentação)."))
    story.append(B("Função principal: <font face='Courier'>yylex()</font> → próximo token; texto fica em <font face='Courier'>yytext</font>."))
    story.append(fala(
        "O léxico é um autômato simples: classifica cada pedaço do código. "
        "Exemplo: a palavra 'while' vira o token WHILE; o número 42 vira NUMERO.",
        styles,
    ))

    story.append(PageBreak())

    # ast
    story.append(P("3.4 ast.h / ast.c — Árvore Sintática Abstrata (AST)", "H2"))
    story.append(P(
        "Estrutura intermediária do programa. Cada nó tem: "
        "<b>tipo</b> (ex.: SOMA, IF, DECLARACAO), <b>valor</b> (nome/literal), "
        "<b>tipoVariavel</b> (int, bool…), <b>filho</b> e <b>proximo</b> (irmãos)."
    ))
    story.append(Preformatted(
        "  Exemplo:  a + b\n"
        "            └─ nó SOMA\n"
        "                 ├─ IDENTIFICADOR(\"a\")\n"
        "                 └─ IDENTIFICADOR(\"b\")",
        styles["CodeBlock"],
    ))
    story.append(fala(
        "Depois do parser, o programa deixa de ser texto e vira árvore. "
        "Semântica e codegen só caminham nessa árvore.",
        styles,
    ))

    # parser
    story.append(P("3.5 parser.c / parser.h — Análise sintática", "H2"))
    story.append(P(
        "Técnica: <b>descendente recursiva</b> (Recursive Descent). "
        "Cada regra da gramática vira uma função C. Consome tokens do léxico "
        "e monta a AST. Se a ordem não bater com a gramática → erro de sintaxe."
    ))
    story.append(B("programa := (função | main)*"))
    story.append(B("função := func ID ( params? ) : TIPO bloco"))
    story.append(B("bloco := { (var | comando)* }"))
    story.append(B("comandos: atribuição, if/else, while, for, print, input, return, chamada"))
    story.append(B("expressões com precedência: || && relacional + − * / unário"))
    story.append(fala(
        "O parser é recursive descent: a função do if espera 'if', '(', condição, ')', bloco… "
        "Se faltar um ponto e vírgula, por exemplo, acusamos erro de sintaxe.",
        styles,
    ))

    # semantica
    story.append(P("3.6 semantica.c / semantica.h — Análise semântica", "H2"))
    story.append(P(
        "Caminha a AST e valida o <b>significado</b>: variáveis declaradas antes do uso, "
        "sem redeclarar no mesmo escopo, funções existentes, aridade correta, "
        "compatibilidade simples de tipos."
    ))
    story.append(B("<b>Pilha de escopos:</b> cada <font face='Courier'>{ }</font> abre um escopo; ao sair, variáveis locais somem."))
    story.append(B("Tabela de funções: nome, tipo de retorno, número de parâmetros."))
    story.append(B("Erros típicos: variável não declarada, função inexistente, tipo incompatível."))
    story.append(fala(
        "Sintaxe pode estar correta e ainda assim o programa estar errado. "
        "A semântica pega coisas como usar 'x' sem declarar ou chamar soma com 3 argumentos quando ela espera 2.",
        styles,
    ))

    # codegen
    story.append(P("3.7 codegen.c / codegen.h — Geração de código x86-64", "H2"))
    story.append(P(
        "Percorre a AST e emite assembly (GAS, sintaxe Intel) para Windows x64 / MinGW:"
    ))
    story.append(B("Cada função/main vira um label assembly."))
    story.append(B("Variáveis locais na pilha: <font face='Courier'>[rbp − offset]</font>."))
    story.append(B("Resultado de expressões em <font face='Courier'>RAX</font>."))
    story.append(B("Condição: 0 = falso, ≠0 = verdadeiro (labels de if/while/for)."))
    story.append(B("<font face='Courier'>print</font>/<font face='Courier'>input</font> → <font face='Courier'>printf</font>/<font face='Courier'>scanf</font> da libc."))
    story.append(B("Convenção Windows x64: args em RCX, RDX, R8, R9 + 32 bytes de shadow space."))
    story.append(fala(
        "No codegen a gente traduz a árvore para instruções de máquina. "
        "Soma vira add; if vira cmp + je/jne com labels; print chama printf.",
        styles,
    ))

    # outros
    story.append(P("3.8 Outros arquivos de apoio", "H2"))
    apoio = [
        [P("<b>Arquivo</b>", "CellBold"), P("<b>Papel</b>", "CellBold")],
        [P("Makefile", "Cell"), P("Compila o compilador e facilita testes (make / make run-soma)", "Cell")],
        [P("README.md", "Cell"), P("Como compilar e rodar rapidamente", "Cell")],
        [P("DOCUMENTACAO.md", "Cell"), P("Documentação longa + legendas de apresentação", "Cell")],
        [P("testes/*.macs", "Cell"), P("Programas de demonstração (soma, while, for, if…)", "Cell")],
        [P(".gitignore", "Cell"), P("Ignora .exe, .o, saida.s no versionamento", "Cell")],
    ]
    t2 = Table(apoio, colWidths=[4.0 * cm, 12.5 * cm])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("BACKGROUND", (0, 2), (-1, 2), CINZA_CLARO),
        ("BACKGROUND", (0, 4), (-1, 4), CINZA_CLARO),
        ("BOX", (0, 0), (-1, -1), 0.6, BORDA),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, BORDA),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t2)

    story.append(PageBreak())

    # ========== 4. LINGUAGEM ==========
    story.append(P("4. O que a MACSLang deste compilador aceita", "H1"))
    story.append(hr())
    story.append(B("<b>var</b> nome: tipo = valor?;  → int, float, char, bool, string"))
    story.append(B("<b>print</b>(expr);  /  <b>input</b>(variável);"))
    story.append(B("<b>if</b> (cond) { … } <b>else</b> { … }"))
    story.append(B("<b>while</b> (cond) { … }"))
    story.append(B("<b>for</b> (init; cond; incr) { … }"))
    story.append(B("<b>func</b> nome(params): tipo { … return …; }"))
    story.append(B("<b>main</b>() { … }"))
    story.append(Spacer(1, 0.2 * cm))
    story.append(P(
        "<b>Observação honesta para a banca:</b> o codegen está estável e completo "
        "para <b>int</b> (e bool como 0/1). float/string são reconhecidos no léxico/parser, "
        "mas a geração de código deles é simplificada — alinhado aos exemplos do PDF."
    ))

    # ========== 5. DEMO ==========
    story.append(P("5. Roteiro de demonstração ao vivo", "H1"))
    story.append(hr())
    story.append(P("<b>Pré-requisito:</b> MinGW/GCC no PATH (ex.: MSYS2 em C:\\msys64\\mingw64\\bin)."))
    story.append(Preformatted(
        "# 1) Compilar o compilador\n"
        "gcc -Wall -std=c11 main.c lexico.c ast.c semantica.c parser.c codegen.c -o compilador.exe\n"
        "\n"
        "# 2) Compilar um programa MACSLang → assembly (+ ver AST)\n"
        ".\\compilador.exe testes\\soma.macs -o saida.s --ast\n"
        "\n"
        "# 3) Montar e executar\n"
        "gcc saida.s -o programa.exe\n"
        ".\\programa.exe\n"
        "# saída esperada: 9",
        styles["CodeBlock"],
    ))
    story.append(P("<b>Sugestão de demos (2 minutos cada):</b>"))

    demos = [
        [P("<b>Arquivo</b>", "CellBold"), P("<b>Mostra</b>", "CellBold"), P("<b>Saída</b>", "CellBold")],
        [P("soma.macs", "Cell"), P("função + chamada + print", "Cell"), P("9", "Cell")],
        [P("maior.macs", "Cell"), P("if / else", "Cell"), P("7", "Cell")],
        [P("while_contagem.macs", "Cell"), P("laço while", "Cell"), P("3 2 1", "Cell")],
        [P("for_contagem.macs", "Cell"), P("laço for", "Cell"), P("0 1 2", "Cell")],
    ]
    t3 = Table(demos, colWidths=[4.5 * cm, 8.5 * cm, 3.5 * cm])
    t3.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("BACKGROUND", (0, 1), (-1, 1), CINZA_CLARO),
        ("BACKGROUND", (0, 3), (-1, 3), CINZA_CLARO),
        ("BOX", (0, 0), (-1, -1), 0.6, BORDA),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, BORDA),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t3)
    story.append(Spacer(1, 0.25 * cm))
    story.append(fala(
        "Vou compilar soma.macs, mostrar a AST com --ast, gerar o .s, montar o .exe e rodar. "
        "Depois mostro um while ou for para provar controle de fluxo.",
        styles,
    ))

    # ========== 6. DIVISAO ==========
    story.append(P("6. Divisão sugerida por integrante", "H1"))
    story.append(hr())
    story.append(P(
        "Cada um explica <b>um</b> módulo (há legendas LEGENDA (APRESENTAÇÃO) no código):"
    ))
    div = [
        [P("<b>Quem</b>", "CellBold"), P("<b>Módulo</b>", "CellBold"), P("<b>Ponto a destacar</b>", "CellBold")],
        [P("Integrante 1", "Cell"), P("lexico.c", "Cell"), P("Como o token é reconhecido; WHILE ≠ FOR", "Cell")],
        [P("Integrante 2", "Cell"), P("parser.c + ast", "Cell"), P("Recursive descent + precedência", "Cell")],
        [P("Integrante 3", "Cell"), P("semantica.c", "Cell"), P("Pilha de escopos e erros semânticos", "Cell")],
        [P("Integrante 4", "Cell"), P("codegen.c", "Cell"), P("RAX, pilha, ABI Windows, labels", "Cell")],
    ]
    t4 = Table(div, colWidths=[3.2 * cm, 4.0 * cm, 9.3 * cm])
    t4.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("BACKGROUND", (0, 1), (-1, 1), CINZA_CLARO),
        ("BACKGROUND", (0, 3), (-1, 3), CINZA_CLARO),
        ("BOX", (0, 0), (-1, -1), 0.6, BORDA),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, BORDA),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t4)

    story.append(PageBreak())

    # ========== 7. PERGUNTAS ==========
    story.append(P("7. Perguntas típicas do professor (e respostas curtas)", "H1"))
    story.append(hr())

    qa = [
        ("Por que tem analiselexica.l e também lexico.c?",
         "O .l documenta as regras no estilo Flex. O lexico.c implementa o mesmo "
         "sem depender do Flex instalado na apresentação."),
        ("Por que assembly via GCC e não NASM?",
         "Alvo continua x86 Windows. Emitimos GAS com .intel_syntax noprefix; "
         "monta com gcc saida.s -o programa.exe no MinGW — fluxo simples na demo."),
        ("Qual a convenção de chamada?",
         "Windows x64: 1º arg RCX, 2º RDX, 3º R8, 4º R9; retorno em RAX; "
         "32 bytes de shadow space antes do call."),
        ("A semântica é avançada?",
         "Não. Escopos, declaração prévia, aridade e tipos simples — suficiente para o A3."),
        ("Tem otimização / código intermediário?",
         "Não. O enunciado dispensa essas fases."),
        ("O switch do tokens.h funciona?",
         "Existe no léxico, mas não no parser. O PDF da MACSLang não exige switch."),
    ]
    for i, (q, a) in enumerate(qa, 1):
        story.append(P(f"<b>Q{i}. {q}</b>", "Body"))
        story.append(P(a, "Body"))

    # ========== 8. CHECKLIST ==========
    story.append(P("8. Checklist final (antes de apresentar)", "H1"))
    story.append(hr())
    story.append(B("Compilador gera saida.s e o .exe roda nos testes (soma + while/for)"))
    story.append(B("Cada integrante sabe explicar um módulo (abrir o arquivo com LEGENDA)"))
    story.append(B("Código enviado para otaviano.monteiro@ulife.com.br"))
    story.append(B("Demo testada na máquina da apresentação (PATH do GCC ok)"))
    story.append(B("Saber citar a limitação: codegen focado em int"))

    story.append(Spacer(1, 0.6 * cm))
    story.append(box_table(
        "Ordem sugerida na apresentação (~10–12 min)",
        [
            P("1) Abrir com a frase-resumo (capa deste guia) — 30 s"),
            P("2) Mostrar o diagrama do pipeline no quadro/tela — 1 min"),
            P("3) Cada um explica seu módulo (2 min × 4) — 8 min"),
            P("4) Demo ao vivo: soma.macs + while ou for — 2 min"),
            P("5) Perguntas do professor"),
        ],
        styles,
    ))

    story.append(Spacer(1, 0.8 * cm))
    story.append(P(
        "Boa apresentação. Foquem no fluxo das fases e na demo — "
        "é o que o professor avalia junto com as respostas.",
        "Small",
    ))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"PDF gerado: {OUT}")


if __name__ == "__main__":
    build()
