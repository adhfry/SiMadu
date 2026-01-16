<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { analyzeTabacco, type TobaccoAnalysisResponse } from "@/services/api";
import DefuzzChart from "@/components/DefuzzChart.vue";
import MembershipChart from "@/components/MembershipChart.vue";
import OutputMembershipChart from "@/components/OutputMembershipChart.vue";

const router = useRouter();

const selectedImage = ref<File | null>(null);
const imagePreview = ref<string | null>(null);
const isLoading = ref(false);
const error = ref<string | null>(null);
const result = ref<TobaccoAnalysisResponse | null>(null);

const handleImageSelect = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files[0]) {
    const file = target.files[0];

    console.log("File selected:", file.name, file.type, file.size);

    // Validate file size (not 0 bytes)
    if (file.size === 0) {
      error.value = "File kosong atau corrupt. Silakan pilih file lain.";
      return;
    }

    // Validate file type
    if (!file.type.startsWith("image/")) {
      error.value = "File harus berupa gambar (JPG, PNG, dll)";
      return;
    }

    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      error.value = "Ukuran file maksimal 5MB";
      return;
    }

    selectedImage.value = file;
    error.value = null;
    result.value = null;

    // Create preview
    const reader = new FileReader();
    reader.onload = (e: ProgressEvent<FileReader>) => {
      if (e.target && e.target.result) {
        const result = e.target.result as string;
        imagePreview.value = result;
        console.log("Preview loaded successfully, length:", result.length);
      }
    };
    reader.onerror = (e) => {
      console.error("FileReader error:", e);
      error.value = "Gagal membaca file gambar";
    };
    reader.readAsDataURL(file);
  }
};

const handleDragOver = (event: DragEvent) => {
  event.preventDefault();
};

const handleDrop = (event: DragEvent) => {
  event.preventDefault();
  const files = event.dataTransfer?.files;
  if (files && files[0]) {
    const file = files[0];

    console.log("File dropped:", file.name, file.type, file.size);

    // Validate file size (not 0 bytes)
    if (file.size === 0) {
      error.value = "File kosong atau corrupt. Silakan pilih file lain.";
      return;
    }

    // Validate file type
    if (!file.type.startsWith("image/")) {
      error.value = "File harus berupa gambar (JPG, PNG, dll)";
      return;
    }

    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      error.value = "Ukuran file maksimal 5MB";
      return;
    }

    selectedImage.value = file;
    error.value = null;
    result.value = null;

    const reader = new FileReader();
    reader.onload = (e: ProgressEvent<FileReader>) => {
      if (e.target && e.target.result) {
        const result = e.target.result as string;
        imagePreview.value = result;
        console.log(
          "Preview loaded successfully (drag & drop), length:",
          result.length
        );
      }
    };
    reader.onerror = (e) => {
      console.error("FileReader error:", e);
      error.value = "Gagal membaca file gambar";
    };
    reader.readAsDataURL(file);
  }
};

const analyzeImage = async () => {
  if (!selectedImage.value) {
    error.value = "Silakan pilih gambar terlebih dahulu";
    return;
  }

  isLoading.value = true;
  error.value = null;
  result.value = null;

  try {
    const response = await analyzeTabacco(selectedImage.value);
    result.value = response;
  } catch (err: any) {
    error.value =
      err.response?.data?.error || "Terjadi kesalahan saat menganalisis gambar";
  } finally {
    isLoading.value = false;
  }
};

const resetAnalysis = () => {
  selectedImage.value = null;
  imagePreview.value = null;
  result.value = null;
  error.value = null;
};

const getGradeColor = (grade: string) => {
  if (grade.includes("Sangat Tinggi") || grade.includes("Premium+"))
    return "text-green-700";
  if (grade.includes("Tinggi") || grade.includes("Grade A"))
    return "text-green-600";
  if (grade.includes("Standar") || grade.includes("Grade B"))
    return "text-yellow-600";
  if (grade.includes("Rendah") && grade.includes("Grade C"))
    return "text-orange-600";
  if (grade.includes("Sangat Rendah") || grade.includes("Grade D"))
    return "text-red-600";
  return "text-gray-600";
};

