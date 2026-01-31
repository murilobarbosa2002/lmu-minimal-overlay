# Setup WSL

Guia completo de configuração do ambiente WSL para desenvolvimento.

## Requisitos

- WSL2 Ubuntu 20.04+
- Python 3.9+
- X Server

## Instalação

```bash
# Clone repositório
git clone <repo-url>
cd lmu-minimal-overlay

# Ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Dependências
pip install -r requirements.txt
```

## Configuração X Server

```bash
export DISPLAY=:0
```

Adicione ao `~/.bashrc`.

## Verificação

```bash
python main.py
```

Veja [Guia de Desenvolvimento](../development/index.md) para mais detalhes.
