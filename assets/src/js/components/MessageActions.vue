<template>
    <div class="flex flex-row-reverse py-2">
        <button role="button" @click="release" class="bg-green hover:bg-green-dark text-white py-1 px-2 border border-green-light rounded shadow text-sm no-underline ml-2">Release message</button>
        <button role="button" @click="spam" class="bg-red hover:bg-red-dark text-white py-1 px-2 border border-red-light rounded shadow text-sm no-underline ml-2">Mark as spam</button>
        <button role="button" @click="nonspam" class="bg-orange hover:bg-orange-dark text-white py-1 px-2 border border-orange-light rounded shadow text-sm no-underline ml-2">Mark as non-spam</button>
        <button role="button" @click="view" class="bg-white hover:bg-grey-lightest text-grey-darkest py-1 px-2 border border-grey-light rounded shadow text-sm no-underline ml-2">View message</button>
    </div>
</template>
<script>
export default {
    props: ['uuid'],
    methods: {
        view() {
            this.$emit('view');
        },
        release() {
            this.$emit('release');
        },
        spam() {
            this.$emit('spam');
        },
        nonspam() {
            this.$emit('nonspam');
        }
    }
}
</script>

