<script setup lang="ts">
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
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
  type ChartData
} from 'chart.js'
import annotationPlugin from 'chartjs-plugin-annotation'

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
)

interface Props {
  graphData: Array<{ x: number; y: number }>
  aggregation: {
    A_plus: number
    A: number
    A_minus: number
    B_plus: number
    B: number
    B_minus: number
    C_plus: number
    C: number
    C_minus: number
  }
  score: number
}

const props = defineProps<Props>()

// Generate membership function curves (full curves, not clipped)
const generateMembershipCurves = () => {
  const xValues = Array.from({ length: 101 }, (_, i) => i)
  
  // Grade C: Trapesium Kiri [0, 0, 20, 50]
  const gradeC = xValues.map(x => {
    if (x <= 20) return 1.0
    if (x > 20 && x < 50) return (50 - x) / 30
    return 0.0
  })
  
  // Grade B: Segitiga [30, 50, 70]
  const gradeB = xValues.map(x => {
    if (x <= 30 || x >= 70) return 0.0
    if (x > 30 && x <= 50) return (x - 30) / 20
    return (70 - x) / 20
  })
  
  // Grade A: Trapesium Kanan [50, 80, 100, 100]
  const gradeA = xValues.map(x => {
    if (x < 50) return 0.0
    if (x >= 50 && x < 80) return (x - 50) / 30
    return 1.0
  })
  
  return { xValues, gradeC, gradeB, gradeA }
}

const { xValues, gradeC, gradeB, gradeA } = generateMembershipCurves()

// Find intersection points
const findIntersections = () => {
  const intersections: Array<{ x: number; y: number; label: string }> = []
  
  // C-B intersection
  for (let x = 30; x <= 50; x++) {
    const cVal = gradeC[x] ?? 0
    const bVal = gradeB[x] ?? 0
    if (Math.abs(cVal - bVal) < 0.05 && cVal > 0 && bVal > 0) {
      intersections.push({ x, y: cVal, label: 'C∩B' })
      break
    }
  }
  
  // B-A intersection
  for (let x = 50; x <= 70; x++) {
    const bVal = gradeB[x] ?? 0
    const aVal = gradeA[x] ?? 0
    if (Math.abs(bVal - aVal) < 0.05 && bVal > 0 && aVal > 0) {
      intersections.push({ x, y: bVal, label: 'B∩A' })
      break
    }
  }
  
  return intersections
}

const intersections = findIntersections()

const chartData = computed<ChartData<'line'>>(() => ({
  labels: xValues,
  datasets: [
    // Full membership curves (faded/dashed)
    {
      label: '📉 Grade C (Sangat Rendah - Rendah)',
      data: gradeC,
      borderColor: 'rgba(239, 68, 68, 0.4)',
      backgroundColor: 'rgba(239, 68, 68, 0.08)',
      borderWidth: 2,
      borderDash: [6, 3],
      fill: false,
      pointRadius: 0,
      tension: 0
    },
    {
      label: '📊 Grade B (Standar)',
      data: gradeB,
      borderColor: 'rgba(234, 179, 8, 0.4)',
      backgroundColor: 'rgba(234, 179, 8, 0.08)',
      borderWidth: 2,
      borderDash: [6, 3],
      fill: false,
      pointRadius: 0,
      tension: 0
    },
    {
      label: '📈 Grade A (Tinggi - Sangat Tinggi)',
      data: gradeA,
      borderColor: 'rgba(34, 197, 94, 0.4)',
      backgroundColor: 'rgba(34, 197, 94, 0.08)',
      borderWidth: 2,
      borderDash: [6, 3],
      fill: false,
      pointRadius: 0,
      tension: 0
    },
    // Aggregated curve (clipped) - MAIN RESULT
    {
      label: '⭐ Hasil Agregasi (Clipped & Union)',
      data: props.graphData.map(d => d.y),
      borderColor: 'rgb(59, 130, 246)',
      backgroundColor: 'rgba(59, 130, 246, 0.3)',
      borderWidth: 3.5,
      fill: true,
      pointRadius: 0,
      tension: 0.1
    },
    // Intersection points
    {
      label: '▲ Titik Potong (Intersections)',
      data: xValues.map(x => {
        const intersection = intersections.find(i => i.x === x)
        return intersection ? intersection.y : null
      }) as (number | null)[],
      borderColor: 'rgb(147, 51, 234)',
      backgroundColor: 'rgb(147, 51, 234)',
      pointRadius: 8,
      pointStyle: 'triangle',
      showLine: false,
      pointBorderWidth: 2,
      pointBorderColor: 'white'
    },
    // Centroid point
    {
      label: `✖️ Centroid (Score: ${props.score.toFixed(2)})`,
      data: xValues.map(x => {
        const roundedScore = Math.round(props.score)
        if (x === roundedScore) {
          return props.graphData[roundedScore]?.y || 0
        }
        return null
      }) as (number | null)[],
      borderColor: 'rgb(220, 38, 38)',
      backgroundColor: 'rgb(220, 38, 38)',
      pointRadius: 12,
      pointStyle: 'crossRot',
      showLine: false,
      pointBorderWidth: 4,
      pointBorderColor: 'white'
    }
  ]
}))

