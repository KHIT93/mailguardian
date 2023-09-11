<template>
    <MainLayout>
        <Card class="z-10">
            <h2 class="prose">Active Filters</h2>
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-white">
                    <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                        Field
                    </th>
                    <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                        Operator
                    </th>
                    <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                        Value
                    </th>
                    <th></th>
                </thead>
                <tbody class="bg-white">
                    <tr class="border-bg-green-200 transition duration-300">
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700">
                            <USelectMenu class="w-full" size="md" placeholder="Select Field..." name="field" id="field" v-model="selectedFilterField" :options="store.getAvailableFilters" :disabled="loading"/>
                        </td>
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700">
                            <USelectMenu class="w-full" size="md" placeholder="Select Operator..." name="operator" id="operator" v-if="selectedFilterField" v-model="selectedFilterFieldOperator" :options="selectedFilterField.operators" :disabled="loading"/>
                        </td>
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700">
                            <UInput name="value" size="md" :type="selectedFilterField.field_type || 'text'" id="value" v-model="selectedFilterValue" v-if="selectedFilterField" :disabled="!(!!(selectedFilterField && selectedFilterFieldOperator)) || loading"/>
                        </td>
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700">
                            <button type="button" v-if="selectedFilterField" @click="addFilter" class="transition duration-300 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-500 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                                Add Filter
                            </button>
                        </td>
                    </tr>
                    <tr v-for="filter in store.getActiveFilters" :key="filter.name" class="border-b transition duration-300 hover:shadow-lg hover:font-bold">
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700">
                            {{ filter.label }}
                        </td>
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700">
                            {{ filter.operator }}
                        </td>
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700">
                            {{ filter.value }}
                        </td>
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700">
                            <TrashIcon class="h-5 w-5 text-red-700 cursor-pointer hover:text-red-900" @click="removeFilter(filter.name)" aria-hidden="true" />
                        </td>
                    </tr>
                </tbody>
            </table>
        </Card>
        <Card class="border mt-6">
            <h2 class="prose">Summary</h2>
            <table class="min-w-full divide-y divide-gray-200">
                <tbody class="bg-white">
                    <tr class="border-b">
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700">First message registered:</td>
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700 font-bold">{{ summary.earliest }}</td>
                    </tr>
                    <tr class="border-b">
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700">Last message registered:</td>
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700 font-bold">{{ summary.latest }}</td>
                    </tr>
                    <tr class="border-b">
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700">Messages registered:</td>
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700 font-bold">{{ summary.count }}</td>
                    </tr>
                </tbody>
            </table>
        </Card>
        <Card class="border mt-6">
            <h2 class="prose">All Filters</h2>
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-white">
                    <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                        Field
                    </th>
                    <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                        Label
                    </th>
                    <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                        Field Type
                    </th>
                </thead>
                <tbody class="bg-white">
                    <tr v-for="filter in store.getAllFilters" :key="filter.name" class="cursor-pointer border-b transition duration-300 hover:shadow-lg hover:font-bold">
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700">
                            {{ filter.name }}
                        </td>
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700">
                            {{ filter.label }}
                        </td>
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700">
                            {{ filter.field_type }}
                        </td>
                    </tr>
                </tbody>
            </table>
        </Card>
    </MainLayout>
</template>

<script setup>
import MainLayout from '~/components/MainLayout.vue'
import { TrashIcon } from '@heroicons/vue/24/solid'
import { useStatisticsStore } from '~/store/index'
import { ref } from 'vue'

useHead({
    title: 'MailGuardian - Statistics & Reports'
})

const store = useStatisticsStore()
const selectedFilterField = ref('')
const selectedFilterFieldOperator = ref('')
const selectedFilterValue = ref('')
const summary = ref({})
const loading = ref(false)

// const selectedFilter = computed(() =>{
//     return store.getAvailableFilters.find(filter => filter.name == selectedFilterField.name) || false
// })

function resetSelectedFilter() {
    selectedFilterField.value = null
    selectedFilterFieldOperator.value = null
    selectedFilterValue.value = null
}

async function addFilter() {
    store.setActiveFilter({
        name: selectedFilterField.value.name,
        label: selectedFilterField.value.label,
        operator: selectedFilterFieldOperator.value.value,
        value: selectedFilterValue.value
    })
    await getStatisticsSummary()
    resetSelectedFilter()
}

function removeFilter(name) {
    if (store.hasActiveFilter(name)) {
        store.removeActiveFilterByName(name)
        getStatisticsSummary()
    }
    else {
        console.error(`Unable to locate an active filter with field name ${name}`)
    }

}

async function getStatisticsSummary() {
    loading.value = true
    summary.value = (await useBackendFetch('/api/reports/summary/', {
        method: 'POST',
        body: store.getActiveFilters
    }))
    loading.value = false
}

onMounted(() => {
    store.getFiltersFromBackend()
    getStatisticsSummary()
})

</script>