<script>
// import { ref } from 'vue';
// import { useRouter } from 'vue-router';
// import SmartFlexBooking from './SmartFlexBooking.vue';
// const bookingType = ref('standard');
// const router = useRouter();
// import axios from 'axios';

// const showSeatModal=false;
// const flightSearch = ref({
//   departure: '',
//   destination: '',
//   date: '',
//   endDate: '',
//   passengers: 1
// });

// const searchResults = ref<Array<{
//   id: string;
//   airline: string;
//   departure: string;
//   destination: string;
//   departureTime: string;
//   arrivalTime: string;
//   duration: string;
//   price: number;
//   aircraft: string;
//   seatsAvailable: number;
// }>>([]);
// const isLoading = ref(false);

// const searchFlights = async () => {
//   isLoading.value = true;

//   // Simulate API delay
//   await new Promise(resolve => setTimeout(resolve, 1000));

//   const formatDate = (date) => {
//     const d = new Date(date);
//     const day = String(d.getDate()).padStart(2, '0');
//     const month = String(d.getMonth() + 1).padStart(2, '0'); // Month is 0-based
//     const year = d.getFullYear();
//     return `${day}-${month}-${year}`;
//   };
//   const dateFromFormatted = formatDate(flightSearch.value.date);
//   axios.get('http://127.0.0.1:5000/flights', {
//     params: {
//       departure: flightSearch.value.departure,
//       destination: flightSearch.value.destination,
//       dateFrom: dateFromFormatted, // Send in DD-MM-YYYY format
//       dateTo: dateFromFormatted // Send in DD-MM-YYYY format
//     }
//   })
//     .then(response => {
//       // this.hasSearched =true;

//       if (response.data.code === 200) {
//         console.log(response);
//         searchResults.value = response.data.data.flights;
//         // console.log(this.flights);
//       } else {
//         // this.flights=[];
//         // console.error('Error fetching flights:', response.data);
//       }
//     })
//     .catch(error => {
//       // this.flights=[];
//       // this.hasSearched =true;
//       console.error('Error fetching flights:', error);
//     });

//   // Hardcoded flight results
//   // searchResults.value = [
//   //   {
//   //     id: '1234',
//   //     airline: 'SkySaver Airways',
//   //     departure: flightSearch.value.departure || 'London',
//   //     destination: flightSearch.value.destination || 'New York',
//   //     departureTime: '08:30',
//   //     arrivalTime: '11:45',
//   //     duration: '3h 15m',
//   //     price: 299.99,
//   //     aircraft: 'Boeing 737-800',
//   //     seatsAvailable: 24
//   //   },
//   //   {
//   //     id: '2345',
//   //     airline: 'SkySaver Airways',
//   //     departure: flightSearch.value.departure || 'London',
//   //     destination: flightSearch.value.destination || 'New York',
//   //     departureTime: '12:15',
//   //     arrivalTime: '15:30',
//   //     duration: '3h 15m',
//   //     price: 349.99,
//   //     aircraft: 'Airbus A320',
//   //     seatsAvailable: 16
//   //   },
//   //   {
//   //     id: '3456',
//   //     airline: 'SkySaver Airways',
//   //     departure: flightSearch.value.departure || 'London',
//   //     destination: flightSearch.value.destination || 'New York',
//   //     departureTime: '16:45',
//   //     arrivalTime: '20:00',
//   //     duration: '3h 15m',
//   //     price: 279.99,
//   //     aircraft: 'Boeing 737-900',
//   //     seatsAvailable: 8
//   //   }
//   // ];

//   isLoading.value = false;
// };

// const selectFlight = async (flight) => {
//   try {
//     let flight_id = flight.id
//     const response = await axios.post('http://localhost:5001/booking/new', {
//       user_id: 1,
//       flight_id: flight_id,
//     });

//     console.log('Booking created:', response.data);
//     router.push("/my-bookings")
//   } catch (error) {
//     console.error('Error creating booking:', error);
//   }
// };


