<script setup lang="ts">
import { ref } from 'vue';

const notifications = ref([]);
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <h1 class="text-3xl font-bold text-gray-900 mb-8">Notifications</h1>

    <div v-if="notifications.length === 0" class="text-center py-12">
      <p class="text-gray-500">No notifications at the moment.</p>
    </div>

    <div v-else class="space-y-4">
      <div
        v-for="(notification, index) in notifications"
        :key="index"
        class="bg-white shadow-sm rounded-lg p-4"
      >
        <!-- Notification content will be displayed here -->
      </div>
    </div>
  </div>
</template>