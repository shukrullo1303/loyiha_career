import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'
import axios from 'axios'

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
        const formData = new FormData()
        formData.append('username', username)
        formData.append('password', password)

        const response = await axios.post(`${API_URL}/auth/login`, formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        })

        const { access_token } = response.data

        // Фойдаланувчи маълумотларини олиш
        const userResponse = await axios.get(`${API_URL}/auth/me`, {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        })

        set({
          token: access_token,
          user: userResponse.data,
          isAuthenticated: true,
        })

        // Axios default header
        axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
      },
      logout: () => {
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        })
        delete axios.defaults.headers.common['Authorization']
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
