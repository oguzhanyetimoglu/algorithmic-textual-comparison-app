<template>
    <div class="p-6">
        <form @submit.prevent="submitForm" class="space-y-6 mb-6">
            <div class="flex flex-row space-x-6">
                <div class="flex space-x-4 flex-grow">
                    <div class="flex-1">
                        <label for="year" class="block text-sm font-medium text-gray-700">Year:</label>
                        <input v-model="form.year" id="year" type="number" min="1000" max="9999"
                            class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
                    </div>

                    <div class="flex-1">
                        <label for="dim_reduction" class="block text-sm font-medium text-gray-700">Dimensionality
                            Reduction:</label>
                        <select v-model="form.dim_reduction_technique" id="dim_reduction"
                            class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
                            <option v-for="(value, key) in dimReductionTechniques" :value="key" :key="key" class="py-1">
                                {{
            value }}
                            </option>
                        </select>
                    </div>

                    <div class="flex-1">
                        <label for="embedding" class="block text-sm font-medium text-gray-700">Embedding:</label>
                        <select v-model="form.embedding_type" id="embedding"
                            class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
                            <option v-for="(value, key) in embeddingTypes" :value="key" :key="key" class="py-1">{{ value
                                }}
                            </option>
                        </select>
                    </div>

                    <div class="flex-1">
                        <label for="clustering" class="block text-sm font-medium text-gray-700">Clustering:</label>
                        <select v-model="form.clustering_technique" id="clustering"
                            class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
                            <option v-for="(value, key) in clusteringTechniques" :value="key" :key="key" class="py-1">
                                {{ value }}
                            </option>
                        </select>
                    </div>

                    <div class="flex-1">
                        <label for="preprocessing"
                            class="block text-sm font-medium text-gray-700">Preprocessing:</label>
                        <select v-model="form.preprocessing" id="preprocessing"
                            class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
                            <option v-for="(value, key) in isPreprocess" :value="key" :key="key" class="py-1">{{ value
                                }}
                            </option>
                        </select>
                    </div>

                    <div class="flex-1">
                        <label for="n_clusters" class="block text-sm font-medium text-gray-700">Number of
                            Clusters:</label>
                        <input v-model="form.n_clusters" id="n_clusters" type="number" min="1"
                            class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
                    </div>
                </div>

                <div class="flex flex-col justify-end flex-shrink">
                    <button :disabled="loading" type="submit"
                        class="inline-flex py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50">
                        Submit
                    </button>
                </div>
            </div>
        </form>
        <div v-if="loading" class="my-4 text-2xl text-black flex items-center justify-center mt-12 flex-col">
            <div class="flex items-center justify-center">
                <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-black" xmlns="http://www.w3.org/2000/svg" fill="none"
                    viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                    </path>
                </svg>
                Calculating...
            </div>
            <p class="text-sm text-gray-500 flex justify-end">This might take a little while.</p>
        </div>
        <scatter-chart v-if="showResultList && !loading" :labels="resultList" :key="chartKey" />
        <p v-if="!showResultList && !loading" class="text-gray-500 text-center mt-4"> {{ errorMessage }}
        </p>
    </div>
</template>
<script>
import ScatterChart from './ScatterChart.vue';
export default {
    name: 'Cluster',
    components: {
        ScatterChart
    },
    data() {
        return {
            config: useRuntimeConfig(),
            token: "",
            loading: false,
            resultList: null,
            showResultList: false,
            chartKey: 0,
            errorMessage: "",
            form: {
                embedding_type: "tfidf",
                dim_reduction_technique: "pca",
                clustering_technique: "kmeans",
                preprocessing: "0",
                n_clusters: 10,
                year: new Date().getFullYear(),
            },
            embeddingTypes: {
                "tfidf": "Tf-Idf",
                "word2vec": "Word2Vec",
                "bert": "Bert",
            },
            dimReductionTechniques: {
                "pca": "PCA",
                "tsne": "t-SNE",
            },
            clusteringTechniques: {
                "kmeans": "K-Means",
                "agglomerative": "Agglomerative",
            },
            isPreprocess: {
                0: "No",
                1: "Yes",
            },
        }
    },
    methods: {
        async submitForm() {
            this.loading = true;
            // Make the HTTP POST request to the specified URL
            fetch(`${this.config.public.apiBase}/nlp/clustering`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    'Authorization': `${this.token}`,
                },
                body: JSON.stringify(this.form)
            })
                .then(response => {
                    response.json()
                        .then(data => {
                            console.log(data)
                            if (data && data.labels && data.labels.length > 0) {
                                console.log(1)

                                this.resultList = data.labels;
                                console.log(this.resultList);
                                this.loading = false;
                                this.errorMessage = "";
                                this.showResultList = true;
                                this.updateResultList();
                            }
                            else if (data && !data.labels && !data.error) {
                                this.resultList = null;
                                console.log(2)
                                this.showResultList = false;
                                this.loading = false;
                                this.errorMessage = data.message;
                            }
                            else {
                                this.resultList = null;
                                console.log(3)
                                this.showResultList = false;
                                this.loading = false;
                                this.errorMessage = data.error;
                            }
                        })
                })
                .catch(error => {
                    this.loading = false;
                });
        },
        updateResultList() {
            this.chartKey += 1;
        },
    }
}
</script>