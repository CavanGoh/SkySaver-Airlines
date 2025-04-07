<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const router = useRouter();
const flightDetails = ref(null);
const seatDetails = ref(null);
const loading = ref(true);
const error = ref(null);

const notificationId = route.params.id;
const flightId = route.params.flightId;
const seatId = route.params.seatId;

onMounted(async () => {
  try {
    loading.value = true;
    
    // Get flight details
    const flightResponse = await axios.get(`http://localhost:5000/flight/${flightId}`);
    
    if (flightResponse.status === 200) {
      flightDetails.value = flightResponse.data.data;
      
      // Get specific seat details
      const seatResponse = await axios.get(`http://localhost:8080/seats/${flightId}/${seatId}`);
      if (seatResponse.status === 200) {
        seatDetails.value = seatResponse.data;
      }
    }
    
    loading.value = false;
  } catch (err) {
    error.value = 'Failed to load flight or seat details';
    loading.value = false;
    console.error(err);
  }
});

const bookDiscountedSeat = () => {
  // Navigate to booking page with flight and seat data
  router.push({
    name: 'DiscountedBooking',
    params: { 
      flightId: flightId,
      seatId: seatId
    }
  });
};
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div v-if="loading" class="text-center py-12">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="error" class="bg-red-50 border-l-4 border-red-400 p-4 mb-6">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <p class="text-sm text-red-700">
            {{ error }}
          </p>
        </div>
      </div>
    </div>

    <div v-else-if="flightDetails" class="bg-white shadow-sm rounded-lg p-6">
      <div class="bg-blue-50 border-l-4 border-blue-400 p-4 mb-6">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <p class="text-sm text-blue-700">
              Seat {{ seatId }} has become available due to a cancellation!
            </p>
          </div>
        </div>
      </div>

      <h1 class="text-2xl font-bold text-gray-900 mb-4">Flight Details</h1>
      
      <div class="border border-gray-200 rounded-lg p-4 mb-6">
        <h2 class="text-lg font-semibold text-gray-800 mb-2">Flight Information</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <p class="text-sm text-gray-500">From</p>
            <p class="font-medium">{{ flightDetails.departure }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">To</p>
            <p class="font-medium">{{ flightDetails.destination }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Date</p>
            <p class="font-medium">{{ flightDetails.departureDate }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Time</p>
            <p class="font-medium">{{ flightDetails.departureTime }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Flight ID</p>
            <p class="font-medium">{{ flightDetails.id }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Seat</p>
            <p class="font-medium">{{ seatId }}</p>
          </div>
        </div>
      </div>

      <div class="mt-6">
        <button
          @click="bookDiscountedSeat"
          class="w-full sm:w-auto rounded-md px-6 py-3 text-base font-semibold text-white shadow-sm bg-blue-600 hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
        >
          Book This Seat
        </button>
      </div>
    </div>
  </div>
</template>



