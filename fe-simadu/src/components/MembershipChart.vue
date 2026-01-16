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
  type: 'hue' | 'value'
  crispValue: number
  membershipValues: {
    emas?: number
    kuning?: number
    hijau?: number
    gelap?: number
    sedang?: number
    cerah?: number
  }
}

const props = defineProps<Props>()

// Generate membership functions for HUE
const generateHueMembership = () => {
  const xValues = Array.from({ length: 181 }, (_, i) => i) // 0-180
  
  // Emas: Trapesium Kiri [0, 0, 25, 45]
  const emas = xValues.map(x => {
    if (x <= 25) return 1.0
    if (x > 25 && x < 45) return (45 - x) / (45 - 25)
    return 0.0
  })
  
  // Kuning: Segitiga [25, 45, 60]
  const kuning = xValues.map(x => {
    if (x <= 25 || x >= 60) return 0.0
    if (x > 25 && x <= 45) return (x - 25) / (45 - 25)
    return (60 - x) / (60 - 45)
  })
  
  // Hijau: Trapesium Kanan [50, 65, 80, 80]
  const hijau = xValues.map(x => {
    if (x < 50) return 0.0
    if (x >= 50 && x < 65) return (x - 50) / (65 - 50)
    return 1.0
  })
  
  return { xValues, emas, kuning, hijau }
}

// Generate membership functions for VALUE
const generateValueMembership = () => {
  const xValues = Array.from({ length: 256 }, (_, i) => i) // 0-255
  
  // Gelap: Trapesium Kiri [0, 0, 80, 120]
  const gelap = xValues.map(x => {
    if (x <= 80) return 1.0
    if (x > 80 && x < 120) return (120 - x) / (120 - 80)
    return 0.0
  })
  
  // Sedang: Segitiga [100, 140, 180]
  const sedang = xValues.map(x => {
    if (x <= 100 || x >= 180) return 0.0
    if (x > 100 && x <= 140) return (x - 100) / (140 - 100)
    return (180 - x) / (180 - 140)
  })
  
  // Cerah: Trapesium Kanan [130, 170, 255, 255]
  const cerah = xValues.map(x => {
    if (x < 130) return 0.0
    if (x >= 130 && x < 170) return (x - 130) / (170 - 130)
    return 1.0
  })
  
  return { xValues, gelap, sedang, cerah }
}

const chartData = computed<ChartData<'line'>>(() => {
  if (props.type === 'hue') {
    const { xValues, emas, kuning, hijau } = generateHueMembership()
    return {
      labels: xValues,
      datasets: [
        {
          label: '🟡 Emas (Premium)',
          data: emas,
          borderColor: 'rgb(234, 179, 8)',
          backgroundColor: 'rgba(234, 179, 8, 0.2)',
          borderWidth: 2.5,
          fill: true,
          pointRadius: 0,
          tension: 0
        },
        {
          label: '🟠 Kuning (Sedang)',
          data: kuning,
          borderColor: 'rgb(249, 115, 22)',
          backgroundColor: 'rgba(249, 115, 22, 0.2)',
          borderWidth: 2.5,
          fill: true,
          pointRadius: 0,
          tension: 0
        },
        {
          label: '🟢 Hijau (Rendah)',
          data: hijau,
          borderColor: 'rgb(34, 197, 94)',
          backgroundColor: 'rgba(34, 197, 94, 0.2)',
          borderWidth: 2.5,
          fill: true,
          pointRadius: 0,
          tension: 0
        }
      ]
    }
  } else {
    const { xValues, gelap, sedang, cerah } = generateValueMembership()
    return {
      labels: xValues,
      datasets: [
        {
          label: '⚫ Gelap (Buruk)',
          data: gelap,
          borderColor: 'rgb(75, 85, 99)',
          backgroundColor: 'rgba(75, 85, 99, 0.2)',
          borderWidth: 2.5,
          fill: true,
          pointRadius: 0,
          tension: 0
        },
        {
          label: '🔵 Sedang',
          data: sedang,
          borderColor: 'rgb(59, 130, 246)',
          backgroundColor: 'rgba(59, 130, 246, 0.2)',
          borderWidth: 2.5,
          fill: true,
          pointRadius: 0,
          tension: 0
        },
        {
          label: '☀️ Cerah (Bagus)',
          data: cerah,
          borderColor: 'rgb(251, 191, 36)',
          backgroundColor: 'rgba(251, 191, 36, 0.2)',
          borderWidth: 2.5,
          fill: true,
          pointRadius: 0,
          tension: 0
        }
      ]
    }
  }
})

