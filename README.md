# Relatório de Análise dos Top-10 Repositórios

##Autores: Pedro Motta e Vítor Lion

## Introdução

O desenvolvimento open source tem ganhado enorme popularidade nas últimas décadas, quebrando barreiras comerciais e proporcionando colaboração entre empresas e comunidades globais. Organizações como Facebook, Microsoft e Google têm adotado estratégias de open source em diversas áreas, colaborando com a comunidade para criar ferramentas e APIs amplamente utilizadas. Um exemplo notável é o React, desenvolvido pelo Facebook, que se tornou um dos frameworks mais utilizados para construção de interfaces web.

Este estudo tem como objetivo comparar os **top-10 repositórios mais populares** (por estrelas) das organizações **Facebook**, **Microsoft** e **Google**, coletando e analisando dados sobre as métricas de atividade, como a idade dos repositórios, número de issues abertas, pull requests aceitas, releases e a frequência de atualizações. A comparação tem como objetivo identificar padrões de comportamento entre essas grandes organizações no GitHub.

## Metodologia

### Organizações Alvo

As organizações analisadas foram definidas pelos seus nomes registrados no GitHub:
- `facebook`
- `microsoft`
- `google`

### Coleta de Dados

#### API do GitHub

Os dados foram obtidos utilizando a API REST do GitHub, com autenticação via **token**.

#### Repositórios Selecionados

- Para cada organização, foi coletada uma lista de todos os repositórios públicos ordenados por número de estrelas, em ordem decrescente.
- Dos repositórios retornados, apenas os 10 mais populares foram selecionados para análise.

#### Informações Extraídas

Foram coletadas as seguintes informações para cada repositório:
- **Dados gerais do repositório:**
  - Nome do repositório.
  - Data de criação (`created_at`).
  - Última atualização (`updated_at`).
  - Número total de estrelas (`stargazers_count`).
  - Linguagem principal (`language`).
  - Descrição do repositório (`description`).
  - Número de forks (`forks_count`).

- **Atividade do repositório:**
  - Número total de issues abertas e fechadas (`open_issues_count`).
  - Número total de pull requests aceitas:
    - Obtido pelo endpoint `/pulls` filtrando apenas pull requests fechadas.
    - O total foi extraído do cabeçalho `Link` retornado pela API.
  - Número total de releases:
    - Obtido pelo endpoint `/releases`.
    - O total foi extraído do cabeçalho `Link`.

### Processamento dos Dados

- Todos os dados coletados foram armazenados em um arquivo CSV (`repositorios_top10.csv`), estruturado com as seguintes colunas:
  - Organização.
  - Nome do repositório.
  - Estrelas.
  - Data de criação.
  - Última atualização.
  - Total de issues.
  - Pull requests aceitas.
  - Total de releases.
  - Linguagem.
  - Descrição.
  - Forks.

- As informações foram processadas, agrupadas e ordenadas para facilitar análises posteriores.

### Limitações

#### Restrição ao Top-10 Repositórios
- Apenas os 10 repositórios mais populares de cada organização foram considerados, o que pode limitar a generalização dos resultados para toda a organização.

#### Problemas de Conexão
- Requisições HTTP podem falhar devido a problemas de rede ou limites da API. Erros foram tratados com mensagens informativas e a coleta continuou para as demais organizações.

#### Métricas Calculadas
- Algumas métricas, como o total de pull requests aceitas e releases, dependem de informações indiretas no cabeçalho da resposta da API, podendo estar sujeitas a inconsistências.

### Ferramentas Utilizadas

- **Linguagem:** Python 3.
- **Bibliotecas:**
  - `requests`: Para realizar requisições HTTP.
  - `csv`: Para salvar e organizar os dados coletados.
  - `datetime`: Para manipulação de datas.

## Resultados

### RQ01: Organização com o repositório mais antigo

- **Hipótese Nula (H0):** Não há diferença significativa entre as organizações em relação à idade do repositório.
- **Hipótese Alternativa (H1):** A organização **Facebook** possui o repositório mais antigo.
- **Justificativa:** O Facebook começou a adotar estratégias de open-source cedo, promovendo tecnologias amplamente aceitas, como React e Jest, enquanto Google e Microsoft inicialmente centralizaram seus desenvolvimentos.
- **Resultado:** Na mediana, a organização **Facebook** tem os repositórios mais antigos, com uma média de idade superior em comparação com Microsoft e Google.

### RQ02: Organização com mais issues

- **Hipótese Nula (H0):** Não há diferença significativa entre as organizações em relação ao número de issues.
- **Hipótese Alternativa (H1):** A organização **Facebook** possui mais issues em seus repositórios.
- **Justificativa:** O maior uso de frameworks do Facebook, como React e React Native, por desenvolvedores externos pode gerar mais issues reportadas pela comunidade.
- **Resultado:** Na mediana, a organização **Facebook** possui o maior número de issues totais nos seus top-10 repositórios.

