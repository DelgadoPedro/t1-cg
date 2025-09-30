# Relatório de Funcionamento

- Aluno 1: responsabilidades e contribuições.
- Aluno 2: responsabilidades e contribuições.

## Objetivo
Implementar preenchimento de polígonos por varredura (scanline) utilizando ET/AET.

## Interface
- Desenho por cliques do mouse
- Cores de contorno e preenchimento
- Largura de traçado ajustável
- Ações: Fechar, Preencher, Desfazer, Limpar

## Algoritmo
- Construção da ET a partir das arestas não horizontais
- Manutenção da AET por linha de varredura (y)
- Ordenação das interseções e formação de spans (pares)
- Incremento coerente das interseções por 1 linha via 1/m

## Testes
- Casos simples e complexos
- Capturas de tela e comentários de resultados

## Execução
```bash
. ./.venv/Scripts/Activate.ps1
pip install -r requirements.txt
python main.py
```
