# PowerFactor Analyzer

**Aplicação de Variáveis Complexas na Análise e Correção do Fator de Potência de Motores Elétricos: Uma Abordagem Computacional**

Aplicação web em Flask para simular o fator de potência de motores em uma instalação industrial hipotética. A análise usa a potência ativa elétrica absorvida em kW, a potência reativa indutiva em kVAr e a meta de fator de potência. Os resultados são didáticos e não correspondem a medições, intervenções físicas ou dimensionamento de capacitores.

## Executar

Na raiz do repositório, entre em `powerfactor-analyzer`. Execute os comandos nessa pasta.

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Abra `http://127.0.0.1:5000`. Os gráficos comparativos usam Chart.js via CDN. Os indicadores e o gráfico SVG de fasores são servidos pela aplicação.

## Cenários simulados

| Carga | Potência ativa | Potência reativa | Meta de FP |
| --- | ---: | ---: | ---: |
| Motor de esteira | 10 kW | 7,5 kVAr | 0,95 |
| Conjunto de bombas | 45 kW | 33 kVAr | 0,95 |
| Ventiladores industriais | 24 kW | 6 kVAr | 0,95 |

A escolha de um cenário preenche os campos e executa a análise. Edite os valores e use **Analisar cenário** para simular uma carga personalizada. No exemplo da esteira, o fator de potência vai de 0,80 a 0,95 com uma compensação estimada de 4,21 kVAr. O cenário dos ventiladores já atende à meta e retorna compensação zero.

## Modelo matemático

- O backend calcula a potência complexa `S = P + jQ`, o módulo `|S| = √(P² + Q²)`, o argumento `θ = arg(S)` e a forma polar `S = |S| · exp(jθ)`.
- O fator de potência é `P / |S|`. Quando o fator inicial está abaixo da meta, a potência reativa residual é `P · tan(acos(FP desejado))` e a compensação capacitiva estimada é a diferença entre Q inicial e residual. Se a carga já atende à meta, a compensação é zero.
- Os fasores pertencem a um **modelo monofásico equivalente agregado**, com tensão RMS fictícia `V = 230 V ∠ 0°`. A corrente equivalente é `I = conj(S / V)`, usando S em VA e V em volts, de modo que `V · conj(I) = S`. Na carga indutiva, a corrente tem ângulo negativo e atrasa em relação à tensão.
- As duas correntes usam a mesma escala no diagrama, normalizada pela corrente inicial. A tensão usa escala própria. Os valores RMS e os ângulos aparecem ao lado dos vetores.

Para a apresentação, use a esteira para introduzir o diagnóstico e o triângulo de potências. Em seguida, mostre a redução da defasagem no diagrama de fasores e use os ventiladores para ilustrar uma carga que já atende à meta.

## Testes

Na pasta `powerfactor-analyzer`:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```