import axios from 'axios';
import { useRouter } from 'vue-router';
import SmartFlexBooking from './SmartFlexBooking.vue';

export default {
  components: {
    SmartFlexBooking
  },
  data() {
    return {
      bookingType: 'standard',
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
      flightId:''
    };
  },
  setup() {
    const router = useRouter();
    return { router };
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

      await new Promise(resolve => setTimeout(resolve, 1000));
      const dateFromFormatted = this.formatDate(this.flightSearch.date);

      axios.get('http://127.0.0.1:5000/flights', {
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
          }
        })
        .catch(error => {
          console.error('Error fetching flights:', error);
        });

      this.isLoading = false;
    },
    // async selectFlight(flight) {
    //   try {
    //     console.log("Flight ID is "+this.flightId)
    //     const response = await axios.post('http://localhost:5001/booking/new', {
    //       user_id: 1,
    //       flight_id: flight.id,
    //     });

    //     console.log('Booking created:', response.data);
    //     this.router.push('/my-bookings');
    //   } catch (error) {
    //     console.error('Error creating booking:', error);
    //   }
    // },
    checkoutSeats(flight) {
      console.log("Flight ID is " + this.flightId)
      console.log('Checking seats for flight:', flight);
      this.currentFlight = flight;

      // Fetch seats for this flight
      axios.get(`http://127.0.0.1:8080/seats/flight/${flight.id}`)
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

      alert(`You have selected seat ${this.selectedSeat} for your flight from ${this.currentFlight.departure} to ${this.currentFlight.destination}.`);
      this.showSeatModal = false;

      try {
        const response = await axios.post('http://localhost:5002/book_flight', {
          user_id: 1,
          flight_id: this.flightId,
          seat_id: this.selectedSeat
        });

        // console.log('Booking created:', response.data);
        this.router.push('/my-bookings');
      } catch (error) {
        console.error('Error creating booking:', error);
      }


      // Here you would typically make an API call to reserve the seat
      // axios.post('http://127.0.0.1:8080/seats/reserve', {
      //   flightID: this.currentFlight.id,
      //   seatID: this.selectedSeat
      // })
      this.selectedSeat = ''
    }
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
          <button v-for="type in ['standard', 'smart-flex']" :key="type" @click="bookingType = type" :class="[
            bookingType === type
              ? 'border-blue-500 text-blue-600'
              : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700',
            'whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium'
          ]">
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
            <input type="text" id="departure" v-model="flightSearch.departure"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              placeholder="City or airport" required />
          </div>
          <div>
            <label for="destination" class="block text-sm font-medium text-gray-700">To</label>
            <input type="text" id="destination" v-model="flightSearch.destination"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              placeholder="City or airport" required />
          </div>
        </div>
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
          <div>
            <label for="date" class="block text-sm font-medium text-gray-700">Departure Date</label>
            <input type="date" id="date" v-model="flightSearch.date"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 date-picker-fix"
              required />
          </div>
          <div>
            <label for="passengers" class="block text-sm font-medium text-gray-700">Passengers</label>
            <input type="number" id="passengers" v-model="flightSearch.passengers" min="1" max="9"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              required />
          </div>
        </div>
        <div>
          <button type="submit"
            class="w-full sm:w-auto rounded-md bg-blue-600 px-6 py-3 text-base font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
            :disabled="isLoading">
            {{ isLoading ? 'Searching...' : 'Search Flights' }}
          </button>
        </div>
      </form>
    </div>

    <!-- Smart Flex Booking Form -->
    <div v-else class="bg-white rounded-lg shadow-sm p-6 mb-8">
      <SmartFlexBooking />
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
            <button @click="flightId=flight.id;checkoutSeats(flight)"
              class="w-full py-2 bg-blue-600 hover:bg-blue-700 text-white rounded font-medium transition-colors">
              Select
            </button>
          </div>
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
              <!-- :disabled="!selectedSeat" -->
              Confirm Seat
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
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