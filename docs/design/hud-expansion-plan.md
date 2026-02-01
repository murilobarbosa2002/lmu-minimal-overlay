# Plano de Expansão do HUD (Fase 5)

Este documento detalha o planejamento para a expansão do HUD do LMU Minimal Overlay, baseada nos assets originais do jogo. A meta é dividir o atual `DashboardCard` em múltiplos componentes especializados.

## 1. Nova Arquitetura de UI

### Refatoração "InputCard"
O atual `DashboardCard` será renomeado para **`InputCard`**.
- **Função**: Visualizar inputs do piloto (volante, pedais) e informações críticas de condução (marcha, velocidade).
- **Componentes**:
  - Steering Indicator (Volante)
  - Speed & Gear Display
  - Throttle/Brake/FFB Bars

### Novos Cards (Overlay Components)

#### A. Fuel & Energy Card
Posicionado adjacente ou separado do InputCard.
- **Barra de Combustível**: Visualização do nível de tanque.
- **Barra de Energia**: Status do ERS/Bateria (para carros híbridos/elétricos do WEC).
- **Estilo**: Visual dark, translúcido, consistente com o design atual.

#### B. Car Status Card
Focado em telemetria de "saúde" do carro.
- **Temperatura de Óleo**: Indicador numérico/barra com warning colors.
- **Temperatura da Água**: Indicador numérico/barra.
- **Pneus (Tyres)**: 4 indicadores (FL, FR, RL, RR) mostrando temperatura e possivelmente desgaste.
- **Freios (Brakes)**: Temperatura dos discos e desgaste de pastilha.

## 2. Estratégia de Implementação

1.  **Renomeação (Refactor)**:
    - Renomear classe `DashboardCard` -> `InputCard`.
    - Atualizar referências no `WidgetFactory` e `config.json`.
    - Migrar configurações legadas automaticamente se possível.

2.  **Criação dos Novos Widgets**:
    - Implementar classes `FuelEnergyCard` e `CarStatusCard` herdando de `Widget`.
    - Registrar no `WidgetFactory`.

3.  **Integração de Dados**:
    - Expandir `ITelemetryProvider` e `TelemetryData` para incluir novos campos (fuel, temps, wear).
    - Mapear memória compartilhada real na Fase 6.

## 3. Layout Padrão Sugerido

```
[ Car Status ]  [ InputCard ]  [ Fuel/Energy ]
(Tyres/Temps)   (Wheel/Pedals) (Fuel/ERS)
```

O sistema de `layout.json` permitirá que o usuário reposicione livremente cada um desses cards.
