<script>
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth.ts';

export default {
  data() {
    return {
      showSeatModal: false,
      flightSearch: {
        departure: '',
        destination: '',
        date: '',
        endDate: '',
        passengers: 1
      },
      searchResults: [],
      isLoading: false,
      selectedSeat: '',
      flightId:'',
      errorMessage: ''
    };
  },
  setup() {
    const router = useRouter();
    const authStore = useAuthStore();
    return { router, authStore };
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
    formatDate(date) {
      const d = new Date(date);
      const day = String(d.getDate()).padStart(2, '0');
      const month = String(d.getMonth() + 1).padStart(2, '0');
      const year = d.getFullYear();
      return `${day}-${month}-${year}`;
    },
    async searchFlights() {
      this.isLoading = true;
      this.errorMessage = '';

      await new Promise(resolve => setTimeout(resolve, 1000));
      const dateFromFormatted = this.formatDate(this.flightSearch.date);

      axios.get('http://localhost:8000/flights', {
        params: {
          departure: this.flightSearch.departure,
          destination: this.flightSearch.destination,
          dateFrom: dateFromFormatted,
          dateTo: dateFromFormatted
        }
      })
        .then(response => {
          if (response.data.code === 200) {
            // console.log(response);
            this.searchResults = response.data.data.flights;
          } else {
            console.error('Error fetching flights:', response.data);
            this.errorMessage = 'No flights found for your search criteria';
          }
        })
        .catch(error => {
          console.error('Error fetching flights:', error);
          this.errorMessage = 'Failed to search flights. Please try again.';
        });

      this.isLoading = false;
    },
    checkoutSeats(flight) {
      console.log("Flight ID is " + this.flightId)
      console.log('Checking seats for flight:', flight);
      this.currentFlight = flight;

      // Fetch seats for this flight
      axios.get(`http://localhost:8000/seats/flight/${flight.id}`)
        .then(response => {
          console.log('Seats data:', response.data);
          this.seats = response.data;
          this.showSeatModal = true;
          // this.selectedSeat = null;
        })
        .catch(error => {
          console.error('Error fetching seats:', error);
          alert('Failed to load seat information. Please try again.');
        });
    },

    // Get seat availability
    getSeatAvailability(row, col) {
      const seatID = `${row}${col}`;
      const seat = this.seats.find(s => s.seatID === seatID);
      return seat ? seat.availability : false;
    },

    // Select a seat
    selectSeat(seatID) {
      this.selectedSeat = seatID;
      console.log(`Selected seat: ${seatID}`);
    },

    // Confirm seat selection
    async confirmSeatSelection() {
      if (!this.selectedSeat) return;

      if (!this.isLoggedIn) {
        alert("Please log in to book a flight");
        this.router.push('/login');
        return;
      }

      this.showSeatModal = false;
      try {
       
        const response = await axios.post('http://localhost:8000/book_flight', {
          user_id: this.userId,
          flight_id: this.flightId,
          seat_id: this.selectedSeat
        });

        console.log('Booking created:', response.data);
        this.router.push('/my-bookings?tab=upcoming');
      } catch (error) {
        console.error('Error creating booking:', error);
      }
      alert(`You have selected seat ${this.selectedSeat} for your flight from ${this.currentFlight.departure} to ${this.currentFlight.destination}.`);

      this.selectedSeat = ''
    }
  }
};
</script>

