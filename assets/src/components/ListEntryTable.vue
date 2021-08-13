<template>
    <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-white">
            <tr>
                <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                    From
                </th>
                <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                    To
                </th>
            </tr>
        </thead>
        <tbody class="bg-white">
            <template v-if="loading">
                <tr class="animate-pulse border-b" v-for="num in 20" :key="num">
                    <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700">
                        <div class="h-4 bg-cool-gray-300 rounded"></div>
                    </td>
                    <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700">
                        <div class="h-4 bg-cool-gray-300 rounded"></div>
                    </td>
                    
                </tr>
            </template>
            <tr v-else-if="entries.length == 0">
                <td class="px-6 py-2 whitespace-nowrap" colspan="99">
                    <span class="px-2 inline-flex text-xs leading-5 font-semibold">
                        No entries are matching your search
                    </span>
                </td>
            </tr>
            <tr v-for="entry in entries" :key="entry.id" v-else class="cursor-pointer border-b transition duration-300 hover:shadow-lg hover:font-bold">
                <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700 truncate">
                    {{ entry.from_address }}
                </td>
                <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700 truncate">
                    {{ entry.to_address }}
                </td>
                <td class="px-6 whitespace-nowrap text-right text-sm font-medium">
                    <router-link :to="`/lists/${entry.id}/edit`" class="text-blue-600 hover:text-blue-900">
                        <PencilIcon class="w-4 h-4"/>
                    </router-link>
                </td>
                <td class="px-6 whitespace-nowrap text-right text-sm font-medium">
                    <router-link :to="`/lists/${entry.id}/delete`" class="text-red-600 hover:text-red-900">
                        <TrashIcon class="w-4 h-4"/>
                    </router-link>
                </td>
            </tr>
        </tbody>
    </table>
</template>

<script>
import { ref, onMounted } from 'vue'
import { PencilIcon, TrashIcon } from '@heroicons/vue/outline'
export default {
    props: ['listingType'],
    components: {
        PencilIcon,
        TrashIcon
    },
    setup(props) {
        console.log(props.listingType)
        let loading = ref(false)
        let entries = ref([])
        let fetchEntries = (async () => {
            loading.value = true
            let res = (await axios.get(`/api/${props.listingType}list/?page_size=20`)).data.results
            loading.value = false
            return res
        })
        onMounted(async () => {
            entries.value = (await fetchEntries())
        })
        return {
            loading,
            entries,
            fetchEntries
        }
    }
}
</script>