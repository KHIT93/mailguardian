<template>
    <MainLayout>
        <div class="flex w-full pb-4">
            <NuxtLink to="/" class="rounded-full hover:bg-gray-200 p-4 cursor-pointer transition duration-200"><ArrowLeftIcon class="w-4 h-4"/></NuxtLink>
        </div>
        <div class="bg-white shadow overflow-hidden sm:rounded-lg">
            <div class="px-4 py-5 sm:px-6">
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                    {{ message.subject }}
                </h3>
                <div class="sm:flex">
                    <div class="sm:w-1/2">
                        <p class="mt-1 max-w-2xl text-sm text-gray-500">
                            From: {{ message.from_address }}
                            <button type="button" class="text-red-600 hover:text-red-900 inline-flex font-semibold"><NoSymbolIcon class="w-4 h-4"/>Block</button>
                        </p>
                        <p class="mt-1 max-w-2xl text-sm text-gray-500">
                            To: {{ message.to_address }}
                            <button type="button" class="text-red-600 hover:text-red-900 inline-flex font-semibold"><NoSymbolIcon class="w-4 h-4"/>Block</button>
                        </p>
                    </div>
                    <div class="sm:w-1/2 border-l">

                    </div>
                </div>
            </div>
            <div class="border-t border-gray-200 bg-gray-50">
                <dl>
                    <div class="md:flex">
                        <div class="md:w-1/2">
                            <div class="px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                                <dt class="text-sm font-medium text-gray-500">
                                    Recieved
                                </dt>
                                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                    {{ new Date(message.timestamp).toLocaleString() }}
                                </dd>
                            </div>
                            <div class="px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                                <dt class="text-sm font-medium text-gray-500">
                                    Recieved by
                                </dt>
                                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                    {{ message.mailscanner_hostname }}
                                </dd>
                            </div>
                            <div class="px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                                <dt class="text-sm font-medium text-gray-500">
                                    Sent from server
                                </dt>
                                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                    {{ message.client_ip }}
                                </dd>
                            </div>
                            <div class="px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                                <dt class="text-sm font-medium text-gray-500">
                                    Size
                                </dt>
                                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                    {{ bytesToHuman(message.size) }}
                                </dd>
                            </div>
                            <div class="px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                                <dt class="text-sm font-medium text-gray-500">
                                    Queue ID
                                </dt>
                                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2" >
                                    {{ message.mailq_id }}
                                </dd>
                            </div>
                        </div>
                        <div class="md:w-1/2">
                            <div class="px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                                <dt class="text-sm font-medium text-gray-500">
                                    Trusted
                                </dt>
                                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                    {{ boolToHuman(message.allowed) }}
                                </dd>
                            </div>
                            <div class="px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                                <dt class="text-sm font-medium text-gray-500">
                                    Blocked
                                </dt>
                                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                    {{ boolToHuman(message.blocked) }}
                                </dd>
                            </div>
                            <div class="px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                                <dt class="text-sm font-medium text-gray-500">
                                    Infected
                                </dt>
                                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                    {{ boolToHuman(message.infected) }}
                                </dd>
                            </div>
                            <div class="px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                                <dt class="text-sm font-medium text-gray-500">
                                    In SPAM list
                                </dt>
                                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                    {{ boolToHuman(message.is_rbl_listed) }}
                                </dd>
                            </div>
                            <div class="px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                                <dt class="text-sm font-medium text-gray-500">
                                    Spam score
                                </dt>
                                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2" >
                                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" :class="{ 'bg-green-100 text-green-800': message.is_clean, 'bg-red-100 text-red-800': message.is_spam }">
                                        {{ message.spam_score }}
                                    </span>
                                </dd>
                            </div>
                        </div>
                    </div>
                </dl>
                <div class="">
                    <Disclosure v-slot="{ open }">
                        <DisclosureButton class="flex justify-between w-full px-4 py-2 text-sm font-medium text-left text-blue-900 bg-blue-100 hover:bg-blue-200 focus:outline-none focus-visible:ring focus-visible:ring-blue-500 focus-visible:ring-opacity-75">
                            <span>Spam Report</span>
                            <ChevronDownIcon :class="open ? 'transform rotate-180' : ''" class="w-5 h-5 text-blue-500"/>
                        </DisclosureButton>
                        <DisclosurePanel class="px-4 pt-4 pb-2 text-sm text-gray-500">
                            <dl>
                                <div class="bg-gray-50 px-2 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-2" v-for="(value, key) in message.spamReport" :key="key">
                                    <dt class="text-sm font-medium text-gray-500" :title="key">
                                        {{value.description}}
                                    </dt>
                                    <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                        {{value.value}}
                                    </dd>
                                </div>
                            </dl>
                        </DisclosurePanel>
                    </Disclosure>
                    <Disclosure v-slot="{ open }">
                        <DisclosureButton class="flex justify-between w-full px-4 py-2 text-sm font-medium text-left text-blue-900 bg-blue-100 hover:bg-blue-200 focus:outline-none focus-visible:ring focus-visible:ring-blue-500 focus-visible:ring-opacity-75">
                            <span>Headers</span>
                            <ChevronDownIcon :class="open ? 'transform rotate-180' : ''" class="w-5 h-5 text-blue-500"/>
                        </DisclosureButton>
                        <DisclosurePanel class="px-4 pt-4 pb-2 text-sm text-gray-500">
                            <dl>
                                <div class="bg-gray-50 px-2 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-2" v-for="(value, key) in message.headers" :key="key">
                                    <dt class="text-sm font-medium text-gray-500">
                                        {{key}}
                                    </dt>
                                    <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                        {{value}}
                                    </dd>
                                </div>
                            </dl>
                        </DisclosurePanel>
                    </Disclosure>
                    <!-- <Disclosure v-slot="{ open }">
                        <DisclosureButton class="flex justify-between w-full px-4 py-2 text-sm font-medium text-left text-blue-900 bg-blue-100 hover:bg-blue-200 focus:outline-none focus-visible:ring focus-visible:ring-blue-500 focus-visible:ring-opacity-75">
                            <span>Scan Report</span>
                            <ChevronDownIcon :class="open ? 'transform rotate-180' : ''" class="w-5 h-5 text-blue-500"/>
                        </DisclosureButton>
                        <DisclosurePanel class="px-4 pt-4 pb-2 text-sm text-gray-500">
                            If you're unhappy with your purchase for any reason, email us within
                            120 days and we'll refund you in full, no questions asked.
                        </DisclosurePanel>
                    </Disclosure> -->
                    <Disclosure v-slot="{ open }" v-if="message.transportLogs && message.transportLogs.length">
                        <DisclosureButton class="flex justify-between w-full px-4 py-2 text-sm font-medium text-left text-blue-900 bg-blue-100 hover:bg-blue-200 focus:outline-none focus-visible:ring focus-visible:ring-blue-500 focus-visible:ring-opacity-75">
                            <span>Transport Log</span>
                            <ChevronDownIcon :class="open ? 'transform rotate-180' : ''" class="w-5 h-5 text-blue-500"/>
                        </DisclosureButton>
                        <DisclosurePanel class="px-4 pt-4 pb-2 text-sm text-gray-500">
                            <table class="min-w-full divide-y divide-gray-200">
                                <thead>
                                    <tr>
                                        <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                                            Timestamp
                                        </th>
                                        <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                                            DSN
                                        </th>
                                        <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                                            Message
                                        </th>
                                        <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                                            From
                                        </th>
                                        <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                                            To
                                        </th>
                                        <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                                            Type
                                        </th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="log in message.transportLogs" :key="log.id">
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                                            {{ log.timestamp }}
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                                            {{ log.dsn }}
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                                            {{ log.dsn_message }}
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                                            {{ log.transport_host }}
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                                            {{ log.relay_host }}
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                                            {{ log.transport_type }}
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </DisclosurePanel>
                    </Disclosure>
                </div>
            </div>
        </div>
    </MainLayout>
