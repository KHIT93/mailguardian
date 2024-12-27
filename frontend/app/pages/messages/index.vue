<template>
    <MainLayout page-title="Messages">
        <UCard>
            <UTable :loading="pending" :columns="columns" :rows="data?.items">
                <template #actions-data="{ row }">
                    <UTooltip text="Show details">
                        <UButton color="gray" variant="ghost" icon="i-heroicons-eye" :to="`/messages/${row.uuid}`" />
                    </UTooltip>
                </template>
                <template #from_address-data="{ row }">
                    <UTooltip :text="row.from_address" v-if="row.from_address.length > 40">
                        {{ row.from_address.substring(0, 40) }}...
                    </UTooltip>
                    <template v-else="">
                        {{ row.from_address }}
                    </template>
                </template>
                <template #to_address-data="{ row }">
                    <UTooltip :text="row.to_address" v-if="row.to_address.length > 40">
                        {{ row.to_address.substring(0, 40) }}...
                    </UTooltip>
                    <template v-else="">
                        {{ row.to_address }}
                    </template>
                </template>
                <template #subject-data="{ row }">
                    <UTooltip :text="row.subject" v-if="row.subject.length > 32">
                        {{ row.subject.substring(0, 32) }}...
                    </UTooltip>
                    <template v-else="">
                        {{ row.subject }}
                    </template>
                </template>
            </UTable>
            <div class="flex justify-end px-3 py-3.5 border-t border-gray-200 dark:border-gray-700">
                <UButton color="gray" leading-icon="i-heroicons-arrow-small-left-20-solid" :disabled="!data?.previous_page" @click="page -= 1" label="Previous"/>
                <UButton color="gray" trailing-icon="i-heroicons-arrow-small-right-20-solid" :disabled="!data?.next_page" @click="page += 1" label="Next"/>
            </div>
        </UCard>
    </MainLayout>
</template>

<script setup>
    import MainLayout from '~/components/MainLayout.vue'
    const page = ref(1)
    const pageCount = 50
    const endpoint = computed(() => `/messages?page=${page.value}`)
    const { pending, data, refresh } = (await useApi(endpoint, {
        watch: [endpoint]
    }))
    const columns = [
        {
            key: 'actions'
        },
        {
            key: 'date',
            label: 'Date'
        },
        {
            key: 'from_address',
            label: 'From'
        },
        {
            key: 'to_address',
            label: 'To'
        },
        {
            key: 'subject',
            label: 'Subject'
        }
    ]
</script>