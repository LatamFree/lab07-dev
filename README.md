# Arquitectura Web

## Configuración ambiente local

```bash
pipenv install --dev
```

```bash
pipenv shell
pipenv run uvicorn --reload src.main:app
```

Visita la url `http://127.0.0.1:8000/docs` y valida los endpoints disponibles

## Actividad 1

### Weather API
Cree una cuenta gratuita con su correo personal en https://www.weatherapi.com en caso de no tener una, en local utilizaremos la cuota personal. En integración configuraremos otra.

Agrega logs en cada servicio para informar:

- Ambiente donde se corre el código
- URL consultada (no incluir api key si existe)
- country code en caso se utilice

### No mostrar error hacia la respuesta del cliente, 

Mostrar mensaje personalizado según cada error. También debemos mover la lógica, pero generar log con el error real.

Cambia el bloque try catch hacia el controlador, en los bloques del servicio utiliza `raise` según corresponda y en el controlador utiliza `HTTPException`.
Para esto último guíate utilizando lo siguiente:

[Documentación FastAPI](https://fastapi.tiangolo.com/tutorial/handling-errors/#raise-an-httpexception-in-your-code)

Finalmente pone en producción la app usando el workflow correspondiente.

## Actividad 2

Crea un nuevo Workflow para el Pipeline llamado `integration-tests.yml` que sea capaz de correr las pruebas con pytest. Para esto utiliza el script `tests/setup` que instalará `pipenv`. 
Utiliza el comando `pipenv run pytest`

El workflow debe utilizar:

```yml
name: Python Integration Tests

on: push
```

Prueba incluir la opción `--log-cli-level=DEBUG` cuando corras el comando `pytest` en integración continua en el `job` que has creado.

edita el workflow `classroom.yml` para que quede como lo que sigue fijándote en las nuevas cosas que hemos agregado:

```yml
name: GitHub Classroom Workflow

on: 
  workflow_run:
    workflows: ['Python Integration Tests']
    types:
      - completed

permissions:
  checks: write
  actions: read
  contents: read

jobs:
  build:
    name: Autograding
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    steps:
      - uses: actions/checkout@v2
      - uses: education/autograding@v1

  on-error-tests:
    name: Check error in tests workflow
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'failure' }}
    steps:
        - run: echo "Tests workflow are failed" && exit 1

```

No olvides incluir las variables de ambiente necesarias para que puedan correr las pruebas.

Sube esto y debería correrse tu workflow y luego el de Github Classroom.

¡Éxito!
