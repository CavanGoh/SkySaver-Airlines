import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import StandardBooking from '../views/StandardBooking.vue';
import SmartFlexBooking from '../views/SmartFlexBooking.vue';
import MyBookings from '../views/MyBookings.vue';
import Notifications from '../views/Notifications.vue';
import Login from '../views/Login.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/book',
      name: 'standard-booking',
      component: StandardBooking
    },
    {
      path: '/smart-flex',
      name: 'smart-flex-booking',
      component: SmartFlexBooking
    },
    {
      path: '/my-bookings',
      name: 'my-bookings',
      component: MyBookings
    },
    {
      path: '/notifications',
      name: 'notifications',
      component: Notifications
    },
    {
      path: '/flex-booking',
      name: 'flex-booking',
      component: SmartFlexBooking
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    }
  ]
});

export default router;