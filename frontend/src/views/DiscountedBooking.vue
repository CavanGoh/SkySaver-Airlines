<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { useAuthStore } from '../stores/auth';
import { computed } from 'vue';


const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const flightId = Number(route.params.flightId);
const seatId = route.params.seatId as string;
const user = computed(() => authStore.user?.id || null); // This would come from your auth store in a real app
const userId=user.value;

const loading = ref(true);
const error = ref(null);
const bookingData = ref(null);
const paypalButtonRendered = ref(false);
const paypalContainer = ref(null);

// Step tracking
const currentStep = ref('loading');
// Possible values: loading, price, payment, confirming, confirmed, error

onMounted(async () => {
  try {
    loading.value = true;
    
    // Step 1: Get discounted price from the booking management service
    const response = await axios.post('http://localhost:5090/api/booking/accept', {
      flight_id: flightId,
      user_id:12
    });
    
    bookingData.value = response.data;
    currentStep.value = 'price';
    loading.value = false;
    
    // Load PayPal script
    loadPayPalScript();
    
  } catch (err) {
    error.value = 'Failed to get booking information';
    currentStep.value = 'error';
    loading.value = false;
    console.error(err);
  }
});

const loadPayPalScript = () => {
  const script = document.createElement('script');
  script.src = 'https://www.paypal.com/sdk/js?client-id=test&currency=SGD';
  script.addEventListener('load', setupPayPalButton);
  document.body.appendChild(script);
  
  return () => {
    document.body.removeChild(script);
  };
};

const setupPayPalButton = () => {
  if (!bookingData.value || paypalButtonRendered.value || !paypalContainer.value) return;
  
  paypalButtonRendered.value = true;
  
  // @ts-ignore - PayPal is loaded from external script
  window.paypal.Buttons({
    createOrder: async () => {
      try {
        // Process payment through your backend
        const response = await axios.post('http://localhost:5090/api/booking/process-payment', {
          user_id: userId,
          booking_id: bookingData.value.booking_id,
          price: bookingData.value.discounted_price
        });
        
        // Extract the EC token from the approval URL
        const approvalUrl = response.data.paypal_approval_url;
        const ecToken = new URLSearchParams(new URL(approvalUrl).search).get('token');
        
        return ecToken;
      } catch (error) {
        console.error('Error creating PayPal order:', error);
        throw error;
      }
    },
    onApprove: async (data, actions) => {
  currentStep.value = 'confirming';
  
  try {
    // IMPORTANT: Execute the PayPal payment first
    console.log("Payment approved with data:", data);
    
    // Call your payment service's success endpoint to execute the payment
    const paymentResult = await axios.get(`http://localhost:5005/api/payment/success?paymentId=${data.paymentID}&PayerID=${data.payerID}`);
    
    console.log("Payment execution result:", paymentResult.data);
    
    if (paymentResult.data.status !== 'success') {
      throw new Error('Payment execution failed');
    }

   ;

//jz ignore startdate enddate
const departureDate = bookingData.value?.departureDate || new Date().toISOString().split('T')[0];

console.log('Sending booking confirmation with payload:', {
  flight_id: flightId,
  seat_id: seatId,
  userId: userId,
  startDestination: bookingData.value.departure,
  endDestination: bookingData.value.destination,
  startDate: departureDate,
  endDate: departureDate
});
    
    
    // Now confirm the booking
    const confirmResponse = await axios.post('http://localhost:5090/api/booking/confirm', {
    flight_id: flightId,
    seat_id: seatId,
    userId: userId,
    startDestination: bookingData.value.departure,
    endDestination: bookingData.value.destination,
    startDate: departureDate,
    endDate: departureDate
    });



      await axios.put('http://localhost:5021/notifications/deactivate', {
      flight_id: flightId,
      user_id: userId
    });
    
    // Update booking data with confirmation
    bookingData.value = {
      ...bookingData.value,
      confirmation: confirmResponse.data
    };
    
    currentStep.value = 'confirmed';
  } catch (error) {
    console.error('Error processing payment or confirming booking:', error);
    currentStep.value = 'error';
    error.value = 'Failed to complete payment or confirm booking';
  }
}
,
    onError: (err) => {
      console.error('PayPal error:', err);
      currentStep.value = 'error';
      error.value = 'Payment processing failed';
    }
  }).render(paypalContainer.value);
};

