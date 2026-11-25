# Documentação do Compilador MACSLang (A3)

**UC:** Teoria da Computação e Compiladores  
**Valor:** 20 pontos  
**Entrega/apresentação:** 25/11/2026  
**Alvo:** x86-64 + Windows (MinGW/GCC)  
**Repositório:** [atv.compiladores1.0](https://github.com/Pedrochristovam/atv.compiladores1.0)

---

## 1. O que é este projeto?

Compilador da linguagem **MACSLang** (imperativa/estruturada) em **C**, com as **4 fases** pedidas no enunciado:

| Fase | Módulo | Arquivo(s) | Saída |
|------|--------|------------|--------|
| 1. Léxico | Léxico | `lexico.c` + `analiselexica.l` | Tokens |
| 2. Sintático | Parser | `parser.c` | AST |
| 3. Semântico | Semântica | `semantica.c` | Validação / tabela de símbolos |
| 4. Gerador de código | Codegen | `codegen.c` | Assembly x86-64 (`.s`) |

Orquestrador: `main.c`.

---

## 2. Roteiro rápido para explicar na apresentação

Use esta ordem (o professor costuma perguntar “como as fases se conectam”):

1. **Léxico** — “Lemos caractere a caractere e devolvemos tokens (`IF`, `NUMERO`, `IDENTIFICADOR`…). O `while` tem token próprio, separado do `for`.”
2. **Sintático** — “Parser descendente recursivo: cada regra da gramática é uma função C. O resultado é a **AST** (árvore).”
3. **Semântico** — “Pilha de escopos + tabela de funções. Detectamos variável/função não declarada, duplicada e incompatibilidade simples de tipos.”
4. **Codegen** — “Percorremos a AST e emitimos assembly x86-64. Expressões ficam em `RAX`; variáveis locais em `[rbp - offset]`; `print`/`input` chamam `printf`/`scanf`.”
5. **Demo** — Compilar um `.macs` → `.s` → `.exe` e mostrar a saída numérica.

### Frases-chave (legendas no código)

Em vários arquivos há blocos `LEGENDA (APRESENTAÇÃO)`. São comentários feitos **para a banca**: diga o que está marcado, não precisa decorar o arquivo inteiro.

| Onde | O que destacar |
|------|----------------|
| `main.c` | Pipeline das 4 fases |
| `lexico.c` | Como o token é reconhecido |
| `parser.c` | Recursive descent + precedência de operadores |
| `semantica.c` | Escopos empilhados / erros semânticos |
| `codegen.c` | `RAX`, pilha, Windows x64 (`RCX`/`RDX`…), labels de `if`/`while`/`for` |
| `ast.h` | Nó = tipo + valor + filho + próximo |
| `tokens.h` | Contrato léxico ↔ parser |
| `Makefile` | Como gerar o compilador e os testes |

---

## 3. Como compilar e testar

Requisito: **GCC** (ex.: MSYS2 MinGW em `C:\msys64\mingw64\bin`).

```powershell
$env:Path = "C:\msys64\mingw64\bin;" + $env:Path
cd C:\Users\teste\Desktop\atv.compiladores

# 1) Compila o compilador
gcc -Wall -std=c11 main.c lexico.c ast.c semantica.c parser.c codegen.c -o compilador.exe

# 2) Compila um programa MACSLang → assembly
.\compilador.exe testes\soma.macs -o saida.s --ast

# 3) Monta/liga o assembly e executa
gcc saida.s -o programa.exe
.\programa.exe
```

Saída esperada de `soma.macs`: **9**

Outros testes em `testes/`:

| Arquivo | Ideia | Saída esperada |
|---------|-------|----------------|
| `soma.macs` | função + call | 9 |
| `expressoes.macs` | `-` | 5 |
| `maior.macs` | `if/else` | 7 |
| `while_contagem.macs` | `while` | 3 2 1 |
| `for_contagem.macs` | `for` | 0 1 2 |
| `multiplicacao.macs` | `*` | 15 |

---

## 4. Gramática suportada (resumo)

```
programa     := (funcao | main)*
funcao       := func ID ( params? ) : TIPO bloco
main         := main ( ) bloco
bloco        := { (var decl | comando)* }
decl         := var ID : TIPO (= expr)? ;
comando      := atrib | call | if | while | for | print | input | return
for          := for ( atrib ; expr ; atrib_sem_pv ) bloco
expr         := || && relacional (+|-) (*|/) unário primário
```

Tipos reconhecidos: `int`, `float`, `char`, `bool`, `string`.  
**Codegen completo e estável:** foco em **`int`** (e `bool` como 0/1), alinhado aos exemplos do PDF.

---

## 5. Principais decisões / entregas deste projeto

| Item | Situação no compilador |
|------|------------------------|
| `while` | Token `WHILE` próprio (separado do `FOR`) |
| Geração de código | Emite `.s` x86-64 Windows |
| Módulos | `lexico` + `parser` + `semantica` + `codegen` + `main` |
| Operadores | `+ - * / == != < > <= >= && \|\| !` |
| `for` | Formato do PDF: `for (init; cond; incr)` |
| Tipos/literais | int, float, bool, char, string no léxico/parser |
| Build | `Makefile` + `.gitignore` |
| Documentação | Este documento + legendas no código + guia PDF |

---

## 6. Arquitetura (para desenhar no quadro)

```
arquivo.macs
     │
     ▼
 [lexico.c] ── tokens ──► [parser.c] ── AST ──► [semantica.c]
                                                      │
                                                      ▼ AST ok
                                               [codegen.c]
                                                      │
                                                      ▼
                                                   saida.s
                                                      │
                                                   gcc / link
                                                      │
                                                      ▼
                                                 programa.exe
```

### AST (estrutura)

Cada nó (`NoArvore`):

- `tipo` — ex.: `SOMA`, `IF`, `DECLARACAO`
- `valor` — ex.: nome da variável ou literal
- `tipoVariavel` — `int` / `bool` / …
- `filho` / `proximo` — árvore + lista de irmãos

---

## 7. Decisões técnicas (perguntas típicas do professor)

**Por que léxico em C e ainda existe `analiselexica.l`?**  
O `.l` documenta as regras (especificação Flex). O `lexico.c` implementa o mesmo comportamento sem depender do Flex instalado na máquina da apresentação.

**Por que assembly via GCC e não NASM?**  
O alvo continua **x86 Windows**. Emitimos GAS com `.intel_syntax noprefix`, montável com `gcc saida.s -o programa.exe` no MinGW — fluxo simples na demo.

**Convenção de chamada?**  
Windows x64: 1º arg `RCX`, 2º `RDX`, 3º `R8`, 4º `R9`, retorno em `RAX`, 32 bytes de *shadow space* antes de `call`.

**Semântica “básica” o suficiente?**  
Sim para o escopo do A3: escopos, declaração prévia, aridade de função e compatibilidade simples de tipos. Não há sistema de tipos avançado nem genéricos.

---

## 8. Limitações conhecidas (fale com honestidade se perguntarem)

- Codegen de `float`/`string` é simplificado (prioridade nos exemplos `int` do PDF).
- Funções: até 4 parâmetros no codegen (registradores Windows x64).
- Sem otimização (o enunciado dispensa otimização e IR).
- `switch` existe no léxico, mas não no parser (não é exigido pelo PDF da MACSLang).

---

## 9. Checklist de entrega

- [ ] Compilador gera `saida.s` e o `.exe` roda nos testes
- [ ] Cada integrante sabe explicar **um** módulo (legendas)
- [ ] Enviar código para `otaviano.monteiro@ulife.com.br`
- [ ] Demo ao vivo: `soma.macs` e um com `while` ou `for`

---

## 10. Referências

- Enunciado A3 — UniBH (MACSLang, 4 fases, x86/Windows)
- Aho et al. — *Compilers: Principles, Techniques, and Tools*
- Documentação GCC / MinGW-w64
- ABI Microsoft x64
