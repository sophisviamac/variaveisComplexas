const form = document.querySelector("#analise-form");
const errorMessage = document.querySelector("#error-message");
const analyzeButton = document.querySelector("#analisar");
const analyzeLabel = document.querySelector("#analisar-label");
const scenario = document.querySelector("#cenario");
const fields = {
    p: document.querySelector("#p"),
    q: document.querySelector("#q"),
    fp: document.querySelector("#fp"),
};

let trianguloChart;
let comparacaoChart;

function formatNumber(value, digits = 2) {
    return new Intl.NumberFormat("pt-BR", {
        minimumFractionDigits: digits,
        maximumFractionDigits: digits,
    }).format(value);
}

function initCharts() {
    const styles = getComputedStyle(document.documentElement);
    const color = (name) => styles.getPropertyValue(name).trim();
    const before = color("--before");
    const after = color("--after");
    const grid = { color: color("--line") };
    const border = { color: color("--line") };

    Chart.defaults.font.family = "Inter, system-ui, sans-serif";
    Chart.defaults.color = color("--muted");
    Chart.defaults.locale = "pt-BR";
    Object.assign(Chart.defaults.plugins.tooltip, {
        backgroundColor: color("--inset"),
        titleColor: color("--text"),
        bodyColor: color("--text"),
        borderColor: color("--line"),
        borderWidth: 1,
        padding: 10,
    });
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) {
        Chart.defaults.animation = false;
    }

    const trianguloContext = document.querySelector("#triangulo-chart");
    trianguloChart = new Chart(trianguloContext, {
        type: "scatter",
        data: {
            datasets: [
                {
                    label: "Triângulo atual",
                    data: [],
                    borderColor: before,
                    backgroundColor: before + "22",
                    borderWidth: 2,
                    fill: true,
                    showLine: true,
                    pointRadius: 0,
                },
                {
                    label: "Triângulo corrigido",
                    data: [],
                    borderColor: after,
                    backgroundColor: after + "18",
                    borderDash: [6, 4],
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
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: ({dataset, parsed}) =>
                            `${dataset.label} · P ${formatNumber(parsed.x)} kW · Q ${formatNumber(parsed.y)} kVAr`,
                    },
                },
            },
            scales: {
                x: { title: { display: true, text: "P · eixo real (kW)" }, beginAtZero: true, grid, border },
                y: { title: { display: true, text: "Q · eixo imaginário (kVAr)" }, beginAtZero: true, grid, border },
            },
        },
    });

    const comparacaoContext = document.querySelector("#comparacao-chart");
    comparacaoChart = new Chart(comparacaoContext, {
        type: "bar",
        data: {
            labels: ["Fator de potência", ["Potência aparente", "(kVA)"]],
            datasets: [
                { label: "Antes", data: [], backgroundColor: before, borderRadius: 5, maxBarThickness: 42 },
                { label: "Depois", data: [], backgroundColor: after, borderRadius: 5, maxBarThickness: 42 },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: "bottom", labels: { boxWidth: 8, usePointStyle: true } },
                tooltip: {
                    callbacks: {
                        title: ([item]) => item.dataIndex === 0 ? "Fator de potência" : "Potência aparente",
                        label: ({dataset, parsed, dataIndex}) =>
                            `${dataset.label}: ${formatNumber(parsed.y)}${dataIndex === 1 ? " kVA" : ""}`,
                    },
                },
            },
            scales: {
                x: { ticks: { maxRotation: 0 }, grid: { display: false }, border },
                y: { beginAtZero: true, title: { display: true, text: "Valor / escala mista" }, grid, border },
            },
        },
    });
}

