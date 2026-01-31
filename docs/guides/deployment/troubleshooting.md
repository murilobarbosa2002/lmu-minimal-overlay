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

## Erros de Fonte ("Passed a NULL pointer")

Geralmente ocorre em ambientes Wine/Proton devido a caminhos de arquivo do Windows (`Z:\...`).
**Solução**: Atualize para a versão mais recente. O sistema de carregamento de fontes foi reescrito para usar streams de memória (`io.BytesIO`) e ignorar caminhos de arquivo problemáticos.

Veja [Getting Started - Installation](../../getting-started/installation.md).
