<template>
    <MainLayout page-title="Blocked senders">
        <UCard>
            <template #header>
                <UButton to="/lists/add" size="md" icon="i-heroicons-plus">Add entry</UButton>
            </template>
            <UTable :loading="pending" :columns="columns" :rows="data?.items">
                <template #actions-data="{ row }">
                    <UTooltip text="Edit entry">
                        <UButton color="gray" variant="ghost" icon="i-heroicons-pencil" :to="`/lists/${row.uuid}/edit`" />
                    </UTooltip>
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
    const endpoint = computed(() => `/blocklist?page=${page.value}`)
    const { pending, data, refresh } = (await useApi(endpoint, {
        watch: [endpoint]
    }))
    const columns = [
        {
            key: 'actions'
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
            key: 'listing_type',
            label: 'Type'
        }
    ]
</script>