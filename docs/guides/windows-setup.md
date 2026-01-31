# Guia de Configuração - Windows

## Pré-requisitos

1.  **Python 3.10+**: Baixe e instale do [python.org](https://www.python.org/downloads/).
    *   **Importante**: Marque a opção "Add Python to PATH" durante a instalação.
2.  **Le Mans Ultimate**: O jogo deve estar instalado (para uso futuro com memória compartilhada).

## Como Rodar (Automático)

1.  Navegue até a pasta do projeto.
2.  Clique duas vezes no arquivo `run_windows.bat`.
    *   Ele irá criar o ambiente virtual (`venv`) automaticamente.
    *   Instalará as dependências listadas em `requirements-windows.txt`.
    *   Iniciará o overlay.

## Como Rodar (Manual)

Se preferir usar o terminal (PowerShell ou CMD):

1.  Abra o terminal na pasta do projeto.
2.  Crie o ambiente virtual:
    ```powershell
    python -m venv venv
    ```
3.  Ative o ambiente:
    ```powershell
    .\venv\Scripts\activate
    ```
4.  Instale as dependências:
    ```powershell
    pip install -r requirements-windows.txt
    ```
5.  Execute o projeto:
    ```powershell
    python -m src.main
    ```

## Solução de Problemas

### Tela Preta ou Fundo não Transparente
Se a janela ficar com fundo preto ao invés de transparente:
1.  Certifique-se de que o driver da sua placa de vídeo está atualizado.
2.  Tente executar em modo janela (windowed) se o problema persistir em tela cheia.

### Overlay não fica sobre o jogo
O overlay usa configurações padrão `ALWAYS_ON_TOP`. Se o jogo estiver em modo "Exclusive Fullscreen", ele pode cobrir o overlay.
*   **Solução**: Configure o Le Mans Ultimate para rodar em modo **Borderless Windowed** (Janela sem bordas).
