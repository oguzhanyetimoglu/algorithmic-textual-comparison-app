<template>
    <div class="p-6">
        <form @submit.prevent="submitForm" class="space-y-6">
            <div class="flex space-x-4">
                <div class="flex-1">
                    <label for="embedding" class="block text-sm font-medium text-gray-700">Embedding Type:</label>
                    <select v-model="form.embedding_type" id="embedding"
                        class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
                        <option v-for="(value, key) in embeddingTypes" :value="key" :key="key" class="py-1">{{ value }}
                        </option>
                    </select>
                </div>

                <div class="flex-1">
                    <label for="similarity" class="block text-sm font-medium text-gray-700">Similarity
                        Technique:</label>
                    <select v-model="form.similarity_technique" id="similarity"
                        class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
                        <option v-for="(value, key) in similarityTechniques" :value="key" :key="key" class="py-1">{{
            value
        }}
                        </option>
                    </select>
                </div>

                <div class="flex-1">
                    <label for="preprocessing" class="block text-sm font-medium text-gray-700">Preprocessing:</label>
                    <select v-model="form.preprocessing" id="preprocessing"
                        class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
                        <option v-for="(value, key) in isPreprocess" :value="key" :key="key" class="py-1">{{ value }}
                        </option>
                    </select>
                </div>
            </div>

            <div class="flex items-center justify-start space-x-2"> <!-- Adjust the justify property here -->
                <!-- Search Bar -->
                <div class="mb-6 w-3/12 relative">
                    <label for="searchInput" class="block text-sm font-medium text-gray-700">Search</label>
                    <input v-model="searchInput" id="searchInput" type="text"
                        class="mt-0.5 p-2 border rounded-md w-full" autocomplete="off" placeholder="Start typing..."
                        @focus="isSearchFocused = true" @blur="isSearchFocused = false">

                    <ul class="absolute z-10 bg-white w-full border rounded-md">
                        <li v-for="recommendation in filteredRecommendations" :key="recommendation.cik"
                            @mousedown="selectRecommendation(recommendation)" class="cursor-pointer">
                            <div class="flex items-center">
                                <div>
                                    <p class="text-sm font-medium">{{ recommendation.company }} - <span
                                            class="text-xs text-gray-500">{{ recommendation.cik }}</span></p>
                                    <p class="text-xs text-gray-500">{{ recommendation.year }}</p>
                                </div>
                            </div>
                        </li>
                    </ul>
                </div>

                <!-- Year Input -->
                <div class="mb-6 w-1/12">
                    <label for="yearInput" class="block text-sm font-medium text-gray-700">Year (optional)</label>
                    <input v-model="yearInput" id="yearInput" type="number" class="mt-0.5 p-2 border rounded-md w-full"
                        min="1000" max="9999" placeholder="Enter year...">
                </div>
                <!-- Text Query -->
                <div class="w-1/6 mb-6 flex-1">
                    <div class="relative flex flex-col h-auto">
                        <label for="query" class="block text-sm font-medium text-gray-700">Text Query:</label>
                        <textarea v-model="form.text_query" id="query" placeholder="Enter your text query..."
                            :class="{ 'h-60': isTextQueryFocused, 'h-10': !isTextQueryFocused }"
                            class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-all duration-200 ease-in-out overflow-auto"
                            @focus="isTextQueryFocused = true" @blur="isTextQueryFocused = false"></textarea>
                    </div>
                </div>
                <div>
                    <button :disabled="loading" type="submit"
                        class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50">
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
        <div v-if="!loading" class="overflow-x-auto">
            <div class="mb-6 flex justify-end">
                <button v-if="resultList && resultList.length > 0"
                    class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                    @click="exportToCSV">Export to
                    CSV</button>
            </div>
            <table v-if="resultList && resultList.length > 0"
                class="min-w-full divide-y divide-gray-200 shadow-sm rounded-lg overflow-hidden">
                <thead class="bg-gray-50">
                    <tr>
                        <th scope="col"
                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Similarity
                        </th>
                        <th scope="col" v-for="(value, key, index) in getFirstNKeys(resultList[0].object, 15)"
                            :key="index"
                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            {{ key }}
                        </th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="(item, index) in resultList" :key="index" @click="openDialog(item.object)">
                        <td class=" px-6 py-4 whitespace-nowrap">{{ item.similarity.toFixed(5) }}</td>
                        <td class="px-6 py-4 whitespace-nowrap"
                            v-for="(value, key, index2) in getFirstNKeys(item.object, 15)" :key="index2">
                            {{ truncateText(value) }}
                        </td>
                    </tr>
                </tbody>
            </table>
            <p v-else-if="!resultList" class="text-gray-500 text-center mt-4">No entries found.
            </p>
            <p v-else-if="resultList && resultList.length == 0" class="text-gray-500 text-center mt-4">No similarities
                found, please try again with different text query.
            </p>

            <Dialog v-if="showDialog" :showDialog="showDialog" :title="dialogTitle" :row="dialogRow"
                :tableName="tableName" :showEdit="false" @row-updated="handleRowUpdated"
                @dialog-closed="handleDialogClosed" @row-error="handleRowError" />
        </div>
    </div>
</template>

<script>
import Dialog from './Dialog.vue';
import { saveAs } from 'file-saver';
import { createObjectCsvWriter } from 'csv-writer';

