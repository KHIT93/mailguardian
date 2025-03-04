<script setup>
    import MainLayout from '~/components/MainLayout.vue'
    const page = ref(1)
    const pageCount = 50
    const endpoint = computed(() => `/allowlist?page=${page.value}`)
    const { status, data, refresh } = (await useApi(endpoint, {
        watch: [endpoint]
    }))
    const columns = [
    {
            accessorKey: 'from_address',
            header: 'From'
        },
        {
            accessorKey: 'to_address',
            header: 'To'
        },
        {
            accessorKey: 'listing_type',
            header: 'Type'
        },
        {
            id: 'actions'
        }
    ]
</script>

<template>
    <MainLayout page-title="Allowed senders">
        <UCard>
            <template #header>
                <UButton to="/lists/add" size="md" icon="i-heroicons-plus">Add entry</UButton>
            </template>
            <UTable :loading="status == 'pending'" :columns="columns" :rows="data?.items">
                <template #actions-cell="{ row }">
                    <UTooltip text="Edit entry">
                        <UButton color="neutral" variant="ghost" icon="i-heroicons-pencil" :to="`/lists/${row.original.uuid}/edit`" />
                    </UTooltip>
                </template>
            </UTable>
            <div class="flex justify-end px-3 py-3.5 border-t border-gray-200 dark:border-gray-700">
                <UButton color="neutral" leading-icon="i-heroicons-arrow-small-left-20-solid" :disabled="!data?.previous_page" @click="page -= 1" label="Previous"/>
                <UButton color="neutral" trailing-icon="i-heroicons-arrow-small-right-20-solid" :disabled="!data?.next_page" @click="page += 1" label="Next"/>
            </div>
        </UCard>
    </MainLayout>
</template>