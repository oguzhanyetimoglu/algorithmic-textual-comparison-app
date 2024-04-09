<script>
import Dialog from './Dialog.vue';

export default {
    props: {
        dictionary: {
            type: Object,
            required: true
        },
        tableName: {
            type: String,
            required: true
        },
        fields: {
            type: Array,
            default: () => []
        },
        searchTerm: {
            type: String,
            default: ""
        }
    },
    emits: ['update:rows'],
    components: {
        Dialog
    },
    data() {
        return {
            config: useRuntimeConfig(),
            token: '',
            currentPage: ref(1),
            itemsPerPage: 10,
            showDialog: false,
            dialogTitle: "Dialog Title",
            dialogRow: null,
            localDictionary: this.dictionary,
            notificationText: "",
            notificationType: "",
            showNotification: false,
            showEdit: true,
        };
    },
    async created() {
        const {
            token
        } = useAuth();
        this.token = token;
    },
    computed: {
        keys() {
            return Object.keys(this.localDictionary["results"][0]);
        },
        rows() {
            return this.localDictionary["results"];
        },
        totalPages() {
            return Math.ceil(this.localDictionary["count"] / this.itemsPerPage);
        },

        getFilteredPages() {
            const startPage = Math.max(this.currentPage - 2, 1);
            const endPage = Math.min(this.currentPage + 2, this.totalPages - 1);
            const filteredPages = [];

            for (let i = startPage; i <= endPage; i++) {
                filteredPages.push(i);
            }

            // If the last page is not already included, add it
            if (!filteredPages.includes(this.totalPages)) {
                // Add a separator (null) if the last page is not the next one
                if (this.totalPages - endPage > 2) {
                    filteredPages.push(null);
                }
                else if (this.totalPages - endPage === 2) {
                    filteredPages.push(this.totalPages - 1);
                }
                filteredPages.push(this.totalPages);
            }

            return filteredPages;

        },
        isCurrentPage() {
            return (page) => this.currentPage === page;
        },

    },
    methods: {
        async goToPage(page, tableName, fields, searchTerm) {
            console.log('Go to page', page);
            let url = `${this.config.public.apiBase}/api/${tableName}/`;
            let anyFieldAdded = false;
            if (searchTerm) {
                url += `?search=${encodeURIComponent(searchTerm)}`;
                anyFieldAdded = true;
            }
            if (tableName === 'ten-k') {
                if (anyFieldAdded) {
                    url += `&fields=${fields.join(',')}`;
                } else {
                    url += `?fields=${fields.join(',')}`;
                    anyFieldAdded = true;
                }
            }
            if (anyFieldAdded) {
                url += `&page=${page}`;
            } else {
                url += `?page=${page}`;
            }
            const response = await fetch(url, {
                headers: {
                    'Authorization': `${this.token}`,
                },
            });
            const data = await response.json();
            this.currentPage = page;
            this.localDictionary = data;
            await this.$nextTick();
        },
        async prevPage() {
            if (this.localDictionary["previous"]) {
                const response = await fetch(`${this.localDictionary["previous"]}`, {
                    headers: {
                        'Authorization': `${this.token}`,
                    },
                });
                const data = await response.json();
                this.currentPage--;
                console.log(this.currentPage);
                this.localDictionary = data;
                console.log(this.localDictionary);
            }
        },
        async nextPage() {
            if (this.localDictionary["next"]) {
                const response = await fetch(`${this.localDictionary["next"]}`, {
                    headers: {
                        'Authorization': `${this.token}`,
                    },
                });
                const data = await response.json();
                this.currentPage++;
                this.localDictionary = data;
            }
        },
        async openDialog(row) {
            this.dialogTitle = row.company;
            this.dialogRow = row;
            console.log('Opening dialog', row)

            let url = `${this.config.public.apiBase}/api/${this.tableName}/`;
            if (this.tableName === 'ten-k') {
                url += row.cik.toString() + '/' + row.filing_date.toString();
            } else {
                url += row.id.toString();
            }
            try {

                const response = await fetch(url, {
                    headers: {
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
        async fetchTableData() {
            let page = 1;
            let tableData = [];
            while (true) {
                let url = `${this.config.public.apiBase}/api/${this.tableName}/?limit=10&page=${page}&search=${encodeURIComponent(this.searchTerm)}`;
                try {
                    const response = await fetch(url, {
                        headers: {
                            'Authorization': `${this.token}`,
                        },
                    });
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    let data = await response.json();
                    if (data.length === 0) {
                        // No more data, break the loop
                        break;
                    }
                    tableData = tableData.concat(data);
                    page++;
                } catch (error) {
                    console.error(error);
                    break;
                }
            }
            return tableData;
        },
        async exportToCSV() {
            let tableData = await this.fetchTableData();
            let results = tableData.flatMap(item => item.results);
            results = results.map(item => {
                for (let key in item) {
                    if (typeof item[key] === 'string' && item[key].length > 32767) {
                        item[key] = item[key].substring(0, 32767);
                    }
                }
                return item;
            });

            const csvContent = "data:text/csv;charset=utf-8," + this.convertToCSV(results);
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "Export.csv");
            document.body.appendChild(link);
            link.click();
        },
        convertToCSV(data) {
            const header = Object.keys(data[0]).join(",");
            const rows = data.map(item => Object.values(item).join(","));
            return header + "\n" + rows.join("\n");
        },
        handleDialogClosed() {
            console.log('Dialog closed');
            this.showDialog = false;
        },
        handleRowUpdated(newRow) {
            console.log(newRow);
            this.dialogRow = newRow;
            console.log(this.localDictionary["results"]);
            this.localDictionary["results"].forEach((row, index) => {
                if (this.tableName === "ten-k" && (row.cik === newRow.cik || row.filing_date === newRow.filing_date)) {
                    Object.keys(this.localDictionary["results"][index]).forEach(key => {
                        if (newRow.hasOwnProperty(key)) {
                            this.localDictionary["results"][index][key] = newRow[key];
                        }
                    });
                }
                else if (this.tableName !== "ten-k" && row.id === newRow.id) {
                    Object.keys(this.localDictionary["results"][index]).forEach(key => {
                        if (newRow.hasOwnProperty(key)) {
                            this.localDictionary["results"][index][key] = newRow[key];
                        }
                    });
                }
            });
            console.log(this.localDictionary["results"]);
            this.$emit('update:rows', this.localDictionary);
            this.notificationText = "Row updated";
            this.notificationType = "success";
            this.showNotification = true;
        },
        handleRowError(error) {
            console.error(error);
            this.notificationText = "Error updating row";
            this.notificationType = "danger";
            this.showNotification = true;
        },
        async handleRowDeleted() {
            console.log('Row deleted');
            this.localDictionary["results"] = this.localDictionary["results"].filter(row => {
                if (this.tableName === "ten-k") {
                    return row.cik !== this.dialogRow.cik && row.filing_date !== this.dialogRow.filing_date;
                }
                return row.id !== this.dialogRow.id;
            });
            console.log(this.localDictionary);
            this.localDictionary["count"] = this.localDictionary["count"] - 1;
            if (this.localDictionary["results"].length === 0 && this.currentPage > 1) {
                await this.prevPage();
            }
            console.log(this.localDictionary);
            this.$emit('update:rows', this.localDictionary);
            this.notificationText = "Row deleted";
            this.notificationType = "success";
            this.showNotification = true;
        },
        handleRowDeleteError(error) {
            console.error(error);
            this.notificationText = "Error deleting row";
            this.notificationType = "danger";
            this.showNotification = true;
        }
    },
};
</script>

<template>
    <div class="relative overflow-x-auto">

        <table v-if="rows && rows.length > 0"
            class="min-w-full divide-y divide-gray-200 shadow-sm rounded-lg overflow-hidden">
            <thead class="bg-gray-50">
                <tr>
                    <th scope="col"
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        {{ keys[0] }}
                    </th>
                    <th scope="col" v-for="(key, index) in keys.slice(1)" :key="index"
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        {{ key }}
                    </th>
                </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="(row, index) in rows" :key="index" @click="openDialog(row)">
                    <td class="px-6 py-4 whitespace-nowrap">{{ row[keys[0]] }}</td>
                    <td class="px-6 py-4 whitespace-nowrap" v-for="(key, index) in keys.slice(1)" :key="index">
                        {{ row[key] }}
                    </td>
                </tr>
            </tbody>
        </table>
        <Dialog v-if="showDialog" :showDialog="showDialog" :title="dialogTitle" :row="dialogRow" :tableName="tableName"
            :showEdit="showEdit" @row-updated="handleRowUpdated" @dialog-closed="handleDialogClosed"
            @row-error="handleRowError" @row-deleted="handleRowDeleted" @row-delete-error="handleRowDeleteError" />

        <div class="flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3 sm:px-6">
            <div class="flex flex-1 justify-between sm:hidden">
                <a href="#"
                    class="relative inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50">Previous</a>
                <a href="#"
                    class="relative ml-3 inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50">Next</a>
            </div>
        </div>
    </div>
    <div>

        <div class="flex justify-between items-center p-6">
            <button @click="exportToCSV"
                class="px-4 py-2 flex items-center justify-center border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
                Export to Excel
            </button>
            <div class="flex items-center justify-between">
                <p class="text-sm text-gray-700">
                    Showing
                    <span class="font-medium">{{ (this.currentPage - 1) * this.itemsPerPage + 1 }}</span>
                    to
                    <span class="font-medium">{{ Math.min(this.localDictionary["count"], this.currentPage *
            this.itemsPerPage) }}</span>
                    of
                    <span class="font-medium">{{ this.localDictionary["count"] }}</span>
                    results
                </p>
            </div>
            <nav class="flex items-center justify-between" aria-label="Pagination">
                <button :disabled="!localDictionary['previous']" @click="prevPage"
                    class="px-4 py-2 text-black ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0">
                    Prev
                </button>
                <button v-for="page in getFilteredPages" :key="page"
                    @click="page !== null && goToPage(page, tableName, fields, searchTerm)" :class="{
            'px-4 py-2 text-white bg-indigo-600 focus:z-20 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600': isCurrentPage(page),
            'px-4 py-2 text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0': !isCurrentPage(page)
        }">
                    {{ page !== null ? page : '...' }}
                </button>
                <button :disabled="!localDictionary['next']" @click="nextPage"
                    class="px-4 py-2 text-black ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0">
                    Next
                </button>
            </nav>
        </div>
    </div>
    <Notification v-if="showNotification" :text="notificationText" :type="notificationType"
        @close="showNotification = false" />
</template>