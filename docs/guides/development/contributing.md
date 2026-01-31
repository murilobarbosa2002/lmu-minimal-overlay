# Contribuindo

Como contribuir para o projeto.

## Workflow

1. Fork o repositório
2. Crie branch (`git checkout -b feat/nova-feature`)
3. Commit (padrão Commitizen)
4. Push (`git push origin feat/nova-feature`)
5. Abra Pull Request

## Commits

Padrão Commitizen em português:

```bash
git commit -m "feat(widgets): adiciona widget de temperatura"
git commit -m "fix(telemetry): corrige normalização"
```

## Checklist PR

- [ ] PEP 8
- [ ] Type hints
- [ ] Testes
- [ ] Documentação
- [ ] Cobertura 80%+

Veja [.agent/rules/git_commit_standards.md](../../../.agent/rules/git_commit_standards.md).
