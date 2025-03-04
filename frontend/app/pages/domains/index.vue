<script setup>
    import MainLayout from '~/components/MainLayout.vue'
    const page = ref(1)
    const pageCount = 50
    const endpoint = computed(() => `/domains?page=${page.value}`)
    const { status, data, refresh } = (await useApi(endpoint, {
        watch: [endpoint]
    }))
    const columns = [
        {
            accessorKey: 'name',
            header: 'Domain'
        },
        {
            accessorKey: 'relay_type',
            header: 'Transport'
        },
        {
            accessorKey: 'destination',
            header: 'Deliver To'
        },
        {
            accessorKey: 'reception_type',
            header: 'Configuration'
        },
        {
            accessorKey: 'created_at',
            header: 'Created'
        },
        {
            accessorKey: 'updated_at',
            header: 'Updated'
        },
        {
            id: 'actions'
        }
    ]
</script>

<template>
    <MainLayout page-title="Domains">
        <UCard>
            <template #header>
                <UButton to="/domains/add" size="md" icon="i-heroicons-plus">Add Domain</UButton>
            </template>
            <UTable :loading="status != 'success'" :columns="columns" :data="data?.items">
                <template #actions-cell="{ row }">
                    <UTooltip text="Edit entry">
                        <UButton color="neutral" variant="ghost" icon="i-heroicons-pencil" :to="`/domains/${row.original.uuid}/edit`" />
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