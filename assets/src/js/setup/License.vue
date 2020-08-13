<template>
    <div>
        <h1 class="text-2xl mb-2 text-center border-b pb-1">License Agreement</h1>
        <div class="h-64 overflow-scroll"><nl2br tag="p" :text="license" /></div>
        <div class="text-gray-700 text-sm">
            <label class="inline-flex items-center">
                <input type="checkbox" class="form-checkbox h-4 w-4" v-model="checked" name="checked" @change="complete">
                <span class="ml-2">I accept the license terms for usage of this application</span>
            </label>
        </div>
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
    created() {
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