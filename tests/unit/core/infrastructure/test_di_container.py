import pytest
from src.core.infrastructure.di_container import SimpleDIContainer, IDIContainer


class TestDIContainer:
    def test_register_and_resolve_transient(self):
        container = SimpleDIContainer()

        class TestService:
            def __init__(self):
                self.id = id(self)

        container.register(TestService, lambda c: TestService(), singleton=False)

        instance1 = container.resolve(TestService)
        instance2 = container.resolve(TestService)

        assert instance1 is not instance2
        assert isinstance(instance1, TestService)
        assert isinstance(instance2, TestService)

    def test_register_and_resolve_singleton(self):
        container = SimpleDIContainer()

        class TestService:
            def __init__(self):
                self.id = id(self)

        container.register(TestService, lambda c: TestService(), singleton=True)

        instance1 = container.resolve(TestService)
        instance2 = container.resolve(TestService)

        assert instance1 is instance2

    def test_register_instance(self):
        container = SimpleDIContainer()

        class TestService:
            pass

        expected_instance = TestService()
        container.register_instance(TestService, expected_instance)

        resolved = container.resolve(TestService)

        assert resolved is expected_instance

    def test_resolve_unregistered_service_raises_error(self):
        container = SimpleDIContainer()

        class UnregisteredService:
            pass

        with pytest.raises(ValueError, match="Service .* not registered"):
            container.resolve(UnregisteredService)

    def test_dependency_injection_chain(self):
        container = SimpleDIContainer()

        class Repository:
            def __init__(self):
                self.name = "Repository"

        class Service:
            def __init__(self, repo: Repository):
                self.repo = repo

        container.register(Repository, lambda c: Repository(), singleton=True)
        container.register(
            Service, lambda c: Service(c.resolve(Repository)), singleton=False
        )

        service1 = container.resolve(Service)
        service2 = container.resolve(Service)

        assert service1.repo is service2.repo
        assert service1 is not service2
