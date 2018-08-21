<template>
    <div class="text-center text-grey-darker py-6">
        <div>
            <div class="mb-2">
                <span class="text-5xl">Access Denied</span>
            </div>
            <div class="uppercase">
                Sorry mate. You are not allowed to go here.
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        mounted() {
            console.log('Access to this page has been denied.');
            this.$store.commit('setLoading', false);
        }
    }
</script>