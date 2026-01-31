# Estratégia de Testes E2E (End-to-End)

## Contexto

O **LMU Telemetry Overlay** é uma aplicação cuja função primária é visualizar dados provindos de **memória compartilhada** de um jogo externo (Le Mans Ultimate / rFactor 2).

## Desafio de Testes E2E Reais

Um teste E2E "verdadeiro" implicaria:
1.  Iniciar o jogo *Le Mans Ultimate*.
2.  Entrar em uma sessão de prática (carregar pista/carro).
3.  Pilotar o carro virtualmente.
4.  Verificar se o Overlay está exibindo os dados daquele momento.

Isso é inviável em ambientes de CI/CD padrão e difícil de automatizar localmente sem scripts complexos de automação de GUI do jogo.

## Nossa Abordagem

Adotamos a estratégia de **Mocking de Alta Fidelidade** para garantir a qualidade sem depender do jogo:

1.  **Testes Unitários de Domínio (Core)**:
    *   A lógica de conversão de dados (`normalize.py`, `TelemetryData`) é testada exaustivamente (100% cobertura) com dados estáticos.

2.  **Mock Telemetry Provider**:
    *   Criamos um `MockTelemetryProvider` que gera ondas senoidais realistas (RPM sobe/desce, velocidade varia, marchas trocam).
    *   Isso permite verificações manuais e testes de integração do fluxo de dados completo sem abrir o jogo.

3.  **Testes de Interface (UI)**:
    *   Os Widgets são testados isoladamente injetando `TelemetryData` forjado.
    *   Verificamos se o `draw` e `update` reagem corretamente aos dados.

## Cobertura Atual

Optamos por focar em **100% de Cobertura de Código** nos testes unitários e de integração (componentes conversando entre si via Mocks). Isso garante que, assumindo que a leitura de memória esteja correta (o que é validado pelo driver `SharedMemoryProvider`), o resto da aplicação funcionará perfeitamente.

## Futuro

Para a Fase 5 (Produção Windows), planejamos criar um pequeno executável "Simulador de Shared Memory" em C++ ou Python que escreve no buffer de memória real do Windows. Isso permitirá testes E2E automatizados que validam inclusive a leitura da memória compartilhada pelo `mmap`.