const chartOptions = computed<ChartOptions<'line'>>(() => ({
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: 'index',
    intersect: false
  },
  plugins: {
    legend: {
      display: true,
      position: 'top',
      labels: {
        usePointStyle: true,
        padding: 15,
        font: {
          size: 11,
          weight: 500,
          family: "'Inter', -apple-system, sans-serif"
        },
        boxWidth: 12,
        boxHeight: 12
      }
    },
    title: {
      display: true,
      text: 'Grafik Defuzzification - Metode Mamdani (Discretized Centroid)',
      font: {
        size: 17,
        weight: 'bold',
        family: "'Inter', -apple-system, sans-serif"
      },
      padding: {
        top: 5,
        bottom: 20
      }
    },
    tooltip: {
      backgroundColor: 'rgba(17, 24, 39, 0.95)',
      padding: 14,
      titleFont: {
        size: 13,
        weight: 'bold'
      },
      bodyFont: {
        size: 12
      },
      borderColor: 'rgba(255, 255, 255, 0.1)',
      borderWidth: 1,
      callbacks: {
        label: function(context) {
          const label = context.dataset.label || ''
          const value = context.parsed.y
          if (value === null) return ''
          return `${label}: μ = ${value.toFixed(4)}`
        },
        footer: function(tooltipItems) {
          const x = tooltipItems[0]?.parsed?.x
          if (x === null || x === undefined) return ''
          let zone = ''
          if (x < 30) zone = '🔴 Sangat Rendah (0-30)'
          else if (x < 50) zone = '🟠 Rendah (30-50)'
          else if (x < 70) zone = '🟡 Standar (50-70)'
          else if (x < 85) zone = '🟢 Tinggi (70-85)'
          else zone = '🟢 Sangat Tinggi (85-100)'
          return `Grade: ${zone}`
        }
      }
    },
    annotation: {
      annotations: {
        // Vertical line at centroid
        centroidLine: {
          type: 'line',
          xMin: props.score,
          xMax: props.score,
          borderColor: 'rgb(220, 38, 38)',
          borderWidth: 2.5,
          borderDash: [8, 4],
          label: {
            content: `Centroid: ${props.score.toFixed(2)}`,
            display: true,
            position: 'start',
            backgroundColor: 'rgb(220, 38, 38)',
            color: 'white',
            font: {
              weight: 'bold',
              size: 11
            },
            padding: 6
          }
        },
        // Zone labels (top of chart)
        zoneSangatRendah: {
          type: 'label',
          xValue: 15,
          yValue: 1.08,
          content: ['Sangat Rendah', '(0-30)'],
          font: {
            size: 10,
            weight: 'bold'
          },
          color: 'rgb(239, 68, 68)',
          backgroundColor: 'rgba(254, 226, 226, 0.8)',
          borderRadius: 4,
          padding: 4
        },
        zoneRendah: {
          type: 'label',
          xValue: 40,
          yValue: 1.08,
          content: ['Rendah', '(30-50)'],
          font: {
            size: 10,
            weight: 'bold'
          },
          color: 'rgb(249, 115, 22)',
          backgroundColor: 'rgba(255, 237, 213, 0.8)',
          borderRadius: 4,
          padding: 4
        },
        zoneStandar: {
          type: 'label',
          xValue: 60,
          yValue: 1.08,
          content: ['Standar', '(50-70)'],
          font: {
            size: 10,
            weight: 'bold'
          },
          color: 'rgb(234, 179, 8)',
          backgroundColor: 'rgba(254, 249, 195, 0.8)',
          borderRadius: 4,
          padding: 4
        },
        zoneTinggi: {
          type: 'label',
          xValue: 77.5,
          yValue: 1.08,
          content: ['Tinggi', '(70-85)'],
          font: {
            size: 10,
            weight: 'bold'
          },
          color: 'rgb(34, 197, 94)',
          backgroundColor: 'rgba(220, 252, 231, 0.8)',
          borderRadius: 4,
          padding: 4
        },
        zoneSangatTinggi: {
          type: 'label',
          xValue: 92.5,
          yValue: 1.08,
          content: ['Sangat Tinggi', '(85-100)'],
          font: {
            size: 10,
            weight: 'bold'
          },
          color: 'rgb(22, 163, 74)',
          backgroundColor: 'rgba(187, 247, 208, 0.8)',
          borderRadius: 4,
          padding: 4
        },
        // Alpha cut lines (horizontal)
        alphaA: {
          type: 'line',
          yMin: props.aggregation.A,
          yMax: props.aggregation.A,
          borderColor: 'rgba(34, 197, 94, 0.6)',
          borderWidth: 2,
          borderDash: [4, 4],
          label: {
            content: `α-cut A: ${props.aggregation.A.toFixed(4)}`,
            display: props.aggregation.A > 0,
            position: 'end',
            backgroundColor: 'rgba(34, 197, 94, 0.9)',
            color: 'white',
            font: {
              size: 10,
              weight: 'bold'
            },
            padding: 4
          }
        },
        alphaB: {
          type: 'line',
          yMin: props.aggregation.B,
          yMax: props.aggregation.B,
          borderColor: 'rgba(234, 179, 8, 0.6)',
          borderWidth: 2,
          borderDash: [4, 4],
          label: {
            content: `α-cut B: ${props.aggregation.B.toFixed(4)}`,
            display: props.aggregation.B > 0,
            position: 'end',
            backgroundColor: 'rgba(234, 179, 8, 0.9)',
            color: 'white',
            font: {
              size: 10,
              weight: 'bold'
            },
            padding: 4
          }
        },
        alphaC: {
          type: 'line',
          yMin: props.aggregation.C,
          yMax: props.aggregation.C,
          borderColor: 'rgba(249, 115, 22, 0.6)',
          borderWidth: 2,
          borderDash: [4, 4],
          label: {
            content: `α-cut C: ${props.aggregation.C.toFixed(4)}`,
            display: props.aggregation.C > 0,
            position: 'end',
            backgroundColor: 'rgba(249, 115, 22, 0.9)',
            color: 'white',
            font: {
              size: 10,
              weight: 'bold'
            },
            padding: 4
          }
        }
      }
    }
  },
  scales: {
    x: {
      title: {
        display: true,
        text: 'Nilai Mutu (Grade Score)',
        font: {
          size: 14,
          weight: 'bold',
          family: "'Inter', -apple-system, sans-serif"
        },
        padding: { top: 10 }
      },
      ticks: {
        maxTicksLimit: 21,
        font: {
          size: 10
        },
        callback: function(value) {
          const x = Number(value)
          // Highlight zona boundaries
          if ([0, 30, 50, 70, 85, 100].includes(x)) {
            return '⭐ ' + x
          }
          return x
        }
      },
      grid: {
        color: function(context) {
          const value = context.tick?.value
          // Darker grid lines at zone boundaries
          if ([30, 50, 70, 85].includes(Number(value))) {
            return 'rgba(0, 0, 0, 0.2)'
          }
          return 'rgba(0, 0, 0, 0.05)'
        },
        lineWidth: function(context) {
          const value = context.tick?.value
          if ([30, 50, 70, 85].includes(Number(value))) {
            return 2
          }
          return 1
        }
      }
    },
    y: {
      title: {
        display: true,
        text: 'Derajat Keanggotaan (μ)',
        font: {
          size: 14,
          weight: 'bold',
          family: "'Inter', -apple-system, sans-serif"
        }
      },
      min: 0,
      max: 1.12,
      ticks: {
        stepSize: 0.1,
        font: {
          size: 10
        },
        callback: function(value) {
          return Number(value).toFixed(1)
        }
      },
      grid: {
        color: 'rgba(0, 0, 0, 0.08)',
        lineWidth: 1
      }
    }
  }
}))
</script>

