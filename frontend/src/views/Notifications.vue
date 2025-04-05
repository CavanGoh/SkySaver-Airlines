<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const notifications = ref([]);
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  try {
    loading.value = true;
    
    // In a real implementation, you would fetch notifications from an API
    // For now, we'll create mock data to simulate notifications from RabbitMQ
    notifications.value = [
      {
        id: '123',
        event_type: 'booking_cancelled',
        booking_id: 456,
        timestamp: new Date().toISOString(),
        details: {
          message: 'A seat has become available at a discounted price!',
          status: 'cancelled',
          flight: {
            id: 1,
            departure: 'New York',
            destination: 'London',
            departureDate: '06-04-2025',
            departureTime: '08:30:00',
            price: 550
          },
          seat: {
            flightID: 1,
            seatID: '10A',
            availability: 1
          }
        }
      },
      {
        id: '124',
        event_type: 'booking_cancelled',
        booking_id: 457,
        timestamp: new Date(Date.now() - 86400000).toISOString(), // 1 day ago
        details: {
          message: 'A seat has become available at a discounted price!',
          status: 'cancelled',
          flight: {
            id: 2,
            departure: 'Singapore',
            destination: 'Tokyo',
            departureDate: '10-04-2025',
            departureTime: '14:15:00',
            price: 420
          },
          seat: {
            flightID: 2,
            seatID: '15C',
            availability: 1
          }
        }
      }
    ];
    
    loading.value = false;
  } catch (err) {
    error.value = 'Failed to load notifications';
    loading.value = false;
    console.error(err);
  }
});

const formatDate = (dateString) => {
  const options = { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  };
  return new Date(dateString).toLocaleDateString(undefined, options);
};

const viewDiscountedSeat = (notification) => {
  router.push({
    name: 'NotificationDetail',
    params: { 
      id: notification.id,
      flightId: notification.details.flight.id,
      seatId: notification.details.seat.seatID
    }
  });
};
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <h1 class="text-3xl font-bold text-gray-900 mb-8">Notifications</h1>

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

    <div v-else-if="notifications.length === 0" class="text-center py-12">
      <p class="text-gray-500">No notifications at the moment.</p>
    </div>

    <div v-else class="space-y-4">
      <div
        v-for="notification in notifications"
        :key="notification.id"
        class="bg-white shadow-sm rounded-lg p-6 border-l-4 border-blue-500"
      >
        <div class="flex justify-between items-start mb-4">
          <div>
            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
              Discounted Seat Available
            </span>
            <p class="text-sm text-gray-500 mt-1">
              {{ formatDate(notification.timestamp) }}
            </p>
          </div>
          <span class="text-sm font-medium text-green-600">
            Save 30%
          </span>
        </div>
        
        <h3 class="text-lg font-semibold text-gray-900 mb-2">
          {{ notification.details.message }}
        </h3>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div>
            <p class="text-sm text-gray-500">Flight</p>
            <p class="font-medium">{{ notification.details.flight.departure }} to {{ notification.details.flight.destination }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Date & Time</p>
            <p class="font-medium">{{ notification.details.flight.departureDate }} at {{ notification.details.flight.departureTime }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Seat</p>
            <p class="font-medium">{{ notification.details.seat.seatID }}</p>
          </div>
        </div>
        
        <div class="flex items-center justify-between mt-4">
          <div>
            <p class="text-sm text-gray-500">Original Price</p>
            <p class="text-lg font-medium line-through">${{ notification.details.flight.price }}</p>
          </div>
          <div class="text-right">
            <p class="text-sm text-green-600 font-medium">Discounted Price</p>
            <p class="text-xl font-bold text-green-600">${{ Math.round(notification.details.flight.price * 0.7) }}</p>
          </div>
        </div>
        
        <div class="mt-4 flex justify-end">
          <button
            @click="viewDiscountedSeat(notification)"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Book This Seat
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