<template>

  <div class="booking-page">
    <div class="booking-header">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 class="text-4xl font-bold text-white mb-4">Book Your Flight</h1>
        <p class="text-white text-lg max-w-2xl">Search for flights to destinations around the world and book your next
          adventure with SkySaver Airlines.</p>
      </div>
    </div>

    <!-- Standard Booking Form -->
    <div class="bg-white rounded-lg shadow-sm p-6 mb-8">
      <form @submit.prevent="searchFlights" class="space-y-6">
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
          <div>
            <label for="departure" class="block text-sm font-medium text-gray-700">From</label>
            <select id="departure" v-model="flightSearch.departure"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              required>
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
            <label for="destination" class="block text-sm font-medium text-gray-700">To</label>
            <select id="destination" v-model="flightSearch.destination"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              required>
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
            <label for="date" class="block text-sm font-medium text-gray-700">Departure Date</label>
            <input type="date" id="date" v-model="flightSearch.date"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 date-picker-fix"
              required />
          </div>
        </div>
        <div>
          <button type="submit"
            class="w-full sm:w-auto rounded-md bg-blue-600 px-6 py-3 text-base font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
            :disabled="isLoading">
            {{ isLoading ? 'Searching...' : 'Search Flights' }}
          </button>
          <p v-if="errorMessage" class="text-sm text-red-600">{{ errorMessage }}</p>
        </div>
      </form>
    </div>

    <!-- Search Results -->
    <div v-if="searchResults.length > 0" class="mt-8">
      <h2 class="text-2xl font-bold text-gray-900 mb-6">Available Flights</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div v-for="flight in searchResults" :key="flight.id"
          class="bg-white shadow rounded-lg overflow-hidden border border-gray-200 flex flex-col">
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
            <button @click="flightId = flight.id; checkoutSeats(flight)"
              class="w-full py-2 bg-blue-600 hover:bg-blue-700 text-white rounded font-medium transition-colors">
              Select
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Travel Inspiration Section -->
    <div class="mb-8 mt-12">
      <h2 class="text-2xl font-bold text-gray-900 mb-6 text-center">Explore Popular Destinations</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Destination Card 1 -->
        <div
          class="bg-white rounded-lg overflow-hidden shadow-md transition-transform hover:shadow-lg hover:-translate-y-1">
          <img
            src="https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80"
            alt="New York skyline" class="w-full h-48 object-cover">
          <div class="p-4">
            <h3 class="text-lg font-bold text-gray-900">New York</h3>
            <p class="text-gray-600 text-sm">Experience the vibrant city that never sleeps with iconic landmarks and
              world-class entertainment.</p>
            <p class="mt-2 text-blue-600 font-medium">Flights from $299</p>
          </div>
        </div>

        <!-- Destination Card 2 -->
        <div
          class="bg-white rounded-lg overflow-hidden shadow-md transition-transform hover:shadow-lg hover:-translate-y-1">
          <img
            src="https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80"
            alt="London landmarks" class="w-full h-48 object-cover">
          <div class="p-4">
            <h3 class="text-lg font-bold text-gray-900">London</h3>
            <p class="text-gray-600 text-sm">Discover the perfect blend of history and modernity in one of the world's
              most visited cities.</p>
            <p class="mt-2 text-blue-600 font-medium">Flights from $350</p>
          </div>
        </div>

        <!-- Destination Card 3 -->
        <div
          class="bg-white rounded-lg overflow-hidden shadow-md transition-transform hover:shadow-lg hover:-translate-y-1">
          <img
            src="https://images.unsplash.com/photo-1503899036084-c55cdd92da26?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80"
            alt="Tokyo cityscape" class="w-full h-48 object-cover">
          <div class="p-4">
            <h3 class="text-lg font-bold text-gray-900">Tokyo</h3>
            <p class="text-gray-600 text-sm">Immerse yourself in Japan's captivating blend of ultramodern and
              traditional culture.</p>
            <p class="mt-2 text-blue-600 font-medium">Flights from $450</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Promotional Banner -->
    <div class="bg-gradient-to-r from-blue-500 to-indigo-600 rounded-lg shadow-lg mb-8 overflow-hidden">
      <div class="md:flex items-center">
        <div class="p-6 md:w-2/3">
          <h3 class="text-xl md:text-2xl font-bold text-white mb-2">Summer Special: 15% Off All International Flights
          </h3>
          <p class="text-blue-100 mb-4">Book by June 30th for travel between July and September. Use promo code
            SUMMER23.</p>
          <button class="bg-white text-blue-600 px-6 py-2 rounded font-medium hover:bg-blue-50 transition-colors">
            Learn More
          </button>
        </div>
        <div class="md:w-1/3 p-6 hidden md:block">
          <img
            src="https://images.unsplash.com/photo-1436491865332-7a61a109cc05?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80"
            alt="Airplane wing view" class="rounded-lg shadow">
        </div>
      </div>
    </div>



    <!-- Seat Selection Modal -->
    <div v-if="showSeatModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-xl w-full max-w-3xl max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-bold text-gray-800">Select Your Seat</h2>
            <button @click="showSeatModal = false; selectedSeat = ''" class="text-gray-500 hover:text-gray-700">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div class="mb-4 flex justify-center">
            <div class="flex items-center mr-4">
              <div class="w-4 h-4 bg-blue-500 rounded mr-2"></div>
              <span class="text-sm">Available</span>
            </div>
            <div class="flex items-center">
              <div class="w-4 h-4 bg-gray-300 rounded mr-2"></div>
              <span class="text-sm">Unavailable</span>
            </div>
          </div>

          <!-- Aircraft Layout -->
          <div class="relative bg-gray-100 p-4 rounded-lg airplane-container">
            <!-- Aircraft Nose - More Pointy -->
            <div class="relative mb-6">
              <div class="airplane-nose">
                <div class="cockpit-windows">
                  <div class="window"></div>
                  <div class="window"></div>
                </div>
              </div>
            </div>

            <!-- Seat Labels -->
            <div class="flex justify-between px-2 mb-2">
              <div class="flex justify-between w-[48%]">
                <div class="text-center font-bold text-xs">A</div>
                <div class="text-center font-bold text-xs">B</div>
                <div class="text-center font-bold text-xs">C</div>
              </div>
              <div class="flex justify-between w-[48%]">
                <div class="text-center font-bold text-xs">D</div>
                <div class="text-center font-bold text-xs">E</div>
                <div class="text-center font-bold text-xs">F</div>
              </div>
            </div>

            <!-- Seats -->
            <div class="relative">
              <div v-for="row in 15" :key="row" class="flex justify-between mb-2 items-center">
                <div class="flex justify-between w-[48%]">
                  <button v-for="col in ['A', 'B', 'C']" :key="`${row}${col}`" :class="[
                    'w-[31%] h-8 rounded flex items-center justify-center text-xs font-medium',
                    getSeatAvailability(row, col) ? 'bg-blue-500 text-white hover:bg-blue-600' : 'bg-gray-300 cursor-not-allowed'
                  ]" :disabled="!getSeatAvailability(row, col)" @click="selectSeat(`${row}${col}`)">
                    {{ row }}{{ col }}
                  </button>
                </div>

                <!-- Row Number in Aisle -->
                <div class="w-[4%] text-center font-bold text-xs">{{ row }}</div>

                <div class="flex justify-between w-[48%]">
                  <button v-for="col in ['D', 'E', 'F']" :key="`${row}${col}`" :class="[
                    'w-[31%] h-8 rounded flex items-center justify-center text-xs font-medium',
                    getSeatAvailability(row, col) ? 'bg-blue-500 text-white hover:bg-blue-600' : 'bg-gray-300 cursor-not-allowed'
                  ]" :disabled="!getSeatAvailability(row, col)" @click="selectSeat(`${row}${col}`)">
                    {{ row }}{{ col }}
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div class="mt-6 flex justify-between">
            <button @click="showSeatModal = false; selectedSeat = ''"
              class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300">
              Cancel
            </button>
            <button @click="confirmSeatSelection" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
              Confirm Seat
            </button>
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
  /* Ensure it's not above other elements when not focused */
}


/* Aircraft styling */
.airplane-container {
  position: relative;
  background-color: #f3f4f6;
  padding: 1.5rem;
  border-radius: 0.5rem;
}

.airplane-nose {
  position: relative;
  width: 120px;
  height: 60px;
  margin: 0 auto;
  background-color: #e5e7eb;
  border-top-left-radius: 60px;
  border-top-right-radius: 60px;
  overflow: hidden;
}

.airplane-nose:before {
  content: '';
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 40px;
  background-color: #e5e7eb;
  clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
}

.cockpit-windows {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 10px;
}

.window {
  width: 15px;
  height: 8px;
  background-color: #93c5fd;
  border-radius: 4px;
}
</style>
