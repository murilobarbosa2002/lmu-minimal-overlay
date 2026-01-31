# Deploy Windows

Instalação e configuração para produção.

## Requisitos

- Windows 10/11
- Python 3.9+
- Le Mans Ultimate

## Instalação

```cmd
pip install -r requirements-windows.txt
python Scripts\pywin32_postinstall.py -install
```

## Executar

```cmd
python main.py
```

## Configuração

Edite `config/config.json`:

```json
{
  "telemetry": {
    "provider": "shared_memory"
  }
}
```

Veja [Getting Started - Installation](../../getting-started/installation.md) para detalhes.
