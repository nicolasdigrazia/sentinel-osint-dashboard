# Sentinel OSINT Dashboard

Pipeline de inteligencia competitiva y monitoreo de riesgo del mercado argentino.

## ¿Qué es?

Sentinel es una plataforma OSINT que recolecta y procesa información de fuentes 
abiertas (medios argentinos) para su análisis de riesgo regulatorio, reputacional 
y competitivo. El sistema aplica metodología de análisis de inteligencia estructurada 
sobre los datos recolectados para producir informes accionables.

## Stack

- Python 3.11 / Django 5
- Django Rest Framework
- PostgreSQL 15
- Docker / Docker Compose
- GitHub Actions (CI)

## Arquitectura

Fuentes RSS → Scraper → Collector → Base de datos → Análisis → Informe

## Estado actual

- Recolección de noticias desde rss de medios argentinos
- Deduplicación automática por URL
- Panel de administración para gestión de fuentes y datos recolectados
- Tests automatizados con CI en cada push

## Próximas iteraciones

- Detección de señales de riesgo por keywords
- API REST completa con DRF
- Dashboard React
- Informes con metodología estructurada

## Cómo correr el proyecto

Requisitos: Docker y Docker Compose instalados.

docker-compose up

El sistema queda disponible en http://localhost:8000

## Autor

Nicolás Di Grazia — Analista de Inteligencia & Data Analyst