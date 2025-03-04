<script setup>
    import MainLayout from '~/components/MainLayout.vue'
    const { uuid } = useRoute().params

    const showHeaders = ref(false)
    const showContents = ref(false)
    const showSpamAnalysis = ref(false)

    const { status, data } = (await useApi(`/messages/${uuid}`))

    const { status: headers_status, data: headers } = (await useApi(`/messages/${uuid}/headers`))
    const { status: spamreport_status, data: spamreport } = (await useApi(`/messages/${uuid}/reports/spam`))
    const { status: logs_status, data: logs } = (await useApi(`/messages/${uuid}/logs`))
    const { status: contents_status, data: contents } = (await useApi(`/messages/${uuid}/view`))

    const pageTitle = computed(() =>  `Message Details (${uuid})`)

    const messageActions = [
        [
            {
                label: 'View Headers',
                icon: 'i-heroicons-eye',
                onSelect: () => {
                    showHeaders.value = true
                }
            },
            {
                label: 'View Contents',
                icon: 'i-heroicons-eye',
                onSelect: () => {
                    showContents.value = true
                }
            },
            {
                label: 'View Spam Analysis',
                icon: 'i-heroicons-academic-cap',
                onSelect: () => {
                    showSpamAnalysis.value = true
                }
            },
            {
                label: 'Mark as spam',
                icon: 'i-heroicons-hand-thumb-down'
            },
            {
                label: 'Mark as safe',
                icon: 'i-heroicons-hand-thumb-up'
            },
            {
                label: 'Release',
                icon: 'i-heroicons-envelope'
            },
        ]
    ]

    const headerColumns = [
        {
            accessorKey: 'key',
            header: 'Name'
        },
        {
            accessorKey: 'value',
            header: 'Value'
        }
    ]

    const logsColumns = [
        {
            accessorKey: 'timestamp',
            header: 'When'
        },
        {
            accessorKey: 'transport_host',
            header: 'Transport Host'
        },
        {
            accessorKey: 'relay_host',
            header: 'Relay Host'
        },
        {
            accessorKey: 'delay',
            header: 'Delay'
        },
        {
            accessorKey: 'dsn',
            header: 'DSN'
        },
        {
            accessorKey: 'dsn_message',
            header: 'Message'
        }
    ]

    const spamReportColumns = [
        {
            accessorKey: 'rule',
            header: 'Rule'
        },
        {
            accessorKey: 'score',
            header: 'Score'
        }
    ]

    function boolToHuman(value) {
        return value ? 'Yes' : 'No';
    }
</script>

