<template>
    <div>
        <h1 class="text-2xl mb-2 text-center border-b pb-1">License Agreement</h1>
        <div class="h-64 overflow-scroll"><nl2br tag="p" :text="license" /></div>
        <label class="md:w-2/3 block font-bold">
            <input class="mr-2" type="checkbox" v-model="checked" @change="complete">
            <span class="text-sm">
                I accept the license terms for usage of this application
            </span>
        </label>
    </div>
</template>

<script>
export default {
    data: () => {
        return {
            license: "",
            checked: false
        }
    },
    mounted() {
        axios.get('/api/license/').then(response => this.license = response.data).catch(error => this.license = error.response.data)
    },
    methods: {
        complete() {
            this.$emit('complete', { completed:this.checked, action: 'manual' });
        },
        error() {
            this.$emit('error');
        }
    }
}
</script>