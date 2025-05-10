import requests
import os
import json

from typing import List

class EuskadiHolidays:
    
    """
        Clase para obtener los festivos de Euskadi: (falta implementar que se guarden en alguna ruta para no tener que depender siempre de Open Data Euskadi).
    """
    
    base_url = "https://opendata.euskadi.eus/contenidos/ds_eventos/calendario_laboral_{year}/opendata/calendario_laboral_{year}.json"
    platform_name = "Open Data Euskadi"
    cache_dir = os.path.join(os.path.dirname(__file__), ".cache")
    
    def __init__(self, year: int):
        self.year = str(year)
        os.makedirs(self.cache_dir, exist_ok=True)
        self.cache_path = os.path.join(self.cache_dir, f"{self.year}.json")

        if os.path.exists(self.cache_path):
            with open(self.cache_path, "r", encoding="utf-8") as f:
                self.holidays: List[dict] = json.load(f)
        else:
            self._download_and_cache()
    
    def _download_and_cache(self):
        url = self.base_url.format(year=self.year)
        response = requests.get(url)
        if not response.ok:
            raise Exception(f"Error fetching holidays for year {self.year}")

        try:
            self.holidays = response.json()
        except Exception as e:
            raise Exception(f"Error parsing JSON data: {e}")
        
        with open(self.cache_path, "w", encoding="utf-8") as f:
            json.dump(self.holidays, f, ensure_ascii=False, indent=2)
    
    def get_all(self) -> List[dict]:
        """
            :return: Lista de todos los festivos del País Vasco
        """
        return self.holidays
    
    def get_holidays_by_province(self, province: str) -> List[dict]:
        """
            :param province: Provincia de búsqueda (Ej: Gipuzkoa)
            :return: Lista de todos los festivos generales del País Vasco y la provincia seleccionada
        """
        territory_lower = province.lower()
        def filter_fn(day: dict) -> bool:
            territory_field = day.get("territory", "").lower()
            return "todos" in territory_field or territory_lower in territory_field
        
        return list(filter(filter_fn, self.holidays))
    
    
    def get_holidays_by_muncipality(self, municipality: str) -> List[dict]:
        """
            :param municipality: Municipio de búsqueda (Ej: Donostia-San Sebastian)
            :return: Lista de todos los festivos generales del País Vasco y el municipio proporcionado 
        """
        municipality_lower = municipality.lower()
        def filter_fn(day: dict) -> bool:
            municipality_field = day.get("municipalityEs", "").lower()
            territory_field = day.get("territory", "").lower()
            return "todos" in territory_field or municipality_lower in municipality_field
        
        return list(filter(filter_fn, self.holidays))