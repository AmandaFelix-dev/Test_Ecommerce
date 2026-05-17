# Análise de Stress Testing

## Objetivo

Avaliar o comportamento da aplicação sob alta carga de usuários simultâneos, identificando:

- ponto de joelho
- ponto de saturação
- ponto de ruptura
- possíveis gargalos arquiteturais
- integridade do sistema após stress

---
# Configuração do Ambiente
## Variáveis utilizadas
```env
GATEWAY_DELAY_SECONDS=0
```
A variável foi configurada para remover atrasos artificiais no gateway durante os testes.
O valor foi registrado automaticamente no diário de execução.

---
# Ambiente de Teste
## Estrutura utilizada
- Testes de stress: `tests/stress/`
- Testes smoke pós-stress: `tests/smoke/`
- Evidências e relatórios: `tests/stress/relatorios/`
- Documentação: `docs/MEUS_TESTES/`
---

# Estratégia de Teste
Os testes foram executados com aumento progressivo de usuários simultâneos para observar:
- crescimento da latência
- aumento da taxa de erro
- comportamento do backend
- estabilidade geral da aplicação
Os resultados foram exportados em CSV para posterior análise.
---
# Marcos Identificados
## Observações

- Até 50 usuários o sistema respondeu normalmente.
- Em 75 usuários houve aumento abrupto de latência.
- Em 150 usuários o sistema entrou em saturação.
- Em 300 usuários ocorreram erros HTTP 500 e timeout.

## 1. Joelho (~75 usuários)
A partir de aproximadamente 75 usuários simultâneos foi observado:
- aumento abrupto de latência
- crescimento do tempo médio de resposta
- início da degradação perceptível
Este ponto caracteriza o início da perda de eficiência do sistema.
---
## 2. Saturação (~150 usuários)
Com aproximadamente 150 usuários simultâneos:
- tempo de resposta elevado
- aumento consistente de filas
- redução da estabilidade
- crescimento de timeout
Neste estágio o sistema operava próximo do limite.
---
## 3. Ruptura (~300 usuários)
Com aproximadamente 300 usuários simultâneos ocorreram:
- erros HTTP 500
- falhas de timeout
- perda de estabilidade
- indisponibilidade parcial da aplicação
Esse comportamento caracteriza ruptura operacional.
---

# Hipóteses de Gargalo
Com base nos resultados observados, os possíveis gargalos identificados foram:
## Banco de dados
Possível limitação no pool de conexões simultâneas.
Sintomas observados:
- aumento de latência
- timeout em carga elevada
---
## CPU do backend
Sob alta concorrência houve indícios de:
- alto uso de processamento
- degradação progressiva das respostas
---
## Operações de I/O
Possível bloqueio em operações síncronas durante acesso ao banco e processamento de requisições.
---
# Integridade Pós-Stress
Após a execução do stress test foi realizado smoke test de verificação.
Endpoints validados:
- `/`
- `/health`
Resultado:
- aplicação permaneceu funcional após carga elevada
- endpoints responderam corretamente
---
# Evidências Geradas
## Arquivos exportados
- `tests/stress/relatorios/stress_resultados.csv`
- `tests/stress/relatorios/diario_stress.md`
Os arquivos contêm:
- métricas coletadas
- horários de execução
- configuração utilizada
- resultados observados
---

# Discussão Arquitetural
## Impacto de troca de banco de dados

### SQLite → PostgreSQL
A substituição por PostgreSQL poderia:
- aumentar concorrência
- melhorar gerenciamento de conexões
- deslocar o ponto de saturação
---
### Uso de cache (Redis)
A introdução de cache reduziria:
- leituras repetidas
- carga no banco
- tempo médio de resposta
---
### Banco remoto
O uso de banco remoto poderia introduzir:
- maior latência de rede
- aumento de timeout
- deslocamento do joelho para cargas menores
---
# Conclusão
Os testes permitiram identificar os limites operacionais da aplicação sem necessidade de alteração do código Foi possível:
- identificar os marcos principais de carga
- coletar evidências objetivas
- validar integridade pós-stress
- levantar hipóteses de gargalo
- discutir impactos arquiteturais
A aplicação apresentou degradação progressiva sob alta concorrência, com ruptura observada em aproximadamente 300 usuários simultâneos.
