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
        R7: number
        R8: number
        R9: number
      }
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
      dominant_rule: string
    }
    defuzzification: {
      score: number
      numerator: number
      denominator: number
    }
    result: {
      tobacco_type: string
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
