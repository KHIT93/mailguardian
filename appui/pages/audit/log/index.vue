<template>
    <MainLayout>
        <div class="bg-white p-4 shadow border rounded-md space-y-8 sm:space-y-5 divide-y divide-gray-200 relative pb-8">
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-white">
                    <tr>
                        <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                            Date
                        </th>
                        <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                            User
                        </th>
                        <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                            From
                        </th>
                        <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                            <span class="sr-only">View Entry</span>
                        </th>
                    </tr>
                </thead>
                <tbody class="bg-white">
                    <template v-if="loading">
                        <tr class="animate-pulse border-b" v-for="num in 20" :key="num">
                            <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700">
                                <div class="h-4 bg-gray-300 rounded"></div>
                            </td>
                            <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700">
                                <div class="h-4 bg-gray-300 rounded"></div>
                            </td>
                            <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700" colspan="2">
                                <div class="h-4 bg-gray-300 rounded"></div>
                            </td>
                        </tr>
                    </template>
                    <tr v-else-if="entries.length == 0">
                        <td class="px-6 py-2 whitespace-nowrap" colspan="99">
                            <span class="px-2 inline-flex text-xs leading-5 font-semibold">
                                No entries in the log
                            </span>
                        </td>
                    </tr>
                    <tr v-for="entry in entries" :key="entry.id" v-else class="cursor-pointer border-b transition duration-300 hover:shadow-lg hover:font-bold">
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700 truncate">
                            {{ entry.timestamp }}
                        </td>
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700 truncate">
                            {{ entry.actor_email }}
                        </td>
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700 truncate">
                            {{ entry.remote_addr }}
                        </td>
                        <td class="px-6 whitespace-nowrap text-right text-sm font-medium">
                            <NuxtLink :to="`/audit/log/${entry.id}`" class="text-blue-600 hover:text-blue-900">
                                <MagnifyingGlassIcon class="w-4 h-4"/>
                            </NuxtLink>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </MainLayout>
</template>

<script setup>
import { onMounted } from '@vue/runtime-core'
import { ref } from 'vue'
import MainLayout from '~/components/MainLayout.vue'
import { MagnifyingGlassIcon } from '@heroicons/vue/24/outline'

let entries = ref([])
let loading = ref(false)

onMounted(async () => {
    loading.value = true
    let res = (await useBackendFetch('/api/datalog/?page_size=20')).results
    entries.value = res
    loading.value = false
})
</script>