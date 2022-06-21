<template>
    <form @submit.prevent="nextStep">
        <FormSelection input-id="method" v-model="method" label="Validation Method">
            <template v-slot:inputOptions>
                <option value="email">Email</option>
                <option value="app">App</option>
            </template>
        </FormSelection>
        <div class="pt-5">
            <div class="flex">
                <button type="submit" @click="nextStep" class="transition duration-300 ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-500 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                    Next
                </button>
            </div>
        </div>
    </form>
</template>
<script setup>
import { ref } from 'vue'
import FormSelection from '~/components/FormSelection.vue'

const emits = defineEmits(['complete'])

let method = ref('')

function nextStep() {
    emits('complete', this.method)
}
</script>