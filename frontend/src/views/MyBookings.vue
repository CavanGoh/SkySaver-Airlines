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
        const bookingToCancel = this.bookings.find(b => b.booking_id === booking_id);

        if (bookingToCancel) {
          await axios.post(`http://localhost:5100/booking_cancelled`, {
            booking_id: booking_id,
            flight_id: bookingToCancel.flight_id,
            seat_id: bookingToCancel.seat_id,
            user_id: this.userId,
          });
          this.bookings = this.bookings.filter(b => b.booking_id !== booking_id);
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
  <div class="booking-page">
    <div class="booking-header">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 class="text-4xl font-bold text-white mb-4">My Bookings</h1>
        <p class="text-white text-lg max-w-2xl">View and manage all your flight bookings in one place.</p>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="bg-white rounded-lg shadow-lg p-8 -mt-16 relative z-10">
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
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
.booking-page {
  min-height: 100vh;
  background-color: #f8fafc;
}

.booking-header {
  background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
    url('https://images.unsplash.com/photo-1500835556837-99ac94a94552?q=80&w=2069&auto=format&fit=crop');
  background-size: cover;
  background-position: center;
  padding: 6rem 0 8rem;
  position: relative;
}

.booking-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 70px;
  background-image: url('data:image/svg+xml;charset=utf8,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 70" preserveAspectRatio="none"%3E%3Cpath fill="%23f8fafc" d="M0,0 C240,70 480,70 720,35 C960,0 1200,0 1440,35 L1440,70 L0,70 Z"%3E%3C/path%3E%3C/svg%3E');
  background-size: cover;
  background-position: center;
}
</style>