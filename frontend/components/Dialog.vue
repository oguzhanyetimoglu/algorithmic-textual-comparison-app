<script>
import TextDialog from './TextDialog.vue';
import DialogMixin from './DialogMixin.js';
export default {
    components: {
        TextDialog,
    },
    props: {
        showDialog: {
            type: Boolean,
            required: true,
        },
        title: {
            type: String,
            default: 'Dialog Title',
        },
        row: {
            type: Object,
            required: true,
        },
        tableName: {
            type: String,
            required: true,
        },
        showEdit: {
            type: Boolean,
            default: true,
        }
    },
    data() {
        return {
            config: useRuntimeConfig(),
            token: '',
            specialField: '',
            specialText: '',
            showSmallDialog: false,
            newRow: { ...this.row },
            notifications: [],
            showDeleteConfirmation: false,
        };
    },
    async created() {
        const {
            token
        } = useAuth();
        this.token = token;
    },
    methods: {
        truncateText(text, length = 100) {
            if (typeof text === 'string') {
                if (text.length > length) {
                    return text.substring(0, length) + '...';
                } else {
                    return text;
                }
            }
        },
        handleClick(key) {
            this.specialField = key;
            this.specialText = this.row[key];
            this.showSmallDialog = true;
        },
        updateText(newText) {
            this.patchTextToServer(newText);
        },

        async patchTextToServer(newText) {
            // Perform the PATCH request using your API endpoint
            let url = `${this.config.public.apiBase}/api/${this.tableName}/`;
            if (this.tableName === 'ten-k') {
                url += `${this.row['cik']}/${this.row['filing_date']}`;
            } else {
                url += `${this.row['id']}`;
            }
            const dataToSend = {
                [this.specialField]: newText,
            };
            console.log('Data to send', dataToSend);
            try {
                const response = await fetch(url, {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `${this.token}`,
                    },
                    body: JSON.stringify(dataToSend),
                });
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                // Handle success
                const data = await response.json();
                this.specialText = newText;
                this.newRow[this.specialField] = newText;

                console.log('Text updated successfully', data);
                this.$emit('row-updated', this.newRow);
            } catch (error) {
                // Handle error
                console.error('Error updating text', error);
                this.$emit('row-error', error);
            }
        },
        async deleteElement() {
            let url = `${this.config.public.apiBase}/api/${this.tableName}/`;
            if (this.tableName === 'ten-k') {
                url += `${this.row['cik']}/${this.row['filing_date']}`;
            } else {
                url += `${this.row['id']}`;
            }
            try {
                const response = await fetch(url, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `${this.token}`,
                    },
                });
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                // Handle success
                console.log('Element deleted successfully');
                this.showDeleteConfirmation = false;
                this.$emit('row-deleted');
                this.closeDialog();
            } catch (error) {
                // Handle error
                console.error('Error deleting element', error);
                this.$emit('row-delete-error', error);
            }
        }
    },

    mixins: [DialogMixin],
    emits: ['dialog-closed', 'row-updated', 'row-error', 'row-deleted', 'row-delete-error'],
};
</script>

<template>
    <div v-if="showDialog" class="fixed inset-0 flex items-center justify-center z-50" @click.self="closeDialog">
        <div class="bg-white p-4 rounded shadow-lg">
            <div class="flex justify-between items-center">
                <div class="text-xl font-bold mb-4">{{ title }}</div>
                <button @click="closeDialog" class="p-1 hover:bg-gray-200 rounded-full">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"
                        class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12">
                        </path>
                    </svg>
                </button>
            </div>
            <div v-if="showDeleteConfirmation" class="p-4 bg-red-100 border border-red-400 text-red-700 mb-4 rounded">
                Are you sure that you want to delete this element? This action is irreversible.
                <div class="mt-4">
                    <button @click="deleteElement" class="p-1 bg-red-500 text-white hover:bg-red-700 rounded mr-2">
                        Confirm
                    </button>
                    <button @click="showDeleteConfirmation = false"
                        class="p-1 bg-gray-500 text-white hover:bg-gray-700 rounded">
                        Cancel
                    </button>
                </div>
            </div>
            <div class="text-gray-800 overflow-auto h-3/4">
                <div v-for="(value, key) in newRow" :key="key" class="mb-4">
                    <p class="text-sm" @click="handleClick(key)">
                        <span class="font-bold text-lg">{{ key }}:</span>
                        <span v-if="value === null" class="ml-2"></span>
                        <span v-else-if="value.toString().length < 100" class="ml-2">
                            <a v-if="isUrl(value)" :href="value" target="_blank" @click.stop
                                class="text-blue-500 hover:underline cursor-pointer">{{ value }}</a>
                            <span v-else>{{ value }}</span>
                        </span>
                        <span v-else class="ml-2">{{ truncateText(value) }}
                        </span>
                    </p>
                </div>
            </div>
            <div class="flex justify-end mt-4">
                <button v-if="showEdit" @click="showDeleteConfirmation = true"
                    class="px-4 py-2 font-medium text-white bg-red-500 border border-transparent shadow-sm text-sm font-medium rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition duration-150 ease-in-out">
                    Delete
                </button>
            </div>
        </div>
    </div>
    <TextDialog v-if="showSmallDialog" :showDialog="showSmallDialog" :title="specialField" :text="specialText"
        :showEdit="showEdit" @dialog-closed="showSmallDialog = false" @update:text="updateText" />
</template>
