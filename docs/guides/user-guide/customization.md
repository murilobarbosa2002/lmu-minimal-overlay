# Customização

Personalize o overlay.

## Cores

Edite `config/config.json`:

```json
{
  "colors": {
    "ffb_normal": [0, 255, 0],
    "ffb_clipping": [255, 0, 0]
  }
}
```

## Thresholds

```json
{
  "thresholds": {
    "ffb_high": 0.7,
    "ffb_clipping": 0.95
  }
}
```

## Posições

Use modo Edit (`F1`) e arraste widgets.

## Visibilidade

Edite `layout.json`:

```json
{
  "widgets": [
    {
      "id": "speedometer",
      "visible": false
    }
  ]
}
```

Veja [Configuration](../../getting-started/configuration.md).
