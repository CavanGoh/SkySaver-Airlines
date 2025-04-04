<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const name = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const error = ref('');
const loading = ref(false);

const handleRegister = async () => {
  error.value = '';
  
  // Basic validation
  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match';
    return;
  }

  loading.value = true;
  
  try {
    // Call the registration API
    await axios.post('http://localhost:5500/register', {
      name: name.value,
      email: email.value,
      password: password.value
    });
    
    // Auto-login after successful registration
    await authStore.login(email.value, password.value);
    
    // Redirect to home page
    router.push('/');
  } catch (err: any) {
    error.value = err.response?.data?.message || 'Registration failed';
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="max-w-md mx-auto my-12 p-6 bg-white rounded shadow">
    <h2 class="text-2xl font-bold mb-6">Create an Account</h2>
    
    <div v-if="error" class="bg-red-100 text-red-700 p-3 rounded mb-4">
      {{ error }}
    </div>
    
    <form @submit.prevent="handleRegister">
      <div class="mb-4">
        <label class="block mb-1">Name</label>
        <input v-model="name" type="text" class="w-full border rounded p-2" required />
      </div>
      
      <div class="mb-4">
        <label class="block mb-1">Email</label>
        <input v-model="email" type="email" class="w-full border rounded p-2" required />
      </div>
      
      <div class="mb-4">
        <label class="block mb-1">Password</label>
        <input v-model="password" type="password" class="w-full border rounded p-2" required minlength="6" />
      </div>
      
      <div class="mb-6">
        <label class="block mb-1">Confirm Password</label>
        <input v-model="confirmPassword" type="password" class="w-full border rounded p-2" required />
      </div>
      
      <button 
        type="submit" 
        class="w-full bg-blue-600 text-white p-2 rounded"
        :disabled="loading"
      >
        {{ loading ? 'Creating Account...' : 'Register' }}
      </button>
    </form>
    
    <div class="mt-6 text-center">
      <p class="text-gray-600">
        Already have an account? 
        <router-link to="/login" class="text-blue-600 hover:underline">Login</router-link>
      </p>
    </div>
  </div>
</template>