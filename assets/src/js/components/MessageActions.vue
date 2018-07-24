<template>
    <div class="flex flex-row-reverse py-2">
        <button role="button" @click="release" class="btn btn-sm btn-green shadow ml-2">Release message</button>
        <button role="button" @click="spam" class="btn btn-sm btn-red shadow ml-2">Mark as spam</button>
        <button role="button" @click="nonspam" class="btn btn-sm btn-orange shadow ml-2">Mark as non-spam</button>
        <button role="button" @click="view" class="btn btn-sm btn-white shadow ml-2">View message</button>
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

