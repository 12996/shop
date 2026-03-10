<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";

import HomeTopNav from "./components/HomeTopNav.vue";
import MobileTabBar from "./components/MobileTabBar.vue";

const route = useRoute();
const showTopNav = computed(() => route.meta?.showTopNav !== false);
</script>

<template>
  <div class="app-shell">
    <main class="app-main" :class="{ compact: !showTopNav }">
      <HomeTopNav v-if="showTopNav" />
      <router-view />
      <MobileTabBar />
    </main>
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
  background: #f8fafc;
}

.app-main {
  padding: 20px 16px 0;
  box-sizing: border-box;
}

.app-main.compact {
  padding: 0;
}
</style>
