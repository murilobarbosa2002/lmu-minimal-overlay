from abc import ABC, abstractmethod
from src.core.domain.telemetry_data import TelemetryData


class ITelemetryProvider(ABC):
    """
    Interface abstrata para providers de telemetria.
    
    Define o contrato que todos os providers (Mock, SharedMemory, etc) devem seguir.
    Usa o padrão Strategy para permitir diferentes fontes de dados de telemetria.
    """

    @abstractmethod
    def get_data(self) -> TelemetryData:
        """
        Retorna os dados de telemetria atuais.
        
        Returns:
            TelemetryData: Dados normalizados de telemetria
            
        Raises:
            RuntimeError: Se o provider não estiver conectado
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Verifica se o provider está disponível para uso.
        
        Returns:
            bool: True se disponível, False caso contrário
        """
        pass

    @abstractmethod
    def connect(self) -> None:
        """
        Conecta ao provider de telemetria.
        
        Raises:
            ConnectionError: Se não conseguir conectar
        """
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """
        Desconecta do provider de telemetria.
        
        Libera recursos e fecha conexões.
        """
        pass
