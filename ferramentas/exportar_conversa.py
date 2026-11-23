# ============================================================
# FERRAMENTA (não faz parte do jogo)
# Transforma as conversas com o Claude Code deste projeto num arquivo Markdown legível,
# para anexar na entrega (regra da disciplina sobre uso de IA).
#
# O Claude Code guarda cada conversa num arquivo .jsonl dentro de ~/.claude/projects/.
# Este script acha as conversas deste projeto e gera conversas_ia/conversa_<nome>.md
#
# Como usar (de dentro da pasta do projeto):
#   python ferramentas/exportar_conversa.py --listar          -> mostra as conversas encontradas
#   python ferramentas/exportar_conversa.py joao               -> exporta TODAS as conversas do projeto
#   python ferramentas/exportar_conversa.py joao ID1 ID2       -> exporta só as conversas escolhidas
#                                                                 (ID = começo do nome do arquivo, ex: d5088d11)
# ============================================================

import glob
import json
import os
import re
import sys
from datetime import datetime, timedelta

PROJETO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
NOME_DA_PASTA = os.path.basename(os.path.abspath(PROJETO))


def pastas_de_conversa():
    """Pastas do Claude Code que pertencem a este projeto (o nome delas termina com o nome da pasta do projeto)."""
    base = os.path.join(os.path.expanduser("~"), ".claude", "projects")
    final = re.sub(r"[^A-Za-z0-9]", "-", NOME_DA_PASTA)
    return [p for p in glob.glob(os.path.join(base, "*")) if os.path.basename(p).endswith(final)]


def ler(caminho):
    linhas = []
    for bruto in open(caminho, encoding="utf-8"):
        try:
            linhas.append(json.loads(bruto))
        except Exception:
            pass
    return linhas


def hora(ts):
    if not ts:
        return ""
    t = datetime.fromisoformat(ts.replace("Z", "+00:00")) - timedelta(hours=3)  # horário de Brasília
    return t.strftime("%d/%m %H:%M")


def sem_blocos_automaticos(texto):
    """Tira os blocos que o sistema coloca sozinho (<system-reminder>, <ide_opened_file>...)."""
    return re.sub(r"<([a-z_\-]+)[^>]*>.*?</\1>", "", texto, flags=re.S).strip()


def sem_dados_pessoais(texto):
    texto = re.sub(r"[\w.+-]+@[\w-]+\.[\w.]+", "(e-mail removido)", texto)
    texto = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"*(imagem de teste: \1)*", texto)
    texto = re.sub(r"[A-Za-z]:\\Users\\[^\\\s]+\\AppData\\Local\\Temp\\[^\s`)]*", "(arquivo de teste local)", texto)
    return texto.strip()


NOMES_ACAO = {"Edit": "Editou", "Write": "Criou/reescreveu", "Read": "Leu", "Bash": "Rodou comando",
              "PowerShell": "Rodou comando", "Grep": "Procurou no código", "Glob": "Listou arquivos"}


def resumo_acao(bloco):
    nome = bloco.get("name", "")
    entrada = bloco.get("input", {}) or {}
    if nome in ("Edit", "Write", "Read"):
        caminho = entrada.get("file_path", "")
        if NOME_DA_PASTA in caminho:
            caminho = caminho.split(NOME_DA_PASTA)[-1].lstrip("\\/")
        else:
            caminho = "(arquivo fora do projeto)"
        return NOMES_ACAO[nome] + ": `" + caminho + "`"
    if nome in ("Bash", "PowerShell"):
        return "Rodou comando: " + (entrada.get("description") or "comando no terminal")
    return NOMES_ACAO.get(nome, "Usou a ferramenta " + nome)


def primeiras_mensagens(linhas):
    msgs = []
    for d in linhas:
        if d.get("type") != "user":
            continue
        c = d.get("message", {}).get("content")
        textos = [c] if isinstance(c, str) else [x.get("text", "") for x in (c or []) if isinstance(x, dict) and x.get("type") == "text"]
        for t in textos:
            t = sem_blocos_automaticos(t)
            if t and not t.startswith("[Request interrupted"):
                msgs.append(t)
    return msgs


