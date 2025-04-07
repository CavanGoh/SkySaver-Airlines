<script setup lang="ts">
import { ref, watch, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { useAuthStore } from '../stores/auth.ts';

const router = useRouter();
const authStore = useAuthStore();

const flexBooking = ref({
  departure: '',
  destination: '',
  startDate: '',
  endDate: '',
  passengers: 1
});

const isLoading = ref(false);

// Get today's date in YYYY-MM-DD format for min attribute
const today = new Date().toISOString().split('T')[0];
const minEndDate = ref(today);

const isLoggedIn = () => authStore.isAuthenticated;
const userId = () => authStore.user?.id || null;

const errorMessage = ref('');

// Watch for changes in startDate and update minEndDate
watch(() => flexBooking.value.startDate, (newStartDate) => {
  if (newStartDate) {
    minEndDate.value = newStartDate;
    // If current end date is before new start date, reset it
    if (flexBooking.value.endDate && flexBooking.value.endDate < newStartDate) {
      flexBooking.value.endDate = '';
    }
  } else {
    minEndDate.value = today;
  }
});

const submitFlexBooking = async () => {
  try {
    isLoading.value = true;
    errorMessage.value = '';

    if (!isLoggedIn()) {
      errorMessage.value = "You must be logged in to create a flex booking";
      setTimeout(() => {
        router.push('/login');
      }, 2000);
      return;
    }
    // Validate dates
    if (!flexBooking.value.startDate || !flexBooking.value.endDate) {
      alert('Please select both start and end dates');
      isLoading.value = false;
      return;
    }

    const startDate = new Date(flexBooking.value.startDate);
    const endDate = new Date(flexBooking.value.endDate);

    if (startDate > endDate) {
      alert('End date must be after start date');
      isLoading.value = false;
      return;
    }

    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    console.log('Submitting flex booking:', flexBooking.value);
    
    try {
      const response = await axios.post('http://localhost:5003/flexseat/new', {
        userId: userId(),  // Update this value as per your application’s data
        startDestination: flexBooking.value.departure,
        endDestination: flexBooking.value.destination,
        startDate: flexBooking.value.startDate,
        endDate: flexBooking.value.endDate,
      });
      
      console.log('Flex booking created:', response.data);
      alert(`Your flex seat booking has been confirmed for your flight from ${flexBooking.value.departure} to ${flexBooking.value.destination} from ${flexBooking.value.startDate} to ${flexBooking.value.endDate}.`);

    } catch (error) {
      console.error('Error creating flex booking:', error);
      alert('Error creating booking. Please try again.');
    }
    
    isLoading.value = false;
  } catch (error) {
    console.error('Error submitting booking:', error);
    alert('Error submitting booking. Please try again.');
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="booking-page">
    <div class="booking-header">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 class="text-4xl font-bold text-white mb-4">Smart Flex Booking</h1>
        <p class="text-white text-lg max-w-2xl">Get up to 50% off by being flexible with your travel dates. We'll notify you when discounted seats become available!</p>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="bg-white rounded-lg shadow-lg p-8 -mt-16 relative z-10">
        <form @submit.prevent="submitFlexBooking" class="space-y-6">
          <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <div>
              <label for="flex-departure" class="block text-sm font-medium text-gray-700">From</label>
              <select
                id="flex-departure"
                v-model="flexBooking.departure"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                required
              >
                <option value="" disabled>Select departure city</option>
                <option value="New York">New York</option>
                <option value="London">London</option>
                <option value="Tokyo">Tokyo</option>
                <option value="Seoul">Seoul</option>
                <option value="Paris">Paris</option>
                <option value="Singapore">Singapore</option>
                <option value="Dubai">Dubai</option>
                <option value="Sydney">Sydney</option>
              </select>
            </div>
            <div>
              <label for="flex-destination" class="block text-sm font-medium text-gray-700">To</label>
              <select
                id="flex-destination"
                v-model="flexBooking.destination"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                required
              >
                <option value="" disabled>Select destination city</option>
                <option value="New York">New York</option>
                <option value="London">London</option>
                <option value="Tokyo">Tokyo</option>
                <option value="Seoul">Seoul</option>
                <option value="Paris">Paris</option>
                <option value="Singapore">Singapore</option>
                <option value="Dubai">Dubai</option>
                <option value="Sydney">Sydney</option>
              </select>
            </div>
          </div>
          
          <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <div>
              <label for="flex-start-date" class="block text-sm font-medium text-gray-700">Earliest Travel Date</label>
              <input
                type="date"
                id="flex-start-date"
                v-model="flexBooking.startDate"
                :min="today"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 date-picker-fix"
                required
              />
            </div>
            <div>
              <label for="flex-end-date" class="block text-sm font-medium text-gray-700">Latest Travel Date</label>
              <input
                type="date"
                id="flex-end-date"
                v-model="flexBooking.endDate"
                :min="minEndDate"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 date-picker-fix"
                required
              />
            </div>
          </div>
         
          <div>
            <button
              type="submit"
              class="w-full sm:w-auto rounded-md bg-blue-600 px-6 py-3 text-base font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
              :disabled="isLoading"
            >
              {{ isLoading ? 'Processing...' : 'Book Smart Flex Seat' }}
            </button>
          </div>
        </form>
      </div>
      
      <!-- Smart Flex Explanation -->
      <div class="bg-blue-50 rounded-lg shadow-sm p-6 mt-8 border-l-4 border-blue-500">
        <h3 class="text-xl font-bold text-blue-700 mb-3">How Smart Flex Booking Works</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="flex flex-col items-center text-center">
            <div class="bg-blue-100 rounded-full p-4 mb-3">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <h4 class="text-lg font-semibold text-gray-800 mb-1">Set Your Date Range</h4>
            <p class="text-gray-600 text-sm">Specify the earliest and latest dates you can travel</p>
          </div>
          <div class="flex flex-col items-center text-center">
            <div class="bg-blue-100 rounded-full p-4 mb-3">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
            </div>
            <h4 class="text-lg font-semibold text-gray-800 mb-1">Get Notified</h4>
            <p class="text-gray-600 text-sm">We'll alert you when a discounted seat becomes available</p>
          </div>
          <div class="flex flex-col items-center text-center">
            <div class="bg-blue-100 rounded-full p-4 mb-3">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h4 class="text-lg font-semibold text-gray-800 mb-1">Save Up to 50%</h4>
            <p class="text-gray-600 text-sm">Book instantly at significantly reduced rates</p>
          </div>
        </div>
      </div>
      
      <!-- Travel Inspiration Section -->
      <div class="mb-8 mt-12">
        <h2 class="text-2xl font-bold text-gray-900 mb-6 text-center">Popular Flex Deal Destinations</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Destination Card 1 -->
          <div class="bg-white rounded-lg overflow-hidden shadow-md transition-transform hover:shadow-lg hover:-translate-y-1">
            <img src="https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80" 
                 alt="Paris landmarks" 
                 class="w-full h-48 object-cover">
            <div class="p-4">
              <h3 class="text-lg font-bold text-gray-900">Paris</h3>
              <p class="text-gray-600 text-sm">Experience the romance of the City of Light with its iconic architecture and world-class cuisine.</p>
              <p class="mt-2 text-green-600 font-medium">Up to 40% off with Flex</p>
            </div>
          </div>
          
          <!-- Destination Card 2 -->
          <div class="bg-white rounded-lg overflow-hidden shadow-md transition-transform hover:shadow-lg hover:-translate-y-1">
            <img src="https://images.unsplash.com/photo-1533929736458-ca588d08c8be?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80" 
                 alt="Singapore skyline" 
                 class="w-full h-48 object-cover">
            <div class="p-4">
              <h3 class="text-lg font-bold text-gray-900">Singapore</h3>
              <p class="text-gray-600 text-sm">Discover the perfect blend of cultures, futuristic architecture, and lush gardens in this city-state.</p>
              <p class="mt-2 text-green-600 font-medium">Up to 35% off with Flex</p>
            </div>
          </div>
          
          <!-- Destination Card 3 -->
          <div class="bg-white rounded-lg overflow-hidden shadow-md transition-transform hover:shadow-lg hover:-translate-y-1">
            <img src="https://images.unsplash.com/photo-1616064959886-a500e5c38e1e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80" 
                 alt="Dubai cityscape" 
                 class="w-full h-48 object-cover">
            <div class="p-4">
              <h3 class="text-lg font-bold text-gray-900">Dubai</h3>
              <p class="text-gray-600 text-sm">Experience luxury and innovation in this ultramodern desert metropolis with stunning architecture.</p>
              <p class="mt-2 text-green-600 font-medium">Up to 45% off with Flex</p>
            </div>
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

.date-picker-fix {
  position: relative;
  z-index: 1;
}
</style>
