<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const features = [
  {
    icon: '🎯',
    title: 'Akurat',
    description: 'Menggunakan metode Fuzzy Mamdani dengan tingkat akurasi tinggi'
  },
  {
    icon: '⚡',
    title: 'Cepat',
    description: 'Hasil analisis didapatkan dalam hitungan detik'
  },
  {
    icon: '📊',
    title: 'Detail',
    description: 'Menampilkan setiap tahapan proses fuzzy secara transparan'
  },
  {
    icon: '🔬',
    title: 'Ilmiah',
    description: 'Berdasarkan penelitian dan metodologi yang terbukti'
  }
]
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-amber-50 via-green-50 to-yellow-50">
    <!-- Header/Navbar -->
    <nav class="backdrop-blur-md bg-white/30 border-b border-white/20 sticky top-0 z-50">
      <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex justify-between items-center">
          <div class="flex items-center space-x-3">
            <div class="text-3xl">🌿</div>
            <h1 class="text-xl sm:text-2xl font-bold text-amber-900">SiMadu</h1>
          </div>
          <div class="flex gap-2 sm:gap-4">
            <button @click="router.push('/')" 
              class="px-3 sm:px-4 py-2 text-sm sm:text-base text-amber-900 hover:text-amber-700 font-medium transition">
              Beranda
            </button>
            <button @click="router.push('/analyze')" 
              class="px-3 sm:px-4 py-2 text-sm sm:text-base text-amber-900 hover:text-amber-700 font-medium transition">
              Analisis
            </button>
            <button @click="router.push('/about')" 
              class="px-3 sm:px-4 py-2 text-sm sm:text-base text-amber-900 hover:text-amber-700 font-medium transition">
              Tentang
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="container mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-20">
      <div class="text-center max-w-4xl mx-auto">
        <div class="inline-block mb-6 px-4 sm:px-6 py-2 sm:py-3 rounded-full backdrop-blur-md bg-white/40 border border-white/30">
          <p class="text-sm sm:text-base text-amber-800 font-medium">Sistem Klasifikasi Mutu Tembakau</p>
        </div>
        
        <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold text-amber-950 mb-4 sm:mb-6 leading-tight">
          Klasifikasi Mutu<br/>
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-green-600 via-yellow-600 to-amber-700">
            Tembakau Otomatis
          </span>
        </h1>
        
        <p class="text-base sm:text-lg lg:text-xl text-gray-700 mb-6 sm:mb-8 max-w-2xl mx-auto px-4">
          Menggunakan teknologi Fuzzy Logic Mamdani untuk mengklasifikasikan mutu tembakau berdasarkan 
          warna (Hue) dan kecerahan (Value) dengan akurasi tinggi
        </p>
        
        <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <button @click="router.push('/analyze')"
            class="w-full sm:w-auto px-6 sm:px-8 py-3 sm:py-4 bg-gradient-to-r from-green-600 to-green-700 text-white rounded-xl font-semibold text-base sm:text-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300">
            🚀 Mulai Analisis
          </button>
          <button @click="router.push('/about')"
            class="w-full sm:w-auto px-6 sm:px-8 py-3 sm:py-4 backdrop-blur-md bg-white/50 border border-white/30 text-amber-900 rounded-xl font-semibold text-base sm:text-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300">
            📖 Pelajari Lebih Lanjut
          </button>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="container mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16">
      <h2 class="text-2xl sm:text-3xl font-bold text-center text-amber-900 mb-8 sm:mb-12">Keunggulan Sistem</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        <div v-for="feature in features" :key="feature.title"
          class="backdrop-blur-md bg-white/40 border border-white/30 rounded-2xl p-6 sm:p-8 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105">
          <div class="text-4xl sm:text-5xl mb-4">{{ feature.icon }}</div>
          <h3 class="text-lg sm:text-xl font-bold text-amber-900 mb-2">{{ feature.title }}</h3>
          <p class="text-sm sm:text-base text-gray-700">{{ feature.description }}</p>
        </div>
      </div>
    </section>

    <!-- How It Works -->
    <section class="container mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16">
      <h2 class="text-2xl sm:text-3xl font-bold text-center text-amber-900 mb-8 sm:mb-12">Cara Kerja Sistem</h2>
      <div class="max-w-4xl mx-auto">
        <div class="backdrop-blur-md bg-white/40 border border-white/30 rounded-2xl p-6 sm:p-10 shadow-xl">
          <div class="space-y-6 sm:space-y-8">
            <!-- Step 1 -->
            <div class="flex items-start gap-4">
              <div class="flex-shrink-0 w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-gradient-to-br from-green-500 to-green-600 flex items-center justify-center text-white font-bold text-lg sm:text-xl shadow-lg">
                1
              </div>
              <div>
                <h3 class="text-lg sm:text-xl font-bold text-amber-900 mb-2">Crisp Input</h3>
                <p class="text-sm sm:text-base text-gray-700">Upload foto tembakau. Sistem mengekstrak nilai Hue (warna) dan Value (kecerahan) dari gambar</p>
              </div>
            </div>

            <!-- Arrow -->
            <div class="text-center text-2xl sm:text-3xl text-amber-600">↓</div>

            <!-- Step 2 -->
            <div class="flex items-start gap-4">
              <div class="flex-shrink-0 w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-gradient-to-br from-yellow-500 to-yellow-600 flex items-center justify-center text-white font-bold text-lg sm:text-xl shadow-lg">
                2
              </div>
              <div>
                <h3 class="text-lg sm:text-xl font-bold text-amber-900 mb-2">Fuzzification</h3>
                <p class="text-sm sm:text-base text-gray-700">Nilai crisp dikonversi menjadi fuzzy set (Emas, Kuning, Hijau untuk Hue | Gelap, Sedang, Cerah untuk Value)</p>
              </div>
            </div>

            <!-- Arrow -->
            <div class="text-center text-2xl sm:text-3xl text-amber-600">↓</div>

            <!-- Step 3 -->
            <div class="flex items-start gap-4">
              <div class="flex-shrink-0 w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-gradient-to-br from-amber-500 to-amber-600 flex items-center justify-center text-white font-bold text-lg sm:text-xl shadow-lg">
                3
              </div>
              <div>
                <h3 class="text-lg sm:text-xl font-bold text-amber-900 mb-2">Inference</h3>
                <p class="text-sm sm:text-base text-gray-700">Aturan fuzzy IF-THEN diterapkan dengan operator MIN, lalu diagregasi dengan MAX</p>
              </div>
            </div>

            <!-- Arrow -->
            <div class="text-center text-2xl sm:text-3xl text-amber-600">↓</div>

            <!-- Step 4 -->
            <div class="flex items-start gap-4">
              <div class="flex-shrink-0 w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-gradient-to-br from-green-600 to-green-700 flex items-center justify-center text-white font-bold text-lg sm:text-xl shadow-lg">
                4
              </div>
              <div>
                <h3 class="text-lg sm:text-xl font-bold text-amber-900 mb-2">Defuzzification</h3>
                <p class="text-sm sm:text-base text-gray-700">Metode Centroid Diskrit menghasilkan nilai crisp output (Grade A/B/C) dengan skor 0-100</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="container mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16">
      <div class="max-w-4xl mx-auto backdrop-blur-md bg-gradient-to-r from-green-500/20 to-yellow-500/20 border border-white/30 rounded-2xl p-8 sm:p-12 text-center shadow-xl">
        <h2 class="text-2xl sm:text-3xl lg:text-4xl font-bold text-amber-950 mb-4">Siap Menganalisis Tembakau Anda?</h2>
        <p class="text-base sm:text-lg text-gray-700 mb-6 sm:mb-8">
          Upload foto tembakau Anda sekarang dan dapatkan hasil klasifikasi mutu dalam hitungan detik
        </p>
        <button @click="router.push('/analyze')"
          class="px-8 sm:px-10 py-3 sm:py-4 bg-gradient-to-r from-green-600 to-green-700 text-white rounded-xl font-bold text-base sm:text-lg shadow-lg hover:shadow-2xl transform hover:scale-105 transition-all duration-300">
          Mulai Sekarang →
        </button>
      </div>
    </section>

    <!-- Footer -->
    <footer class="backdrop-blur-md bg-white/30 border-t border-white/20 py-6 sm:py-8 mt-12 sm:mt-20">
      <div class="container mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <p class="text-sm sm:text-base text-gray-700">
          © 2026 SiMadu - Sistem Klasifikasi Mutu Tembakau | Kelompok 3
        </p>
        <p class="text-xs sm:text-sm text-gray-600 mt-2">
          Fuzzy Logic Mamdani | UAS Artificial Intelligence
        </p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
/* Additional animations */
@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

.animate-float {
  animation: float 3s ease-in-out infinite;
}
</style>
