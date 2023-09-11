<template>
    <form @submit.prevent="nextStep">
        <UFormGroup label="Validation Method" size="md">
            <USelectMenu class="w-full" size="md" placeholder="Select validation method..." value-attribute="value" v-model="method" name="method" id="method" :options="validationMethods">
                <template #label>{{ selectedMethod.label }}</template>
            </USelectMenu>
        </UFormGroup>
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

const emits = defineEmits(['complete'])

const validationMethods = [
    { value: "email", label: "Email" },
    { value: "app", label: "Mobile App" }
]
const selectedMethod = computed(() => validationMethods.find(validationMethod => validationMethod.value == method) || {value: '', label: '-- Select --'})

let method = ref('')

function nextStep() {
    emits('complete', method)
}
</script>