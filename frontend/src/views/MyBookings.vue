<script setup lang="ts">
import { ref } from 'vue';

const activeTab = ref('upcoming');
// Hardcoded example booking
const bookings = ref([
  {
    id: '1234',
    flightNumber: 'SK123',
    departure: {
      airport: 'LHR',
      city: 'London',
      date: '2025-04-15',
      time: '14:30'
    },
    arrival: {
      airport: 'JFK',
      city: 'New York',
      date: '2025-04-15',
      time: '17:45'
    },
    passengers: 1,
    price: 349.99,
    status: 'confirmed'
  }
]);
const flexBookings = ref([]);

// Function to handle booking cancellation
const cancelBooking = (bookingId: string) => {
  // In a real app, this would make an API call
  // For now, just remove from the local array
  const index = bookings.value.findIndex(booking => booking.id === bookingId);
  if (index !== -1) {
    bookings.value.splice(index, 1);
  }
};
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
      <!-- Upcoming bookings -->
      <div v-if="activeTab === 'upcoming'">
        <div v-if="bookings.length === 0" class="text-center py-12">
          <p class="text-gray-500">No upcoming bookings found.</p>
        </div>
        
        <div v-else class="space-y-4">
          <div v-for="booking in bookings" :key="booking.id" class="border rounded-lg p-4 shadow-sm relative">
            <button 
              @click="cancelBooking(booking.id)" 
              class="absolute top-4 right-4 text-gray-400 text-red-500"
              aria-label="Cancel booking"
            >
              ✕
            </button>
            
            <div class="flex flex-col md:flex-row md:justify-between">
              <div>
                <p class="text-sm text-gray-500">Flight Number</p>
                <p class="font-semibold">{{ booking.flightNumber }}</p>
              </div>
              
              <div class="flex flex-col md:flex-row gap-8 mt-4 md:mt-0">
                <div>
                  <p class="text-sm text-gray-500">From</p>
                  <p class="font-semibold">{{ booking.departure.city }} ({{ booking.departure.airport }})</p>
                  <p>{{ booking.departure.date }}, {{ booking.departure.time }}</p>
                </div>
                
                <div>
                  <p class="text-sm text-gray-500">To</p>
                  <p class="font-semibold">{{ booking.arrival.city }} ({{ booking.arrival.airport }})</p>
                  <p>{{ booking.arrival.date }}, {{ booking.arrival.time }}</p>
                </div>
              </div>
              
              <div>
                <p class="text-sm text-gray-500">Price</p>
                <p class="font-semibold">${{ booking.price.toFixed(2) }}</p>
              </div>
            </div>
          </div>
        </div>
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