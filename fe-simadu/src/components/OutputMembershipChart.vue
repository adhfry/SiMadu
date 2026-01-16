<script setup lang="ts">
import { computed } from "vue";
import { Line } from "vue-chartjs";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
  type ChartOptions,
  type ChartData,
} from "chart.js";
import annotationPlugin from "chartjs-plugin-annotation";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
  annotationPlugin
);

interface Props {
  aggregation: {
    A_plus: number;
    A: number;
    A_minus: number;
    B_plus: number;
    B: number;
    B_minus: number;
    C_plus: number;
    C: number;
    C_minus: number;
  };
}

const props = defineProps<Props>();

// Generate output membership functions - 9 GRADES
const generateOutputMembership = () => {
  const xValues = Array.from({ length: 101 }, (_, i) => i);

  // Grade C-: Trapesium Kiri [0, 0, 5, 15]
  const gradeC_minus = xValues.map((x) => {
    if (x <= 5) return 1.0;
    if (x > 5 && x < 15) return (15 - x) / 10;
    return 0.0;
  });

  // Grade C: Segitiga [10, 20, 30]
  const gradeC = xValues.map((x) => {
    if (x <= 10 || x >= 30) return 0.0;
    if (x > 10 && x <= 20) return (x - 10) / 10;
    return (30 - x) / 10;
  });

  // Grade C+: Segitiga [25, 35, 45]
  const gradeCPlus = xValues.map((x) => {
    if (x <= 25 || x >= 45) return 0.0;
    if (x > 25 && x <= 35) return (x - 25) / 10;
    return (45 - x) / 10;
  });

  // Grade B-: Segitiga [40, 48, 56]
  const gradeBMinus = xValues.map((x) => {
    if (x <= 40 || x >= 56) return 0.0;
    if (x > 40 && x <= 48) return (x - 40) / 8;
    return (56 - x) / 8;
  });

  // Grade B: Segitiga [52, 60, 68]
  const gradeB = xValues.map((x) => {
    if (x <= 52 || x >= 68) return 0.0;
    if (x > 52 && x <= 60) return (x - 52) / 8;
    return (68 - x) / 8;
  });

  // Grade B+: Segitiga [64, 72, 80]
  const gradeBPlus = xValues.map((x) => {
    if (x <= 64 || x >= 80) return 0.0;
    if (x > 64 && x <= 72) return (x - 64) / 8;
    return (80 - x) / 8;
  });

  // Grade A-: Segitiga [75, 82, 89]
  const gradeAMinus = xValues.map((x) => {
    if (x <= 75 || x >= 89) return 0.0;
    if (x > 75 && x <= 82) return (x - 75) / 7;
    return (89 - x) / 7;
  });

  // Grade A: Segitiga [85, 91, 97]
  const gradeA = xValues.map((x) => {
    if (x <= 85 || x >= 97) return 0.0;
    if (x > 85 && x <= 91) return (x - 85) / 6;
    return (97 - x) / 6;
  });

  // Grade A+: Trapesium Kanan [92, 96, 100, 100]
  const gradeAPlus = xValues.map((x) => {
    if (x < 92) return 0.0;
    if (x >= 92 && x < 96) return (x - 92) / 4;
    return 1.0;
  });

  return {
    xValues,
    gradeC_minus,
    gradeC,
    gradeCPlus,
    gradeBMinus,
    gradeB,
    gradeBPlus,
    gradeAMinus,
    gradeA,
    gradeAPlus,
  };
};

const {
  xValues,
  gradeC_minus,
  gradeC,
  gradeCPlus,
  gradeBMinus,
  gradeB,
  gradeBPlus,
  gradeAMinus,
  gradeA,
  gradeAPlus,
} = generateOutputMembership();

