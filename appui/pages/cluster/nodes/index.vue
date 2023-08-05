<template>
    <MainLayout>
        <div class="bg-white p-4 shadow border rounded-md space-y-8 sm:space-y-5 divide-y divide-gray-200 relative pb-8">
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-white">
                    <tr>
                        <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                            Hostname
                        </th>
                        <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                            IP Address
                        </th>
                        <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                            Priority
                        </th>
                        <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                            Use TLS
                        </th>
                        <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                            <span class="sr-only">Edit</span>
                        </th>
                        <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                            <span class="sr-only">Delete</span>
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
                            <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700">
                                <div class="h-4 bg-gray-300 rounded"></div>
                            </td>
                            <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700">
                                <div class="h-4 bg-gray-300 rounded"></div>
                            </td>
                        </tr>
                    </template>
                    <tr v-else-if="filteredEntries.length == 0">
                        <td class="px-6 py-2 whitespace-nowrap" colspan="99">
                            <span class="px-2 inline-flex text-xs leading-5 font-semibold">
                                No entries are matching your search
                            </span>
                        </td>
                    </tr>
                    <tr v-for="node in filteredEntries" :key="node.id" v-else class="cursor-pointer border-b transition duration-300 hover:shadow-lg hover:font-bold">
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700 truncate">
                            {{ node.hostname }}
                        </td>
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700 truncate">
                            {{ node.ip_address }}
                        </td>
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700 truncate">
                            {{ node.priority }}
                        </td>
                        <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700 truncate">
                            {{ boolToHuman(node.use_tls) }}
                        </td>
                        <td class="px-6 whitespace-nowrap text-right text-sm font-medium">
                            <NuxtLink :to="`/cluster/nodes/${node.id}/edit`" class="text-blue-600 hover:text-blue-900">
                                <PencilIcon class="w-4 h-4"/>
                            </NuxtLink>
                        </td>
                        <td class="px-6 whitespace-nowrap text-right text-sm font-medium">
                            <NuxtLink :to="`/cluster/nodes/${node.id}/delete`" class="text-red-600 hover:text-red-900">
                                <TrashIcon class="w-4 h-4"/>
                            </NuxtLink>
                        </td>
                    </tr>
                </tbody>
            </table>
            <NuxtLink to="/cluster/nodes/create" class="absolute right-4 -bottom-5 inline-flex items-center p-2 border border-transparent rounded-full shadow hover:shadow-lg transition-all duration-300 text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                <PlusSmallIcon class="h-6 w-6" aria-hidden="true" />
            </NuxtLink>
        </div>
    </MainLayout>
</template>

<script setup>
import MainLayout from '~/components/MainLayout.vue'
import { ref, onMounted, computed } from 'vue'
import { PencilIcon, TrashIcon, PlusSmallIcon } from '@heroicons/vue/24/outline'
import { boolToHuman } from '~/filters'

useHead({
    title: 'MailGuardian - Manage Cluster Nodes'
})

let loading = ref(false)
let entries = ref([])
let searchKey = ref('')
async function fetchEntries() {
    loading.value = true
    let res = (await useBackendFetch(`/api/hosts/?page_size=20`)).results
    loading.value = false
    return res
}
let filteredEntries = computed(() => {
    let res = entries.value.filter(entry => entry.hostname.toLowerCase().includes(searchKey.value.toLowerCase()))
    return res
})
onMounted(async () => {
    entries.value = (await fetchEntries())
})
</script>