def converter(linhas, partes):
    acoes = []

    def soltar_acoes():
        if acoes:
            partes.append("\n".join("> 🔧 " + a for a in acoes) + "\n")
            acoes.clear()

    for d in linhas:
        if d.get("isSidechain"):
            continue
        tipo = d.get("type")
        if tipo == "user":
            c = d.get("message", {}).get("content")
            textos = [c] if isinstance(c, str) else [x.get("text", "") for x in (c or []) if isinstance(x, dict) and x.get("type") == "text"]
            for t in textos:
                t = sem_blocos_automaticos(t)
                if not t or t.startswith("[Request interrupted"):
                    continue
                soltar_acoes()
                partes.append("---\n### 👤 Nós · " + hora(d.get("timestamp")) + "\n\n" + sem_dados_pessoais(t) + "\n")
        elif tipo == "attachment" and d.get("attachment", {}).get("type") == "queued_command":
            t = d["attachment"].get("prompt") or ""
            if isinstance(t, list):
                t = " ".join(x.get("text", "") for x in t if isinstance(x, dict))
            t = sem_blocos_automaticos(t)
            if t:
                soltar_acoes()
                partes.append("---\n### 👤 Nós (enviada enquanto a IA trabalhava) · " + hora(d.get("timestamp")) + "\n\n" + sem_dados_pessoais(t) + "\n")
        elif tipo == "assistant":
            for b in d.get("message", {}).get("content", []) or []:
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "tool_use":
                    acoes.append(resumo_acao(b))
                elif b.get("type") == "text" and b.get("text", "").strip():
                    soltar_acoes()
                    partes.append("### 🤖 Claude · " + hora(d.get("timestamp")) + "\n\n" + sem_dados_pessoais(b["text"]) + "\n")
    soltar_acoes()


def conversas_encontradas():
    arquivos = []
    for pasta in pastas_de_conversa():
        arquivos.extend(glob.glob(os.path.join(pasta, "*.jsonl")))
    resultado = []
    for caminho in arquivos:
        linhas = ler(caminho)
        datas = [d["timestamp"] for d in linhas if d.get("timestamp")]
        if not datas:
            continue
        resultado.append({"id": os.path.basename(caminho)[:-6], "linhas": linhas,
                          "inicio": min(datas), "fim": max(datas), "msgs": primeiras_mensagens(linhas)})
    resultado.sort(key=lambda c: c["inicio"])
    return resultado


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__ or "Uso: python ferramentas/exportar_conversa.py --listar | NOME [IDs]")
        sys.exit(1)
    conversas = conversas_encontradas()
    if not conversas:
        print("Nenhuma conversa do Claude Code encontrada para a pasta", NOME_DA_PASTA)
        sys.exit(1)

    if sys.argv[1] == "--listar":
        for c in conversas:
            primeira = c["msgs"][0][:70].replace("\n", " ") if c["msgs"] else "(sem mensagens)"
            print(c["id"][:8], "|", hora(c["inicio"]), "->", hora(c["fim"]), "|", len(c["msgs"]), "mensagens |", primeira)
        sys.exit(0)

    nome = sys.argv[1].lower()
    escolhidas = sys.argv[2:]
    if escolhidas:
        conversas = [c for c in conversas if any(c["id"].startswith(e) for e in escolhidas)]

    partes = ["# 🤖 Conversas com a IA – " + nome.capitalize() + "\n",
              "Registro das conversas de **" + nome.capitalize() + "** com o **Claude** (Claude Code) usadas para fazer o jogo *Segura Aí!*. "
              "Estão aqui as mensagens (**👤 Nós**) e as respostas da IA (**🤖 Claude**), em ordem. "
              "As ações que a IA fez nos arquivos aparecem resumidas em uma linha (🔧). Horários de Brasília.\n",
              "> Gerado por `ferramentas/exportar_conversa.py`. Mensagens automáticas do sistema e o conteúdo completo dos arquivos "
              "editados foram omitidos para a leitura ficar possível; e-mails são removidos automaticamente.\n"]
    for numero, c in enumerate(conversas):
        partes.append("\n## 💬 Conversa " + str(numero + 1) + " (" + hora(c["inicio"]) + " até " + hora(c["fim"]) + ")\n")
        converter(c["linhas"], partes)

    os.makedirs(os.path.join(PROJETO, "conversas_ia"), exist_ok=True)
    destino = os.path.join(PROJETO, "conversas_ia", "conversa_" + nome + ".md")
    with open(destino, "w", encoding="utf-8") as f:
        f.write("\n".join(partes))
    print("Pronto:", os.path.relpath(destino, PROJETO), "-", len(conversas), "conversa(s)")