const chartData = computed<ChartData<"line">>(() => ({
  labels: xValues,
  datasets: [
    {
      label: "🔴 C-",
      data: gradeC_minus,
      borderColor: "rgb(127, 29, 29)",
      backgroundColor: "rgba(127, 29, 29, 0.12)",
      borderWidth: 1.8,
      fill: true,
      pointRadius: 0,
      tension: 0,
    },
    {
      label: "🟠 C",
      data: gradeC,
      borderColor: "rgb(220, 38, 38)",
      backgroundColor: "rgba(220, 38, 38, 0.12)",
      borderWidth: 1.8,
      fill: true,
      pointRadius: 0,
      tension: 0,
    },
    {
      label: "🟡 C+",
      data: gradeCPlus,
      borderColor: "rgb(249, 115, 22)",
      backgroundColor: "rgba(249, 115, 22, 0.12)",
      borderWidth: 1.8,
      fill: true,
      pointRadius: 0,
      tension: 0,
    },
    {
      label: "🟢 B-",
      data: gradeBMinus,
      borderColor: "rgb(251, 191, 36)",
      backgroundColor: "rgba(251, 191, 36, 0.12)",
      borderWidth: 1.8,
      fill: true,
      pointRadius: 0,
      tension: 0,
    },
    {
      label: "🟦 B",
      data: gradeB,
      borderColor: "rgb(234, 179, 8)",
      backgroundColor: "rgba(234, 179, 8, 0.12)",
      borderWidth: 1.8,
      fill: true,
      pointRadius: 0,
      tension: 0,
    },
    {
      label: "🔵 B+",
      data: gradeBPlus,
      borderColor: "rgb(59, 130, 246)",
      backgroundColor: "rgba(59, 130, 246, 0.12)",
      borderWidth: 1.8,
      fill: true,
      pointRadius: 0,
      tension: 0,
    },
    {
      label: "💙 A-",
      data: gradeAMinus,
      borderColor: "rgb(14, 165, 233)",
      backgroundColor: "rgba(14, 165, 233, 0.12)",
      borderWidth: 1.8,
      fill: true,
      pointRadius: 0,
      tension: 0,
    },
    {
      label: "💚 A",
      data: gradeA,
      borderColor: "rgb(34, 197, 94)",
      backgroundColor: "rgba(34, 197, 94, 0.12)",
      borderWidth: 1.8,
      fill: true,
      pointRadius: 0,
      tension: 0,
    },
    {
      label: "⭐ A+",
      data: gradeAPlus,
      borderColor: "rgb(22, 163, 74)",
      backgroundColor: "rgba(22, 163, 74, 0.12)",
      borderWidth: 1.8,
      fill: true,
      pointRadius: 0,
      tension: 0,
    },
  ],
}));

const chartOptions = computed<ChartOptions<"line">>(() => ({
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: "index",
    intersect: false,
  },
  layout: {
    padding: {
      top: 5,
      bottom: 5,
      left: 5,
      right: 5,
    },
  },
  plugins: {
    legend: {
      display: true,
      position: "top",
      align: "center",
      labels: {
        usePointStyle: true,
        padding: 4,
        font: {
          size: 8,
          weight: 500,
        },
        boxWidth: 7,
        boxHeight: 7,
      },
    },
    title: {
      display: true,
      text: "Fungsi Keanggotaan OUTPUT (Mutu Tembakau)",
      font: {
        size: 12,
        weight: "bold",
      },
      padding: {
        top: 0,
        bottom: 8,
      },
    },
    tooltip: {
      backgroundColor: "rgba(17, 24, 39, 0.95)",
      padding: 10,
      titleFont: {
        size: 11,
        weight: "bold",
      },
      bodyFont: {
        size: 10,
      },
      callbacks: {
        label: function (context) {
          const label = context.dataset.label || "";
          const value = context.parsed.y;
          return `${label}: μ = ${value?.toFixed(3)}`;
        },
      },
    },
    annotation: {
      annotations: {
        // Alpha-cut lines
        alphaA: {
          type: "line",
          yMin: props.aggregation.A,
          yMax: props.aggregation.A,
          borderColor: "rgba(34, 197, 94, 0.7)",
          borderWidth: 2,
          borderDash: [6, 3],
          label: {
            content: `α-cut A: ${props.aggregation.A.toFixed(3)}`,
            display: props.aggregation.A > 0.01,
            position: "end",
            backgroundColor: "rgba(34, 197, 94, 0.9)",
            color: "white",
            font: {
              size: 9,
              weight: "bold",
            },
            padding: 4,
          },
        },
        alphaB: {
          type: "line",
          yMin: props.aggregation.B,
          yMax: props.aggregation.B,
          borderColor: "rgba(234, 179, 8, 0.7)",
          borderWidth: 2,
          borderDash: [6, 3],
          label: {
            content: `α-cut B: ${props.aggregation.B.toFixed(3)}`,
            display: props.aggregation.B > 0.01,
            position: "end",
            backgroundColor: "rgba(234, 179, 8, 0.9)",
            color: "white",
            font: {
              size: 9,
              weight: "bold",
            },
            padding: 4,
          },
        },
        alphaC: {
          type: "line",
          yMin: props.aggregation.C,
          yMax: props.aggregation.C,
          borderColor: "rgba(249, 115, 22, 0.7)",
          borderWidth: 2,
          borderDash: [6, 3],
          label: {
            content: `α-cut C: ${props.aggregation.C.toFixed(3)}`,
            display: props.aggregation.C > 0.01,
            position: "end",
            backgroundColor: "rgba(249, 115, 22, 0.9)",
            color: "white",
            font: {
              size: 9,
              weight: "bold",
            },
            padding: 4,
          },
        },
        alphaCMinus: {
          type: "line",
          yMin: props.aggregation.C_minus,
          yMax: props.aggregation.C_minus,
          borderColor: "rgba(127, 29, 29, 0.7)",
          borderWidth: 2,
          borderDash: [6, 3],
          label: {
            content: `α C-: ${props.aggregation.C_minus.toFixed(3)}`,
            display: props.aggregation.C_minus > 0.01,
            position: "start",
            backgroundColor: "rgba(127, 29, 29, 0.9)",
            color: "white",
            font: {
              size: 9,
              weight: "bold",
            },
            padding: 4,
          },
        },
      },
    },
  },
  scales: {
    x: {
      title: {
        display: true,
        text: "Nilai Mutu (0-100)",
        font: {
          size: 11,
          weight: "bold",
        },
        padding: { top: 8 },
      },
      ticks: {
        maxTicksLimit: 12,
        font: {
          size: 8,
        },
      },
      grid: {
        color: "rgba(0, 0, 0, 0.05)",
      },
    },
    y: {
      title: {
        display: true,
        text: "Derajat Keanggotaan (μ)",
        font: {
          size: 11,
          weight: "bold",
        },
        padding: { bottom: 8 },
      },
      min: 0,
      max: 1.05,
      ticks: {
        stepSize: 0.2,
        font: {
          size: 8,
        },
        callback: function (value) {
          return Number(value).toFixed(1);
        },
      },
      grid: {
        color: "rgba(0, 0, 0, 0.08)",
      },
    },
  },
}));
</script>

