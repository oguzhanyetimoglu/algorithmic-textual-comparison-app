<script setup lang="ts">
import { nextTick, onBeforeMount } from 'vue';

interface TableData {
    id: number;
    rows: {
        results: any[];
    };
}

interface Tables {
    [key: string]: TableData;
}
const config = useRuntimeConfig();
const token = ref<string>("");
const { token: authDataToken } = useAuth();
const searchTerm = ref("");
const tableNames = ["ten-k", "sic-codes", "naics-codes"];
const showNotification = ref(false);
const notificationText = ref("");
const notificationType = ref("");
const fieldsWithoutItems = [
    'id',
    'is_active',
    'cik',
    'trading_symbol',
    'company',
    'exchange',
    'filing_date',
    'currency',
    'filing_type',
    'period_of_report',
    'sic',
    'state_of_inc',
    'content',
    'state_location',
    'fiscal_year_end',
    'filing_html_index',
    'htm_filing_link',
    'complete_text_filing_link',
    'filename'
]
const tables = reactive(
    tableNames.reduce((acc, tableName, index) => {
        acc[tableName] = { id: index + 1, rows: { results: [] } };
        return acc;
    }, {} as Tables)
);

const state = reactive({
    table: "" as keyof Tables,
    loading: false,
});

function setTableRows(tableName: keyof Tables, rows: any) {
    const table = tables[tableName];
    if (table) {
        table.rows = rows;
    }
}

const openTable = async function (name: keyof typeof tables) {
    state.loading = true;
    let url = `${config.public.apiBase}/api/${name}/`;
    if (name === 'ten-k') {
        url += `?fields=${fieldsWithoutItems.join(',')}`;
    }
    try {
        const { data, pending, error, refresh } = await useAsyncData("table", () =>
            $fetch(url)
        );
        setTableRows(name, data);
        state["table"] = name;
    } catch (error) {
        console.error(error);
    } finally {
        nextTick(() => {
            state.loading = false;
        });
    }

};

const searchTable = async function (name: keyof typeof tables, searchTerm: string) {
    state.loading = true;
    let url = `${config.public.apiBase}/api/${name}/?search=${encodeURIComponent(searchTerm)}`;
    if (name === 'ten-k') {
        url += `&fields=${fieldsWithoutItems.join(',')}`;
    }
    try {
        const { data, pending, error, refresh } = await useAsyncData("table", () =>
            $fetch(url)
        );
        setTableRows(name, data);
        state["table"] = name;
    } catch (error) {
        console.error(error);
    } finally {
        nextTick(() => {
            state.loading = false;
        });
    }
};

const addEntry = async function (tableName: string, entry: any) {
    state.loading = true;
    let url = `${config.public.apiBase}/api/${tableName}/`;
    try {
        const response = await fetch(url, {
            headers: {
                'Authorization': `${token}`,
                'Content-Type': 'application/json'
            },
            method: 'POST',
            body: JSON.stringify(entry)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        console.log(response);
    } catch (error) {
        console.error(error);
        throw error; // re-throw the error so it can be caught by the calling code
    }
};

const selectedTable = ref('ten-k');

function updateDictionary(rows: any) {
    tables[state['table']].rows = rows;
    console.log("updateDictionary", rows);
}

function importData(tableName: string) {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.json';
    fileInput.multiple = true; // Allow multiple files

    fileInput.addEventListener('change', async (event) => {
        const files = (event.target as HTMLInputElement).files;
        if (files && files.length > 0) {
            for (let i = 0; i < files.length; i++) { // Loop over the selected files
                const file = files[i];
                const reader = new FileReader();
                reader.onload = async (e) => {
                    try {
                        const jsonData = JSON.parse((e.target?.result as string) || "");
                        await addEntry(tableName, jsonData);

                        showNotification.value = true;
                        notificationText.value = `Data imported successfully to ${tableName}`;
                        notificationType.value = "success";

                    } catch (error) {
                        console.error('Error:', error);
                        showNotification.value = true;
                        notificationText.value = `Error importing data to ${tableName}`;
                        notificationType.value = "danger";
                    }
                };

                reader.readAsText(file);
            }
        }
    });

    fileInput.click();
}

onBeforeMount(() => {
    if (authDataToken) {
        token.value = String(authDataToken);
    }
});
</script>

<template>
    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
        <div class="px-4 py-5 sm:px-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900">
                Database Management
            </h3>
        </div>
        <div class="border-t border-gray-200">

            <div class="flex items-end justify-between space-x-4 m-6">
                <div>
                    <label for="selectedTable" class="block text-sm font-medium text-gray-700">Select a Table:</label>
                    <select v-model="selectedTable" id="selectedTable"
                        class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                        <option v-for="(table, name) in tables" :key="table.id" :value="name"
                            :selected="name === selectedTable">
                            {{ name }}
                        </option>
                    </select>
                </div>
                <div>
                    <label for="searchTerm" class="block text-sm font-medium text-gray-700">Search:</label>
                    <input v-model="searchTerm" id="searchTerm" type="text" placeholder="Start typing..."
                        class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                </div>
                <div>
                    <button @click="searchTable(selectedTable, searchTerm)"
                        class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50">
                        Run
                    </button>
                </div>
                <div>
                    <button @click="importData(selectedTable)"
                        class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-green-500 hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
                        Import data ({{ selectedTable }})
                    </button>
                </div>

            </div>
            <div>
                <ul class="border border-gray-200 rounded-md divide-y divide-gray-200">

                    <template v-if="state['table'] !== '' && !state.loading">
                        <Table v-if="tables[state['table']].rows && tables[state['table']].rows.results.length > 0"
                            :dictionary="tables[state['table']].rows" :tableName="state['table'].toString()"
                            :fields="fieldsWithoutItems" :searchTerm="searchTerm" @update:rows="updateDictionary" />
                        <div v-else class="p-4 text-center text-gray-500">No elements in the table yet.</div>
                    </template>
                </ul>
            </div>
        </div>
    </div>
    <Notification v-if="showNotification" :text="notificationText" :type="notificationType"
        @close="showNotification = false" />
</template>
