# Getting Started

Bem-vindo ao LMU Telemetry Overlay! Este guia irá ajudá-lo a começar rapidamente.

## O que é LMU Telemetry Overlay?

Aplicação desktop de alta performance que exibe telemetria e inputs do simulador Le Mans Ultimate como um overlay transparente (HUD). Desenvolvido em Python com Pygame, seguindo princípios de Clean Code e SOLID.

## Pré-requisitos

- **Python 3.9+**
- **Le Mans Ultimate** (para uso em produção)
- **WSL2** (opcional, para desenvolvimento)

## Próximos Passos

1. [**Instalação**](installation.md) - Configure seu ambiente de desenvolvimento ou produção
2. [**Quick Start**](quick-start.md) - Execute o overlay pela primeira vez
3. [**Configuração**](configuration.md) - Personalize o overlay

## Desenvolvimento vs Produção

### Desenvolvimento (WSL)

Ideal para desenvolver novos widgets e testar funcionalidades sem o jogo rodando.

- Usa `MockTelemetryProvider` com dados fake
- Não precisa do Le Mans Ultimate
- Permite testar UI e drag & drop

### Produção (Windows)

Para uso real durante corridas.

- Usa `SharedMemoryProvider` conectado ao jogo
- Requer Le Mans Ultimate rodando
- Overlay transparente sobre o jogo

## Estrutura da Documentação

- **Getting Started**: Você está aqui! Instalação e primeiros passos
- **Architecture**: Entenda como o sistema funciona
- **Guides**: Guias práticos para desenvolvimento, deploy e uso
- **API Reference**: Referência completa de classes e métodos

## Precisa de Ajuda?

- [Troubleshooting](../guides/deployment/troubleshooting.md)
- [Guia do Usuário](../guides/user-guide/index.md)
- Abra uma issue no GitHub
