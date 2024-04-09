<template>
    <NuxtLink :to="link" class="flex items-center rounded-md p-2 text-white hover:bg-gray-700 group">
        <span class="flex-1 whitespace-nowrap">{{ text }}</span>
    </NuxtLink>
</template>
  
<script>
export default {

    props: {
        link: String,
        text: String,
    },
};
</script>
  