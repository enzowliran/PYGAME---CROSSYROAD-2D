# 🚽 Segura Aí!

Jogo 2D feito em Python com PyGame para o Projeto Final de Design de Software (Insper).

## 👥 Membros do grupo
- Joao Vieira
- Enzo Liran
- Eduardo Manino

## 🎮 Sobre o jogo
Você está **muito apertado** e precisa chegar ao banheiro! Atravesse o corredor desviando das pessoas e dos carrinhos de limpeza antes que a **barra de aperto** encha.

Inspirado na mecânica de jogos de "atravessar a rua": o personagem anda de casa em casa e precisa acertar o momento de cada passo.

- **Objetivo:** avançar o máximo possível no corredor sem bater em ninguém e antes que a barra de aperto encha.
- **Mapa infinito:** a escola nunca acaba. O cenário passa por três ambientes que se repetem (o corredor das salas, a cantina e o parquinho), e quem anda em cada faixa é sorteado entre os personagens daquele ambiente: alunos, professora, diretor, zelador com carrinho, merendeira com carrinho de comida, aluno de skate e criança de bicicleta.
- **Barra de aperto:** enche em 7 segundos. Cada faixa nova alcançada esvazia a barra, então é preciso continuar avançando.
- **Game over:** bater em alguém ou deixar a barra encher.
- **Pontuação:** cada faixa nova alcançada vale 1 pulo. O jogo guarda o **recorde** de pulos enquanto estiver aberto.

## 🕹️ Controles
| Tecla | Ação |
|---|---|
| ↑ ↓ ← → | Andar uma casa |
| ESPAÇO | Começar / jogar de novo |

## ⚙️ Como instalar e rodar
1. Tenha o **Python 3** instalado.
2. Instale o PyGame (versão `pygame-ce`, compatível com as versões novas do Python):
   ```
   pip install pygame-ce
   ```
3. Na pasta do projeto, rode:
   ```
   python jogo.py
   ```
   O jogo também funciona se for aberto de outra pasta (ex: `python PYGAME---CROSSYROAD-2D/jogo.py`) ou pelo botão "Run" do VS Code: ele sempre procura as imagens e os sons na pasta onde está o `jogo.py`.

## 🎥 Vídeo do jogo
[▶️ Assistir ao vídeo do jogo funcionando](https://drive.google.com/file/d/16s13aiBDHwT_NnlGyauAQ8roaatDQcCH/view?usp=sharing)

## 📁 Arquivos
| Arquivo | O que é |
|---|---|
| `jogo.py` | Código do jogo |
| `notebook.ipynb` | Caderno de estudos: o código explicado bloco por bloco |
| `musica.wav` | Música de fundo (toca em loop) |
| `batida.wav` | Efeito de som quando o personagem bate em alguém |
| `imagens/` | Imagens do jogo em pixel art (personagem com animações, 8 tipos de obstáculo, os 3 mapas e os letreiros de título e GAME OVER) |
| `ferramentas/gerar_imagens.py` | Script usado para desenhar as imagens da pasta `imagens/` (não faz parte do jogo) |
| `ferramentas/exportar_conversa.py` | Script que transforma as conversas com o Claude Code em Markdown (não faz parte do jogo) |
| `conversas_ia/` | As conversas de cada membro com a IA |

## 🎨 Fonte das imagens
Todas as imagens foram feitas especialmente para este jogo, em pixel art, pelo script `ferramentas/gerar_imagens.py` (escrito com a ajuda do Claude). Cada imagem é desenhada a partir de um "mapa" de letras, em que cada letra é a cor de um pixel. Não usamos imagens de terceiros.

## 🔊 Fonte dos sons
Os dois sons (`musica.wav` e `batida.wav`) foram feitos especialmente para este jogo: são ondas sonoras simples geradas por um pequeno script Python, escrito com a ajuda do Claude. Não usamos nenhum som de terceiros, então não há direitos autorais de outras pessoas envolvidos.

## 🤖 Uso de Inteligência Artificial
Seguindo as regras da disciplina, declaramos o uso de IA generativa:

| Parte | Quanto foi gerado por IA |
|---|---|
| `jogo.py` | 100% gerado por IA (Claude) |
| `notebook.ipynb` | 100% gerado por IA (Claude) |
| `ferramentas/gerar_imagens.py` e `imagens/` | 100% gerado por IA (Claude) |
| `musica.wav` e `batida.wav` | 100% gerados por um script feito por IA (Claude) |

**Como a IA foi usada:** usamos o Claude (Claude Code, dentro do VS Code) para escrever o jogo e o caderno de estudos. O trabalho foi dividido em blocos pequenos (janela, personagem, obstáculos, colisão, pontuação, barra de aperto, telas, sons, gráficos em pixel art, mapa infinito...), e cada bloco seguiu este processo:

1. **Pedido:** o grupo dizia qual seria o próximo passo do jogo.
2. **Proposta:** o Claude explicava o plano do bloco (e, quando havia imagens novas, mostrava uma prévia), **sem alterar os arquivos ainda**. Na maior parte dos blocos foi assim; nos Blocos 3 e 4 ele implementou direto, e a partir daí combinamos que sempre explicaria antes e só implementaria depois da nossa aprovação (isso aparece na conversa anexada).
3. **Conferência:** nós líamos o código linha por linha, tirávamos dúvidas e pedíamos mudanças quando algo não fazia sentido. Só depois da nossa aprovação o código entrava no `jogo.py` e a explicação no `notebook.ipynb`.
4. **Teste:** antes de enviar para o GitHub, rodávamos o jogo para conferir se o bloco novo funcionava e se nada que já existia tinha quebrado.
5. **Envio:** só então era feito o commit e o push.

Assim, mesmo com o código 100% gerado por IA, o grupo acompanhou e conferiu cada parte o tempo todo, e usou o notebook (com as perguntas de prova de cada bloco) para estudar o que foi feito. A IA também ajudou na escolha do tema.

**Anexo:** as conversas de cada membro com a IA estão na pasta [`conversas_ia/`](conversas_ia/):

| Membro | Conversa com a IA |
|---|---|
| Enzo Liran | [conversa_enzo.md](conversas_ia/conversa_enzo.md) |
| Joao Vieira | (pendente) |
| Eduardo Manino | [conversa_eduardo.md](conversas_ia/conversa_eduardo.md) |

Os arquivos foram gerados a partir do histórico do Claude Code com o script `ferramentas/exportar_conversa.py`, que transforma a conversa em texto legível e remove dados pessoais (como e-mails).
