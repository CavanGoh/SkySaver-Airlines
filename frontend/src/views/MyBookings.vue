<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';

const activeTab = ref('upcoming');
const bookings = ref([]);
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

const fetchUserBookings = async () =>{
  try{
    let response = await axios.get("http://localhost:5000/get/userflight/101");
    let userFlights = response.data.data.booking;
    console.log(userFlights);
  }catch (err) {
    console.error('Error fetching bookings:', err);
  }
}

onMounted(() => {
  fetchUserBookings();
})
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