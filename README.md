# Polygon Fill (ET/AET) - PyQt5

Aplicação em PyQt5 para desenhar polígonos 2D com o mouse e preencher usando a
varredura por linhas (scanline) com coerência de arestas via ET (Edge Table)
e AET (Active Edge Table).

## Como usar
1. Execute `python main.py` com o venv ativo.
2. Clique com o botão esquerdo para adicionar vértices.
3. Clique com o botão direito (ou botão "Close Polygon") para fechar o polígono.
4. Clique em "Fill" para preencher.
5. Use a toolbar para escolher cores (contorno e preenchimento) e espessura.
6. "Undo" remove o último ponto (ou o preenchimento se já aplicado). "Clear" limpa tudo.

## Requisitos
- Python 3.9+ (testado em Windows)
- PyQt5

Ative o ambiente e instale dependências:

```bash
. ./.venv/Scripts/Activate.ps1
pip install -r requirements.txt
```

Depois execute:

```bash
python main.py
```

## Testes sugeridos
- Polígonos simples (convexos e côncavos)
- Polígonos com arestas horizontais e vértices colineares
- Polígonos complexos (auto-interseções não são suportadas pela versão básica)

## Observações
- Implementação segue a abordagem clássica de ET/AET, ignorando arestas
  horizontais e usando `y < y_max` para evitar duplo-contagem em vértices.