<template>
  <div class="output-chart-container">
    <Line :data="chartData" :options="chartOptions" />

    <!-- Aggregation values display - 9 GRADES -->
    <div class="mt-2 grid grid-cols-3 sm:grid-cols-9 gap-1.5">
      <div class="bg-red-50 border border-red-300 rounded-lg p-1.5 text-center">
        <p class="text-[9px] text-gray-600">α C-</p>
        <p class="text-sm font-bold text-red-700">
          {{ aggregation.C_minus.toFixed(3) }}
        </p>
      </div>
      <div
        class="bg-red-100 border border-red-400 rounded-lg p-1.5 text-center"
      >
        <p class="text-[9px] text-gray-600">α C</p>
        <p class="text-sm font-bold text-red-800">
          {{ aggregation.C.toFixed(3) }}
        </p>
      </div>
      <div
        class="bg-orange-50 border border-orange-300 rounded-lg p-1.5 text-center"
      >
        <p class="text-[9px] text-gray-600">α C+</p>
        <p class="text-sm font-bold text-orange-700">
          {{ aggregation.C_plus.toFixed(3) }}
        </p>
      </div>
      <div
        class="bg-yellow-50 border border-yellow-300 rounded-lg p-1.5 text-center"
      >
        <p class="text-[9px] text-gray-600">α B-</p>
        <p class="text-sm font-bold text-yellow-700">
          {{ aggregation.B_minus.toFixed(3) }}
        </p>
      </div>
      <div
        class="bg-yellow-100 border border-yellow-400 rounded-lg p-1.5 text-center"
      >
        <p class="text-[9px] text-gray-600">α B</p>
        <p class="text-sm font-bold text-yellow-800">
          {{ aggregation.B.toFixed(3) }}
        </p>
      </div>
      <div
        class="bg-blue-50 border border-blue-300 rounded-lg p-1.5 text-center"
      >
        <p class="text-[9px] text-gray-600">α B+</p>
        <p class="text-sm font-bold text-blue-700">
          {{ aggregation.B_plus.toFixed(3) }}
        </p>
      </div>
      <div
        class="bg-cyan-50 border border-cyan-300 rounded-lg p-1.5 text-center"
      >
        <p class="text-[9px] text-gray-600">α A-</p>
        <p class="text-sm font-bold text-cyan-700">
          {{ aggregation.A_minus.toFixed(3) }}
        </p>
      </div>
      <div
        class="bg-green-50 border border-green-300 rounded-lg p-1.5 text-center"
      >
        <p class="text-[9px] text-gray-600">α A</p>
        <p class="text-sm font-bold text-green-700">
          {{ aggregation.A.toFixed(3) }}
        </p>
      </div>
      <div
        class="bg-green-100 border border-green-400 rounded-lg p-1.5 text-center"
      >
        <p class="text-[9px] text-gray-600">α A+</p>
        <p class="text-sm font-bold text-green-800">
          {{ aggregation.A_plus.toFixed(3) }}
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.output-chart-container {
  position: relative;
  height: 560px;
  width: 100%;
  background: white;
  border-radius: 0.75rem;
  padding: 0.875rem;
  padding-top: 0.5rem;
  padding-bottom: 0.375rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

@media (max-width: 640px) {
  .output-chart-container {
    height: 500px;
    padding: 0.75rem;
    padding-top: 0.5rem;
    padding-bottom: 0.375rem;
  }
}
</style>
