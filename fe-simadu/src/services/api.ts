import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'multipart/form-data',
  },
})

export interface TobaccoAnalysisResponse {
  success: boolean
  data: {
    input: {
      hue: number
      value: number
    }
    fuzzification: {
      emas: number
      kuning: number
      hijau: number
      gelap: number
      sedang: number
      cerah: number
    }
    inference: {
      rules: {
        R1: number
        R2: number
        R3: number
        R4: number
        R5: number
        R6: number
      }
      aggregation: {
        A: number
        B: number
        C: number
      }
    }
    defuzzification: {
      score: number
      numerator: number
      denominator: number
    }
    result: {
      grade: string
      price: number
    }
    graph_data: Array<{
      x: number
      y: number
    }>
  }
}

export const analyzeTabacco = async (imageFile: File): Promise<TobaccoAnalysisResponse> => {
  const formData = new FormData()
  formData.append('image', imageFile)

  const response = await apiClient.post<TobaccoAnalysisResponse>('/api/classify', formData)
  return response.data
}

export const healthCheck = async (): Promise<{ status: string }> => {
  const response = await apiClient.get<{ status: string }>('/api/health')
  return response.data
}