onUnmounted(() => {
  // Cleanup if needed
});

const goToBookings = () => {
  router.push('/my-bookings');
};
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <!-- Loading State -->
    <div v-if="currentStep === 'loading'" class="text-center py-12">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-4 text-gray-600">Calculating your discounted price...</p>
    </div>
    
    <!-- Error State -->
    <div v-else-if="currentStep === 'error'" class="bg-red-50 border-l-4 border-red-400 p-4 mb-6">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <p class="text-sm text-red-700">
            {{ error }}
          </p>
        </div>
      </div>
    </div>
    
    <!-- Price Calculation State -->
    <div v-else-if="currentStep === 'price' && bookingData">
      <h1 class="text-2xl font-bold text-gray-900 mb-4">Your Discounted Booking</h1>
      
      <div class="bg-white shadow-sm rounded-lg p-6 mb-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div>
            <p class="text-sm text-gray-500">From</p>
            <p class="font-medium">{{ bookingData.departure }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">To</p>
            <p class="font-medium">{{ bookingData.destination }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Flight ID</p>
            <p class="font-medium">{{ bookingData.flight_id }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Seat</p>
            <p class="font-medium">{{ seatId }}</p>
          </div>
        </div>
        
        <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg mb-6">
          <div>
            <p class="text-sm text-gray-500">Original Price</p>
            <p class="text-lg font-medium line-through">${{ bookingData.original_price }}</p>
          </div>
          <div class="text-right">
            <p class="text-sm text-green-600 font-medium">Discounted Price</p>
            <p class="text-2xl font-bold text-green-600">${{ bookingData.discounted_price }}</p>
          </div>
        </div>
        
        <div class="mt-6">
          <h2 class="text-lg font-semibold text-gray-800 mb-4">Complete Your Payment</h2>
          <div ref="paypalContainer" class="paypal-button-container"></div>
        </div>
      </div>
    </div>
    
    <!-- Confirming State -->
    <div v-else-if="currentStep === 'confirming'" class="text-center py-12">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-4 text-gray-600">Confirming your booking...</p>
    </div>
    
    <!-- Confirmed State -->
    <div v-else-if="currentStep === 'confirmed' && bookingData" class="bg-white shadow-sm rounded-lg p-6">
      <div class="text-center mb-6">
        <svg class="mx-auto h-12 w-12 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        <h1 class="mt-3 text-2xl font-bold text-gray-900">Booking Confirmed!</h1>
        <p class="mt-2 text-gray-600">Your discounted seat has been successfully booked.</p>
      </div>
      
      <div class="border border-gray-200 rounded-lg p-4 mb-6">
        <h2 class="text-lg font-semibold text-gray-800 mb-2">Booking Details</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <p class="text-sm text-gray-500">From</p>
            <p class="font-medium">{{ bookingData.departure }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">To</p>
            <p class="font-medium">{{ bookingData.destination }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Flight ID</p>
            <p class="font-medium">{{ bookingData.flight_id }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Seat</p>
            <p class="font-medium">{{ seatId }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Price Paid</p>
            <p class="font-medium text-green-600">${{ bookingData.discounted_price }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Booking Status</p>
            <p class="font-medium text-green-600">Confirmed</p>
          </div>
        </div>
      </div>
      
      <div class="mt-6 text-center">
        <button
          @click="goToBookings"
          class="rounded-md bg-blue-600 px-6 py-3 text-base font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
        >
          View My Bookings
        </button>
      </div>
    </div>
  </div>
</template>

