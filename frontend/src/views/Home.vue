<template>
  <div>
    <!-- Hero Section -->
    <div class="relative isolate overflow-hidden bg-gradient-to-b from-blue-100/20">
      <div class="mx-auto max-w-7xl pb-24 pt-10 sm:pb-32 lg:gap-x-8">
        <div class="px-6 lg:px-0">
          <div class="mx-auto max-w-2xl">
            <div class="max-w-lg">
              <h1 class="mt-10 text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
                Find Affordable Flights with SkySaver
              </h1>
              <p class="mt-6 text-lg leading-8 text-gray-600">
                Book your next adventure at the best prices. Choose between standard bookings or try our Smart Flex
                option for last-minute deals.
              </p>
            </div>

            <!-- Search Form -->
            <div class="mt-10 bg-white p-6 rounded-lg shadow-lg">
              <form @submit.prevent="searchFlights" class="space-y-6">
                <div class="space-y-4">
                  <div>
                    <label for="departure" class="block text-sm font-medium text-gray-700">Departure</label>
                    <div class="relative mt-1">
                      <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-500">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" 
                          stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M2 22h20"></path>
                          <path d="M6.36 17.4L4 17l-2-4 1.1-.5m13.26 5L18 17l2-4-1.1-.5M2 12h20M2 7h20M6.5 2h11"></path>
                          <path d="M9 2v5.2M15 2v5.2"></path>
                        </svg>
                      </span>
                      <input type="text" id="departure" v-model="searchForm.departure"
                        class="block w-full rounded-md border-gray-300 pl-10 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                        placeholder="From where?" 
                        required/>
                    </div>
                  </div>
                  <div>
                    <label for="destination" class="block text-sm font-medium text-gray-700">Destination</label>
                    <div class="relative mt-1">
                      <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-500">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" 
                          stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M22 12h-20"></path>
                          <path d="M5.45 5.11L2 12v2a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-2l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"></path>
                          <line x1="12" y1="16" x2="12" y2="20"></line>
                          <line x1="8" y1="20" x2="16" y2="20"></line>
                        </svg>
                      </span>
                      <input type="text" id="destination" v-model="searchForm.destination"
                        class="block w-full rounded-md border-gray-300 pl-10 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                        placeholder="Where to?" 
                        required/>
                    </div>
                  </div>
                </div>

                <!-- Availability Section -->
                <div class="space-y-3">
  <h3 class="text-sm font-medium text-gray-700">Availability</h3>
  <div class="grid grid-cols-2 gap-4">
    <div>
      <label for="dateFrom" class="block text-sm font-medium text-gray-700">Date From</label>
      <div class="relative mt-1">
        <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-500">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" 
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="16" y1="2" x2="16" y2="6"></line>
            <line x1="8" y1="2" x2="8" y2="6"></line>
            <line x1="3" y1="10" x2="21" y2="10"></line>
          </svg>
        </span>
        <input 
          type="date" 
          id="dateFrom" 
          v-model="searchForm.dateFrom"
          :min="todayFormatted"
          :max="searchForm.dateTo"
          class="block w-full rounded-md border-gray-300 pl-10 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          @change="validateDates('from')"
          required
        />
      </div>
      <p v-if="dateErrors.from" class="mt-1 text-sm text-red-600">{{ dateErrors.from }}</p>
    </div>
    <div>
      <label for="dateTo" class="block text-sm font-medium text-gray-700">Date To</label>
      <div class="relative mt-1">
        <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-500">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" 
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="16" y1="2" x2="16" y2="6"></line>
            <line x1="8" y1="2" x2="8" y2="6"></line>
            <line x1="3" y1="10" x2="21" y2="10"></line>
          </svg>
        </span>
        <input 
          type="date" 
          id="dateTo" 
          v-model="searchForm.dateTo"
          :min="searchForm.dateFrom || todayFormatted"
          class="block w-full rounded-md border-gray-300 pl-10 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          @change="validateDates('to')"
          required
        />
      </div>
      <p v-if="dateErrors.to" class="mt-1 text-sm text-red-600">{{ dateErrors.to }}</p>
    </div>
  </div>
