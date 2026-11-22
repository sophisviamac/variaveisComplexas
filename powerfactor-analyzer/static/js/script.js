const form = document.querySelector("#analise-form");
const errorMessage = document.querySelector("#error-message");

let trianguloChart;
let comparacaoChart;

function formatNumber(value, digits = 2) {
    return new Intl.NumberFormat("pt-BR", {
        minimumFractionDigits: digits,
        maximumFractionDigits: digits,
    }).format(value);
}

function initCharts() {
    Chart.defaults.font.family = "DM Sans";
    Chart.defaults.color = "#6d7f8d";

    const trianguloContext = document.querySelector("#triangulo-chart");
    trianguloChart = new Chart(trianguloContext, {
        type: "scatter",
        data: {
            datasets: [
                {
                    label: "Triângulo atual",
                    data: [{x: 0, y: 0}, {x: 10, y: 0}, {x: 10, y: 7.5}, {x: 0, y: 0}],
                    borderColor: "#2f74a5",
                    backgroundColor: "rgba(47,116,165,.12)",
                    borderWidth: 2,
                    fill: true,
                    showLine: true,
                    pointRadius: 0,
                },
                {
                    label: "Triângulo corrigido",
                    data: [{x: 0, y: 0}, {x: 10, y: 0}, {x: 10, y: 3.29}, {x: 0, y: 0}],
                    borderColor: "#138a72",
                    backgroundColor: "rgba(19,138,114,.09)",
                    borderWidth: 2,
                    fill: true,
                    showLine: true,
                    pointRadius: 0,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { title: { display: true, text: "Potência ativa P (kW)" }, beginAtZero: true, grid: { color: "#edf1f3" } },
                y: { title: { display: true, text: "Potência reativa Q (kVAr)" }, beginAtZero: true, grid: { color: "#edf1f3" } },
            },
        },
    });

    const comparacaoContext = document.querySelector("#comparacao-chart");
    comparacaoChart = new Chart(comparacaoContext, {
        type: "bar",
        data: {
            labels: ["Fator de potência", "Potência aparente"],
            datasets: [
                { label: "Antes", data: [0.8, 12.5], backgroundColor: "#2f74a5", borderRadius: 4, maxBarThickness: 42 },
                { label: "Depois", data: [0.95, 10.53], backgroundColor: "#55a7a3", borderRadius: 4, maxBarThickness: 42 },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: "bottom", labels: { boxWidth: 8, usePointStyle: true } } },
            scales: {
                x: { grid: { display: false } },
                y: { beginAtZero: true, title: { display: true, text: "Valor / escala mista" }, grid: { color: "#edf1f3" } },
            },
        },
    });
}

function updateUI(resultado) {
    const complexa = resultado.potencia_complexa.retangular;
    document.querySelector("#potencia-complexa").textContent = complexa.replace(" kVA", "");
    document.querySelector("#potencia-aparente").textContent = `${formatNumber(resultado.potencia_aparente_kva)} kVA`;
    document.querySelector("#angulo").textContent = `${formatNumber(resultado.angulo_graus)}°`;
    document.querySelector("#fp-atual").textContent = formatNumber(resultado.fp_atual);
    document.querySelector("#fp-novo").textContent = formatNumber(resultado.fp_novo);
    document.querySelector("#compensacao").textContent = `${formatNumber(resultado.qc_kvar)} kVAr`;

    const banner = document.querySelector("#diagnostico");
    const titulo = document.querySelector("#diagnostico-titulo");
    const texto = document.querySelector("#diagnostico-texto");
    const icone = banner.querySelector(".diagnostic-icon");

    banner.className = resultado.atende_meta ? "diagnostic-banner ok" : "diagnostic-banner warning";
    icone.textContent = resultado.atende_meta ? "✓" : "!";
    titulo.textContent = resultado.atende_meta ? "Fator de potência adequado" : "Fator de potência inadequado";
    texto.textContent = resultado.diagnostico;

    const p = resultado.entrada.p_kw;
    const q = resultado.entrada.q_kvar;
    const qNovo = resultado.q_novo_kvar;
    const maxQ = Math.max(q, qNovo, p * 0.2) * 1.18;
    const maxP = p * 1.18;

    trianguloChart.data.datasets[0].data = [
        {x: 0, y: 0}, {x: p, y: 0}, {x: p, y: q}, {x: 0, y: 0},
    ];
    trianguloChart.data.datasets[1].data = [
        {x: 0, y: 0}, {x: p, y: 0}, {x: p, y: qNovo}, {x: 0, y: 0},
    ];
    trianguloChart.options.scales.x.suggestedMax = maxP;
    trianguloChart.options.scales.y.suggestedMax = maxQ;
    trianguloChart.update();

    comparacaoChart.data.datasets[0].data = [resultado.fp_atual, resultado.potencia_aparente_kva];
    comparacaoChart.data.datasets[1].data = [resultado.fp_novo, resultado.potencia_aparente_nova_kva];
    comparacaoChart.update();
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    errorMessage.textContent = "";

    const body = {
        p_kw: document.querySelector("#p").value,
        q_kvar: document.querySelector("#q").value,
        fp_desejado: document.querySelector("#fp").value,
    };

    try {
        const response = await fetch("/api/analisar", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(body),
        });
        const resultado = await response.json();

        if (!response.ok) {
            throw new Error(resultado.error || "Nao foi possivel realizar a analise.");
        }

        updateUI(resultado);
    } catch (error) {
        errorMessage.textContent = error.message;
    }
});

initCharts();

fetch("/api/analisar", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({p_kw: 10, q_kvar: 7.5, fp_desejado: 0.95}),
})
    .then((response) => response.json())
    .then((resultado) => {
        if (!resultado.error) updateUI(resultado);
    });
