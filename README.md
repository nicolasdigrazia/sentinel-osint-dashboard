# Sentinel OSINT Dashboard

Plataforma modular de recolección y análisis de información desde fuentes abiertas.

## ¿Qué es?

Sentinel es una plataforma OSINT que recolecta y procesa información de fuentes 
abiertas (medios, blogs, RSS) para su análisis estructurado. El sistema es agnóstico 
al dominio: puede usarse para inteligencia política, económica, financiera, 
regulatoria o cualquier área temática según las fuentes que se configuren.

## Stack

- Python 3.11 / Django 5
- Django Rest Framework
- PostgreSQL 15
- spaCy 3 (`es_core_news_lg`)
- Docker / Docker Compose
- GitHub Actions (CI)

## Arquitectura
```
Fuentes RSS → Scraper → Collector → RawData
                                       ↓
                                  NLPPipeline (spaCy)
                                       ↓
                              Entity + EntityMention
```

## Estado actual

- Recolección de noticias desde RSS de medios argentinos
- Deduplicación automática por URL
- Análisis NLP automático con spaCy al momento de recolección
- Extracción de entidades nombradas (personas, organizaciones, lugares)
- Registro de frecuencia de entidades por noticia y a lo largo del tiempo
- Panel de administración para gestión de fuentes, datos y entidades
- Filtros por categoría en el admin
- Backup y restore de fuentes RSS
- Tests automatizados con CI en cada push

## Próximas iteraciones

- API REST completa con DRF
- Dashboard React
- Informes con metodología estructurada

## Primeros pasos

Requisitos: Docker y Docker Compose instalados.
```bash
# 1. Buildear los containers (necesario la primera vez, descarga el modelo de spaCy)
docker-compose build

# 2. Levantar los containers
docker-compose up

# 3. En otra terminal, correr migraciones
docker-compose run web python manage.py migrate

# 4. Crear superusuario para el admin
docker-compose run web python manage.py createsuperuser

# 5. Cargar las fuentes RSS
docker-compose run web python manage.py loaddata sources_backup.json

# 6. Recolectar noticias y disparar análisis NLP
docker-compose run web python manage.py shell
>>> from intelligence.tasks.collect_news import run
>>> run()
```

Admin disponible en http://localhost:8000/admin

## Comandos útiles

### Backup y restore de sources
```bash
# Exportar sources
docker-compose run web python manage.py dumpdata intelligence.Source --indent 2 > sources_backup.json

# Importar sources
docker-compose run web python manage.py loaddata sources_backup.json
```

### Recolectar noticias
```bash
docker-compose run web python manage.py shell
>>> from intelligence.tasks.collect_news import run
>>> run()
```

### Si se corrompe el volumen
```bash
docker-compose down
docker-compose up
docker-compose run web python manage.py migrate
docker-compose run web python manage.py loaddata sources_backup.json
```

## Autor

Nicolás Di Grazia — Analista de Inteligencia & Data Analyst