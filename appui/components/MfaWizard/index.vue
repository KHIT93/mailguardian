<template>
    <div>By following the next steps, you will be able to ewnable two-factor authentication (2FA) on your account. Press <code class="text-blue-700 bg-gray-100 p-1">Next</code> to start</div>
    <div class="pt-5">
        <div class="flex">
            <button type="button" @click="nextStep" class="transition duration-300 ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-500 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                Next
            </button>
        </div>
    </div>
</template>
<script>
export default {
    methods: {
        nextStep() {
            this.$emit('complete')
        }
    }
}
</script>