<template>
  <div class="space-y-4">
    <!-- Chart Container -->
    <div class="chart-container">
      <Line :data="chartData" :options="chartOptions" />
    </div>

    <!-- Legend Info -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
      <div class="bg-blue-50 border border-blue-200 rounded-lg p-3">
        <p class="font-bold text-blue-900 mb-1">⭐ Kurva Hasil Agregasi</p>
        <p class="text-blue-700">Area biru = hasil MIN (clipping) dan MAX (union) dari semua fuzzy rules</p>
      </div>
      <div class="bg-purple-50 border border-purple-200 rounded-lg p-3">
        <p class="font-bold text-purple-900 mb-1">▲ Titik Potong</p>
        <p class="text-purple-700">Intersection points antar membership functions (C∩B, B∩A)</p>
      </div>
      <div class="bg-red-50 border border-red-200 rounded-lg p-3">
        <p class="font-bold text-red-900 mb-1">✖️ Centroid</p>
        <p class="text-red-700">Titik pusat massa: (Σ(x·μ) / Σμ) = <span class="font-bold">{{ score.toFixed(2) }}</span></p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chart-container {
  position: relative;
  height: 550px;
  width: 100%;
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

@media (max-width: 640px) {
  .chart-container {
    height: 450px;
    padding: 1rem;
  }
}
</style>



