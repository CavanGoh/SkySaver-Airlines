<script setup lang="ts">
import { ref } from 'vue';

const flexBooking = ref({
  destination: '',
  startDate: '',
  endDate: '',
  passengers: 1
});

const submitFlexBooking = async () => {
  // TODO: Implement flex booking submission
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
          <div>
            <label for="destination" class="block text-sm font-medium text-gray-700">Destination</label>
            <input
              type="text"
              id="destination"
              v-model="flexBooking.destination"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              placeholder="Where do you want to go?"
              required
            />
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