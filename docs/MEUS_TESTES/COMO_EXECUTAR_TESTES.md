# Configuração do Ambiente e Execução dos Testes

## Objetivo

Este documento descreve como configurar o ambiente da aplicação legado e executar os testes de stress e smoke sem alterar o código-fonte do sistema.

---

# Requisitos

## Python

Versão utilizada:

```bash
Python 3.11
```

---

# Criação do ambiente virtual

Na raiz do projeto:

```bash
python -m venv venv
```

---

# Ativação do ambiente virtual

## Git Bash

```bash
source venv/Scripts/activate
```

## CMD Windows

```cmd
venv\\Scripts\\activate
```

---

# Instalação das dependências

## Dependências da aplicação

```bash
pip install -r requirements.txt
```

## Dependências de desenvolvimento/testes

```bash
pip install -r requirements-dev.txt
```

## Dependências adicionais utilizadas no stress test

```bash
pip install pytest requests python-dotenv
```

---

# Configuração do .env

Criar arquivo `.env` na raiz do projeto:

```env
cp .env.example .env
```
Edite .env para ajustar o GATEWAY_DELAY_SECONDS = 0 :
```env
GATEWAY_DELAY_SECONDS=0
```

---

# Aplicação das migrations

Executar:

```bash
alembic upgrade head
```

---

# Inicialização da API

O projeto utiliza factory pattern (`criar_app()`).

Comando correto:

```bash
uvicorn ecommerce.api:criar_app --factory --reload
```

API disponível em:

```text
http://127.0.0.1:8000
```

---

# Estrutura criada para os testes

```text
tests/
 ├── smoke/
 └── stress/
      ├── relatorios/
      └── evidencias/
```

---

# Execução do Stress Test

```bash
python -m pytest tests/stress/test_stress.py -v
```

---

# Execução do Smoke Test

```bash
python -m pytest tests/smoke/test_smoke_pos_stress.py -v
```

---

# Evidências geradas

## CSV

```text
tests/stress/relatorios/stress_resultados.csv
```

## Diário

```text
tests/stress/relatorios/diario_stress.md
```

---

# Critérios atendidos

- Configuração do `.env`
- Execução de stress test
- Identificação de joelho/saturação/ruptura
- Exportação CSV
- Smoke pós-stress
- Análise de gargalo
- Discussão arquitetural

---

# Observações

Nenhum código legado foi alterado.

Todas as implementações foram adicionadas apenas em:

- `tests/`
- `docs/MEUS_TESTES/`