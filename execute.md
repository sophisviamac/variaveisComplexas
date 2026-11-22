# PROJETO: PowerFactor Analyzer — Diagnóstico de Eficiência Energética com Variáveis Complexas

Atue como um desenvolvedor Full-Stack Python experiente, com conhecimentos de UX/UI Design, Figma e desenvolvimento de aplicações científicas.

Preciso que você desenvolva uma aplicação web acadêmica chamada **PowerFactor Analyzer**, voltada à análise e correção do fator de potência em instalações elétricas utilizando números complexos.

O projeto será apresentado individualmente na disciplina de **Variáveis Complexas**, do curso de Engenharia de Computação.

**Prioridade:** simplicidade, organização, precisão matemática, interface visualmente bonita e facilidade de demonstração.

## 1. Objetivo do projeto

Desenvolver um sistema que permita ao usuário inserir dados elétricos de uma instalação, calcular a potência complexa, identificar um fator de potência inadequado e estimar a compensação reativa necessária para atingir uma meta definida.

O sistema deve demonstrar claramente como números complexos são aplicados à resolução de um problema real da Engenharia.

Não desenvolver uma aplicação industrial completa. Trata-se de um protótipo acadêmico com dados simulados.

## 2. Tecnologias

Utilize:

- **Python:** responsável pelos cálculos matemáticos.
- **Flask:** integração entre o Python e a interface web.
- **HTML5:** estrutura da interface.
- **CSS3:** estilização moderna, organizada e responsiva.
- **JavaScript:** interatividade sem recarregar a página.
- **Chart.js:** visualização de resultados, quando adequado.
- **Figma:** referência de design e organização da identidade visual.

Evite bancos de dados, autenticação, bibliotecas desnecessárias e arquiteturas complexas.

## 3. Integração com Figma

Verifique se existe uma integração MCP com o Figma disponível no ambiente de desenvolvimento.

Caso esteja disponível:

1. Verifique se existe um arquivo ou design de referência fornecido no projeto.
2. Utilize as informações visuais desse arquivo para implementar a interface.
3. Preserve cores, tipografia, espaçamento, componentes e organização visual.
4. Se as ferramentas conectadas permitirem criar um design no Figma, organize uma proposta visual correspondente ao dashboard.
5. Mantenha consistência entre o design e sua implementação.

Se o Figma não estiver conectado ou nenhum arquivo estiver disponível, continue normalmente com uma identidade visual própria e um conjunto organizado de design tokens em CSS, preparado para futura utilização no Figma.

Não interrompa o desenvolvimento por falta dessa integração e não afirme que houve sincronização caso ela não tenha ocorrido.

## 4. Identidade visual

Quero uma interface com aparência de software profissional de monitoramento energético.

Diretrizes:

- Design minimalista e moderno.
- Paleta baseada em azul-marinho, azul, verde e tons neutros.
- Cards com bordas suaves e cantos arredondados.
- Tipografia limpa e legível.
- Ícones discretos.
- Espaçamento consistente.
- Gráficos com legendas e unidades.
- Layout responsivo para desktop e notebook.
- Feedback visual para diagnóstico adequado ou inadequado.

Evite excesso de animações, elementos decorativos e informações desnecessárias.

## 5. Estrutura da interface

Desenvolva uma única página principal, organizada nas seguintes seções:

### A. Cabeçalho

Exibir:

**PowerFactor Analyzer**

Subtítulo: "Análise e Correção do Fator de Potência utilizando Números Complexos".

### B. Entrada de dados

Criar três campos:

- Potência ativa (P), em kW.
- Potência reativa indutiva (Q), em kVAr.
- Fator de potência desejado.

Adicionar um botão **Analisar instalação**.

Iniciar com valores demonstrativos:

- P = 10 kW
- Q = 7,5 kVAr
- FP desejado = 0,95

### C. Diagnóstico energético

Apresentar cards com:

- Potência complexa.
- Potência aparente.
- Ângulo de defasagem.
- Fator de potência atual.
- Fator de potência após a compensação proposta.
- Compensação reativa necessária.

Exibir um diagnóstico textual simples, informando se o fator de potência está abaixo da meta.

### D. Gráficos interativos

Desenvolver dois gráficos:

**Gráfico 1 — Triângulo de potências**

Representar geometricamente a potência complexa no plano complexo:

- Eixo horizontal: potência ativa P.
- Eixo vertical: potência reativa Q.
- Hipotenusa: módulo da potência complexa.
- Ângulo de defasagem.

Exibir visualmente os triângulos antes e depois da compensação.

**Gráfico 2 — Comparação de resultados**

Comparar:

- Fator de potência antes e depois.
- Potência aparente antes e depois.

Usar gráficos adequados e unidades corretas.

