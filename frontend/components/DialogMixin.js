// DialogMixin.js
export default {
    methods: {
        closeDialog() {
            this.$emit('dialog-closed');
        },
        isUrl(string) {
            const urlPattern = new RegExp('^(https?:\\/\\/)?' + // protocol
                '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|' + // domain name
                '((\\d{1,3}\\.){3}\\d{1,3}))' + // OR ip (v4) address
                '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*' + // port and path
                '(\\?[;&a-z\\d%_.~+=-]*)?' + // query string
                '(\\#[-a-z\\d_]*)?$', 'i'); // fragment locator
            return !!urlPattern.test(string);
        },

        closeDialogOnEsc(event) {
            if (event.key === 'Escape') {
                if (this.showTextDialog) {
                    this.$emit('close-text-dialog');
                } else {
                    this.closeDialog();
                }
            }
        },
    },

    watch: {
        showDialog(newVal) {
            if (newVal) {
                window.addEventListener('keydown', this.closeDialogOnEsc);
            } else {
                window.removeEventListener('keydown', this.closeDialogOnEsc);
            }
        },
    },

    mounted() {
        window.addEventListener('keydown', this.closeDialogOnEsc);
    },

    beforeUnmount() {
        window.removeEventListener('keydown', this.closeDialogOnEsc);
    },
}