<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import SmartFlexBooking from './SmartFlexBooking.vue';
const bookingType = ref('standard');
const router = useRouter();
import axios from 'axios';

const flightSearch = ref({
  departure: '',
  destination: '',
  date: '',
  endDate: '',
  passengers: 1
});

const searchResults = ref<Array<{
  id: string;
  airline: string;
  departure: string;
  destination: string;
  departureTime: string;
  arrivalTime: string;
  duration: string;
  price: number;
  aircraft: string;
  seatsAvailable: number;
}>>([]);
const isLoading = ref(false);

const searchFlights = async () => {
  isLoading.value = true;
  
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  // Hardcoded flight results
  searchResults.value = [
    {
      id: '1234',
      airline: 'SkySaver Airways',
      departure: flightSearch.value.departure || 'London',
      destination: flightSearch.value.destination || 'New York',
      departureTime: '08:30',
      arrivalTime: '11:45',
      duration: '3h 15m',
      price: 299.99,
      aircraft: 'Boeing 737-800',
      seatsAvailable: 24
    },
    {
      id: '2345',
      airline: 'SkySaver Airways',
      departure: flightSearch.value.departure || 'London',
      destination: flightSearch.value.destination || 'New York',
      departureTime: '12:15',
      arrivalTime: '15:30',
      duration: '3h 15m',
      price: 349.99,
      aircraft: 'Airbus A320',
      seatsAvailable: 16
    },
    {
      id: '3456',
      airline: 'SkySaver Airways',
      departure: flightSearch.value.departure || 'London',
      destination: flightSearch.value.destination || 'New York',
      departureTime: '16:45',
      arrivalTime: '20:00',
      duration: '3h 15m',
      price: 279.99,
      aircraft: 'Boeing 737-900',
      seatsAvailable: 8
    }
  ];
  
  isLoading.value = false;
};

const selectFlight = async (flight) => {
  try {
    let flight_id = flight.id
    const response = await axios.post('http://localhost:5000/booking/new', {
      user_id: 1,
      flight_id:flight_id,
    });
    
    console.log('Booking created:', response.data);
    router.push("/my-bookings")
  } catch (error) {
    console.error('Error creating booking:', error);
  }
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
    <div v-if="searchResults.length > 0" class="mt-8">
      <h2 class="text-2xl font-bold text-gray-900 mb-6">Available Flights</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div 
          v-for="flight in searchResults" 
          :key="flight.id" 
          class="bg-white shadow rounded-lg overflow-hidden border border-gray-200 flex flex-col"
        >
          <!-- Flight header -->
          <div class="bg-blue-50 px-4 py-3 border-b border-gray-200">
            <div class="flex justify-between items-center">
              <h3 class="font-bold text-lg text-blue-700">{{ flight.airline }}</h3>
              <span class="text-sm bg-blue-100 text-blue-800 py-1 px-2 rounded">{{ flight.id }}</span>
            </div>
          </div>
          
          <!-- Flight details -->
          <div class="p-4 flex-grow">
            <div class="flex justify-between mb-4">
              <div class="text-center">
                <p class="text-xl font-bold">{{ flight.departureTime }}</p>
                <p class="text-sm text-gray-600">{{ flight.departure }}</p>
              </div>
              <div class="flex items-center px-2">
                <div class="h-0.5 w-16 bg-gray-300 relative">
                  <span class="text-xs text-gray-500 absolute -top-5 left-1/2 transform -translate-x-1/2">
                    {{ flight.duration }}
                  </span>
                </div>
              </div>
              <div class="text-center">
                <p class="text-xl font-bold">{{ flight.arrivalTime }}</p>
                <p class="text-sm text-gray-600">{{ flight.destination }}</p>
              </div>
            </div>
            
            <div class="grid grid-cols-2 gap-3 text-sm">
              <div class="bg-gray-50 p-2 rounded">
                <span class="text-gray-600">Aircraft:</span>
                <span class="font-medium ml-1">{{ flight.aircraft }}</span>
              </div>
              <div class="bg-gray-50 p-2 rounded">
                <span class="text-gray-600">Seats:</span>
                <span class="font-medium ml-1">{{ flight.seatsAvailable }}</span>
              </div>
            </div>
          </div>
          
          <!-- Price and select button -->
          <div class="bg-gray-50 p-4 border-t border-gray-200">
            <div class="flex justify-between items-center mb-3">
              <span class="text-gray-600 text-sm">Price per passenger</span>
              <span class="text-xl font-bold text-blue-700">${{ flight.price }}</span>
            </div>
            <button
              @click="selectFlight(flight)"
              class="w-full py-2 bg-blue-600 hover:bg-blue-700 text-white rounded font-medium transition-colors"
            >
              Select
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>