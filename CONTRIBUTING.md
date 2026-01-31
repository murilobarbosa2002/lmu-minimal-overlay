# Contribuindo para LMU Telemetry Overlay

Obrigado por considerar contribuir para o LMU Telemetry Overlay! 🎉

## Código de Conduta

Este projeto segue um código de conduta. Ao participar, você concorda em manter um ambiente respeitoso e inclusivo.

## Como Contribuir

### Reportando Bugs

Antes de criar uma issue:

1. Verifique se o bug já não foi reportado
2. Verifique se está usando a versão mais recente
3. Colete informações sobre o ambiente (OS, Python version, etc)

**Template de Bug Report**:

```markdown
**Descrição do Bug**
Descrição clara e concisa do bug.

**Passos para Reproduzir**
1. Vá para '...'
2. Clique em '...'
3. Veja o erro

**Comportamento Esperado**
O que deveria acontecer.

**Screenshots**
Se aplicável, adicione screenshots.

**Ambiente**
- OS: [ex: Windows 11]
- Python: [ex: 3.9.7]
- Versão: [ex: 0.1.0]
```

### Sugerindo Melhorias

Issues de melhoria são bem-vindas! Inclua:

- Descrição clara da melhoria
- Justificativa (por que é útil)
- Exemplos de uso
- Possíveis implementações

### Pull Requests

#### Workflow

1. **Fork** o repositório
2. **Clone** seu fork:
   ```bash
   git clone https://github.com/seu-usuario/lmu-minimal-overlay.git
   cd lmu-minimal-overlay
   ```

3. **Crie branch** para sua feature:
   ```bash
   git checkout -b feat/minha-feature
   ```

4. **Configure ambiente**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Faça suas mudanças** seguindo os padrões de código

6. **Teste** suas mudanças:
   ```bash
   pytest
   pytest --cov=.
   mypy .
   black .
   flake8 .
   ```

7. **Commit** seguindo padrão Commitizen:
   ```bash
   git commit -m "feat(widgets): adiciona widget de temperatura"
   ```

8. **Push** para seu fork:
   ```bash
   git push origin feat/minha-feature
   ```

9. **Abra Pull Request** no repositório original

#### Padrão de Commits

Use **Commitizen** em **português**:

```
tipo(escopo): descrição curta

- Detalhes da mudança
- Mais detalhes
```

**Tipos válidos**:
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação (sem mudança de código)
- `refactor`: Refatoração
- `test`: Testes
- `chore`: Manutenção

**Escopos comuns**:
- `core`: Lógica de negócio
- `ui`: Interface
- `infra`: Infraestrutura
- `config`: Configuração
- `telemetry`: Sistema de telemetria
- `widgets`: Widgets específicos

**Exemplos**:
```bash
git commit -m "feat(widgets): adiciona widget de temperatura dos pneus"
git commit -m "fix(telemetry): corrige normalização de RPM"
git commit -m "docs(api): atualiza documentação do ConfigManager"
git commit -m "refactor(core): simplifica lógica de normalização"
```

## Padrões de Código

### Python

- **Python 3.9+**
- **PEP 8** estrito
- **Type hints** obrigatórios
- **Docstrings** em português (Google Style)

### Type Hints

```python
def normalize_input(raw: int, max_value: int = 255) -> float:
    """Normaliza input raw para 0.0-1.0.
    
    Args:
        raw: Valor raw de entrada (0-255).
        max_value: Valor máximo para normalização.
        
    Returns:
        Valor normalizado entre 0.0 e 1.0.
    """
    return raw / max_value
```

### Docstrings

Use **Google Style** em **português**:

```python
class Widget(ABC):
    """Classe base abstrata para todos widgets.
    
    Todos widgets devem herdar desta classe e implementar
    os métodos abstratos draw(), update() e handle_input().
    
    Attributes:
        rect: Retângulo de colisão do widget.
        visible: Se o widget está visível.
    """
    
    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """Renderiza o widget na surface.
        
        Args:
            surface: Surface do Pygame para renderização.
        """
        pass
```

### Formatação

Use **Black** para formatação automática:

```bash
black .
```

Use **isort** para organizar imports:

```bash
isort .
```

### Linting

Use **flake8**:

```bash
flake8 .
```

Use **mypy** para validação de tipos:

```bash
mypy .
```

## Estrutura de Arquivos

```
lmu-minimal-overlay/
├── main.py
├── core/
│   ├── __init__.py
│   ├── telemetry.py
│   ├── normalization.py
│   └── state.py
├── infra/
│   ├── __init__.py
│   ├── memory_reader.py
│   └── mock_provider.py
├── ui/
│   ├── __init__.py
│   ├── window_manager.py
│   ├── states.py
│   └── widgets/
│       ├── __init__.py
│       ├── base.py
│       └── ...
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── config.json
│   └── layout.json
└── tests/
    ├── __init__.py
    ├── test_telemetry.py
    └── ...
```

## Testes

### Executar Testes

```bash
# Todos testes
pytest

# Com cobertura
pytest --cov=.

# Verbose
pytest -v

# Teste específico
pytest tests/test_telemetry.py
```

### Escrever Testes

```python
import pytest
from core.telemetry import TelemetryData

def test_telemetry_data_creation():
    """Testa criação de TelemetryData."""
    data = TelemetryData(
        speed=100.0,
        rpm=5000,
        throttle_pct=0.5,
        brake_pct=0.0,
        clutch_pct=0.0,
        steering_angle=45.0,
        ffb_level=0.7,
        gear=3,
        timestamp=0.0
    )
    assert data.speed == 100.0
    assert data.gear == 3
```

### Cobertura

Mantenha cobertura **acima de 80%**:

```bash
pytest --cov=. --cov-report=html
```

## Documentação

### Atualizar Documentação

Ao adicionar features, atualize:

1. **README.md** se necessário
2. **docs/** relevantes
3. **CHANGELOG.md**
4. **Docstrings** no código

### Documentação de API

Documente todas classes e métodos públicos:

```python
class MeuWidget(Widget):
    """Widget personalizado que exibe temperatura.
    
    Este widget mostra a temperatura dos pneus em tempo real
    com cores dinâmicas baseadas em thresholds.
    
    Attributes:
        temp_threshold_high: Temperatura considerada alta (°C).
        temp_threshold_critical: Temperatura crítica (°C).
    """
    pass
```

## Checklist de Pull Request

Antes de abrir PR, verifique:

- [ ] Código segue PEP 8
- [ ] Type hints em todas funções
- [ ] Docstrings em classes e métodos públicos
- [ ] Testes adicionados/atualizados
- [ ] Todos testes passando (`pytest`)
- [ ] Cobertura mantida acima de 80%
- [ ] Código formatado (`black .`)
- [ ] Imports organizados (`isort .`)
- [ ] Linting sem erros (`flake8 .`)
- [ ] Type checking sem erros (`mypy .`)
- [ ] Documentação atualizada
- [ ] CHANGELOG.md atualizado
- [ ] Commits seguem padrão Commitizen
- [ ] Branch atualizada com main

## Processo de Review

1. **Automated Checks**: CI/CD roda testes automaticamente
2. **Code Review**: Mantenedor revisa código
3. **Feedback**: Discussão e ajustes se necessário
4. **Merge**: PR é mergeado após aprovação

## Dúvidas?

- Abra uma **Discussion** no GitHub
- Consulte a **documentação** em `docs/`
- Veja **issues** existentes

## Agradecimentos

Obrigado por contribuir! 🙏

Sua contribuição ajuda a melhorar a experiência de toda a comunidade de sim racing.
