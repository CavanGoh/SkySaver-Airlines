<script setup lang="ts">
import { ref } from 'vue';

const activeTab = ref('upcoming');
const bookings = ref([]);
const flexBookings = ref([]);
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <h1 class="text-3xl font-bold text-gray-900 mb-8">My Bookings</h1>

    <!-- Tabs -->
    <div class="border-b border-gray-200">
      <nav class="-mb-px flex space-x-8" aria-label="Tabs">
        <button
          v-for="tab in ['upcoming', 'cancelled', 'smart-flex']"
          :key="tab"
          @click="activeTab = tab"
          :class="[
            activeTab === tab
              ? 'border-blue-500 text-blue-600'
              : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700',
            'whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium'
          ]"
        >
          {{ tab.charAt(0).toUpperCase() + tab.slice(1) }}
        </button>
      </nav>
    </div>

    <!-- Content -->
    <div class="mt-8">
      <div v-if="activeTab === 'upcoming' && bookings.length === 0" class="text-center py-12">
        <p class="text-gray-500">No upcoming bookings found.</p>
      </div>

      <div v-if="activeTab === 'cancelled' && bookings.length === 0" class="text-center py-12">
        <p class="text-gray-500">No cancelled bookings found.</p>
      </div>

      <div v-if="activeTab === 'smart-flex' && flexBookings.length === 0" class="text-center py-12">
        <p class="text-gray-500">No Smart Flex bookings found.</p>
        <router-link
          to="/smart-flex"
          class="mt-4 inline-block rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500"
        >
          Book a Smart Flex Seat
        </router-link>
      </div>
    </div>
  </div>
</template>