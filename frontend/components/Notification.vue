<template>
    <div :id="toastId"
        :class="['fixed bottom-0 left-0 flex items-center w-full max-w-xs p-4 m-8 rounded-lg shadow hover:brightness-90', bgColorClass, { 'opacity-0': isFading }, 'transition-all duration-500 ease-out']"
        role="alert" style="z-index: 9999;" @mouseover="clearTimeout" @mouseleave="startTimeout">
        <div :class="['inline-flex items-center justify-center flex-shrink-0 w-8 h-8', iconColorClass, iconBgColorClass]"
            :aria-label="iconLabel">
            <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor"
                viewBox="0 0 20 20">
                <path :d="iconPath" />
            </svg>
            <span class="sr-only">{{ iconLabel }}</span>
        </div>
        <div class="ms-3 text-sm font-normal">{{ text }}</div>
        <button type="button"
            class="ms-auto -mx-1.5 -my-1.5 bg-white text-gray-400 hover:text-gray-900 rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-100 inline-flex items-center justify-center h-8 w-8"
            :data-dismiss-target="toastId" aria-label="Close" @click="$emit('close')">
            <span class="sr-only">Close</span>
            <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
            </svg>
        </button>
    </div>
</template>

<script>
export default {
    props: {
        text: {
            type: String,
            required: true
        },
        type: {
            type: String,
            required: true
        },
    },
    data() {
        return {
            isFading: false,
            timeoutId: null

        };
    },
    computed: {
        toastId() {
            return 'toast - ' + this._uid;
        },
        iconColorClass() {
            switch (this.type) {
                case 'success':
                    return 'text-green-500';
                case 'danger':
                    return 'text-red-500';
                case 'warning':
                    return 'text-orange-500';
                default:
                    return '';
            }
        },
        iconBgColorClass() {
            switch (this.type) {
                case 'success':
                    return 'bg-green-100';
                case 'danger':
                    return 'bg-red-100';
                case 'warning':
                    return 'bg-orange-100';
                default:
                    return '';
            }
        },
        iconLabel() {
            switch (this.type) {
                case 'success':
                    return 'Check icon';
                case 'danger':
                    return 'Error icon';
                case 'warning':
                    return 'Warning icon';
                default:
                    return '';
            }
        },
        iconPath() {
            switch (this.type) {
                case 'success':
                    return 'M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z';
                case 'danger':
                    return 'M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM10 15a1 1 0 1 1 0-2 1 1 0 0 1 0 2Zm1-4a1 1 0 0 1-2 0V6a1 1 0 0 1 2 0v5Z';
                case 'warning':
                    return 'M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM10 15a1 1 0 1 1 0-2 1 1 0 0 1 0 2Zm1-4a1 1 0 0 1-2 0V6a1 1 0 0 1 2 0v5Z';
                default:
                    return '';
            }
        },
        bgColorClass() {
            switch (this.type) {
                case 'success':
                    return 'bg-green-100';
                case 'danger':
                    return 'bg-red-100';
                case 'warning':
                    return 'bg-yellow-100';
                default:
                    return 'bg-white';
            }
        }
    },
    mounted() {
        this.startTimeout();
    },
    methods: {
        startTimeout() {
            this.timeoutId = setTimeout(() => {
                this.isFading = true;
                setTimeout(() => {
                    this.$emit('close');
                }, 500);
            }, 4500);
        },
        clearTimeout() {
            clearTimeout(this.timeoutId);
        }
    },
    emits: ['close'],
};
</script>