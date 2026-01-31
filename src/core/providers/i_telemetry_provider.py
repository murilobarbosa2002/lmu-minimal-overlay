from abc import ABC ,abstractmethod 
from src .core .domain .telemetry_data import TelemetryData 


class ITelemetryProvider (ABC ):

    @abstractmethod 
    def get_data (self )->TelemetryData :
        pass 

    @abstractmethod 
    def is_available (self )->bool :
        pass 

    @abstractmethod 
    def connect (self )->None :
        pass 

    @abstractmethod 
    def disconnect (self )->None :
        pass 
