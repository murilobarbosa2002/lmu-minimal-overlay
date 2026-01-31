# Speedometer Widget

Velocímetro digital.

## Dados Utilizados

- `speed`: km/h ou mph
- `gear`: Marcha atual

## Visualização

- Velocidade em números grandes
- Indicador de marcha
- Unidade configurável

## Exemplo

```python
speedometer = Speedometer(x=100, y=100)
speedometer.update(data)
speedometer.draw(surface)
```

Veja [Widget Base](base-widget.md).