### E. Fundamentação matemática

Criar uma pequena seção chamada **"Variáveis Complexas aplicadas"**.

Mostrar as equações utilizadas no cálculo e destacar os conceitos:

- Parte real e imaginária.
- Módulo.
- Argumento.
- Forma polar.
- Representação geométrica no plano complexo.

A seção deve ajudar o professor a compreender a relação entre o sistema e os conteúdos da disciplina.

## 6. Fundamentação matemática obrigatória

Implementar os cálculos corretamente em Python, utilizando as bibliotecas `math` e `cmath`.

### Potência complexa

S = P + jQ

### Potência aparente

|S| = sqrt(P² + Q²)

### Ângulo de defasagem

θ = arg(S)

### Fator de potência

FP = P / |S|

### Forma polar

S = |S| · e^(jθ)

### Compensação reativa

Qc = P · [tan(θ_atual) - tan(θ_desejado)]

A potência reativa após a compensação deve ser calculada por:

Q_novo = Q - Qc

A nova potência complexa será:

S_novo = P + jQ_novo

E o fator de potência corrigido deve ser recalculado a partir dessa nova potência complexa.

**Regras de implementação:**

- Considerar inicialmente apenas cargas indutivas, P positivo, Q não negativo, regime senoidal e modelo simplificado de instalação equilibrada.
- Validar entradas e impedir valores inválidos.
- Quando o fator de potência atual já atender à meta, a compensação necessária deve ser zero.
- Não permitir compensação negativa.
- Não confundir potência complexa, em kVA, com seu módulo (potência aparente).
- Manter as unidades físicas corretas.
- Não apresentar a compensação calculada como dimensionamento executivo de capacitores.
- Não prometer economia financeira ou redução direta de consumo em kWh.

## 7. Validação dos resultados

Usar como primeiro caso de teste:

P = 10 kW  
Q = 7,5 kVAr  
FP desejado = 0,95

Resultados esperados, aproximadamente:

- Potência complexa: 10 + 7,5j.
- Potência aparente: 12,50 kVA.
- Ângulo: 36,87°.
- Fator de potência atual: 0,80.
- Compensação: 4,21 kVAr.
- Potência aparente após compensação: 10,53 kVA.
- Fator de potência final: 0,95.

Criar também testes para instalações que já atendem à meta e para entradas inválidas.

## 8. Organização do código

Utilize uma estrutura pequena e didática:

```text
powerfactor-analyzer/
├── app.py
├── calculos.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
└── tests/
    └── test_calculos.py
```

**app.py:** rotas Flask e integração frontend/backend.

**calculos.py:** funções matemáticas independentes e documentadas.

**index.html:** estrutura do dashboard.

**style.css:** identidade visual e responsividade.

**script.js:** comunicação com Flask e atualização dinâmica dos resultados.

**README.md:** instruções de instalação, execução, explicação matemática e funcionamento.

## 9. Requisitos de funcionamento

O sistema deve:

1. Abrir localmente no navegador.
2. Receber os dados inseridos pelo usuário.
3. Enviar os valores ao Python.
4. Executar os cálculos reais no backend.
5. Retornar os resultados para a interface.
6. Atualizar automaticamente os cards e gráficos.
7. Exibir mensagens claras em caso de erro.
8. Funcionar sem banco de dados ou serviços pagos.

Não simular resultados fixos no frontend. Todos os diagnósticos devem depender dos cálculos realizados no Python.

## 10. Cuidados com o contexto acadêmico

Este é um projeto de Variáveis Complexas, não apenas de instalações elétricas.

Portanto, os números complexos devem aparecer explicitamente:

- Nos cálculos do Python.
- Na representação do plano complexo.
- Nos gráficos.
- Na fundamentação matemática.
- Na interpretação dos resultados.

Utilize nomes de variáveis e comentários que facilitem a compreensão.

A aplicação deve ser simples o suficiente para que uma estudante consiga explicar a matemática e demonstrar o funcionamento em aproximadamente 3 minutos durante uma apresentação acadêmica.

## 11. Entregáveis

Ao finalizar, quero:

- Código completo, organizado e funcional.
- Dashboard responsivo e visualmente profissional.
- Cálculos matemáticos implementados em Python.
- Gráficos interativos.
- Testes básicos automatizados.
- README com instruções de execução.
- Instruções para conectar ou utilizar os elementos do Figma, quando a integração estiver disponível.

Não incluir recursos adicionais sem necessidade.

**Importante:** implemente o projeto completo, não apenas um protótipo visual. Priorize primeiro o funcionamento dos cálculos, depois a integração e, por último, o refinamento visual. Execute os testes disponíveis e corrija os problemas encontrados antes de finalizar.
