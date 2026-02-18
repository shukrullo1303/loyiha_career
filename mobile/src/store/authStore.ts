import { create } from 'zustand'
import AsyncStorage from '@react-native-async-storage/async-storage'
import apiClient from '../api/apiClient'

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
  logout: () => Promise<void>
  loadAuth: () => Promise<void>
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  token: null,
  isAuthenticated: false,
  login: async (username: string, password: string) => {
    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)

    const response = await apiClient.post(`/auth/login`, formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })

    const { access_token } = response.data

    const userResponse = await apiClient.get(`/auth/me`, {
      headers: {
        Authorization: `Bearer ${access_token}`,
      },
    })

    await AsyncStorage.setItem('token', access_token)
    await AsyncStorage.setItem('user', JSON.stringify(userResponse.data))

    set({
      token: access_token,
      user: userResponse.data,
      isAuthenticated: true,
    })
  },
  logout: async () => {
    await AsyncStorage.removeItem('token')
    await AsyncStorage.removeItem('user')
    set({
      user: null,
      token: null,
      isAuthenticated: false,
    })
  },
  loadAuth: async () => {
    const token = await AsyncStorage.getItem('token')
    const userStr = await AsyncStorage.getItem('user')

    if (token && userStr) {
      set({
        token,
        user: JSON.parse(userStr),
        isAuthenticated: true,
      })
    }
  },
}))
