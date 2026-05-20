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

Com base nos resultados registrados no arquivo `stress_resultados.csv`, foram observados os seguintes comportamentos:

| Usuários | Falhas | Taxa de Falha | Comportamento |
|---|---|---|---|
| 1.000 | 0 | 0% | Sistema estável |
| 2.500 | 0 | 0% | Sistema estável |
| 5.000 | 122 | 2,44% | Início de degradação |
| 7.500 | 210 | 2,8% | Latência elevada |
| 10.000 | 9.997 | 99,97% | Ruptura crítica |
| 15.000 | 14.995 | 99,96% | Sistema praticamente indisponível |
| 20.000 | 4.328 | 21,64% | Recuperação parcial sob oscilação |
| 30.000 | 26.163 | 87,21% | Forte instabilidade |

## 1. Joelho (~5.000 usuários)
O ponto de joelho representa o momento em que o sistema começa a perder eficiência sob aumento de carga, apresentando crescimento perceptível no tempo de resposta e início de falhas.

A partir de aproximadamente 5.000 usuários simultâneos foi observado:
- Primeiros erros de requisição
- Aumento da latência média
- Crescimento do tempo total de execução
- Início de degradação perceptível

Esse comportamento caracteriza o início da perda de eficiência da aplicação.

---
## 2. Saturação (~7.500 usuários)
O ponto de saturação ocorre quando o sistema opera próximo do limite de capacidade, mantendo aumento consistente de lentidão e falhas.

Com aproximadamente 7.500 usuários simultâneos ocorreram:
- Crescimento consistente da taxa de erro
- Latência significativamente maior
- Redução perceptível da estabilidade
- Aumento de timeout e degradação das respostas

Nesse estágio o sistema já demonstrava comportamento instável sob alta concorrência.

---
## 3. Ruptura (~10.000 usuários)
O ponto de ruptura representa a incapacidade do sistema de continuar operando corretamente sob a carga aplicada.

Com aproximadamente 10.000 usuários simultâneos ocorreram:
- Taxa de falha próxima de 100%
- Grande volume de requisições não respondidas
- Forte degradação operacional
- Indisponibilidade parcial do sistema

Esse comportamento caracteriza ruptura operacional crítica.

---
## 4. Oscilação pós-ruptura (20.000 usuários)
Durante os testes foi identificado um comportamento de oscilação após a ruptura inicial.

Mesmo com carga extremamente elevada, o sistema apresentou recuperação parcial em aproximadamente 20.000 usuários, reduzindo temporariamente a taxa de falha.

Esse comportamento pode indicar:
- Recuperação parcial do pool de conexões
- Liberação temporária de recursos
- Retentativas internas do backend
- Oscilação do balanceamento interno de processamento

Apesar dessa recuperação parcial, o sistema permaneceu instável.

---
![Executar o stress test mostrando usuários](/docs/MEUS_TESTES/images/executa-stress.png)
![Mostrar conteúdo do Diario Stress](/docs/MEUS_TESTES/images/diario-stress.png)
![Mostrar conteúdo do CSV](/docs/MEUS_TESTES/images/resustados-csv.png)
---

# Hipóteses de Gargalo
Com base nos resultados observados, os possíveis gargalos identificados foram:

## Banco de dados
Possível limitação no gerenciamento de conexões simultâneas.

Sintomas observados:
- Crescimento abrupto da taxa de falha em alta concorrência
- Oscilação de estabilidade após ruptura
- Possível saturação do pool de conexões
- Timeout durante picos de carga
---
## CPU do backend
Sob carga extrema houve indícios de:
- Alto consumo de processamento
- Crescimento progressivo do tempo total de execução
- Queda significativa na capacidade de resposta
---
## Operações de I/O (Input/Output)
Possível bloqueio em operações síncronas relacionadas a:
- Escrita e leitura em banco
- Processamento de requisições simultâneas
- Espera por recursos compartilhados
---
## Limitações de concorrência
Os resultados sugerem possível limitação estrutural relacionada a:
- Threads simultâneas
- Workers do servidor
- Gerenciamento de filas internas
- Capacidade de escalabilidade horizontal
---
# Integridade Pós-Stress
Após a execução do stress test foi realizado smoke test de verificação.

Endpoints validados:
- `/`
- `/health`

Resultado observado:
- Os testes smoke pós-stress foram executados com sucesso
- Todos os endpoints responderam corretamente
- A aplicação permaneceu funcional após as cargas elevadas
- Não foram identificadas falhas persistentes após o encerramento do stress test

Resultado dos smoke tests:
- `test_home_responde` → PASSED
- `test_healthcheck` → PASSED
---
# Evidências Geradas
## Arquivos exportados
- `tests/stress/relatorios/stress_resultados.csv`
- `tests/stress/relatorios/diario_stress.md`

Os arquivos contêm:
- Quantidade de usuários simultâneos
- Sucessos e falhas por execução
- Taxa percentual de falhas
- Tempo total de execução
- Configuração utilizada
- Horários de execução
- Métricas observadas durante o stress test

As evidências permitem rastreabilidade completa dos resultados obtidos.

---

# Discussão Arquitetural
## Impacto de troca de banco de dados

### SQLite → PostgreSQL
A substituição por PostgreSQL poderia:
- Melhorar concorrência simultânea
- Reduzir contenção de escrita
- Melhorar gerenciamento de conexões
- Deslocar o ponto de saturação para cargas maiores
- Aumentar estabilidade em cenários de alto volume
---
### Uso de cache (Redis)
A introdução de cache poderia:
- Reduzir leituras repetidas no banco
- Diminuir carga do backend
- Melhorar tempo médio de resposta
- Reduzir gargalos de I/O
- Aumentar estabilidade sob concorrência elevada
---
### Escalabilidade horizontal
A aplicação poderia se beneficiar de:
- Múltiplos workers/processos
- Balanceamento de carga
- Distribuição de requisições
- Separação entre API e processamento assíncrono
---
### Banco remoto
O uso de banco remoto poderia introduzir:
- Maior latência de rede
- Crescimento de timeout
- Dependência de estabilidade da conexão
- Deslocamento do ponto de joelho para cargas menores
---
# Conclusão
Os testes permitiram identificar de forma objetiva os limites operacionais da aplicação sob diferentes níveis de concorrência.

Foi possível:
- Identificar os principais marcos de carga
- Coletar métricas quantitativas de falha
- Validar integridade pós-stress
- Detectar comportamentos de degradação progressiva
- Levantar hipóteses de gargalo arquitetural
- Observar oscilações de recuperação após ruptura

A aplicação apresentou estabilidade até aproximadamente 2.500 usuários simultâneos.

Os primeiros sinais de degradação ocorreram próximos de 5.000 usuários, com saturação perceptível em 7.500 usuários e ruptura crítica em torno de 10.000 usuários simultâneos.

Mesmo após a ruptura, o sistema demonstrou capacidade parcial de recuperação em determinados cenários, indicando possíveis oscilações relacionadas ao gerenciamento interno de recursos.

Os resultados obtidos fornecem base técnica para futuras otimizações de infraestrutura, concorrência e persistência de dados.