const chartOptions = computed<ChartOptions<'line'>>(() => {
  const isHue = props.type === 'hue'
  const maxX = isHue ? 180 : 255
  
  return {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: 'index',
      intersect: false
    },
    layout: {
      padding: {
        top: 5,
        bottom: 5,
        left: 5,
        right: 5
      }
    },
    plugins: {
      legend: {
        display: true,
        position: 'top',
        align: 'center',
        labels: {
          usePointStyle: true,
          padding: 6,
          font: {
            size: 9,
            weight: 500
          },
          boxWidth: 8,
          boxHeight: 8
        }
      },
      title: {
        display: true,
        text: isHue 
          ? `Fungsi Keanggotaan HUE (Warna)` 
          : `Fungsi Keanggotaan VALUE (Kecerahan)`,
        font: {
          size: 12,
          weight: 'bold'
        },
        padding: {
          top: 0,
          bottom: 8
        }
      },
      tooltip: {
        backgroundColor: 'rgba(17, 24, 39, 0.95)',
        padding: 10,
        titleFont: {
          size: 11,
          weight: 'bold'
        },
        bodyFont: {
          size: 10
        },
        callbacks: {
          label: function(context) {
            const label = context.dataset.label || ''
            const value = context.parsed.y
            return `${label}: μ = ${value !== null ? value.toFixed(3) : '0.000'}`
          }
        }
      },
      annotation: {
        annotations: {
          // Vertical line at crisp input value
          inputLine: {
            type: 'line',
            xMin: props.crispValue,
            xMax: props.crispValue,
            borderColor: 'rgb(220, 38, 38)',
            borderWidth: 2.5,
            borderDash: [5, 3],
            label: {
              content: `Input: ${props.crispValue}`,
              display: true,
              position: 'end',
              yAdjust: 25,
              backgroundColor: 'rgb(220, 38, 38)',
              color: 'white',
              font: {
                weight: 'bold',
                size: 8
              },
              padding: 3
            }
          }
        }
      }
    },
    scales: {
      x: {
        title: {
          display: true,
          text: isHue ? 'Nilai Hue (0-180)' : 'Nilai Value (0-255)',
          font: {
            size: 11,
            weight: 'bold'
          },
          padding: { top: 8 }
        },
        ticks: {
          maxTicksLimit: 12,
          font: {
            size: 8
          }
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)'
        }
      },
      y: {
        title: {
          display: true,
          text: 'Derajat Keanggotaan (μ)',
          font: {
            size: 11,
            weight: 'bold'
          },
          padding: { bottom: 8 }
        },
        min: 0,
        max: 1.05,
        ticks: {
          stepSize: 0.2,
          font: {
            size: 8
          },
          callback: function(value) {
            return Number(value).toFixed(1)
          }
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.08)'
        }
      }
    }
  }
})
</script>

<template>
  <div class="membership-chart-container">
    <Line :data="chartData" :options="chartOptions" />
    
    <!-- Input value indicator -->
    <div class="text-center mb-2 mt-1">
      <span class="text-xs font-semibold text-red-600 bg-red-50 px-3 py-1 rounded-full border border-red-200">
        📍 Nilai Input: {{ crispValue }}
      </span>
    </div>
    
    <!-- Membership values display -->
    <div class="mt-2 grid gap-2" :class="type === 'hue' ? 'grid-cols-3' : 'grid-cols-3'">
      <template v-if="type === 'hue'">
        <div class="bg-yellow-50 border border-yellow-300 rounded-lg p-2 text-center">
          <p class="text-xs text-gray-600">μ Emas</p>
          <p class="text-lg font-bold text-yellow-700">{{ membershipValues.emas?.toFixed(4) }}</p>
        </div>
        <div class="bg-orange-50 border border-orange-300 rounded-lg p-2 text-center">
          <p class="text-xs text-gray-600">μ Kuning</p>
          <p class="text-lg font-bold text-orange-700">{{ membershipValues.kuning?.toFixed(4) }}</p>
        </div>
        <div class="bg-green-50 border border-green-300 rounded-lg p-2 text-center">
          <p class="text-xs text-gray-600">μ Hijau</p>
          <p class="text-lg font-bold text-green-700">{{ membershipValues.hijau?.toFixed(4) }}</p>
        </div>
      </template>
      <template v-else>
        <div class="bg-gray-50 border border-gray-300 rounded-lg p-2 text-center">
          <p class="text-xs text-gray-600">μ Gelap</p>
          <p class="text-lg font-bold text-gray-700">{{ membershipValues.gelap?.toFixed(4) }}</p>
        </div>
        <div class="bg-blue-50 border border-blue-300 rounded-lg p-2 text-center">
          <p class="text-xs text-gray-600">μ Sedang</p>
          <p class="text-lg font-bold text-blue-700">{{ membershipValues.sedang?.toFixed(4) }}</p>
        </div>
        <div class="bg-amber-50 border border-amber-300 rounded-lg p-2 text-center">
          <p class="text-xs text-gray-600">μ Cerah</p>
          <p class="text-lg font-bold text-amber-700">{{ membershipValues.cerah?.toFixed(4) }}</p>
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.membership-chart-container {
  position: relative;
  height: 480px;
  width: 100%;
  background: white;
  border-radius: 0.75rem;
  padding: 0.875rem;
  padding-top: 0.5rem;
  padding-bottom: 0.375rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

@media (max-width: 640px) {
  .membership-chart-container {
    height: 420px;
    padding: 0.75rem;
    padding-top: 0.5rem;
    padding-bottom: 0.375rem;
  }
}
</style>
