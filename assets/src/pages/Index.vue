<template>
    <MainLayout>
        <div class="flex justify-between border-b">
            <button type="button" @click.native="messageType = ''">
                <div class="relative">
                    <template v-if="statsLoading">
                        <ProgressRing :radius="60" :progress="100" :stroke="6" class="text-cool-gray-300 animate-pulse" stroke-linecap="round"/>
                    </template>
                    <template v-else>
                        <ProgressRing :radius="60" :progress="100" :stroke="6" fillColor="currentColor" class="text-cool-gray-200" stroke-linecap="round"></ProgressRing>
                        <div class="absolute top-0 bottom-0 left-0 right-0 text-xl">
                            <div class="flex w-full h-full items-center justify-center">
                                {{ stats.daily_total }}
                            </div>
                        </div>
                    </template>
                </div>
                <span class="font-lg text-gray-700 font-bold">All Emails</span>
                <div class="px-8">
                    <div class="border-t-4 border-blue-400 rounded-t-full" v-if="!messageType"/>
                    <div class="border-t-4 border-transparent rounded-t-full" v-else/>
                </div>
            </button>
            <button type="button" @click.native="messageType = 'is_clean'">
                <div class="relative">
                    <template v-if="statsLoading">
                        <ProgressRing :radius="60" :progress="100" :stroke="6" class="text-cool-gray-100 animate-pulse" stroke-linecap="round"/>
                    </template>
                    <template v-else>
                        <ProgressRing :radius="60" :progress="((stats.daily_total - stats.daily_spam - stats.daily_virus) * stats.daily_total) * 100" :stroke="6" class="text-blue-500" stroke-linecap="round"></ProgressRing>
                        <div class="absolute top-0 bottom-0 left-0 right-0 text-xl">
                            <div class="flex w-full h-full items-center justify-center">
                                {{ stats.daily_total - stats.daily_spam - stats.daily_virus }}
                            </div>
                        </div>
                    </template>
                </div>
                <span class="font-lg text-gray-700">General</span>
                <div class="px-8">
                    <div class="border-t-4 border-blue-400 rounded-t-full" v-if="messageType == 'is_clean'"/>
                    <div class="border-t-4 border-transparent rounded-t-full" v-else/>
                </div>
            </button>
            <button type="button">
                <div class="relative">
                    <template v-if="statsLoading">
                        <ProgressRing :radius="60" :progress="100" :stroke="6" class="text-cool-gray-100 animate-pulse" stroke-linecap="round"/>
                    </template>
                    <template v-else>
                        <ProgressRing :radius="60" :progress="0" :stroke="6" class="text-green-500" stroke-linecap="round"></ProgressRing>
                        <div class="absolute top-0 bottom-0 left-0 right-0 text-xl">
                            <div class="flex w-full h-full items-center justify-center">
                                0
                            </div>
                        </div>
                    </template>
                </div>
                <span class="font-lg text-gray-700">Important</span>
                <div class="px-8">
                    <div class="border-t-4 border-blue-400 rounded-t-full" v-if="messageType == 'important'"/>
                    <div class="border-t-4 border-transparent rounded-t-full" v-else/>
                </div>
            </button>
            <button type="button">
                <div class="relative">
                    <template v-if="statsLoading">
                        <ProgressRing :radius="60" :progress="100" :stroke="6" class="text-cool-gray-100 animate-pulse" stroke-linecap="round"/>
                    </template>
                    <template v-else>
                        <ProgressRing :radius="60" :progress="0" :stroke="6" class="text-yellow-500" stroke-linecap="round"></ProgressRing>
                        <div class="absolute top-0 bottom-0 left-0 right-0 text-xl">
                            <div class="flex w-full h-full items-center justify-center">
                                0
                            </div>
                        </div>
                    </template>
                </div>
                <span class="font-lg text-gray-700">Flagged</span>
                <div class="px-8">
                    <div class="border-t-4 border-blue-400 rounded-t-full" v-if="messageType == 'flagged'"/>
                    <div class="border-t-4 border-transparent rounded-t-full" v-else/>
                </div>
            </button>
            <button type="button" @click.native="messageType = 'is_spam'">
                <div class="relative">
                    <template v-if="statsLoading">
                        <ProgressRing :radius="60" :progress="100" :stroke="6" class="text-cool-gray-100 animate-pulse" stroke-linecap="round"/>
                    </template>
                    <template v-else>
                        <ProgressRing :radius="60" :progress="(stats.daily_spam / stats.daily_total) * 100" :stroke="6" class="text-red-500" stroke-linecap="round"></ProgressRing>
                        <div class="absolute top-0 bottom-0 left-0 right-0 text-xl">
                            <div class="flex w-full h-full items-center justify-center">
                                {{ stats.daily_spam }}
                            </div>
                        </div>
                    </template>
                </div>
                <span class="font-lg text-gray-700">Spam</span>
                <div class="px-8">
                    <div class="border-t-4 border-blue-400 rounded-t-full" v-if="messageType == 'is_spam'"/>
                    <div class="border-t-4 border-transparent rounded-t-full" v-else/>
                </div>
            </button>
            <button type="button" @click.native="messageType = 'infected'">
                <div class="relative">
                    <template v-if="statsLoading">
                        <ProgressRing :radius="60" :progress="100" :stroke="6" class="text-cool-gray-100 animate-pulse" stroke-linecap="round"/>
                    </template>
                    <template v-else>
                        <ProgressRing :radius="60" :progress="(stats.daily_virus / stats.daily_total) * 100" :stroke="6" class="text-purple-500" stroke-linecap="round"></ProgressRing>
                        <div class="absolute top-0 bottom-0 left-0 right-0 text-xl">
                            <div class="flex w-full h-full items-center justify-center">
                                {{ stats.daily_virus }}
                            </div>
                        </div>
                    </template>
                </div>
                <span class="font-lg text-gray-700">Viruses</span>
                <div class="px-8">
                    <div class="border-t-4 border-blue-400 rounded-t-full" v-if="messageType == 'infected'"/>
                    <div class="border-t-4 border-transparent rounded-t-full" v-else/>
                </div>
            </button>
        </div>
        <div class="flex pt-4 items-center">
            <div class="w-1/2 text-left">
                <div class="mt-1 relative rounded-md shadow-sm">
                    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <span class="text-gray-500 sm:text-sm">
                            <SearchIcon class="w-4 h-4"/>
                        </span>
                    </div>
                    <input v-model="searchKey" id="search-key" name="search-key" type="search" class="peer placeholder-transparent transition duration-300 focus:ring-blue-500 focus:border-blue-500 block w-1/2 pl-10 pr-2 sm:text-sm border-gray-300 rounded-md" placeholder="Search by name, email or more" />
                    <label for="search-key" class="absolute flex bg-white px-1 left-2 -top-2.5 text-gray-600 text-sm transition-all duration-200 peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-400 peer-placeholder-shown:top-2 peer-placeholder-shown:left-8 sm:peer-placeholder-shown:text-sm peer-focus:-top-2.5 peer-focus:left-2 peer-focus:text-blue-500 peer-focus:text-sm peer-focus:bg-white peer-focus:px-1 peer-focus:flex peer-focus:z-50">Search by name, email or more</label>
                </div>
            </div>
            <div class="w-1/2 text-right">
                <button type="button" class="text-gray-400 hover:text-gray-600 transition duration-300" @click.native="refreshDashboard">
                    <RefreshIcon class="w-6 h-6"/>
                </button>
            </div>
        </div>
        <div class="flex flex-col pt-4">
            <div class="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
                <div class="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
                    <div class="border-b border-gray-200">
                        <table class="min-w-full divide-y divide-gray-200">
                            <thead class="bg-white">
                                <tr>
                                    <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                                        Date
                                    </th>
                                    <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                                        From
                                    </th>
                                    <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                                        To
                                    </th>
                                    <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                                        Subject
                                    </th>
                                    <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                                        Actions
                                    </th>
                                </tr>
                            </thead>
                            <tbody class="bg-white">
                                <template v-if="messagesLoading">
                                    <tr class="animate-pulse" v-for="num in 10" :key="num">
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                                            <div class="h-4 bg-cool-gray-300 rounded"></div>
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                                            <div class="h-4 bg-cool-gray-300 rounded"></div>
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                                            <div class="h-4 bg-cool-gray-300 rounded"></div>
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                                            <div class="h-4 bg-cool-gray-300 rounded"></div>
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                            <div class="h-4 bg-cool-gray-300 rounded"></div>
                                        </td>
                                    </tr>
                                </template>
                                <tr v-else-if="filteredMessages.length == 0">
                                    <td class="px-6 py-4 whitespace-nowrap" colspan="99">
                                        <span class="px-2 inline-flex text-xs leading-5 font-semibold">
                                            No messages are matching your search
                                        </span>
                                    </td>
                                </tr>
                                <tr v-for="message in filteredMessages" :key="message.id" v-else @click.native="goToMessage(message.id)" class="border-b transition duration-300 hover:shadow-lg hover:font-bold">
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                                        {{ message.date }}
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                                        {{ message.from_address }}
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                                        {{ message.to_address }}
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                                        {{ message.subject }}
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                        <a href="#" class="text-blue-600 hover:text-blue-900">Edit</a>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </MainLayout>
</template>

