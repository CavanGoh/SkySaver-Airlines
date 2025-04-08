<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { useAuthStore } from '../stores/auth.ts';
import { computed } from 'vue';

const router = useRouter();
const notifications = ref([]);
const loading = ref(true);
const error = ref(null);
const authStore = useAuthStore(); // Access the auth store
const isLoggedIn = computed(() => authStore.isAuthenticated);
const userId = computed(() => authStore.user?.id || null);

onMounted(async () => {
  try {
    loading.value = true;
    
    // Fetch notifications from the notification service
    const response = await axios.get(`http://localhost:5021/notifications?user_id=${userId.value}`);
    
    if (response.status === 200) {
      notifications.value = response.data;
    }
    
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
  // Mark notification as seen
  axios.put('http://localhost:5021/notifications/mark-seen', {
    notification_id: notification.notification_id
  });
  

  router.push({
    name: 'NotificationDetail',
    params: { 
      id: notification.notification_id,
      flightId: notification.flight_id,
      seatId: notification.seat_id 
    }
  });
};
</script>

<template>
  <div class="booking-page">
    <div class="booking-header">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 class="text-4xl font-bold text-white mb-4">Notifications</h1>
        <p class="text-white text-lg max-w-2xl">Stay updated with the latest available seats for your travel plans.</p>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="bg-white rounded-lg shadow-lg p-8 -mt-16 relative z-10">
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
            :key="notification.notification_id"
            class="bg-white shadow-sm rounded-lg p-6 border-l-4"
            :class="notification.seen ? 'border-gray-300' : 'border-blue-500'"
          >
            <div class="flex justify-between items-start mb-4">
              <div>
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  Seat Available
                </span>
                <p class="text-sm text-gray-500 mt-1">
                  {{ formatDate(notification.created_at) }}
                </p>
              </div>
              <span v-if="!notification.seen" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                New
              </span>
            </div>
            
            <h3 class="text-lg font-semibold text-gray-900 mb-2">
              {{ notification.message }}
            </h3>
            
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
    </div>
  </div>
</template>