const getGradeBg = (grade: string) => {
  if (grade.includes("Sangat Tinggi") || grade.includes("Premium+"))
    return "bg-green-100 border-green-400";
  if (grade.includes("Tinggi") || grade.includes("Grade A"))
    return "bg-green-100 border-green-300";
  if (grade.includes("Standar") || grade.includes("Grade B"))
    return "bg-yellow-100 border-yellow-300";
  if (grade.includes("Rendah") && grade.includes("Grade C"))
    return "bg-orange-100 border-orange-300";
  if (grade.includes("Sangat Rendah") || grade.includes("Grade D"))
    return "bg-red-100 border-red-300";
  return "bg-gray-100 border-gray-300";
};

const formatPrice = (price: number) => {
  return new Intl.NumberFormat("id-ID", {
    style: "currency",
    currency: "IDR",
    minimumFractionDigits: 0,
  }).format(price);
};
</script>

<template>
  <div
    class="min-h-screen bg-gradient-to-br from-amber-50 via-green-50 to-yellow-50"
  >
    <!-- Header/Navbar -->
    <nav
      class="backdrop-blur-md bg-white/30 border-b border-white/20 sticky top-0 z-50"
    >
      <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex justify-between items-center">
          <div class="flex items-center space-x-3">
            <div class="text-3xl">🌿</div>
            <h1 class="text-xl sm:text-2xl font-bold text-amber-900">SiMadu</h1>
          </div>
          <div class="flex gap-2 sm:gap-4">
            <button
              @click="router.push('/')"
              class="px-3 sm:px-4 py-2 text-sm sm:text-base text-amber-900 hover:text-amber-700 font-medium transition"
            >
              Beranda
            </button>
            <button
              @click="router.push('/analyze')"
              class="px-3 sm:px-4 py-2 text-sm sm:text-base text-amber-900 hover:text-amber-700 font-medium transition border-b-2 border-amber-900"
            >
              Analisis
            </button>
            <button
              @click="router.push('/about')"
              class="px-3 sm:px-4 py-2 text-sm sm:text-base text-amber-900 hover:text-amber-700 font-medium transition"
            >
              Tentang
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      <div class="text-center mb-8 sm:mb-12">
        <h1
          class="text-3xl sm:text-4xl lg:text-5xl font-bold text-amber-950 mb-4"
        >
          Analisis Mutu Tembakau
        </h1>
        <p class="text-base sm:text-lg text-gray-700 max-w-2xl mx-auto">
          Upload foto tembakau untuk mendapatkan klasifikasi mutu berdasarkan
          Fuzzy Logic Mamdani
        </p>
      </div>

      <!-- Upload Section -->
      <div v-if="!result" class="max-w-3xl mx-auto">
        <div
          class="backdrop-blur-md bg-white/40 border border-white/30 rounded-2xl p-6 sm:p-10 shadow-xl"
        >
          <!-- Drag & Drop Area -->
          <div
            @dragover="handleDragOver"
            @drop="handleDrop"
            class="border-2 border-dashed border-amber-300 rounded-xl p-8 sm:p-12 text-center hover:border-amber-500 transition-colors cursor-pointer"
            :class="{ 'bg-amber-50': imagePreview }"
          >
            <input
              type="file"
              id="imageInput"
              accept="image/*"
              @change="handleImageSelect"
              class="hidden"
            />

            <div v-if="!imagePreview">
              <div class="text-6xl sm:text-7xl mb-4">📷</div>
              <h3 class="text-xl sm:text-2xl font-bold text-amber-900 mb-2">
                Upload Foto Tembakau
              </h3>
              <p class="text-sm sm:text-base text-gray-600 mb-6">
                Drag & drop atau klik untuk memilih gambar
              </p>
              <label
                for="imageInput"
                class="inline-block px-6 sm:px-8 py-3 bg-gradient-to-r from-green-600 to-green-700 text-white rounded-xl font-semibold cursor-pointer hover:shadow-lg transform hover:scale-105 transition-all duration-300"
              >
                Pilih Gambar
              </label>
              <p class="text-xs sm:text-sm text-gray-500 mt-4">
                Format: JPG, PNG | Maksimal: 5MB
              </p>
              <!-- Debug info -->
              <!-- <p class="text-xs text-gray-400 mt-2">Debug: imagePreview = {{ imagePreview ? 'loaded' : 'null' }}</p>-->
            </div>

            <div v-else class="space-y-4">
              <img
                v-if="imagePreview"
                :src="imagePreview"
                alt="Preview"
                class="max-h-64 sm:max-h-96 mx-auto rounded-lg shadow-lg object-contain"
                @error="
                  () => {
                    console.error('Image load error');
                    error = 'Gagal memuat preview gambar';
                  }
                "
              />
              <p class="text-xs text-gray-400">
                Debug: Preview URL length = {{ imagePreview?.length || 0 }}
              </p>
              <div class="flex gap-4 justify-center flex-wrap">
                <label
                  for="imageInput"
                  class="px-4 sm:px-6 py-2 bg-white border border-amber-300 text-amber-900 rounded-lg font-medium cursor-pointer hover:bg-amber-50 transition"
                >
                  Ganti Gambar
                </label>
                <button
                  @click="resetAnalysis"
                  class="px-4 sm:px-6 py-2 bg-red-100 border border-red-300 text-red-700 rounded-lg font-medium hover:bg-red-200 transition"
                >
                  Reset
                </button>
              </div>
            </div>
          </div>

          <!-- Error Message -->
          <div
            v-if="error"
            class="mt-6 p-4 bg-red-100 border border-red-300 text-red-700 rounded-lg"
          >
            {{ error }}
          </div>

          <!-- Analyze Button -->
          <div v-if="imagePreview" class="mt-6 text-center">
            <button
              @click="analyzeImage"
              :disabled="isLoading"
              class="px-8 sm:px-12 py-3 sm:py-4 bg-gradient-to-r from-green-600 to-green-700 text-white rounded-xl font-bold text-base sm:text-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            >
              <span v-if="isLoading">⏳ Menganalisis...</span>
              <span v-else>🔬 Analisis Sekarang</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Result Section -->
      <div v-if="result" class="max-w-6xl mx-auto space-y-6">
        <!-- Header Result -->
        <div
          class="backdrop-blur-md bg-white/40 border border-white/30 rounded-2xl p-6 sm:p-8 shadow-xl text-center"
        >
          <h2 class="text-2xl sm:text-3xl font-bold text-amber-900 mb-4">
            Hasil Analisis
          </h2>
          <div
            class="flex flex-col sm:flex-row gap-6 items-center justify-center"
          >
            <img
              v-if="imagePreview"
              :src="imagePreview"
              alt="Analyzed"
              class="max-h-48 rounded-lg shadow-lg"
            />
            <div class="text-left">
              <div
                :class="[
                  'inline-block px-6 py-3 rounded-xl border-2 font-bold text-xl sm:text-2xl',
                  getGradeBg(result.data.result.grade),
                ]"
              >
                <span :class="getGradeColor(result.data.result.grade)">
                  {{ result.data.result.grade }}
                </span>
              </div>
              <p class="text-3xl sm:text-4xl font-bold text-amber-950 mt-4">
                Skor: {{ result.data.defuzzification.score }}
              </p>
              <p class="text-xl sm:text-2xl font-bold text-green-700 mt-2">
                {{ formatPrice(result.data.result.price) }}/kg
              </p>
              <p
                class="text-base sm:text-lg font-semibold text-amber-800 mt-3 bg-amber-50 px-4 py-2 rounded-lg border border-amber-200"
              >
                {{ result.data.result.tobacco_type }}
              </p>
            </div>
          </div>
          <button
            @click="resetAnalysis"
            class="mt-6 px-6 py-2 bg-amber-600 text-white rounded-lg font-medium hover:bg-amber-700 transition"
          >
            Analisis Gambar Lain
          </button>
        </div>

        <!-- Crisp Input -->
        <div
          class="backdrop-blur-md bg-white/40 border border-white/30 rounded-2xl p-6 sm:p-8 shadow-xl"
        >
          <h3
            class="text-xl sm:text-2xl font-bold text-amber-900 mb-4 flex items-center gap-2"
          >
            <span class="text-2xl">📥</span> 1. Crisp Input
          </h3>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="bg-white/60 rounded-xl p-4 border border-amber-200">
              <p class="text-sm text-gray-600 mb-1">Hue (Warna)</p>
              <p class="text-2xl sm:text-3xl font-bold text-amber-900">
                {{ result.data.input.hue }}
              </p>
              <p class="text-xs text-gray-500 mt-1">Range: 0-180</p>
            </div>
            <div class="bg-white/60 rounded-xl p-4 border border-amber-200">
              <p class="text-sm text-gray-600 mb-1">Value (Kecerahan)</p>
              <p class="text-2xl sm:text-3xl font-bold text-amber-900">
                {{ result.data.input.value }}
              </p>
              <p class="text-xs text-gray-500 mt-1">Range: 0-255</p>
            </div>
          </div>
        </div>

        <!-- Fuzzification -->
        <div
          class="backdrop-blur-md bg-white/40 border border-white/30 rounded-2xl p-6 sm:p-8 shadow-xl"
        >
          <h3
            class="text-xl sm:text-2xl font-bold text-amber-900 mb-4 flex items-center gap-2"
          >
            <span class="text-2xl">🔀</span> 2. Fuzzification (Fuzzy Input)
          </h3>

          <!-- Grafik Keanggotaan HUE -->
          <div class="mb-36">
            <h4 class="font-bold text-amber-800 mb-3 text-lg">
              📊 Grafik Keanggotaan Hue (Warna)
            </h4>
            <MembershipChart
              type="hue"
              :crispValue="result.data.input.hue"
              :membershipValues="{
                emas: result.data.fuzzification.emas,
                kuning: result.data.fuzzification.kuning,
                hijau: result.data.fuzzification.hijau,
              }"
            />
          </div>

          <!-- Grafik Keanggotaan VALUE -->
          <div class="mb-36">
            <h4 class="font-bold text-amber-800 mb-3 text-lg">
              📊 Grafik Keanggotaan Value (Kecerahan)
            </h4>
            <MembershipChart
              type="value"
              :crispValue="result.data.input.value"
              :membershipValues="{
                gelap: result.data.fuzzification.gelap,
                sedang: result.data.fuzzification.sedang,
                cerah: result.data.fuzzification.cerah,
              }"
            />
          </div>

          <div class="space-y-6">
            <!-- Hue Membership -->
            <div>
              <h4 class="font-bold text-amber-800 mb-3">
                Derajat Keanggotaan Hue (Warna)
              </h4>
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div
                  class="bg-yellow-50 rounded-lg p-4 border border-yellow-300"
                >
                  <p class="text-sm text-gray-600">Emas (Premium)</p>
                  <p class="text-xl font-bold text-yellow-700">
                    {{ result.data.fuzzification.emas }}
                  </p>
                </div>
                <div class="bg-amber-50 rounded-lg p-4 border border-amber-300">
                  <p class="text-sm text-gray-600">Kuning (Sedang)</p>
                  <p class="text-xl font-bold text-amber-700">
                    {{ result.data.fuzzification.kuning }}
                  </p>
                </div>
                <div class="bg-green-50 rounded-lg p-4 border border-green-300">
                  <p class="text-sm text-gray-600">Hijau (Rendah)</p>
                  <p class="text-xl font-bold text-green-700">
                    {{ result.data.fuzzification.hijau }}
                  </p>
                </div>
              </div>
            </div>

            <!-- Value Membership -->
            <div>
              <h4 class="font-bold text-amber-800 mb-3">
                Derajat Keanggotaan Value (Kecerahan)
              </h4>
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div class="bg-gray-50 rounded-lg p-4 border border-gray-300">
                  <p class="text-sm text-gray-600">Gelap (Buruk)</p>
                  <p class="text-xl font-bold text-gray-700">
                    {{ result.data.fuzzification.gelap }}
                  </p>
                </div>
                <div class="bg-blue-50 rounded-lg p-4 border border-blue-300">
                  <p class="text-sm text-gray-600">Sedang</p>
                  <p class="text-xl font-bold text-blue-700">
                    {{ result.data.fuzzification.sedang }}
                  </p>
                </div>
                <div
                  class="bg-yellow-50 rounded-lg p-4 border border-yellow-300"
                >
                  <p class="text-sm text-gray-600">Cerah (Bagus)</p>
                  <p class="text-xl font-bold text-yellow-700">
                    {{ result.data.fuzzification.cerah }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Inference -->
        <div
          class="backdrop-blur-md bg-white/40 border border-white/30 rounded-2xl p-6 sm:p-8 shadow-xl"
        >
          <h3
            class="text-xl sm:text-2xl font-bold text-amber-900 mb-4 flex items-center gap-2"
          >
            <span class="text-2xl">⚙️</span> 3. Inference (Fuzzy Output)
          </h3>

          <!-- Rules Alpha -->
          <div class="mb-6">
            <h4 class="font-bold text-amber-800 mb-3">
              Aturan Fuzzy (MIN Implication) - Total 9 Rules
            </h4>
            <div
              class="bg-white/60 rounded-lg p-4 border border-amber-200 space-y-2.5 text-sm"
            >
              <!-- KATEGORI EMAS -->
              <div
                class="bg-gradient-to-r from-yellow-50 to-yellow-100 border-l-4 border-yellow-600 p-3 rounded space-y-2"
              >
                <p class="font-bold text-yellow-900 mb-2">
                  🟡 KATEGORI EMAS (Premium)
                </p>

                <div class="bg-white/80 p-2 rounded">
                  <p>
                    <span class="font-semibold text-green-800">R1:</span>
                    <span class="text-gray-700"
                      >IF Emas AND Cerah THEN Emas Cerah (A+)</span
                    >
                  </p>
                  <p class="mt-1 text-xs text-gray-600">
                    α₁ = MIN({{ result.data.fuzzification.emas.toFixed(3) }},
                    {{ result.data.fuzzification.cerah.toFixed(3) }}) =
                    <span class="font-bold text-green-700">{{
                      result.data.inference.rules.R1.toFixed(4)
                    }}</span>
                  </p>
                </div>

                <div class="bg-white/80 p-2 rounded">
                  <p>
                    <span class="font-semibold text-green-700">R2:</span>
                    <span class="text-gray-700"
                      >IF Emas AND Sedang THEN Emas Sedang (A)</span
                    >
                  </p>
                  <p class="mt-1 text-xs text-gray-600">
                    α₂ = MIN({{ result.data.fuzzification.emas.toFixed(3) }},
                    {{ result.data.fuzzification.sedang.toFixed(3) }}) =
                    <span class="font-bold text-green-700">{{
                      result.data.inference.rules.R2.toFixed(4)
                    }}</span>
                  </p>
                </div>

                <div class="bg-white/80 p-2 rounded">
                  <p>
                    <span class="font-semibold text-yellow-700">R3:</span>
                    <span class="text-gray-700"
                      >IF Emas AND Gelap THEN Emas Gelap (B)</span
                    >
                  </p>
                  <p class="mt-1 text-xs text-gray-600">
                    α₃ = MIN({{ result.data.fuzzification.emas.toFixed(3) }},
                    {{ result.data.fuzzification.gelap.toFixed(3) }}) =
                    <span class="font-bold text-yellow-700">{{
                      result.data.inference.rules.R3.toFixed(4)
                    }}</span>
                  </p>
                </div>
              </div>

              <!-- KATEGORI KUNING -->
              <div
                class="bg-gradient-to-r from-orange-50 to-orange-100 border-l-4 border-orange-600 p-3 rounded space-y-2"
              >
                <p class="font-bold text-orange-900 mb-2">
                  🟠 KATEGORI KUNING (Sedang)
                </p>

                <div class="bg-white/80 p-2 rounded">
                  <p>
                    <span class="font-semibold text-yellow-700">R4:</span>
                    <span class="text-gray-700"
                      >IF Kuning AND Cerah THEN Kuning Cerah (B+)</span
                    >
                  </p>
                  <p class="mt-1 text-xs text-gray-600">
                    α₄ = MIN({{ result.data.fuzzification.kuning.toFixed(3) }},
                    {{ result.data.fuzzification.cerah.toFixed(3) }}) =
                    <span class="font-bold text-yellow-700">{{
                      result.data.inference.rules.R4.toFixed(4)
                    }}</span>
                  </p>
                </div>

                <div class="bg-white/80 p-2 rounded">
                  <p>
                    <span class="font-semibold text-yellow-600">R5:</span>
                    <span class="text-gray-700"
                      >IF Kuning AND Sedang THEN Kuning Sedang (B)</span
                    >
                  </p>
                  <p class="mt-1 text-xs text-gray-600">
                    α₅ = MIN({{ result.data.fuzzification.kuning.toFixed(3) }},
                    {{ result.data.fuzzification.sedang.toFixed(3) }}) =
                    <span class="font-bold text-yellow-600">{{
                      result.data.inference.rules.R5.toFixed(4)
                    }}</span>
                  </p>
                </div>

                <div class="bg-white/80 p-2 rounded">
                  <p>
                    <span class="font-semibold text-orange-700">R6:</span>
                    <span class="text-gray-700"
                      >IF Kuning AND Gelap THEN Kuning Gelap (C)</span
                    >
                  </p>
                  <p class="mt-1 text-xs text-gray-600">
                    α₆ = MIN({{ result.data.fuzzification.kuning.toFixed(3) }},
                    {{ result.data.fuzzification.gelap.toFixed(3) }}) =
                    <span class="font-bold text-orange-700">{{
                      result.data.inference.rules.R6.toFixed(4)
                    }}</span>
                  </p>
                </div>
              </div>

              <!-- KATEGORI HIJAU -->
              <div
                class="bg-gradient-to-r from-green-50 to-green-100 border-l-4 border-green-600 p-3 rounded space-y-2"
              >
                <p class="font-bold text-green-900 mb-2">
                  🟢 KATEGORI HIJAU (Rendah)
                </p>

                <div class="bg-white/80 p-2 rounded">
                  <p>
                    <span class="font-semibold text-orange-600">R7:</span>
                    <span class="text-gray-700"
                      >IF Hijau AND Cerah THEN Hijau Cerah (C+)</span
                    >
                  </p>
                  <p class="mt-1 text-xs text-gray-600">
                    α₇ = MIN({{ result.data.fuzzification.hijau.toFixed(3) }},
                    {{ result.data.fuzzification.cerah.toFixed(3) }}) =
                    <span class="font-bold text-orange-600">{{
                      result.data.inference.rules.R7.toFixed(4)
                    }}</span>
                  </p>
                </div>

                <div class="bg-white/80 p-2 rounded">
                  <p>
                    <span class="font-semibold text-orange-700">R8:</span>
                    <span class="text-gray-700"
                      >IF Hijau AND Sedang THEN Hijau Sedang (C)</span
                    >
                  </p>
                  <p class="mt-1 text-xs text-gray-600">
                    α₈ = MIN({{ result.data.fuzzification.hijau.toFixed(3) }},
                    {{ result.data.fuzzification.sedang.toFixed(3) }}) =
                    <span class="font-bold text-orange-700">{{
                      result.data.inference.rules.R8.toFixed(4)
                    }}</span>
                  </p>
                </div>

                <div class="bg-white/80 p-2 rounded">
                  <p>
                    <span class="font-semibold text-red-700">R9:</span>
                    <span class="text-gray-700"
                      >IF Hijau AND Gelap THEN Hijau Gelap (D)</span
                    >
                  </p>
                  <p class="mt-1 text-xs text-gray-600">
                    α₉ = MIN({{ result.data.fuzzification.hijau.toFixed(3) }},
                    {{ result.data.fuzzification.gelap.toFixed(3) }}) =
                    <span class="font-bold text-red-700">{{
                      result.data.inference.rules.R9.toFixed(4)
                    }}</span>
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- Aggregation -->
          <div>
            <h4 class="font-bold text-amber-800 mb-3">
              Agregasi (MAX Composition)
            </h4>
            <p
              class="text-xs text-gray-600 mb-3 bg-blue-50 p-2 rounded border border-blue-200"
            >
              💡 Menggabungkan hasil rules dengan operasi MAX untuk setiap grade
            </p>

            <!-- Grafik Output Membership Functions -->
            <div class="mb-32">
              <h5 class="font-semibold text-amber-700 mb-3 text-sm">
                📊 Grafik Fungsi Keanggotaan Output (Grade)
              </h5>
              <OutputMembershipChart
                :aggregation="result.data.inference.aggregation"
              />
            </div>

            <div class="grid grid-cols-3 sm:grid-cols-9 gap-2">
              <div class="bg-red-50 rounded-lg p-2 border-2 border-red-300">
                <p class="text-[10px] text-gray-600 font-semibold mb-1">C-</p>
                <p class="text-xs text-gray-500 mb-1">α₉</p>
                <p class="text-lg font-bold text-red-700">
                  {{ result.data.inference.aggregation.C_minus.toFixed(4) }}
                </p>
              </div>
              <div class="bg-red-100 rounded-lg p-2 border-2 border-red-400">
                <p class="text-[10px] text-gray-600 font-semibold mb-1">C</p>
                <p class="text-xs text-gray-500 mb-1">α₈</p>
                <p class="text-lg font-bold text-red-800">
                  {{ result.data.inference.aggregation.C.toFixed(4) }}
                </p>
              </div>
              <div class="bg-orange-50 rounded-lg p-2 border-2 border-orange-300">
                <p class="text-[10px] text-gray-600 font-semibold mb-1">C+</p>
                <p class="text-xs text-gray-500 mb-1">α₇</p>
                <p class="text-lg font-bold text-orange-700">
                  {{ result.data.inference.aggregation.C_plus.toFixed(4) }}
                </p>
              </div>
              <div class="bg-yellow-50 rounded-lg p-2 border-2 border-yellow-300">
                <p class="text-[10px] text-gray-600 font-semibold mb-1">B-</p>
                <p class="text-xs text-gray-500 mb-1">α₆</p>
                <p class="text-lg font-bold text-yellow-700">
                  {{ result.data.inference.aggregation.B_minus.toFixed(4) }}
                </p>
              </div>
              <div class="bg-yellow-100 rounded-lg p-2 border-2 border-yellow-400">
                <p class="text-[10px] text-gray-600 font-semibold mb-1">B</p>
                <p class="text-xs text-gray-500 mb-1">α₅</p>
                <p class="text-lg font-bold text-yellow-800">
                  {{ result.data.inference.aggregation.B.toFixed(4) }}
                </p>
              </div>
              <div class="bg-blue-50 rounded-lg p-2 border-2 border-blue-300">
                <p class="text-[10px] text-gray-600 font-semibold mb-1">B+</p>
                <p class="text-xs text-gray-500 mb-1">α₄</p>
                <p class="text-lg font-bold text-blue-700">
                  {{ result.data.inference.aggregation.B_plus.toFixed(4) }}
                </p>
              </div>
              <div class="bg-cyan-50 rounded-lg p-2 border-2 border-cyan-300">
                <p class="text-[10px] text-gray-600 font-semibold mb-1">A-</p>
                <p class="text-xs text-gray-500 mb-1">α₃</p>
                <p class="text-lg font-bold text-cyan-700">
                  {{ result.data.inference.aggregation.A_minus.toFixed(4) }}
                </p>
              </div>
              <div class="bg-green-50 rounded-lg p-2 border-2 border-green-300">
                <p class="text-[10px] text-gray-600 font-semibold mb-1">A</p>
                <p class="text-xs text-gray-500 mb-1">α₂</p>
                <p class="text-lg font-bold text-green-700">
                  {{ result.data.inference.aggregation.A.toFixed(4) }}
                </p>
              </div>
              <div class="bg-green-100 rounded-lg p-2 border-2 border-green-400">
                <p class="text-[10px] text-gray-600 font-semibold mb-1">A+</p>
                <p class="text-xs text-gray-500 mb-1">α₁</p>
                <p class="text-lg font-bold text-green-800">
                  {{ result.data.inference.aggregation.A_plus.toFixed(4) }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Defuzzification & Chart -->
        <div
          class="backdrop-blur-md bg-white/40 border border-white/30 rounded-2xl p-6 sm:p-8 shadow-xl"
        >
          <h3
            class="text-xl sm:text-2xl font-bold text-amber-900 mb-4 flex items-center gap-2"
          >
            <span class="text-2xl">📊</span> 4. Defuzzification (Crisp Output)
          </h3>

          <!-- Defuzz Info -->
          <div class="bg-white/60 rounded-lg p-4 border border-amber-200 mb-6">
            <p class="text-sm text-gray-600 mb-2">
              Metode:
              <span class="font-bold">Discretized Centroid (Mamdani)</span>
            </p>
            <p class="text-sm text-gray-600 mb-2">
              Numerator (Σ(xi × μi)):
              <span class="font-bold">{{
                result.data.defuzzification.numerator
              }}</span>
            </p>
            <p class="text-sm text-gray-600">
              Denominator (Σμi):
              <span class="font-bold">{{
                result.data.defuzzification.denominator
              }}</span>
            </p>
          </div>

          <!-- Chart -->
          <div class="mb-6 bg-white rounded-xl p-4 border border-amber-200">
            <DefuzzChart
              :graphData="result.data.graph_data"
              :aggregation="result.data.inference.aggregation"
              :score="result.data.defuzzification.score"
            />
          </div>

          <!-- Final Result -->
          <div
            :class="[
              'rounded-xl p-6 border-2 text-center',
              getGradeBg(result.data.result.grade),
            ]"
          >
            <p class="text-lg font-semibold mb-2">Hasil Akhir</p>
            <p
              class="text-4xl sm:text-5xl font-bold mb-2"
              :class="getGradeColor(result.data.result.grade)"
            >
              {{ result.data.defuzzification.score }}
            </p>
            <p
              class="text-xl font-bold mb-2"
              :class="getGradeColor(result.data.result.grade)"
            >
              {{ result.data.result.grade }}
            </p>
            <p
              class="text-2xl font-bold text-amber-900 mb-2 bg-white/60 rounded-lg px-4 py-2 inline-block"
            >
              {{ result.data.result.tobacco_type }}
            </p>
            <p class="text-2xl font-bold text-green-700 mt-3">
              {{ formatPrice(result.data.result.price) }}/kg
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer
      class="backdrop-blur-md bg-white/30 border-t border-white/20 py-6 sm:py-8 mt-12 sm:mt-20"
    >
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