export default {
    async created() {
        const {
            token
        } = useAuth();
        this.token = token;
    },
    async mounted() {
        await this.fetchData();
    },
    components: {
        Dialog
    },
    data() {
        return {
            config: useRuntimeConfig(),
            token: "",
            tableName: "ten-k",
            loading: false,
            showDialog: false,
            dialogTitle: "Dialog Title",
            dialogRow: null,
            resultList: null,
            yearInput: new Date().getFullYear(), // Set initial value to current year
            form: {
                embedding_type: "tfidf",
                similarity_technique: "cosine",
                text_query: "",
                preprocessing: "0",
                year: null,
            },
            embeddingTypes: {
                "tfidf": "Tf-Idf",
                "word2vec": "Word2Vec",
                "bert": "Bert"
                // Add more embedding types as needed
            },
            similarityTechniques: {
                "cosine": "Cosine Similarity"
                // Add more similarity techniques as needed
            },
            isPreprocess: {
                0: "No",
                1: "Yes",
            },
            searchInput: '',
            recommendations: [], // Initialize as empty
            page: 1, // Initialize page number
            isLastPage: false, // Flag to check if it's the last page
            selectedRecommendation: null,
            isSearchFocused: false,
            isTextQueryFocused: false,
        }
    },
    computed: {
        filteredRecommendations() {
            if (this.searchInput || this.isSearchFocused) {
                return this.recommendations.filter(recommendation =>
                    (recommendation.company && recommendation.company.toLowerCase().includes(this.searchInput.toLowerCase())) ||
                    (recommendation.cik && recommendation.cik.toString().includes(this.searchInput))
                ).slice(0, 5);
            } else {
                return [];
            }
        },
    },
    methods: {
        truncateText(text, length = 20) {
            if (typeof text === "string") {
                if (text.length > length) {
                    return text.substring(0, length) + '...';
                } else {
                    return text;
                }
            }
            else {
                return text;
            }
        },
        getFirstNKeys(obj, n) {
            return Object.keys(obj)
                .slice(0, n)
                .reduce((result, key) => {
                    result[key] = obj[key];
                    return result;
                }, {});
        },
        submitForm() {
            this.loading = true;
            this.form.year = this.yearInput;
            // Make the HTTP POST request to the specified URL
            fetch(`${this.config.public.apiBase}/nlp/similarity`, {
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
                            this.resultList = data.result_list;
                            this.loading = false;
                            console.log(data);
                        })
                })
                .catch(error => {
                    // Handle any errors here...
                    this.loading = false;
                });
        },
        async openDialog(row) {
            this.dialogTitle = row.company;
            this.dialogRow = row;


            let url = `${this.config.public.apiBase}/api/${this.tableName}/`;
            if (this.tableName === 'ten-k') {
                url += row.cik.toString() + '/' + row.filing_date.toString();
            } else {
                url += row.id.toString();
            }

            try {

                const response = await fetch(url, {
                    headers: {
                        "Content-Type": "application/json",
                        'Authorization': `${this.token}`,
                    },
                });
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                this.dialogRow = await response.json();
                this.showDialog = true;
            } catch (error) {
                console.error(error);
            };
        },
        handleDialogClosed() {
            console.log('Dialog closed');
            this.showDialog = false;
        },
        async fetchData() {
            try {
                const response = await fetch(`${this.config.public.apiBase}/api/ten-k/?page=${this.page}&fields=company,cik,filing_date`); if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                const recommendationsWithYear = data.results.map(recommendation => {
                    recommendation.year = new Date(recommendation.filing_date).getFullYear();
                    return recommendation;
                });
                this.recommendations = [...this.recommendations, ...recommendationsWithYear];
                if (data.next) {
                    this.page += 1;
                    await this.fetchData();
                } else {
                    this.isLastPage = true;
                }
            } catch (error) {
                console.error('There was a problem with the fetch operation: ', error);
            }
        },
        selectRecommendation(recommendation) {
            recommendation.year = new Date(recommendation.filing_date).getFullYear();
            this.yearInput = recommendation.year;
            this.selectedRecommendation = recommendation;
            this.searchInput = `${recommendation.company} - ${recommendation.cik} - ${recommendation.year}`;

            // Fetch specific data from the API
            let url = `${this.config.public.apiBase}/api/ten-k/${recommendation.cik}/${recommendation.filing_date}`;
            fetch(url, {
                headers: {
                    "Content-Type": "application/json",
                    'Authorization': `${this.token}`,
                },
            })
                .then(response => response.json())
                .then(data => {
                    this.form.text_query = data.item_1;
                })
                .catch(error => console.error(error));

        },
        exportToCSV() {
            console.log('Exporting to CSV...');
            const csvWriter = createObjectCsvWriter({
                path: 'Export.csv',
                header: [
                    { id: 'id', title: 'ID' },
                    { id: 'similarity', title: 'Similarity' },
                    { id: 'company', title: 'Company' },
                    { id: 'filing_html_index', title: 'Filing HTML Index' },
                    { id: 'item_1', title: 'Item 1' }
                ]
            });

            const csvData = this.resultList.map(item => {
                return {
                    id: item.id,
                    similarity: item.similarity,
                    company: item.object.company,
                    filing_html_index: item.object.filing_html_index,
                    item_1: item.object.item_1
                };
            });

            csvWriter.writeRecords(csvData)
                .then(() => console.log('CSV file has been written successfully'))
                .catch(error => console.error('Error while generating CSV:', error));
        },
    },
}
</script>
