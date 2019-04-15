# Práctica 1: Web scraping

## Descripción

Esta práctica se ha realizado bajo el contexto de la asignatura _Tipología y ciclo de vida de los datos_, perteneciente al Máster en Ciencia de Datos de la Universitat Oberta de Catalunya. En ella, se aplican técnicas de _web scraping_ mediante el lenguaje de programación Python para extraer así datos de una web de comparación de vuelos y generar un _dataset_.

## Miembros del equipo

La actividad ha sido realizada por:
  
* **Anna Llorens Roig**
* **Carlos Villar Robles**

## Ejecución:
El script se debe ejecutar de la siguiente manera:
```
python3 src/main.py --origin Madrid --destination Paris
```

Actualmente se pueden combinar las siguientes ciudades origen-destino:

- Madrid
- Barcelona
- London
- Paris
- Rome
- Lisbon
- Amsterdam
- Berlin
- Zurich
- Brussels
- Dublin
- Vienna

Los datos se almacenan en el fichero 'FlightPriceEvolution.csv'. Se pueden realizar diferentes ejecuciones que irán concatenando los resultados en el fichero. 