</div>

                <button type="submit"
                  class="w-full rounded-md bg-blue-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600 transition duration-200">
                  Search Flights
                </button>
                <div v-if="hasSearched && flights.length===0" style="color:red">No flights found</div>
              </form>
            </div>

            <div v-if="flights.length > 0" class="showFlights mt-10">
              <!-- Flight Table -->
              <table class="w-full table-auto border-separate border-spacing-0">
                <thead>
                  <tr class="text-left text-sm font-medium text-gray-800 bg-gray-100">
                    <th class="py-3 px-6">Departure</th>
                    <th class="py-3 px-6">Departure Date</th>
                    <th class="py-3 px-6">Destination</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  <!-- Loop through flights and display each row -->
                  <tr v-for="(flight, index) in flights" :key="index" class="border-b hover:bg-gray-50">
                    <td class="py-4 px-6">{{ flight.departure }}</td>
                    <td class="py-4 px-6">{{ flight.departureDate }}</td>
                    <td class="py-4 px-6">{{ flight.destination }}</td>
                    <td class="py-4 px-6">
                      <button @click="checkoutSeats(flight)"
                        class="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-blue-700 transition duration-200">
                        Check Seats
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      searchForm: {
        departure: '',
        destination: '',
        dateFrom: '',
        dateTo: ''
      },
      dateErrors: {
        from: '',
        to: ''
      },
      flights: [],
      hasSearched :false
    };
  },
  computed: {
    // Format today's date as YYYY-MM-DD for the min attribute
    todayFormatted() {
      const today = new Date();
      const year = today.getFullYear();
      const month = String(today.getMonth() + 1).padStart(2, '0');
      const day = String(today.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    }
  },
  methods: {
    // Validate dates
    validateDates(field) {
      // Clear previous errors
      this.dateErrors.from = '';
      this.dateErrors.to = '';
      
      const { dateFrom, dateTo } = this.searchForm;
      
      // Check if dates are provided
      if (!dateFrom && !dateTo) return;
      
      // Convert string dates to Date objects for comparison
      const fromDate = dateFrom ? new Date(dateFrom) : null;
      const toDate = dateTo ? new Date(dateTo) : null;
      const today = new Date();
      today.setHours(0, 0, 0, 0); // Set to beginning of day for fair comparison
      
      // Validate "Date From" is not before today
      if (fromDate && fromDate < today) {
        this.dateErrors.from = 'Date cannot be in the past';
        this.searchForm.dateFrom = this.todayFormatted;
      }
      
      // Validate date relationship only if both dates are provided
      if (fromDate && toDate) {
        if (fromDate > toDate) {
          if (field === 'from') {
            this.dateErrors.from = 'Date From cannot be after Date To';
            // You could automatically adjust the date if desired:
            // this.searchForm.dateFrom = this.searchForm.dateTo;
          } else {
            this.dateErrors.to = 'Date To cannot be before Date From';
            // You could automatically adjust the date if desired:
            // this.searchForm.dateTo = this.searchForm.dateFrom;
          }
        }
      }
    },
    
    // Format date for display in DD-MM-YYYY format (for API calls)
    formatDateForAPI(apiDate) {
      if (!apiDate) return '';
      
      const [year, month, day] = apiDate.split('-');
      return `${day}-${month}-${year}`;
    },
    
    // Modified search flights method
    searchFlights() {
      // Validate dates before submitting
      this.validateDates('both');
      
      // Don't proceed if there are validation errors
      if (this.dateErrors.from || this.dateErrors.to) {
        return;
      }
      
      // Rest of your search logic
      const { departure, destination, dateFrom, dateTo } = this.searchForm;
      
      // Format dates for API if needed (DD-MM-YYYY)
      const dateFromFormatted = this.formatDateForAPI(dateFrom);
      const dateToFormatted = this.formatDateForAPI(dateTo);
      
      axios.get('http://127.0.0.1:5000/flights', {
        params: {
          departure,
          destination,
          dateFrom: dateFromFormatted, // Send in DD-MM-YYYY format
          dateTo: dateToFormatted // Send in DD-MM-YYYY format
        }
      })
      .then(response => {
        this.hasSearched =true;

        if (response.data.code === 200) {
          console.log(response);
          this.flights = response.data.data.flights;
          console.log(this.flights);
        } else {
          this.flights=[];
          console.error('Error fetching flights:', response.data);
        }
      })
      .catch(error => {
        this.flights=[];
        this.hasSearched =true;
        console.error('Error fetching flights:', error);
      });
    },
    
    // Method to handle seat checkout
    checkoutSeats(flight) {
      console.log('Checking seats for flight:', flight);
      // Implement your seat checkout logic here
    }
  }
};
</script>

<style>
input[type="date"] {
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
}

/* Hide the calendar icon in some browsers */
input[type="date"]::-webkit-calendar-picker-indicator {
  opacity: 0;
  position: absolute;
  right: 0;
  top: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
}
</style>