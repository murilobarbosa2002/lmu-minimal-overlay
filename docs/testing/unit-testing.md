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

## Executando Testes

```bash
# Executar todos os testes
pytest

# Verificar cobertura
pytest --cov=src --cov-report=term-missing
```
