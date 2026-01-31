# Quick Start

Execute o LMU Telemetry Overlay pela primeira vez.

## Desenvolvimento (WSL)

### 1. Ative o Ambiente Virtual

```bash
cd lmu-minimal-overlay
source venv/bin/activate
```

### 2. Inicie o X Server

No Windows, abra VcXsrv ou Xming.

### 3. Execute o Overlay

```bash
python main.py
```

### 4. Explore a Interface

Você verá o overlay com dados mockados senoidais simulando:
- Velocidade variando entre 50-150 km/h
- RPM oscilando entre 3000-7000
- Inputs de pedais e volante

### 5. Teste o Modo Edit

Pressione `F1` para entrar no modo Edit:
- Fundo fica visível
- Clique e arraste widgets
- Posicione como preferir
- Pressione `F1` novamente para voltar ao modo Running

### 6. Feche o Overlay

Pressione `ESC` ou feche a janela. O layout será salvo automaticamente.

## Produção (Windows)

### 1. Inicie Le Mans Ultimate

Abra o jogo e entre em uma sessão (treino, corrida, etc).

### 2. Execute o Overlay

```cmd
cd C:\lmu-minimal-overlay
python main.py
```

### 3. Overlay Transparente

O overlay aparecerá sobre o jogo:
- Transparente
- Click-through (não captura mouse)
- Exibindo telemetria real

### 4. Posicione os Widgets

1. Pressione `F1` (modo Edit)
2. Arraste widgets para posições desejadas
3. Pressione `F1` (volta ao modo Running)

### 5. Durante a Corrida

O overlay exibirá em tempo real:
- **Speedometer**: Velocidade e marcha
- **Pedals**: Pressão de throttle, brake, clutch
- **Steering Wheel**: Ângulo do volante
- **FFB Indicator**: Força do force feedback com clipping

## Atalhos de Teclado

| Atalho | Ação |
|--------|------|
| `F1` | Alternar entre modo Running e Edit |
| `F2` | Mostrar/ocultar FPS counter |
| `ESC` | Fechar overlay |

## Modos de Operação

### Running Mode (Padrão)

- Overlay transparente
- Click-through (não captura mouse)
- Apenas visualização
- Ideal para uso durante corrida

### Edit Mode

- Fundo visível (escuro)
- Captura mouse
- Permite drag & drop
- Ideal para posicionar widgets

## Estrutura de Arquivos Criados

Após primeira execução:

```
lmu-minimal-overlay/
├── config/
│   ├── config.json (configurações globais)
│   └── layout.json (posições dos widgets)
└── logs/
    └── overlay.log (logs da aplicação)
```

## Customização Rápida

### Mudar Cores

Edite `config/config.json`:

```json
{
  "colors": {
    "ffb_normal": [0, 255, 0],
    "ffb_clipping": [255, 0, 0]
  }
}
```

### Ocultar Widget

Edite `config/layout.json`:

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

## Próximos Passos

- [Configuração](configuration.md) - Personalize cores, thresholds, etc
- [Guia do Usuário](../guides/user-guide/index.md) - Aprenda todos recursos
- [Customização](../guides/user-guide/customization.md) - Customize widgets

## Problemas?

- Overlay não aparece? Veja [Troubleshooting](../guides/deployment/troubleshooting.md)
- Dados não atualizam? Verifique se o jogo está rodando
- Performance ruim? Veja [Otimizações](../guides/deployment/performance.md)
