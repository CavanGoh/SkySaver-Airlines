<script setup lang="ts">
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();

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
      const response = await axios.post('http://localhost:5000/booking/flex', {
        user_id: 1,
        departure: flexBooking.value.departure,
        destination: flexBooking.value.destination,
        start_date: flexBooking.value.startDate,
        end_date: flexBooking.value.endDate,
        passengers: flexBooking.value.passengers
      });
      
      console.log('Flex booking created:', response.data);
      router.push('/booking-confirmation');
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
              <input
                type="text"
                id="flex-departure"
                v-model="flexBooking.departure"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                placeholder="City or airport"
                required
              />
            </div>
            <div>
              <label for="flex-destination" class="block text-sm font-medium text-gray-700">To</label>
              <input
                type="text"
                id="flex-destination"
                v-model="flexBooking.destination"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                placeholder="City or airport"
                required
              />
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
    </div>
  </div>
</template>

<style>
.date-picker-fix {
  position: relative;
  z-index: 1;
}
</style>
