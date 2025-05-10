# Euskadi Holidays

**Librería en Python para obtener festivos del País Vasco desde Open Data Euskadi.**  
Permite filtrar por provincia o municipio, y es útil para proyectos de análisis temporal, predicción, visualización o planificación operativa.

## 🚀 Instalación

```bash
pip install euskadi-holidays
```

## 🧠 Uso básico

```python
from euskadi_holidays import EuskadiHolidays

# Obtener todos los festivos del País Vasco para 2025
cal = EuskadiHolidays(2025)
todos = cal.get_all()

# Obtener festivos de Gipuzkoa
gipuzkoa = cal.get_holidays_by_province("Gipuzkoa")

# Obtener festivos de Donostia
donostia = cal.get_holidays_by_muncipality("Donostia-San Sebastian")

```

## 📦 Funcionalidades

-    Descarga de datos JSON directamente desde Open Data Euskadi
-    Filtros por provincia o municipio
-    Preparado para usarse en proyectos de predicción, calendario laboral, hostelería, logística etc.

## 🛠️ Pendiente

-   Cacheo local para evitar dependencia online
-   CLI para consultar desde terminal
-   Exportación a CSV / iCal


## 📄 Licencia

MIT © Diego Piedra