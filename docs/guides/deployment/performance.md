# Performance

Otimizações para melhor desempenho.

## FPS Target

```json
{
  "performance": {
    "fps_target": 60
  }
}
```

Reduza para 30 em PCs fracos.

## Ocultar Widgets

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

## Dirty Rectangles

Implementado automaticamente. Apenas áreas alteradas são redesenhadas.

## Caching

Widgets cacheia elementos estáticos automaticamente.

Veja [Architecture - Data Flow](../../architecture/data-flow.md).
