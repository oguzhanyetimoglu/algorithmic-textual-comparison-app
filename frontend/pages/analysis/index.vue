<script>
import Similarity from '@/components/Similarity'
import Cluster from '@/components/Cluster'

export default {
  components: {
    Similarity,
    Cluster
  },
  data() {
    return {
      activeTab: 'Similarity'
    }
  }
}
</script>


<template>
  <div class="p-6">
    <div class="flex mb-4">
      <button class="w-1/2 py-2 px-4 bg-blue-500 text-white rounded-l-lg"
        :class="{ 'bg-blue-700': activeTab === 'Similarity' }" @click="activeTab = 'Similarity'">Similarity</button>
      <button class="w-1/2 py-2 px-4 bg-blue-500 text-white rounded-r-lg"
        :class="{ 'bg-blue-700': activeTab === 'Cluster' }" @click="activeTab = 'Cluster'">Cluster</button>
    </div>

    <div class="border p-4 rounded-lg">
      <component :is="activeTab" />
    </div>
  </div>
</template>