</template>

<script setup>
import { onMounted, ref, computed, toRefs } from 'vue'
import { RouterLink, useLink, useRouter, useRoute } from 'vue-router'
import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/vue'
import { ChevronDownIcon } from '@heroicons/vue/24/solid'
import { ArrowLeftIcon, NoSymbolIcon } from '@heroicons/vue/24/outline'
import MainLayout from '~/components/MainLayout.vue'
import { bytesToHuman, boolToHuman } from '~/filters'

let { id } = useRoute().params
let message = ref({})
let messageLoading = ref(false)
async function getMessage() {
    console.log('Started fetching message')
    messageLoading.value = true
    let res = (await useBackendFetch(`/api/messages/${id}/`))
    messageLoading.value = false
    return res
}
async function getMessageHeaders() {
    let res = (await useBackendFetch(`/api/messages/${id}/headers/`)).headers
    return res
}
async function getMessageSpamReport() {
    let res = (await useBackendFetch(`/api/messages/${id}/spam-report/`)).report
    return res
}
async function getMessageTransportLogs() {
    let res = (await useBackendFetch(`/api/messages/${id}/transport-log/`))
    return res
}

onMounted(async () => {
    message.value = (await getMessage())
    message.value['headers'] = (await getMessageHeaders())
    message.value['spamReport'] = (await getMessageSpamReport())
    message.value['transportLogs'] = (await getMessageTransportLogs())
})
</script>