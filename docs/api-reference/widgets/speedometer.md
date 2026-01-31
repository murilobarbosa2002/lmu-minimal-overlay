# Speedometer

Widget principal para exibição de velocidade e marcha.

## Features

- Exibe velocidade atual (km/h) centralizada com fonte grande.
- Exibe marcha engatada logo acima da velocidade.
- Exibe unidade ("km/h") abaixo da velocidade.
- Renderização otimizada (cache de texturas) para evitar recrio de fontes a cada frame.

## Detalhes de Implementação

- **Classe**: `src.ui.widgets.speedometer.Speedometer`
- **Herança**: `src.ui.widgets.widget.Widget`
- **Dependências**: `src.ui.utils.fonts.FontManager`

### Estrutura Visual

```
    [ R / N / 1..6 ]   <- Gear (Amber Color)
        [ 120 ]        <- Speed (White, Large)
         km/h          <- Unit (Grey, Small)
```

### Configuração Padrão

- **Tamanho**: 200x150
- **Cores**:
  - Texto: Branco (255, 255, 255)
  - Gear: Amarelo (255, 200, 0)
  - Background: Preto Semitransparente

## Interação

- **Drag & Drop**: Clique e arraste para reposicionar o widget.
- **Unidades**: Suporte para alternar entre "km/h" (padrão) e "mph" via método `set_unit(unit: str)`.

