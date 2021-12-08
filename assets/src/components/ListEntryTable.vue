<template>
    <div class="bg-white relative pb-8">
        <div class="w-1/2 text-left bg-white">
                <div class="relative transition duration-300 border border-gray-300 rounded-md px-3 py-2 shadow-sm focus-within:ring-1 focus-within:ring-blue-600 focus-within:border-blue-600">
                    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <span class="text-gray-500 sm:text-sm">
                            <SearchIcon class="w-4 h-4"/>
                        </span>
                    </div>
                    <!-- <label for="search-key" class="absolute -top-2 left-2 -mt-px inline-block px-1 bg-white text-xs font-base text-gray-900">Search by name, email or more</label> -->
                    <input v-model="searchKey" id="search-key" name="search-key" type="search" class="block w-full border-0 pl-6 p-0 text-gray-900 placeholder-gray-500 focus:ring-0 sm:text-sm" placeholder="Search by name, email or more" />
                </div>
            </div>
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
                <tr v-else-if="filteredEntries.length == 0">
                    <td class="px-6 py-2 whitespace-nowrap" colspan="99">
                        <span class="px-2 inline-flex text-xs leading-5 font-semibold">
                            No entries are matching your search
                        </span>
                    </td>
                </tr>
                <tr v-for="entry in filteredEntries" :key="entry.id" v-else class="cursor-pointer border-b transition duration-300 hover:shadow-lg hover:font-bold">
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
        <router-link to="/domains/create" class="absolute right-4 -bottom-8 inline-flex items-center p-2 border border-transparent rounded-full shadow hover:shadow-lg transition-all duration-300 text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
            <PlusSmIcon class="h-6 w-6" aria-hidden="true" />
        </router-link>
    </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { PencilIcon, TrashIcon, SearchIcon, PlusSmIcon } from '@heroicons/vue/outline'
export default {
    props: ['listingType'],
    components: {
        PencilIcon,
        TrashIcon,
        SearchIcon,
        PlusSmIcon
    },
    setup(props) {
        console.log(props.listingType)
        let loading = ref(false)
        let entries = ref([])
        let searchKey = ref('')
        let fetchEntries = (async () => {
            loading.value = true
            let res = (await axios.get(`/api/${props.listingType}list/?page_size=20`)).data.results
            loading.value = false
            return res
        })
        let filteredEntries = computed(() => {
            let res = entries.value.filter(entry => entry.from_address.toLowerCase().includes(searchKey.value.toLowerCase()) || entry.from_domain.toLowerCase().includes(searchKey.value.toLowerCase()) || entry.to_address.toLowerCase().includes(searchKey.value.toLowerCase()) || entry.to_domain.toLowerCase().includes(searchKey.value.toLowerCase()))
            return res
        })
        onMounted(async () => {
            entries.value = (await fetchEntries())
        })
        return {
            loading,
            entries,
            searchKey,
            fetchEntries,
            filteredEntries
        }
    }
}
</script>