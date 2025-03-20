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
      flights: []  // This will store the fetched flight data
    };
  },
  methods: {
    // Method to fetch flights from the API
    fetchFlights() {
      axios.get('http://127.0.0.1:5000/flights')
        .then(response => {
          // Assign the fetched flights data to the flights array
          if (response.data.code === 200) {
            this.flights = response.data.data.flights;
            console.log(this.flights);
          } else {
            console.error('Error fetching flights:', response.data);
          }
        })
        .catch(error => {
          console.error('Error fetching flights:', error);
        });
    }
  },
  mounted() {
    // Call the fetchFlights method when the component is mounted
    this.fetchFlights();
  }
};
</script>



<template>
  <div>
    <!-- Hero Section -->
    <div class="relative isolate overflow-hidden bg-gradient-to-b from-blue-100/20">
      <div class="mx-auto max-w-7xl pb-24 pt-10 sm:pb-32 lg:gap-x-8"> <!--removed: lg:grid lg:grid-cols-2 lg:py-40 lg:px-8-->
        <div class="px-6 lg:px-0"> <!--lg:pt-4-->
          <div class="mx-auto max-w-2xl">
            <div class="max-w-lg">
              <h1 class="mt-10 text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
                Find Affordable Flights with SkySaver
              </h1>
              <p class="mt-6 text-lg leading-8 text-gray-600">
                Book your next adventure at the best prices. Choose between standard bookings or try our Smart Flex option
                for last-minute deals.
              </p>
            </div>
            
            <!-- Search Form -->
            <div class="mt-10 bg-white p-6 rounded-lg shadow-lg">
              <form class="space-y-4">
                <div>
                  <label for="departure" class="block text-sm font-medium text-gray-700">Departure</label>
                  <input
                    type="text"
                    id="departure"
                    v-model="searchForm.departure"
                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    placeholder="From where?"
                  />
                </div>
                <div>
                  <label for="destination" class="block text-sm font-medium text-gray-700">Destination</label>
                  <input
                    type="text"
                    id="destination"
                    v-model="searchForm.destination"
                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    placeholder="Where to?"
                  />
                </div>
                <div class="flex space-x-4">
  <div class="w-1/2">
    <label for="dateFrom" class="block text-sm font-medium text-gray-700">Date from</label>
    <input
      type="date"
      id="dateFrom"
      v-model="searchForm.dateFrom"
      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
    />
  </div>
  
  <div class="w-1/2">
    <label for="dateTo" class="block text-sm font-medium text-gray-700">Date To</label>
    <input
      type="date"
      id="dateTo"
      v-model="searchForm.dateTo"
      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
    />
  </div>
</div>

                <button
                  type="submit"
                  class="w-full rounded-md bg-blue-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
                >
                  Search Flights
                </button>
              </form>
            </div>

           
            <div class="showFlights mt-10">
    <!-- Flight Table -->
    <table class="w-full table-auto border-separate border-spacing-0">
      <thead>
        <tr class="text-left text-sm font-medium text-gray-800 bg-gray-100">
          <th class="py-3 px-6">Departure</th>
          <th class="py-3 px-6">Departure Date</th>
          <th class="py-3 px-6">Departure Time</th>
          <th class="py-3 px-6">Destination</th>
          <th class="py-3 px-6">Price</th>
          <th class="py-3 px-6">Action</th>
        </tr>
      </thead>
      <tbody>
        <!-- Loop through flights and display each row -->
        <tr v-for="(flight, index) in flights" :key="index" class="border-b hover:bg-gray-50">
          <td class="py-4 px-6">{{ flight.departure }}</td>
          <td class="py-4 px-6">{{ flight.departureDate }}</td>
          <td class="py-4 px-6">{{ flight.departureTime }}</td>
          <td class="py-4 px-6">{{ flight.destination }}</td>
          <td class="py-4 px-6">${{ flight.price }}</td>
          <td class="py-4 px-6">
            <button
              @click="checkoutSeats(flight)"
              class="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-blue-700 transition duration-200"
            >
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

    <!-- Smart Flex Section -->
    <div class="bg-white py-24 sm:py-32">
      <div class="mx-auto max-w-7xl px-6 lg:px-8">
        <div class="mx-auto max-w-2xl text-center">
          <h2 class="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            Get Last-Minute Discounted Seats!
          </h2>
          <p class="mt-6 text-lg leading-8 text-gray-600">
            Book a Smart Flex Seat and save up to 50% on last-minute flight deals. Perfect for flexible travelers!
          </p>
          <div class="mt-10 flex items-center justify-center gap-x-6">
            <router-link
              to="/smart-flex"
              class="rounded-md bg-blue-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
            >
              Book a Smart Flex Seat
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Testimonials Section -->
    <div class="bg-gray-50 py-24 sm:py-32">
      <div class="mx-auto max-w-7xl px-6 lg:px-8">
        <div class="mx-auto max-w-2xl text-center">
          <h2 class="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            What Our Customers Say
          </h2>
        </div>
        <div class="mx-auto mt-16 grid max-w-2xl grid-cols-1 gap-8 text-center sm:grid-cols-2 lg:mx-0 lg:max-w-none lg:grid-cols-3">
          <div class="rounded-2xl bg-white p-8 shadow-lg">
            <q class="text-lg text-gray-600">Saved 40% on my flight to Paris using Smart Flex. Amazing service!</q>
            <p class="mt-6 text-base font-semibold text-gray-900">Sarah Johnson</p>
          </div>
          <div class="rounded-2xl bg-white p-8 shadow-lg">
            <q class="text-lg text-gray-600">The flexible booking option is perfect for my unpredictable schedule.</q>
            <p class="mt-6 text-base font-semibold text-gray-900">Mike Chen</p>
          </div>
          <div class="rounded-2xl bg-white p-8 shadow-lg">
            <q class="text-lg text-gray-600">Best prices I've found for last-minute business trips!</q>
            <p class="mt-6 text-base font-semibold text-gray-900">Emma Davis</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>