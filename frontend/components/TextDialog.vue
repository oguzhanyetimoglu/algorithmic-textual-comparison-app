<template>
    <div v-if="showDialog" class="fixed inset-0 flex items-center justify-center z-50" @click.self="closeDialog">
        <div class="bg-white p-4 rounded shadow-lg" style="max-height: 80vh; min-width: 15vw;">
            <div class="flex justify-between items-center">
                <div class="text-lg font-bold mb-4 flex items-center"> <!-- Modified line -->
                    <div>
                        {{ title }}
                    </div>
                </div>
                <button @click="closeDialog" class="p-1 mb-5 hover:bg-gray-200 rounded-full">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"
                        class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12">
                        </path>
                    </svg>
                </button>
            </div>
            <div class="text-gray-800 overflow-y-auto ml-2 mr-2" :class="{ 'edit-mode': editMode }"
                style="max-height: 60vh;">
                <a v-if="isUrl(text) && !editMode" :href="text" target="_blank" @click.stop
                    class="text-blue-500 hover:underline cursor-pointer">{{ text }}</a>
                <span v-else-if="!editMode" ref="editable">{{ text }}</span>
                <div v-if="editMode" class="flex items-start mt-2 ml-2">
                    <div ref="editable" contenteditable="true" class="w-full p-2 border border-gray-300 rounded"
                        @input="updateText">{{ text }}</div>
                </div>
            </div>
            <div class="flex items-center justify-end mr-2">
                <button v-if="!editMode && showEdit" @click="editMode = !editMode"
                    class="mt-4 px-4 py-1 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">Edit</button>
                <button v-if="editMode && showEdit" @click="doneEditing"
                    class="mt-4 px-4 py-1 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-green-500 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">Done</button>
            </div>
        </div>
    </div>
</template>
<script>
import DialogMixin from './DialogMixin.js';
export default {
    props: ['showDialog', 'title', 'text', 'showEdit'],
    mixins: [DialogMixin],
    emits: ['dialog-closed', 'update:text'],
    data() {
        return {
            editMode: false,
            localText: this.text,
        }
    },

    methods: {
        updateText() {
            this.localText = event.target.innerText;
        },
        calculateRows(text) {
            // Adjust this logic based on your needs
            const lineBreaks = (text.match(/\n/g) || []).length;
            return Math.max(3, lineBreaks + 1); // Minimum of 3 rows
        },
        doneEditing() {
            this.$emit('update:text', this.localText);
            console.log('Done editing', this.localText);
            this.editMode = false;
        },
    }
};
</script>