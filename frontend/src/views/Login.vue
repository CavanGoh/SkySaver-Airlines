<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const email = ref('');
const password = ref('');
const error = ref('');

const handleLogin = async () => {
  try {
    await authStore.login(email.value, password.value);
    router.push('/');
  } catch (err: any) {
    error.value = err.response?.data?.message || 'Login failed';
  }
};
</script>

<template>
  <div class="max-w-md mx-auto my-12 p-6 bg-white rounded shadow">
    <h2 class="text-2xl font-bold mb-6">Login</h2>
    
    <div v-if="error" class="bg-red-100 text-red-700 p-3 rounded mb-4">
      {{ error }}
    </div>
    
    <form @submit.prevent="handleLogin">
      <div class="mb-4">
        <label class="block mb-1">Email</label>
        <input v-model="email" type="email" class="w-full border rounded p-2" required />
      </div>
      
      <div class="mb-4">
        <label class="block mb-1">Password</label>
        <input v-model="password" type="password" class="w-full border rounded p-2" required />
      </div>
      
      <button 
        type="submit" 
        class="w-full bg-blue-600 text-white p-2 rounded"
        :disabled="authStore.loading"
      >
        {{ authStore.loading ? 'Loading...' : 'Login' }}
      </button>
    </form>
    <div class="mt-6 text-center">
      <p class="text-gray-600">
        Don't have an account? 
        <router-link to="/register" class="text-blue-600 hover:underline">Register now</router-link>
      </p>
    </div>
  </div>
</template>