<template>
    <MainLayout :page-title="pageTitle">
        <div v-if="status == 'success'">
            <UCard class="mb-2">
                <template #header>
                    <div class="flex justify-between">
                        <h2 class="truncate text-ellipsis w-1/2">
                            <UTooltip text="Show Spam Analysis">
                                <UBadge :color="(data.is_spam) ? 'error': 'success'" icon="i-heroicons-academic-cap" variant="subtle" class="cursor-pointer"size="md" @click="showSpamAnalysis = true">
                                    {{ data.spam_score }}
                                </UBadge>
                            </UTooltip>
                            {{ data.subject }}
                        </h2>
                        <UDropdownMenu :items="messageActions" mode="click">
                            <template #msgheader>
                                
                            </template>
                            <UButton color="white" label="Actions" trailing-icon="i-heroicons-chevron-down-20-solid" />
                        </UDropdownMenu>
                    </div>
                </template>
                <div class="mt-6">
                    <dl class="grid grid-cols-1 sm:grid-cols-2">
                        <div class="px-4 pb-6 sm:col-span-1 sm:px-0">
                            <dt class="text-sm font-bold leading-6 text-gray-900 dark:text-gray-200">Recieved from</dt>
                            <dd class="mt-1 text-sm leading-6 text-gray-700 dark:text-gray-200 sm:mt-2">{{ data.client_ip }} <UBadge color="sky" variant="subtle"><UIcon name="i-heroicons-clock"/> <span class="pl-1">{{ data.timestamp }}</span></UBadge></dd>
                        </div>
                        <div class="px-4 pb-6 sm:col-span-1 sm:px-0">
                            <dt class="text-sm font-bold leading-6 text-gray-900 dark:text-gray-200">Recieved by</dt>
                            <dd class="mt-1 text-sm leading-6 text-gray-700 dark:text-gray-200 sm:mt-2">{{ data.mailscanner_hostname }} <UBadge color="sky" variant="subtle"><UIcon name="i-heroicons-clock"/> <span class="pl-1">{{ data.timestamp }}</span></UBadge></dd>
                        </div>

                        <div class="border-t border-gray-100 px-4 py-6 sm:col-span-1 sm:px-0">
                            <dt class="text-sm font-bold leading-6 text-gray-900 dark:text-gray-200">From</dt>
                            <dd class="mt-1 text-sm leading-6 text-gray-700 dark:text-gray-200 sm:mt-2">{{ data.from_address }}</dd>
                        </div>
                        <div class="border-t border-gray-100 px-4 py-6 sm:col-span-1 sm:px-0">
                            <dt class="text-sm font-bold leading-6 text-gray-900 dark:text-gray-200">To</dt>
                            <dd class="mt-1 text-sm leading-6 text-gray-700 dark:text-gray-200 sm:mt-2">{{ data.to_address }}</dd>
                        </div>

                        <div class="border-t border-gray-100 px-4 py-6 sm:col-span-2 sm:px-0 grid grid-cols-2 sm:grid-cols-4">
                            <div class="col-span-1">
                                <dt class="text-sm font-bold leading-6 text-gray-900 dark:text-gray-200">Trusted</dt>
                                <dd class="mt-1 text-sm leading-6 text-gray-700 dark:text-gray-200 sm:mt-2">{{ boolToHuman(data.allowed) }}</dd>
                            </div>
                            <div class="col-span-1">
                                <dt class="text-sm font-bold leading-6 text-gray-900 dark:text-gray-200">Blocked</dt>
                                <dd class="mt-1 text-sm leading-6 text-gray-700 dark:text-gray-200 sm:mt-2">{{ boolToHuman(data.blocked) }}</dd>
                            </div>
                            <div class="col-span-1">
                                <dt class="text-sm font-bold leading-6 text-gray-900 dark:text-gray-200">Infected</dt>
                                <dd class="mt-1 text-sm leading-6 text-gray-700 dark:text-gray-200 sm:mt-2">{{ boolToHuman(data.infected) }}</dd>
                            </div>
                            <div class="col-span-1">
                                <dt class="text-sm font-bold leading-6 text-gray-900 dark:text-gray-200">RBL Listed</dt>
                                <dd class="mt-1 text-sm leading-6 text-gray-700 dark:text-gray-200 sm:mt-2">{{ boolToHuman(data.is_rbl_listed) }}</dd>
                            </div>
                        </div>
                    </dl>
                </div>
            </UCard>
            <UCard>
                <!-- <template #header>
                    <h3 class="font-bold">Transport logs</h3>
                </template> -->
                <UTable :loading="logs_status == 'pending'" :columns="logsColumns" :rows="logs" />
            </UCard>
            <UModal v-model:open="showHeaders" :title="`Headers for ${data.uuid}`" :description="`View messages headers for ${data.uuid}`" :ui="{ content: 'w-full sm:max-w-2xl md:max-w-4xl lg:max-w-6xl 2xl:max-w-screen-2xl' }">
                <template #content>
                    <UCard>
                        <template #header>
                            <div class="flex items-center justify-between">
                                <h3>Headers for {{ data.uuid }}</h3>
                                <UButton color="neutral" variant="ghost" icon="i-heroicons-x-mark-20-solid" :ui="{ rounded: 'rounded-full' }" class="-my-1" @click="showHeaders = false" />
                            </div>
                        </template>
                        <UTable :loading="headers_status == 'pending'" :columns="headerColumns" :data="headers"/>
                    </UCard>
                </template>
            </UModal>

            <UModal v-model:open="showContents" :title="`Contents for ${data.uuid}`" :description="`View messages contents for ${data.uuid}`" :ui="{ content: 'w-full sm:max-w-2xl md:max-w-4xl lg:max-w-6xl 2xl:max-w-screen-2xl' }">
                <template #content>
                    <UCard>
                        <template #header>
                            <div class="flex items-center justify-between">
                                <h3>{{ data.subject }}</h3>
                                <UButton color="neutral" variant="ghost" icon="i-heroicons-x-mark-20-solid" :ui="{ rounded: 'rounded-full' }" class="-my-1" @click="showContents = false" />
                            </div>
                            <div>
                                <span class="text-gray-300 font-bold">From:</span> {{ data.from_address }}
                            </div>
                            <div>
                                <span class="text-gray-300 font-bold">To:</span> {{ data.to_address }}
                            </div>
                        </template>
                        <div>
                            {{ contents?.body }}
                        </div>
                        <template #footer v-if="contents?.attachments">
                            <ul>
                                <li v-for="attachment in contents?.attachments" :key="attachment">
                                    {{ attachment }}
                                </li>
                            </ul>
                        </template>
                        <!-- <UTable :loading="contents_status = 'success'" :columns="headerColumns" :data="contents"/> -->
                    </UCard>
                </template>
            </UModal>

            <UModal v-model:open="showSpamAnalysis" :title="`Spam Analysis for ${data.uuid}`" :description="`View Spam Analysis for ${data.uuid}`" :ui="{ content: 'w-full sm:max-w-2xl md:max-w-4xl lg:max-w-6xl 2xl:max-w-screen-2xl' }">
                <template #content>
                    <UCard>
                        <template #header>
                            <div class="flex items-center justify-between">
                                <h3>Spam Analysis {{ data.uuid }}</h3>
                                <UButton color="neutral" variant="ghost" icon="i-heroicons-x-mark-20-solid" :ui="{ rounded: 'rounded-full' }" class="-my-1" @click="showSpamAnalysis = false" />
                            </div>
                        </template>
                        <UTable :loading="spamreport_status == 'pending'" :columns="spamReportColumns" :data="spamreport"/>
                    </UCard>
                </template>
            </UModal>
        </div>
        <UCard v-else="">
            <UProgress animation="carousel" />
        </UCard>
    </MainLayout>
</template>