<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const notification = ref(null);
const loading = ref(true);
const error = ref(null);

// In a real app, this would come from the route params or query
const notificationId = '123'; // Example ID
const flightId = 1; // From your flight DB structure
const seatId = '10A'; // From your seat DB structure

onMounted(async () => {
  try {
    loading.value = true;
    // In a real implementation, you would fetch the actual notification
    // For now, we'll create mock data based on your DB structure
    notification.value = {
      id: notificationId,
      event_type: 'booking_cancelled',
      booking_id: 456,
      timestamp: new Date().toISOString(),
      details: {
        message: 'A seat has become available at a discounted price!',
        status: 'cancelled',
        flight: {
          id: flightId,
          departure: 'New York',
          destination: 'London',
          departureDate: '06-04-2025',
          departureTime: '08:30:00',
          price: 550
        },
        seat: {
          flightID: flightId,
          seatID: seatId,
          availability: 1
        }
      }
    };
    loading.value = false;
  } catch (err) {
    error.value = 'Failed to load notification details';
    loading.value = false;
    console.error(err);
  }
});

const bookDiscountedSeat = () => {
  // Navigate to booking page with notification data
  router.push({
    name: 'DiscountedBooking',
    params: { 
      notificationId: notificationId,
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

    <div v-else-if="error" class="alert alert-danger" role="alert">
      {{ error }}
    </div>

    <div v-else-if="notification" class="bg-white shadow-sm rounded-lg p-6">
      <div class="bg-blue-50 border-l-4 border-blue-400 p-4 mb-6">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <p class="text-sm text-blue-700">
              {{ notification.details.message }}
            </p>
          </div>
        </div>
      </div>

      <h1 class="text-2xl font-bold text-gray-900 mb-4">Special Discount Opportunity!</h1>
      
      <div class="border border-gray-200 rounded-lg p-4 mb-6">
        <h2 class="text-lg font-semibold text-gray-800 mb-2">Flight Details</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <p class="text-sm text-gray-500">From</p>
            <p class="font-medium">{{ notification.details.flight.departure }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">To</p>
            <p class="font-medium">{{ notification.details.flight.destination }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Date</p>
            <p class="font-medium">{{ notification.details.flight.departureDate }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Time</p>
            <p class="font-medium">{{ notification.details.flight.departureTime }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Seat</p>
            <p class="font-medium">{{ notification.details.seat.seatID }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Original Price</p>
            <p class="font-medium line-through">${{ notification.details.flight.price }}</p>
          </div>
        </div>
      </div>

      <div class="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
        <h2 class="text-lg font-semibold text-green-800 mb-2">Your Discounted Offer</h2>
        <p class="text-3xl font-bold text-green-600 mb-2">
          ${{ Math.round(notification.details.flight.price * 0.7) }}
        </p>
        <p class="text-sm text-green-700">
          That's 30% off the original price! This offer is available for a limited time.
        </p>
      </div>

      <div class="mt-6">
        <button
          @click="bookDiscountedSeat"
          class="w-full sm:w-auto rounded-md bg-blue-600 px-6 py-3 text-base font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
        >
          Book This Discounted Seat
        </button>
      </div>
    </div>
  </div>
</template>
