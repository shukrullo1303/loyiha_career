import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'
import apiClient from '../api/client'

const API_URL = import.meta.env.VITE_API_URL;

interface User {
  id: number
  username: string
  email: string
  full_name: string
  role: string
}

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  login: (username: string, password: string) => Promise<void>
  logout: () => void
  setUser: (user: User) => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      login: async (username: string, password: string) => {
        // FastAPI OAuth2PasswordRequestForm URL-encoded body kutadi
        const formData = new URLSearchParams()
        formData.append('username', username)
        formData.append('password', password)

        const response = await apiClient.post('auth/login', formData)

        const { access_token } = response.data

        // Фойдаланувчи маълумотларини олиш
        const userResponse = await apiClient.get('auth/me', {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        })

        set({
          token: access_token,
          user: userResponse.data,
          isAuthenticated: true,
        })

       
        // apiClient headers are set by interceptor
      },
      logout: () => {
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        })
        delete apiClient.defaults.headers.common['Authorization']
      },
      setUser: (user: User) => {
        set({ user })
      },
    }),
    {
      name: 'auth-storage',
      storage: createJSONStorage(() => localStorage),
    }
  )
)
