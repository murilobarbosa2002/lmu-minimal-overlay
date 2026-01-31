# Instalação

Guia completo de instalação para desenvolvimento (WSL) e produção (Windows).

## Instalação para Desenvolvimento (WSL)

### Requisitos

- WSL2 com Ubuntu 20.04+
- Python 3.9+
- X Server para Pygame

### Passo 1: Clone o Repositório

```bash
git clone https://github.com/seu-usuario/lmu-minimal-overlay.git
cd lmu-minimal-overlay
```

### Passo 2: Crie Ambiente Virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Instale Dependências

```bash
pip install -r requirements.txt
```

### Passo 4: Configure X Server

**No WSL**, adicione ao `~/.bashrc`:

```bash
export DISPLAY=:0
```

**No Windows**, instale um X Server:
- [VcXsrv](https://sourceforge.net/projects/vcxsrv/)
- [Xming](http://www.straightrunning.com/XmingNotes/)

Inicie o X Server antes de executar o overlay.

### Passo 5: Verifique Instalação

```bash
python main.py
```

Você deve ver a janela do overlay com dados mockados.

## Instalação para Produção (Windows)

### Requisitos

- Windows 10/11
- Le Mans Ultimate instalado
- Python 3.9+ para Windows

### Passo 1: Instale Python

**Opção A: Python.org**

1. Baixe de [python.org](https://www.python.org/downloads/)
2. Execute o instalador
3. ✅ **Importante:** Marque "Add Python to PATH"
4. Clique em "Install Now"

**Opção B: Microsoft Store**

```powershell
winget install Python.Python.3.9
```

Verifique a instalação:

```cmd
python --version
```

### Passo 2: Clone o Repositório

**Opção A: Git**

```cmd
git clone https://github.com/seu-usuario/lmu-minimal-overlay.git
cd lmu-minimal-overlay
```

**Opção B: Download ZIP**

1. Baixe o ZIP do GitHub
2. Extraia para `C:\lmu-minimal-overlay`

### Passo 3: Instale Dependências Windows

```cmd
pip install -r requirements-windows.txt
```

Isso instalará:
- `pygame`
- `pywin32` (para transparência de janela)

### Passo 4: Configure pywin32

```cmd
python Scripts\pywin32_postinstall.py -install
```

### Passo 5: Verifique Instalação

```cmd
python main.py
```

O overlay deve abrir. Para testar com o jogo:

1. Inicie Le Mans Ultimate
2. Entre em uma sessão
3. Execute `python main.py`

## Instalação Híbrida (WSL → Windows)

Se você desenvolve no WSL mas quer executar no Windows:

### Do WSL, use Python do Windows:

```bash
/mnt/c/Users/SeuUsuario/AppData/Local/Programs/Python/Python39/python.exe -m pip install -r requirements-windows.txt
/mnt/c/Users/SeuUsuario/AppData/Local/Programs/Python/Python39/python.exe main.py
```

## Dependências

### requirements.txt (WSL/Linux)

```
pygame>=2.5.0
typing-extensions>=4.5.0
```

### requirements-windows.txt (Windows)

```
pygame>=2.5.0
pywin32>=305
typing-extensions>=4.5.0
```

## Próximos Passos

- [Quick Start](quick-start.md) - Execute pela primeira vez
- [Configuração](configuration.md) - Personalize o overlay
- [Guia de Desenvolvimento](../guides/development/index.md) - Para desenvolvedores

## Problemas Comuns

### "python: command not found"

Python não está no PATH. Reinstale marcando "Add to PATH".

### "ImportError: No module named 'pygame'"

Dependências não instaladas. Execute:

```bash
pip install -r requirements.txt
```

### "Shared memory not available"

Le Mans Ultimate não está rodando. Inicie o jogo primeiro.

Mais problemas? Veja [Troubleshooting](../guides/deployment/troubleshooting.md).
