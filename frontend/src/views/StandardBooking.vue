<script setup lang="ts">
import { ref } from 'vue';
import SmartFlexBooking from './SmartFlexBooking.vue';

const bookingType = ref('standard');

const flightSearch = ref({
  departure: '',
  destination: '',
  date: '',
  endDate: '',
  passengers: 1
});

const searchResults = ref([]);
const isLoading = ref(false);

const searchFlights = async () => {
  isLoading.value = true;
  // TODO: Implement API call
  isLoading.value = false;
};
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <h1 class="text-3xl font-bold text-gray-900 mb-8">Book Your Flight</h1>
    
    <!-- Booking Type Toggle -->
    <div class="mb-8">
      <div class="border-b border-gray-200">
        <nav class="-mb-px flex space-x-8" aria-label="Tabs">
          <button
            v-for="type in ['standard', 'smart-flex']"
            :key="type"
            @click="bookingType = type"
            :class="[
              bookingType === type
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700',
              'whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium'
            ]"
          >
            {{ type === 'standard' ? 'Standard Booking' : 'Smart Flex Booking' }}
          </button>
        </nav>
      </div>
    </div>

    <!-- Standard Booking Form -->
    <div v-if="bookingType === 'standard'" class="bg-white rounded-lg shadow-sm p-6 mb-8">
      <form @submit.prevent="searchFlights" class="space-y-6">
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
          <div>
            <label for="departure" class="block text-sm font-medium text-gray-700">From</label>
            <input
              type="text"
              id="departure"
              v-model="flightSearch.departure"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              placeholder="City or airport"
              required
            />
          </div>
          <div>
            <label for="destination" class="block text-sm font-medium text-gray-700">To</label>
            <input
              type="text"
              id="destination"
              v-model="flightSearch.destination"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              placeholder="City or airport"
              required
            />
          </div>
        </div>
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
          <div>
            <label for="date" class="block text-sm font-medium text-gray-700">Departure Date</label>
            <input
              type="date"
              id="date"
              v-model="flightSearch.date"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              required
            />
          </div>
          <div>
            <label for="passengers" class="block text-sm font-medium text-gray-700">Passengers</label>
            <input
              type="number"
              id="passengers"
              v-model="flightSearch.passengers"
              min="1"
              max="9"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
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
            {{ isLoading ? 'Searching...' : 'Search Flights' }}
          </button>
        </div>
      </form>
    </div>

    <!-- Smart Flex Booking Form -->
    <div v-else class="bg-white rounded-lg shadow-sm p-6 mb-8">
     <SmartFlexBooking/>
    </div>

    <!-- Search Results -->
    <div v-if="searchResults.length > 0" class="space-y-4">
      <!-- Flight results will be displayed here -->
    </div>
  </div>
</template>