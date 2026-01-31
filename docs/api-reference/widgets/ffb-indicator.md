# FFB Indicator Widget

Indicador de force feedback.

## Dados Utilizados

- `ffb_level`: 0.0-1.0+

## Visualização

Barra horizontal com cores dinâmicas:
- Verde: 0.0-0.7 (normal)
- Amarelo: 0.7-0.95 (alto)
- Vermelho: 0.95+ (clipping)

## Thresholds

Configurável em `config.json`:

```json
{
  "thresholds": {
    "ffb_high": 0.7,
    "ffb_clipping": 0.95
  }
}
```

Veja [Widget Base](base-widget.md).
