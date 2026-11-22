# PowerFactor Analyzer

Aplicacao web academica em Flask para analisar fator de potencia, potencia complexa e estimar uma compensacao reativa em cargas indutivas.

## Executar

```powershell
cd powerfactor-analyzer
py -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
py -m pip install -r requirements.txt
py app.py
```

Abra `http://127.0.0.1:5000`.

## Testes

```powershell
py -m pytest -q
```

## Calculo

O backend representa a potencia como `S = complex(P, Q)`, utiliza `cmath.phase(S)` para o argumento e `abs(S)` para o modulo/potencia aparente.

- `FP atual = P / |S|`
- `theta atual = arg(S)`
- `theta desejado = acos(FP desejado)`
- `Qc = P * (tan(theta atual) - tan(theta desejado))`
- `Qnovo = Q - Qc`
- `Snovo = complex(P, Qnovo)`

O valor mostrado como compensacao e uma estimacao simplificada em kVAr, nao um dimensionamento executivo de capacitores.

## Figma

Nao havia um design ou integracao Figma fornecida neste projeto. Os tokens visuais principais estao em `static/css/style.css`. O layout pode ser usado como referencia para construir um arquivo Figma sem alterar o comportamento da aplicacao.