### RQ03: Organização com mais contribuições via pull requests aceitas

- **Hipótese Nula (H0):** Não há diferença significativa entre as organizações em relação ao número de pull requests aceitas.
- **Hipótese Alternativa (H1):** A organização **Facebook** possui mais pull requests aceitas.
- **Justificativa:**  Repositórios amplamente utilizados e bem documentados frequentemente atraem mais contribuições externas, e o Facebook tende a priorizar colaborações de código aberto.
- **Resultado:** Na mediana, a organização **Facebook** tem mais pull requests aceitas nos seus repositórios em comparação com Microsoft e Google.

### RQ04: Organização que lança releases com mais frequência

- **Hipótese Nula (H0):** Não há diferença significativa entre as organizações em relação à frequência de releases.
- **Hipótese Alternativa (H1):** A organização **Facebook** lança mais releases com mais frequência.
- **Justificativa:** Produtos em rápida evolução e com adoção massiva, como React, demandam lançamentos frequentes para atender às expectativas da comunidade.
- **Resultado:** Na mediana, a organização **Facebook** é a que lança mais releases com mais frequência.

### RQ05: Organização com repositórios mais atualizados recentemente

- **Hipótese Nula (H0):** Não há diferença significativa entre as organizações em relação à frequência de atualizações.
- **Hipótese Alternativa (H1):** A organização **Facebook** possui repositórios mais atualizados recentemente.
- **Justificativa:** A cultura de desenvolvimento iterativo do Facebook pode resultar em atualizações mais frequentes em comparação com os repositórios de Microsoft e Google.
- **Resultado:** Na mediana, a organização **Facebook** possui repositórios mais atualizados recentemente quando comparado com Google e Microsoft.

## Testes Estatísticos ANOVA

Os testes ANOVA foram realizados para determinar se há diferenças estatisticamente significativas entre as organizações nas métricas analisadas.

#### Resultados ANOVA por Métrica

| Métrica                        | Estatística F | P-valor | Interpretação                                   |
|--------------------------------|---------------|---------|------------------------------------------------|
| **Idade do Repositório (dias)**| 83.4441       | 0.0000  | Há diferença significativa entre as organizações. |
| **Total de Issues**            | 6.4451        | 0.0051  | Há diferença significativa entre as organizações. |
| **Pull Requests Aceitas**      | 11.4405       | 0.0003  | Há diferença significativa entre as organizações. |
| **Total de Releases**          | 6.2097        | 0.0060  | Há diferença significativa entre as organizações. |
| **Dias desde Última Atualização** | 3.3195      | 0.0514  | Não há diferença significativa entre as organizações. |

#### Interpretação dos P-valores

Os p-valores apresentados indicam a probabilidade de que os resultados obtidos tenham ocorrido ao acaso, assumindo que a hipótese nula é verdadeira.

- **P-valor < 0.05:** Rejeitamos a hipótese nula (H_0), indicando diferença significativa entre as organizações.
  - Exemplo: Para "Idade do Repositório", o p-valor é 0.0000, indicando que a idade média dos repositórios difere significativamente entre Facebook, Microsoft e Google.

- **P-valor ≥ 0.05:** Não rejeitamos a hipótese nula (H_0), indicando que não há diferença significativa entre as organizações.
  - Exemplo: Para "Dias desde Última Atualização", o p-valor é 0.0514, sugerindo que a frequência de atualizações recentes é semelhante entre as organizações.


## Discussão

A análise dos dados coletados demonstra uma clara predominância da organização **Facebook** em termos de popularidade dos repositórios (medida por estrelas) e atividade de desenvolvimento. A maioria das métricas analisadas (idade, número de issues, pull requests aceitas, releases e atualizações) apontam para o Facebook como a organização mais ativa entre as três consideradas.

É interessante observar que, apesar de o Google e a Microsoft também possuírem repositórios populares e com alta atividade, o Facebook parece ter um maior número de contribuições externas e lançamentos frequentes de releases.

## Conclusão

A análise revelou que a organização **Facebook** apresenta liderança em diversas métricas de popularidade e atividade dos repositórios open-source. O foco em frameworks amplamente utilizados e uma cultura colaborativa parecem justificar esses resultados.

Por outro lado, tanto o Google quanto a Microsoft também apresentam repositórios significativos, mas com abordagens possivelmente mais voltadas para projetos específicos e fechados.

### Implicações

Para Comunidade Open Source: As organizações podem adotar estratégias semelhantes às do Facebook para fomentar contribuições externas, garantindo documentação acessível e uma política ativa de aceitação de pull requests.

Para Pesquisadores: Estudos futuros podem ampliar a análise para incluir mais repositórios, ou investigar como métricas como "qualidade do código" se correlacionam com as atividades analisadas.