<script>
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import MainLayout from '../components/MainLayout.vue'
import ProgressRing from '../components/ProgressRing.vue'
import { RefreshIcon, SearchIcon } from '@heroicons/vue/outline'
export default {
    components: {
        MainLayout,
        ProgressRing,
        RefreshIcon,
        SearchIcon
    },
    setup(props) {
        const router = useRouter()
        let messagesLoading = ref(false)
        let statsLoading = ref(false)
        let messages = ref([])
        let stats = ref({})
        let searchKey = ref('')
        let messageType = ref('')
        let filteredMessages = computed(() => {
            let res = messages.value.filter(message => message.subject.toLowerCase().includes(searchKey.value.toLowerCase()) || message.to_address.toLowerCase().includes(searchKey.value.toLowerCase()) || message.from_address.toLowerCase().includes(searchKey.value.toLowerCase()))
            if (messageType) {
                if (messageType.value == 'is_clean') {
                    res = res.filter(message => message.is_clean)
                }
                else if (messageType.value == 'is_spam') {
                    res = res.filter(message => message.is_spam)
                }
                else if (messageType.value == 'infected') {
                    res = res.filter(message => message.infected)
                }
            }
            return res
        })
        let fetchMessages = (async () => {
            statsLoading.value = true
            messagesLoading.value = true
            let res = (await axios.get('/api/messages/?page_size=20')).data.results
            messagesLoading.value = false
            return res
        })
        let fetchStatistics = (async () => {
            statsLoading.value = true
            let res = (await axios.post('/api/dashboard/', {'interval' : 'daily'})).data
            statsLoading.value = false
            return res
        })
        let refreshDashboard = (async () => {
            messages.value = (await fetchMessages())
            // filteredMessages.value = messages.value
            stats.value = (await fetchStatistics())
        })
        let goToMessage = (messageId => {
            router.push({ name: 'messages.show', params: { id: messageId } })
        })
        onMounted(async () => {
            refreshDashboard()
        })
        return {
            stats,
            messages,
            statsLoading,
            messagesLoading,
            filteredMessages,
            searchKey,
            messageType,
            fetchMessages,
            fetchStatistics,
            refreshDashboard,
            goToMessage
        }
    },
}
</script>