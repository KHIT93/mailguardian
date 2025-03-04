<script setup>
    import MainLayout from '~/components/MainLayout.vue'
    const page = ref(1)
    const pageCount = 50
    const endpoint = computed(() => `/messages?page=${page.value}`)
    const { status, data, refresh } = (await useApi(endpoint, {
        watch: [endpoint]
    }))

    const columns = [
        {
            accessorKey: 'date',
            header: 'Date'
        },
        {
            accessorKey: 'from_address',
            header: 'From'
        },
        {
            accessorKey: 'to_address',
            header: 'To'
        },
        {
            accessorKey: 'subject',
            header: 'Subject'
        },
        {
            id: 'actions'
        },
    ]

</script>

<template>
    <MainLayout page-title="Messages">
        <UCard>
            <UTable :loading="status == 'pending'" :columns="columns" :data="data?.items">
                <template #actions-cell="{ row }">
                    <UTooltip text="Show details">
                        <UButton color="neutral" variant="ghost" icon="i-heroicons-eye" :to="`/messages/${row.original.uuid}`" />
                    </UTooltip>
                </template>
                <template #from_address-cell="{ getValue }">
                    <UTooltip :text="getValue()" v-if="getValue().length > 40">
                        {{ getValue().substring(0, 40) }}...
                    </UTooltip>
                    <template v-else="">
                        {{ getValue() }}
                    </template>
                </template>
                <template #to_address-cell="{ getValue }">
                    <UTooltip :text="getValue()" v-if="getValue().length > 40">
                        {{ getValue().substring(0, 40) }}...
                    </UTooltip>
                    <template v-else="">
                        {{ getValue() }}
                    </template>
                </template>
                <template #subject-cell="{ getValue }">
                    <UTooltip :text="getValue()" v-if="getValue().length > 32">
                        {{ getValue().substring(0, 32) }}...
                    </UTooltip>
                    <template v-else="">
                        {{ getValue() }}
                    </template>
                </template>
            </UTable>
            <div class="flex justify-end px-3 py-3.5 border-t border-gray-200 dark:border-gray-700">
                <UButton color="neutral" leading-icon="i-heroicons-arrow-small-left-20-solid" :disabled="!data?.previous_page" @click="page -= 1" label="Previous"/>
                <UButton color="neutral" trailing-icon="i-heroicons-arrow-small-right-20-solid" :disabled="!data?.next_page" @click="page += 1" label="Next"/>
            </div>
        </UCard>
    </MainLayout>
</template>