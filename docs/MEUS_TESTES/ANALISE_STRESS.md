# Análise de Stress Testing

## Objetivo

Avaliar o comportamento da aplicação sob alta carga de usuários simultâneos, identificando:

- Ponto de joelho
- Ponto de saturação
- Ponto de ruptura
- Possíveis gargalos arquiteturais
- Integridade do sistema após stress

---
# Configuração do Ambiente
## Variáveis utilizadas
```env
GATEWAY_DELAY_SECONDS=0
```
A variável foi configurada para remover atrasos artificiais no gateway durante os testes. O valor foi registrado automaticamente no diário de execução.
---
![Mostrar que o .env GATEWAY_DELAY_SECONDS=0 foi aplicado](/docs/MEUS_TESTES/images/gateway.png)

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
- Crescimento da latência
- Aumento da taxa de erro
- Comportamento do backend
- Estabilidade geral da aplicação
Os resultados foram exportados em CSV para posterior análise.
---
# Marcos Identificados
## Observações

- Até 50 usuários o sistema respondeu normalmente.
- Em 75 usuários houve aumento abrupto de latência.
- Em 150 usuários o sistema entrou em saturação.
- Em 300 usuários ocorreram erros HTTP 500 (Internal Server Error) e timeout.

## 1. Joelho (~75 usuários)
O ponto de joelho representa o momento em que o sistema começa a perder eficiência sob aumento de carga, apresentando crescimento perceptível no tempo de resposta.

A partir de aproximadamente 75 usuários simultâneos foi observado:
- Aumento abrupto de latência
- Crescimento do tempo médio de resposta
- Início da degradação perceptível
Este ponto caracteriza o início da perda de eficiência do sistema.
---
## 2. Saturação (~150 usuários)
O ponto de saturação ocorre quando o sistema opera próximo do seu limite de capacidade, mantendo respostas lentas e estabilidade reduzida.

Com aproximadamente 150 usuários simultâneos:
- Tempo de resposta elevado
- Aumento consistente de filas
- Redução da estabilidade
- Crescimento de timeout
Neste estágio o sistema operava próximo do limite.
---
## 3. Ruptura (~300 usuários)
O ponto de ruptura representa a incapacidade do sistema de continuar operando corretamente sob a carga aplicada, resultando em falhas e indisponibilidade parcial.

Com aproximadamente 300 usuários simultâneos ocorreram:
- Erros HTTP 500  (Internal Server Error)
- Falhas de timeout
- Perda de estabilidade
- Indisponibilidade parcial da aplicação
Esse comportamento caracteriza ruptura operacional.
---
![Executar o stress test mostrando usuários](/docs/MEUS_TESTES/images/executa-stress.png)
![Mostrar conteúdo do Diario Stress](/docs/MEUS_TESTES/images/diario-stress.png)
![Mostrar conteúdo do CSV](/docs/MEUS_TESTES/images/resustados-csv.png)
---

# Hipóteses de Gargalo
Com base nos resultados observados, os possíveis gargalos identificados foram:
## Banco de dados
Possível limitação no pool de conexões simultâneas.
Sintomas observados:
- Aumento de latência
- Timeout em carga elevada
---
## CPU do backend
Sob alta concorrência houve indícios de:
- Alto uso de processamento
- Degradação progressiva das respostas
---
## Operações de I/O (Input/Output)
Possível bloqueio em operações síncronas durante acesso ao banco e processamento de requisições.
---
# Integridade Pós-Stress
Após a execução do stress test foi realizado smoke test de verificação.
Endpoints validados:
- `/`
- `/health`
Resultado:
- Aplicação permaneceu funcional após carga elevada
- Endpoints responderam corretamente
---
# Evidências Geradas
## Arquivos exportados
- `tests/stress/relatorios/stress_resultados.csv`
- `tests/stress/relatorios/diario_stress.md`
Os arquivos contêm:
- Métricas coletadas
- Horários de execução
- Configuração utilizada
- Resultados observados
---

# Discussão Arquitetural
## Impacto de troca de banco de dados

### SQLite → PostgreSQL
A substituição por PostgreSQL poderia:
- Aumentar concorrência
- Melhorar gerenciamento de conexões
- Deslocar o ponto de saturação
---
### Uso de cache (Redis)
A introdução de cache reduziria:
- Leituras repetidas
- Carga no banco
- Tempo médio de resposta
---
### Banco remoto
O uso de banco remoto poderia introduzir:
- Maior latência de rede
- Aumento de timeout
- Deslocamento do joelho para cargas menores
---
# Conclusão
Os testes permitiram identificar os limites operacionais da aplicação sem necessidade de alteração do código. 

Foi possível:
- Identificar os marcos principais de carga
- Coletar evidências objetivas
- Validar integridade pós-stress
- Levantar hipóteses de gargalo
- Discutir impactos arquiteturais

A aplicação apresentou degradação progressiva sob alta concorrência, com ruptura observada em aproximadamente 300 usuários simultâneos.