function updatePhasors(fasores) {
    for (const estado of ["antes", "depois"]) {
        const {corrente_rms_a, angulo_graus, vetor} = fasores[estado];
        const line = document.querySelector(`#corrente-${estado}-vetor`);
        line.setAttribute("x2", vetor.x);
        line.setAttribute("y2", vetor.y);
        document.querySelector(`#corrente-${estado}`).textContent =
            `${formatNumber(corrente_rms_a)} A RMS ∠ ${formatNumber(angulo_graus)}°`;
    }

    const {arco, angulo_graus} = fasores.antes;
    document.querySelector("#defasagem-arco").setAttribute("d",
        angulo_graus === 0 ? "" : `M .29 0 A .29 .29 0 0 1 ${arco.x} ${arco.y}`);
    const {potencia_recomposta_kw, potencia_recomposta_kvar} = fasores.antes;
    document.querySelector("#potencia-recomposta").textContent =
        `${formatNumber(potencia_recomposta_kw)} + j${formatNumber(potencia_recomposta_kvar)} kVA`;
}

function updateUI(resultado, scenarioName) {
    const {modulo_kva, argumento_graus} = resultado.potencia_complexa;
    document.querySelector("#cenario-analisado").textContent = scenarioName;
    document.querySelector("#potencia-complexa").textContent =
        `${formatNumber(resultado.entrada.p_kw, 4)} + j${formatNumber(resultado.entrada.q_kvar, 4)} kVA`;
    document.querySelector("#potencia-polar").textContent =
        `Forma polar · ${formatNumber(modulo_kva)} kVA ∠ ${formatNumber(argumento_graus)}°`;
    document.querySelector("#potencia-aparente").textContent = `${formatNumber(resultado.potencia_aparente_kva)} kVA`;
    document.querySelector("#angulo").textContent = `${formatNumber(resultado.angulo_graus)}°`;
    document.querySelector("#angulo-antes").textContent = `${formatNumber(resultado.angulo_graus)}°`;
    document.querySelector("#angulo-depois").textContent = `${formatNumber(resultado.angulo_novo_graus)}°`;
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
    updatePhasors(resultado.fasores);
    if (!trianguloChart || !comparacaoChart) return;

    const p = resultado.entrada.p_kw;
    const q = resultado.entrada.q_kvar;
    const qNovo = resultado.q_novo_kvar;
    const maxQ = Math.max(q, qNovo, p * 0.2) * 1.18;
    const maxP = p * 1.18;

    trianguloChart.data.datasets[0].data = resultado.triangulos[0];
    trianguloChart.data.datasets[1].data = resultado.triangulos[1];
    trianguloChart.options.scales.x.suggestedMax = maxP;
    trianguloChart.options.scales.y.suggestedMax = maxQ;
    trianguloChart.update();

    comparacaoChart.data.datasets[0].data = [resultado.fp_atual, resultado.potencia_aparente_kva];
    comparacaoChart.data.datasets[1].data = [resultado.fp_novo, resultado.potencia_aparente_nova_kva];
    comparacaoChart.update();
}

scenario.addEventListener("change", () => {
    if (scenario.value === "personalizado") return;
    const {dataset} = scenario.selectedOptions[0];
    for (const [key, field] of Object.entries(fields)) {
        field.value = dataset[key];
    }
    form.requestSubmit();
});

for (const field of Object.values(fields)) {
    field.addEventListener("input", () => { scenario.value = "personalizado"; });
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (analyzeButton.disabled) return;
    errorMessage.textContent = "";
    analyzeButton.disabled = true;
    scenario.disabled = true;
    analyzeLabel.textContent = "Analisando…";

    const scenarioName = scenario.selectedOptions[0].textContent.trim();
    const body = {
        p_kw: fields.p.value,
        q_kvar: fields.q.value,
        fp_desejado: fields.fp.value,
    };

    try {
        const response = await fetch("/api/analisar", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(body),
        });
        const resultado = await response.json();

        if (!response.ok) {
            throw new Error(resultado.error || "Não foi possível realizar a análise.");
        }

        updateUI(resultado, scenarioName);
    } catch (error) {
        errorMessage.textContent = error.message;
    } finally {
        analyzeButton.disabled = false;
        scenario.disabled = false;
        analyzeLabel.textContent = "Analisar cenário";
    }
});

if (typeof Chart === "undefined") {
    document.querySelectorAll(".chart-plot").forEach((plot) => {
        plot.textContent = "Gráfico indisponível. Recarregue a página para tentar novamente.";
    });
} else {
    initCharts();
}
form.requestSubmit();
