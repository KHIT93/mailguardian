<template>
    <MainLayout page-title="Domains">
        <UCard>
            <template #header>
                <UButton to="/domains/add" size="md" icon="i-heroicons-plus">Add Domain</UButton>
            </template>
            <UTable :loading="pending" :columns="columns" :rows="data?.items">
                <template #actions-data="{ row }">
                    <UTooltip text="Edit entry">
                        <UButton color="gray" variant="ghost" icon="i-heroicons-pencil" :to="`/domains/${row.uuid}/edit`" />
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
    const endpoint = computed(() => `/domains?page=${page.value}`)
    const { pending, data, refresh } = (await useApi(endpoint, {
        watch: [endpoint]
    }))
    const columns = [
        {
            key: 'actions'
        },
        {
            key: 'name',
            label: 'Domain'
        },
        {
            key: 'relay_type',
            label: 'Transport'
        },
        {
            key: 'destination',
            label: 'Deliver To'
        },
        {
            key: 'reception_type',
            label: 'Configuration'
        },
        {
            key: 'created_at',
            label: 'Created'
        },
        {
            key: 'updated_at',
            label: 'Updated'
        }
    ]
</script>