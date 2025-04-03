// src/stores/auth.ts
import { defineStore } from 'pinia'
import axios from 'axios'

axios.defaults.withCredentials = true;

export const useAuthStore = defineStore('auth', {
  // State
  state: () => ({
    // Get user from localStorage if it exists
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    loading: false,
    error: null as string | null
  }),

  // Getters
  getters: {
    isAuthenticated: (state) => !!state.user,
  },

  // Actions
  actions: {
    async login(email: string, password: string) {
      this.loading = true
      this.error = null
      
      try {
        // Example API call
        const response = await axios.post('http://localhost:5500/login', {
          email,
          password
        })
        
        // Save user to state and localStorage
        this.user = response.data.user
        localStorage.setItem('user', JSON.stringify(this.user))
        
        return this.user
      } catch (error: any) {
        this.error = error.response?.data?.message || 'Login failed'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    logout() {
      // Clear state and localStorage
      this.user = null
      localStorage.removeItem('user')
    }
  }
})