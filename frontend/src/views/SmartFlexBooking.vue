<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

// Sample airport data - replace with your actual airport data or API call
const airports = [
  { code: 'JFK', name: 'John F. Kennedy International Airport', city: 'New York' },
  { code: 'LAX', name: 'Los Angeles International Airport', city: 'Los Angeles' },
  { code: 'LHR', name: 'Heathrow Airport', city: 'London' },
  { code: 'CDG', name: 'Charles de Gaulle Airport', city: 'Paris' },
  { code: 'DXB', name: 'Dubai International Airport', city: 'Dubai' },
  { code: 'HND', name: 'Haneda Airport', city: 'Tokyo' },
  { code: 'SIN', name: 'Singapore Changi Airport', city: 'Singapore' },
  { code: 'SYD', name: 'Sydney Airport', city: 'Sydney' },
  { code: 'AMS', name: 'Amsterdam Airport Schiphol', city: 'Amsterdam' },
  { code: 'FRA', name: 'Frankfurt Airport', city: 'Frankfurt' },
];
const flexBooking = ref({
  destination: '',
  startDate: '',
  endDate: '',
  passengers: 1
});


const showDropdown = ref(false);
const filteredAirports = computed(() => {
  if (!flexBooking.value.destination) return [];
  
  const searchTerm = flexBooking.value.destination.toLowerCase();
  return airports.filter(airport => 
  airport.code.toLowerCase().includes(searchTerm) || 
  airport.name.toLowerCase().includes(searchTerm) || 
  airport.city.toLowerCase().includes(searchTerm)
).slice(0, 5); 
});

const selectAirport = (airport) => {
  flexBooking.value.destination = `${airport.city} (${airport.code})`;
  showDropdown.value = false;
};

const router = useRouter();
const submitFlexBooking = async () => {
};
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="max-w-2xl mx-auto">
      <h1 class="text-3xl font-bold text-gray-900 mb-4">Smart Flex Booking</h1>
      <p class="text-gray-600 mb-8">
        Get up to 50% off by being flexible with your travel dates. We'll notify you when discounted seats become available!
      </p>

      <div class="bg-white rounded-lg shadow-sm p-6">
        <form @submit.prevent="submitFlexBooking" class="space-y-6">
          <div class="relative">
            <label for="destination" class="block text-sm font-medium text-gray-700">Destination</label>
            <input
              type="text"
              id="destination"
              v-model="flexBooking.destination"
              @focus="showDropdown = true"
              @blur="setTimeout(() => showDropdown = false, 200)"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              placeholder="Where do you want to go?"
              required
            />
            <!-- Airport dropdown -->
            <div v-if="showDropdown && filteredAirports.length > 0" 
                 class="absolute z-10 mt-1 w-full bg-white shadow-lg rounded-md border border-gray-200 max-h-60 overflow-auto">
              <ul class="py-1">
                <li v-for="airport in filteredAirports" :key="airport.code"
                    @mousedown="selectAirport(airport)"
                    class="px-4 py-2 hover:bg-gray-100 cursor-pointer">
                  <div class="font-medium">{{ airport.city }} ({{ airport.code }})</div>
                  <div class="text-sm text-gray-500">{{ airport.name }}</div>
                </li>
              </ul>
            </div>
          </div>
          
          <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <div>
              <label for="startDate" class="block text-sm font-medium text-gray-700">Earliest Travel Date</label>
              <input
                type="date"
                id="startDate"
                v-model="flexBooking.startDate"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                required
              />
            </div>
            <div>
              <label for="endDate" class="block text-sm font-medium text-gray-700">Latest Travel Date</label>
              <input
                type="date"
                id="endDate"
                v-model="flexBooking.endDate"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                required
              />
            </div>
          </div>

          <div>
            <label for="passengers" class="block text-sm font-medium text-gray-700">Number of Passengers</label>
            <input
              type="number"
              id="passengers"
              v-model="flexBooking.passengers"
              min="1"
              max="9"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              required
            />
          </div>

          <button
            type="submit"
            class="w-full rounded-md bg-blue-600 px-4 py-3 text-base font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
          >
            Book Smart Flex Seat
          </button>
        </form>
      </div>
    </div>
  </div>
</template>