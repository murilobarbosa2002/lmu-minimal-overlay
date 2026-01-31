from src.core.infrastructure.app_factory import AppFactory

if __name__ == "__main__":
    app = AppFactory.create()
    app.run()
