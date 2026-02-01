# Testes Unitários e Qualidade de Código

O projeto adota padrões rigorosos de qualidade de código e testes para garantir robustez e manutenibilidade.

## Cobertura de Código

- **100% de Cobertura**: Todo o código em `src/` deve ser coberto por testes.
- Qualquer PR que diminua a cobertura será rejeitado.

## Política de Comentários

- **Zero Comentários em Produção**: O código em `src/` deve ser auto-explicativo.
- **Não são permitidos**:
  - Docstrings em classes e métodos dentro de `src/` (exceto interfaces e dataclasses quando estritamente necessário para intellisense, mas preferencialmente evitado).
  - Comentários inline (`#`).
  - Código comentado.
- **Exceção**: Arquivos de teste (`tests/`) e documentação (`docs/`) podem e devem conter comentários explicativos.

## Estrutura de Testes

- Utilizamos `pytest` como runner.
- Mocking extensivo para isolar unidades com `unittest.mock`.
- Testes unitários focam em comportamento e estados.

## Isolamento de Testes

- **Zero Dependências Externas**: Testes NÃO devem depender de arquivos de configuração reais (`config.json`, `layout.json`).
- **Mocking de I/O**: Use `unittest.mock.mock_open` para simular leitura/escrita de arquivos.
- **Constantes**: Evite importar `src.core.domain.constants`. Mocke valores constantes se necessário, ou use valores literais nos testes para garantir independência.

## Testes de Integração

- Localizados em `tests/integration/`.
- Testam fluxos completos (ex: App Init -> User Input -> State Change -> Persistence).
- Focam na interação entre múltiplos componentes (App, ConfigManager, Widgets, Event Loop).
- Devem ser mantidos junto com os testes unitários para garantir a estabilidade do sistema.

## Executando Testes

```bash
# Executar todos os testes
pytest

# Verificar cobertura
pytest --cov=src --cov-report=term-missing
```
