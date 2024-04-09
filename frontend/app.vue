<script setup lang="ts">
const {
  signIn,
  token,
  data,
  status,
  lastRefreshedAt,
  signOut,
  getSession,
} = useAuth();

const email = ref("");
const password = ref("");
</script>

<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>
