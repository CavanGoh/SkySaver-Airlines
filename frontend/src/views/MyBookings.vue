<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '../stores/auth.ts';

// const activeTab = ref('upcoming');
// const bookings = ref([]);
// const flexBookings = ref([]);

// // Function to handle booking cancellation
// const cancelBooking = async (booking_id: number) => {
//   try {
//     const index = bookings.value.findIndex(booking => booking.booking_id === booking_id);
    
//     if (index !== -1) {
//       await axios.post(`http://localhost:5100/booking_cancelled`, {
//         booking_id: booking_id,
//         user_id: 1,
//       });
      
//       bookings.value.splice(index, 1);

//       console.log(`Booking ${booking_id} cancelled successfully`);
//     }
//   } catch (err) {
//     console.error('Error cancelling booking:', err);
//     alert('Failed to cancel booking. Please try again.');
//   }
// };

// const fetchUserBookings = async () =>{
//   try{
//     let response = await axios.get("http://localhost:5001/booking/1");
//     const allBookings = response.data.data.booking;
//     bookings.value = allBookings.filter(booking => 
//         booking.status === 'Confirmed'
//       );
//     console.log(bookings.value);
//   }catch (err) {
//     console.error('Error fetching bookings:', err);
//   }
// }

// onMounted(() => {
//   fetchUserBookings();
// })


export default {
  data() {
    return {
      activeTab: 'upcoming',  // Reactivity variable for active tab
      bookings: [],  // Stores the confirmed bookings
      flexBookings: []  // (This may be used for different types of bookings if needed)
    };
  },
  setup() {
    const authStore = useAuthStore();
    return { authStore };
  },
  computed: {
    isLoggedIn() {
      return this.authStore.isAuthenticated;
    },
    userId() {
      return this.authStore.user?.id || null;
    }
  },
  methods: {
    // Function to handle booking cancellation
    async cancelBooking(booking_id) {
      try {
        const index = this.bookings.findIndex(booking => booking.booking_id === booking_id);

        if (index !== -1) {
          await axios.post(`http://localhost:5100/booking_cancelled`, {
            booking_id: booking_id,
            user_id: this.userId,
          });

          this.bookings.splice(index, 1);

          console.log(`Booking ${booking_id} cancelled successfully`);
        }
      } catch (err) {
        console.error('Error cancelling booking:', err);
        alert('Failed to cancel booking. Please try again.');
      }
    },

    // Function to fetch the user's bookings
    async fetchUserBookings() {
      try {
        let response = await axios.get("http://localhost:5001/booking/" + this.userId);
        const allBookings = response.data.data.booking;
        this.bookings = allBookings.filter(booking =>
          booking.status === 'Confirmed'
        );
        console.log(this.bookings);
      } catch (err) {
        console.error('Error fetching bookings:', err);
      }
    }
  },
  mounted() {
    // Call fetchUserBookings when the component is mounted
    this.fetchUserBookings();
  }
};
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <h1 class="text-3xl font-bold text-gray-900 mb-8">My Bookings</h1>

    <!-- Tabs -->
    <div class="border-b border-gray-200">
      <nav class="-mb-px flex space-x-8" aria-label="Tabs">
        <button v-for="tab in ['upcoming', 'cancelled', 'smart-flex']" :key="tab" @click="activeTab = tab" :class="[
            activeTab === tab
              ? 'border-blue-500 text-blue-600'
              : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700',
            'whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium'
          ]">
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
          <div v-for="booking in bookings" :key="`${booking.user_id}-${booking.flight_id}`"
            class="border rounded-lg p-6 shadow-sm relative bg-white hover:bg-gray-50">
            <button @click="cancelBooking(booking.booking_id)"
              class="absolute top-4 right-4 text-gray-400 hover:text-red-500 font-bold text-xl"
              aria-label="Cancel booking">
              ✕
            </button>

            <div class="flex items-center">
              <div class="bg-blue-100 rounded-full p-3 mr-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24"
                  stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-semibold">Flight Booking Confirmed</h3>
                <p class="text-gray-600">Flight ID: {{ booking.flight_id }}</p>
                <p class="text-sm text-gray-500">User ID: {{ booking.user_id }}</p>
                <p class="text-sm text-gray-500">Booking ID: {{ booking.booking_id }}</p>
                <p class="text-sm mt-2 text-blue-600">View full booking details</p>
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
        <router-link to="/smart-flex"
          class="mt-4 inline-block rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500">
          Book a Smart Flex Seat
        </router-link>
      </div>
    </div>
  </div>
</template>