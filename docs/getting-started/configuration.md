# Configuração Inicial

Personalize o LMU Telemetry Overlay para suas necessidades.

## Arquivos de Configuração

O overlay usa dois arquivos JSON:

- **config.json**: Configurações globais (cores, thresholds, performance)
- **layout.json**: Posições e visibilidade dos widgets

Ambos ficam em `config/`.

## config.json

### Localização

```
lmu-minimal-overlay/config/config.json
```

### Estrutura Completa

```json
{
  "colors": {
    "background": [30, 30, 30],
    "text": [255, 255, 255],
    "ffb_normal": [0, 255, 0],
    "ffb_high": [255, 255, 0],
    "ffb_clipping": [255, 0, 0],
    "throttle": [0, 255, 0],
    "brake": [255, 0, 0],
    "clutch": [0, 100, 255]
  },
  "thresholds": {
    "ffb_high": 0.7,
    "ffb_clipping": 0.95
  },
  "window": {
    "width": 1920,
    "height": 1080,
    "opacity": 0.8
  },
  "performance": {
    "fps_target": 60
  },
  "telemetry": {
    "provider": "auto",
    "max_rpm": 10000,
    "speed_unit": "kmh"
  }
}
```

### Configurações Principais

#### Cores

Formato RGB (0-255).

```json
"colors": {
  "ffb_normal": [0, 255, 0],
  "ffb_clipping": [255, 0, 0]
}
```

**Cores disponíveis:**
- `background`: Fundo no modo Edit
- `text`: Cor do texto
- `ffb_normal`, `ffb_high`, `ffb_clipping`: Indicador FFB
- `throttle`, `brake`, `clutch`: Cores dos pedais

#### Thresholds

Limites para mudança de cor do FFB.

```json
"thresholds": {
  "ffb_high": 0.7,
  "ffb_clipping": 0.95
}
```

- `ffb_high`: Quando FFB fica amarelo (0.0-1.0)
- `ffb_clipping`: Quando FFB fica vermelho (0.0-1.0)

#### Janela

```json
"window": {
  "width": 1920,
  "height": 1080,
  "opacity": 0.8
}
```

- `width`, `height`: Resolução (use resolução do monitor)
- `opacity`: Transparência no modo Running (0.0-1.0)

#### Performance

```json
"performance": {
  "fps_target": 60
}
```

- `fps_target`: FPS alvo (60 recomendado, 30 para PCs fracos)

#### Telemetria

```json
"telemetry": {
  "provider": "auto",
  "max_rpm": 10000,
  "speed_unit": "kmh"
}
```

- `provider`: `"auto"`, `"shared_memory"` ou `"mock"`
- `max_rpm`: RPM máximo para normalização
- `speed_unit`: `"kmh"` ou `"mph"`

## layout.json

### Localização

```
lmu-minimal-overlay/config/layout.json
```

### Estrutura

```json
{
  "widgets": [
    {
      "id": "speedometer",
      "type": "Speedometer",
      "x": 100,
      "y": 100,
      "width": 200,
      "height": 100,
      "visible": true
    }
  ]
}
```

### Campos

- `id`: Identificador único
- `type`: Classe do widget
- `x`, `y`: Posição em pixels
- `width`, `height`: Dimensões
- `visible`: Se widget está visível

### Ocultar Widget

```json
{
  "id": "speedometer",
  "visible": false
}
```

### Resetar Layout

Delete `layout.json` e reinicie. Layout padrão será criado.

## Exemplos de Configuração

### Tema Escuro com FFB Sensível

```json
{
  "colors": {
    "background": [10, 10, 10],
    "text": [200, 200, 200],
    "ffb_normal": [0, 200, 0],
    "ffb_high": [255, 200, 0],
    "ffb_clipping": [255, 50, 50]
  },
  "thresholds": {
    "ffb_high": 0.6,
    "ffb_clipping": 0.85
  }
}
```

### Performance Máxima

```json
{
  "performance": {
    "fps_target": 30
  },
  "window": {
    "opacity": 0.9
  }
}
```

Oculte widgets não essenciais em `layout.json`.

### Unidades Imperiais

```json
{
  "telemetry": {
    "speed_unit": "mph"
  }
}
```

## Hot Reload

Algumas configurações podem ser recarregadas sem reiniciar:

1. Edite `config.json` ou `layout.json`
2. Pressione `F5` (se implementado)

Ou simplesmente reinicie o overlay.

## Backup

Antes de editar, faça backup:

```bash
cp config/config.json config/config.json.backup
cp config/layout.json config/layout.json.backup
```

## Validação

ConfigManager valida automaticamente:
- Tipos de dados corretos
- Valores dentro de ranges válidos
- Campos obrigatórios presentes

Se houver erro, valores padrão serão usados.

## Próximos Passos

- [Guia do Usuário](../guides/user-guide/index.md) - Aprenda todos recursos
- [Customização Avançada](../guides/user-guide/customization.md)
- [Referência config.json](../api-reference/configuration/config-json.md)
