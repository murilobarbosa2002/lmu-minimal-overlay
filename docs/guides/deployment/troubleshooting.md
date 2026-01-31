# Troubleshooting

Resolução de problemas comuns.

## "Shared memory not available"

Le Mans Ultimate não está rodando. Inicie o jogo primeiro.

## "ImportError: No module named 'win32api'"

```cmd
pip install pywin32
python Scripts\pywin32_postinstall.py -install
```

## Overlay não transparente

```cmd
python Scripts\pywin32_postinstall.py -install
```

## FPS baixo

Reduza `fps_target` em `config.json`:

```json
{
  "performance": {
    "fps_target": 30
  }
}
```

## Widgets não aparecem

Delete `config/layout.json` e reinicie.

Veja [Getting Started - Installation](../../getting-started/installation.md).
