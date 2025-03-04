<script setup>
    import MainLayout from '~/components/MainLayout.vue'
    const page = ref(1)
    const pageCount = 50
    const endpoint = computed(() => `/audit/log?page=${page.value}`)
    const { status, data, refresh } = (await useApi(endpoint, {
        watch: [endpoint]
    }))
    const columns = [
        {
            accessorKey: 'performed_at',
            header: 'When'
        },
        {
            accessorKey: 'allowed',
            header: 'Allowed'
        },
        {
            accessorKey: 'model',
            header: 'Data source'
        },
        {
            accessorKey: 'res_id',
            header: 'Ressource ID'
        },
        {
            accessorKey: 'acted_from',
            header: 'From'
        },
        {
            accessorKey: 'actor_id',
            header: 'Actor'
        },
        {
            accessorKey: 'message',
            header: 'Message'
        },
        // {
        //     id: 'actions'
        // }
    ]
</script>

<template>
    <MainLayout page-title="Audit Log">
        <UCard>
            <!-- <template #header>
                <UButton to="/domains/add" size="md" icon="i-heroicons-plus">Add Domain</UButton>
            </template> -->
            <UTable :loading="status != 'success'" :columns="columns" :data="data?.items">
                <template #allowed-cell="{ getValue }">
                    <UBadge color="success" variant="subtle" size="md" v-if="getValue()">Yes</UBadge>
                    <UBadge color="error" variant="solid" size="md" v-else="">No</UBadge>
                </template>
            </UTable>
            <div class="flex justify-end px-3 py-3.5 border-t border-gray-200 dark:border-gray-700">
                <UButton color="neutral" leading-icon="i-heroicons-arrow-small-left-20-solid" :disabled="!data?.previous_page" @click="page -= 1" label="Previous"/>
                <UButton color="neutral" trailing-icon="i-heroicons-arrow-small-right-20-solid" :disabled="!data?.next_page" @click="page += 1" label="Next"/>
            </div>
        </UCard>
    </MainLayout>
</template>