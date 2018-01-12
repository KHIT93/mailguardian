<template>
    <div class="border px-4 py-3 rounded relative" :class="alertClasses" role="alert" v-if="show">
        <strong class="font-bold"><slot name="title">{{alertType}}</slot></strong>
        <span class="block sm:inline"><slot></slot></span>
        <span v-if="closable" @click="show = false" class="absolute pin-t pin-b pin-r px-4 py-3">
            <svg class="fill-current h-4 w-4" role="button" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><title>Close</title><path d="M14.348 14.849a1.2 1.2 0 0 1-1.697 0L10 11.819l-2.651 3.029a1.2 1.2 0 1 1-1.697-1.697l2.758-3.15-2.759-3.152a1.2 1.2 0 1 1 1.697-1.697L10 8.183l2.651-3.031a1.2 1.2 0 1 1 1.697 1.697l-2.758 3.152 2.758 3.15a1.2 1.2 0 0 1 0 1.698z"/></svg>
        </span>
    </div>
</template>
<script>
export default {
    props: {
        closable: Boolean,
        alertType: {
            type: String,
            required: true
        }
    },
    data: () => {
        return {
            show: true
        }
    },
    computed: {
        alertClasses: () => {
            let classes = 'bg-grey-lightest border-grey-light text-grey-dark';
            if (this.alertType == "info") {
                console.info("Info message");
                classes = 'bg-blue-lightest border-blue-light text-blue-dark';
            }
            if (this.alertType == "success") {
                console.log("Success message");
                classes = 'bg-green-lightest border-green-light text-green-dark';
            }
            if (this.alertType == "warning") {
                console.warn("Warning message");
                classes = 'bg-orange-lightest border-orange-light text-orange-dark';
            }
            if (this.alertType == "error") {
                console.error("Error message");
                classes = 'bg-red-lightest border-red-light text-red-dark';
            }
            return classes;
        }
    },
    methods: {

    },
}
</script>

