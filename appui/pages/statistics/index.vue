<template>
    <MainLayout>
        <Card>
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
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700 truncate">
                            <FormSelection name="field" inputId="field" v-model="selectedFilterField">
                                <template v-slot:inputOptions>
                                    <option v-for="filter in store.getAvailableFilters" :key="filter.name" :value="filter.name">
                                        {{ filter.label }}
                                    </option>
                                </template>
                            </FormSelection>
                        </td>
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700 truncate">
                            <FormSelection name="operator" inputId="operator" :disabled="!(!!selectedFilter)" v-model="selectedFilterFieldOperator">
                                <template v-slot:inputOptions>
                                    <option v-for="option in selectedFilter.operators" :key="option.value" :value="option.value" v-if="selectedFilter">
                                        {{ option.label }}
                                    </option>
                                </template>
                            </FormSelection>
                        </td>
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700 truncate">
                            <FormInput name="value" :type="selectedFilter.field_type || 'text'" inputId="value" v-model="selectedFilterValue" v-if="selectedFilter" :disabled="!(!!(selectedFilter && selectedFilterFieldOperator))"/>
                        </td>
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700 truncate">
                            <button type="button" @click="addFilter" class="transition duration-300 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-500 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                                Add Filter
                            </button>
                        </td>
                    </tr>
                    <tr v-for="filter in store.getActiveFilters" :key="filter.name" class="border-b transition duration-300 hover:shadow-lg hover:font-bold">
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700 truncate">
                            {{ filter.label }}
                        </td>
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700 truncate">
                            {{ filter.operator }}
                        </td>
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700 truncate">
                            {{ filter.value }}
                        </td>
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700 truncate">
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
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700 truncate">First message registered:</td>
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700 truncate font-bold">{{ summary.earliest }}</td>
                    </tr>
                    <tr class="border-b">
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700 truncate">Last message registered:</td>
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700 truncate font-bold">{{ summary.latest }}</td>
                    </tr>
                    <tr class="border-b">
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700 truncate">Messages registered:</td>
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700 truncate font-bold">{{ summary.count }}</td>
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
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700 truncate">
                            {{ filter.name }}
                        </td>
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700 truncate">
                            {{ filter.label }}
                        </td>
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700 truncate">
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
import FormInput from '~/components/FormInput.vue'
import FormSelection from '~/components/FormSelection.vue'
import { TrashIcon } from '@heroicons/vue/24/solid'
import { useStatisticsStore } from '~/store/index'
import { ref } from 'vue'

const store = useStatisticsStore()
const selectedFilterField = ref('')
const selectedFilterFieldOperator = ref('')
const selectedFilterValue = ref('')
const summary = ref({})

const selectedFilter = computed(() =>{
    return store.getAvailableFilters.find(filter => filter.name == selectedFilterField.value) || false
})

function resetSelectedFilter() {
    selectedFilterField.value = null
    selectedFilterFieldOperator.value = null
    selectedFilterValue.value = null
}

function addFilter() {
    store.setActiveFilter({
        name: selectedFilter.value.name,
        label: selectedFilter.value.label,
        operator: selectedFilterFieldOperator.value,
        value: selectedFilterValue.value
    })
    resetSelectedFilter()
    getStatisticsSummary()
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
    summary.value = (await useBackendFetch('/api/reports/summary/', {
        method: 'POST',
        body: store.getActiveFilters
    }))
}

onMounted(() => {
    store.getFiltersFromBackend()
    getStatisticsSummary()
})

</script>