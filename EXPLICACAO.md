# Explicação do código – bloco a bloco

Este arquivo explica cada parte do `jogo.py`. Leia junto com o código.

---

## Bloco 1 – Janela e loop principal

**Objetivo:** abrir uma janela verde que fica aberta até o jogador fechar.

### `import pygame` e `pygame.init()`
- `import pygame` traz a biblioteca para o nosso programa.
- `pygame.init()` "liga" todas as partes do pygame (vídeo, som, teclado...). Sem isso, nada funciona.

### Criando a janela
```python
LARGURA = 600
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Meu Crossy Road")
```
- `set_mode((largura, altura))` cria a janela e devolve a **tela**, que é onde vamos desenhar tudo.
- Os dois valores vão entre **parênteses duplos** porque o pygame recebe o tamanho como um par `(600, 600)`.
- `set_caption` muda o título que aparece em cima da janela.
- Variáveis em MAIÚSCULO são uma convenção: indicam **constantes**, valores que não mudam durante o jogo.

> **Coordenadas no pygame:** o ponto `(0, 0)` fica no **canto superior esquerdo**. O `x` cresce para a direita e o `y` cresce **para baixo** (o contrário da matemática!).

### Cores
```python
VERDE = (100, 200, 100)
```
Toda cor é formada por 3 números de 0 a 255: **(Vermelho, Verde, Azul)** – o famoso RGB.
Exemplos: `(0, 0, 0)` é preto, `(255, 255, 255)` é branco, `(255, 0, 0)` é vermelho.

### O relógio
```python
relogio = pygame.time.Clock()
...
relogio.tick(60)
```
Sem o relógio, o loop rodaria o mais rápido possível (e em cada computador numa velocidade diferente). `tick(60)` faz o jogo rodar a no máximo **60 quadros por segundo (FPS)**.

### O loop principal (o coração do jogo)
Um jogo é, basicamente, um `while` que se repete dezenas de vezes por segundo. Cada volta do loop é um **quadro** (frame), e sempre segue a mesma ordem:

1. **Ler eventos** – o que o jogador fez?
2. **Atualizar** – mover coisas, checar colisões (vamos fazer nos próximos blocos)
3. **Desenhar** – pintar tudo na tela
4. **Mostrar e esperar** – `display.update()` e `tick(60)`

### Eventos
```python
for evento in pygame.event.get():
    if evento.type == pygame.QUIT:
        rodando = False
```
- `pygame.event.get()` devolve uma **lista** com tudo que aconteceu desde o último quadro (teclas, cliques, etc.).
- `pygame.QUIT` é o evento de clicar no **X** da janela. Quando isso acontece, `rodando` vira `False` e o `while` para.

### Desenhar e mostrar
- `tela.fill(VERDE)` pinta a tela inteira de verde. Fazemos isso **todo quadro** para "apagar" o desenho anterior.
- `pygame.display.update()` mostra na janela o que foi desenhado. Tudo é desenhado "escondido" e só aparece quando chamamos o `update`.

### `pygame.quit()`
Depois que o loop acaba, desligamos o pygame e a janela fecha.

### Para testar
No terminal, na pasta do projeto:
```
python jogo.py
```
Deve abrir uma janela verde. Feche no X.

### Perguntas que podem cair na prova
- Por que precisamos de um `while` no jogo?
- O que acontece se tirarmos o `pygame.display.update()`? *(a janela fica preta, nada aparece)*
- Para que serve o `relogio.tick(60)`?
- Onde fica o ponto (0, 0) na tela?
