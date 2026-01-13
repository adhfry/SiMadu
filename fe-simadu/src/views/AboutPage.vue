<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const members = [
  {
    name: 'Ahda Firly Barori',
    nim: '2302310186',
    role: 'Ketua Kelompok'
  },
  {
    name: 'RA. Shofia Tasmin Maulida',
    nim: '2302310162',
    role: 'Anggota'
  },
  {
    name: 'Uswatun Kamilia',
    nim: '2302310150',
    role: 'Anggota'
  },
  {
    name: 'Rofiatul Hasanah',
    nim: '2302310116',
    role: 'Anggota'
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
              class="px-3 sm:px-4 py-2 text-sm sm:text-base text-amber-900 hover:text-amber-700 font-medium transition border-b-2 border-amber-900">
              Tentang
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      <!-- Header -->
      <div class="text-center mb-8 sm:mb-12">
        <div class="inline-block mb-6 px-4 sm:px-6 py-2 sm:py-3 rounded-full backdrop-blur-md bg-white/40 border border-white/30">
          <p class="text-sm sm:text-base text-amber-800 font-medium">Tentang Kami</p>
        </div>
        <h1 class="text-3xl sm:text-4xl lg:text-5xl font-bold text-amber-950 mb-4">
          Kelompok Informatika D - 2023
        </h1>
        <p class="text-base sm:text-lg text-gray-700 max-w-3xl mx-auto mb-3">
          UAS Artificial Intelligence - Sistem Klasifikasi Mutu Tembakau
        </p>
        <div class="max-w-2xl mx-auto bg-white/60 rounded-xl p-4 border border-amber-200">
          <p class="text-sm text-gray-700">
            <span class="font-bold text-amber-900">Fakultas Sains dan Teknologi</span><br>
            Universitas Bahaudin Mudhary Madura
          </p>
          <p class="text-xs text-gray-600 mt-2">
            <span class="font-semibold">Dosen Pengampu:</span> Pyepit Rinekso Andriyanto, S.Kom, M.Kom.
          </p>
        </div>
      </div>

      <!-- Project Info -->
      <div class="max-w-4xl mx-auto mb-8 sm:mb-12">
        <div class="backdrop-blur-md bg-white/40 border border-white/30 rounded-2xl p-6 sm:p-10 shadow-xl">
          <h2 class="text-2xl sm:text-3xl font-bold text-amber-900 mb-6 text-center">
            Tentang Proyek
          </h2>
          <div class="space-y-4 text-gray-700">
            <p class="text-base sm:text-lg leading-relaxed">
              <span class="font-bold text-amber-900">SiMadu</span> (Sistem Klasifikasi Mutu Tembakau) 
              adalah aplikasi berbasis web yang menggunakan metode <span class="font-semibold">Fuzzy Logic Mamdani</span> 
              untuk mengklasifikasikan mutu tembakau secara otomatis.
            </p>
            <p class="text-base sm:text-lg leading-relaxed">
              Sistem ini menganalisis gambar tembakau berdasarkan dua parameter utama: 
              <span class="font-semibold">Hue (Warna)</span> dan <span class="font-semibold">Value (Kecerahan)</span>, 
              kemudian mengklasifikasikannya ke dalam tiga grade: 
              <span class="font-semibold text-green-600">Grade A (Premium)</span>, 
              <span class="font-semibold text-yellow-600">Grade B (Standar)</span>, dan 
              <span class="font-semibold text-orange-600">Grade C (Rendah)</span>.
            </p>
          </div>

          <!-- Technology Stack -->
          <div class="mt-8 pt-8 border-t border-amber-200">
            <h3 class="text-xl font-bold text-amber-900 mb-4">Teknologi yang Digunakan</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div class="bg-white/60 rounded-lg p-4 border border-green-200">
                <p class="font-bold text-green-700 mb-2">🖥️ Frontend</p>
                <p class="text-sm text-gray-600">Vue.js 3 + TypeScript + TailwindCSS</p>
              </div>
              <div class="bg-white/60 rounded-lg p-4 border border-blue-200">
                <p class="font-bold text-blue-700 mb-2">⚙️ Backend</p>
                <p class="text-sm text-gray-600">Python Flask + OpenCV</p>
              </div>
              <div class="bg-white/60 rounded-lg p-4 border border-purple-200">
                <p class="font-bold text-purple-700 mb-2">🧠 Algoritma</p>
                <p class="text-sm text-gray-600">Fuzzy Logic Mamdani</p>
              </div>
              <div class="bg-white/60 rounded-lg p-4 border border-amber-200">
                <p class="font-bold text-amber-700 mb-2">📊 Metode</p>
                <p class="text-sm text-gray-600">Discretized Centroid Defuzzification</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Team Members -->
      <div class="max-w-6xl mx-auto">
        <h2 class="text-2xl sm:text-3xl font-bold text-amber-900 mb-6 sm:mb-8 text-center">
          Anggota Kelompok
        </h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <div v-for="(member, index) in members" :key="index"
            class="backdrop-blur-md bg-white/40 border border-white/30 rounded-2xl p-6 sm:p-8 shadow-xl text-center hover:shadow-2xl transition-all duration-300 transform hover:scale-105">
            <div class="w-20 h-20 sm:w-24 sm:h-24 mx-auto mb-4 rounded-full bg-gradient-to-br from-green-400 to-amber-500 flex items-center justify-center text-white text-3xl sm:text-4xl font-bold shadow-lg">
              {{ member.name.charAt(0) }}
            </div>
            <h3 class="text-lg sm:text-xl font-bold text-amber-900 mb-2">
              {{ member.name }}
            </h3>
            <p class="text-sm sm:text-base text-gray-700 font-mono mb-2">
              {{ member.nim }}
            </p>
            <div class="inline-block px-3 py-1 bg-green-100 border border-green-300 rounded-full text-xs sm:text-sm text-green-700 font-medium">
              {{ member.role }}
            </div>
          </div>
        </div>
      </div>

      <!-- Methodology -->
      <div class="max-w-4xl mx-auto mt-12">
        <div class="backdrop-blur-md bg-white/40 border border-white/30 rounded-2xl p-6 sm:p-10 shadow-xl">
          <h2 class="text-2xl sm:text-3xl font-bold text-amber-900 mb-6 text-center">
            Metodologi Fuzzy Mamdani
          </h2>
          
          <div class="space-y-6">
            <!-- Step 1 -->
            <div class="bg-white/60 rounded-xl p-6 border border-green-200">
              <div class="flex items-start gap-4">
                <div class="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-green-500 to-green-600 flex items-center justify-center text-white font-bold shadow-lg">
                  1
                </div>
                <div>
                  <h3 class="text-lg font-bold text-amber-900 mb-2">Fuzzifikasi</h3>
                  <p class="text-sm text-gray-700">
                    Mengkonversi nilai crisp (Hue & Value) menjadi derajat keanggotaan fuzzy set menggunakan fungsi keanggotaan trapesium dan segitiga.
                  </p>
                </div>
              </div>
            </div>

            <!-- Step 2 -->
            <div class="bg-white/60 rounded-xl p-6 border border-yellow-200">
              <div class="flex items-start gap-4">
                <div class="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-yellow-500 to-yellow-600 flex items-center justify-center text-white font-bold shadow-lg">
                  2
                </div>
                <div>
                  <h3 class="text-lg font-bold text-amber-900 mb-2">Inference</h3>
                  <p class="text-sm text-gray-700">
                    Menerapkan 6 aturan fuzzy IF-THEN dengan operator MIN untuk mendapatkan nilai alpha, kemudian diagregasi dengan operator MAX.
                  </p>
                </div>
              </div>
            </div>

            <!-- Step 3 -->
            <div class="bg-white/60 rounded-xl p-6 border border-amber-200">
              <div class="flex items-start gap-4">
                <div class="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-amber-500 to-amber-600 flex items-center justify-center text-white font-bold shadow-lg">
                  3
                </div>
                <div>
                  <h3 class="text-lg font-bold text-amber-900 mb-2">Defuzzifikasi</h3>
                  <p class="text-sm text-gray-700">
                    Menggunakan metode <span class="font-semibold">Discretized Centroid</span> untuk mengkonversi fuzzy output menjadi nilai crisp (0-100).
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- Formula -->
          <div class="mt-8 bg-gradient-to-r from-green-50 to-yellow-50 rounded-xl p-6 border-2 border-amber-300">
            <p class="text-center font-mono text-sm sm:text-base text-amber-900 font-bold mb-2">
              Rumus Defuzzifikasi Centroid
            </p>
            <p class="text-center font-mono text-lg sm:text-xl text-amber-950">
              Crisp Output = Σ(x<sub>i</sub> × μ<sub>i</sub>) / Σμ<sub>i</sub>
            </p>
          </div>
        </div>
      </div>

      <!-- CTA -->
      <div class="max-w-3xl mx-auto mt-12 text-center">
        <div class="backdrop-blur-md bg-gradient-to-r from-green-500/20 to-yellow-500/20 border border-white/30 rounded-2xl p-8 shadow-xl">
          <h3 class="text-2xl sm:text-3xl font-bold text-amber-950 mb-4">
            Siap Mencoba Sistem Kami?
          </h3>
          <p class="text-base sm:text-lg text-gray-700 mb-6">
            Klik tombol di bawah untuk mulai menganalisis mutu tembakau Anda
          </p>
          <button @click="router.push('/analyze')"
            class="px-8 sm:px-10 py-3 sm:py-4 bg-gradient-to-r from-green-600 to-green-700 text-white rounded-xl font-bold text-base sm:text-lg shadow-lg hover:shadow-2xl transform hover:scale-105 transition-all duration-300">
            Mulai Analisis →
          </button>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="backdrop-blur-md bg-white/30 border-t border-white/20 py-6 sm:py-8 mt-12 sm:mt-20">
      <div class="container mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <p class="text-sm sm:text-base text-gray-700">
          © 2026 SiMadu - Sistem Klasifikasi Mutu Tembakau
        </p>
        <p class="text-xs sm:text-sm text-gray-600 mt-2">
          Kelompok Informatika D - 2023 | Fakultas Sains dan Teknologi UBM Madura
        </p>
        <p class="text-xs text-gray-500 mt-1">
          Fuzzy Logic Mamdani | UAS Artificial Intelligence
        </p>
      </div>
    </footer>
  </div>
</template>
