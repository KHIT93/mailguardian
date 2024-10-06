<template>
    <MainLayout page-title="Audit Log">
        <UCard>
            <!-- <template #header>
                <UButton to="/domains/add" size="md" icon="i-heroicons-plus">Add Domain</UButton>
            </template> -->
            <UTable :loading="pending" :columns="columns" :rows="data?.items">
                <template #allowed-data="{ row }">
                    <UBadge color="green" variant="subtle" size="md" v-if="row.allowed">Yes</UBadge>
                    <UBadge color="red" variant="solid" size="md" v-else="">No</UBadge>
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
    const endpoint = computed(() => `/audit/log?page=${page.value}`)
    const { pending, data, refresh } = (await useApi(endpoint, {
        watch: [endpoint]
    }))
    const columns = [
        // {
        //     key: 'actions'
        // },
        {
            key: 'performed_at',
            label: 'When'
        },
        {
            key: 'allowed',
            label: 'Allowed'
        },
        {
            key: 'model',
            label: 'Data source'
        },
        {
            key: 'res_id',
            label: 'Ressource ID'
        },
        {
            key: 'acted_from',
            label: 'From'
        },
        {
            key: 'actor_id',
            label: 'Actor'
        },
        {
            key: 'message',
            label: 'Message'
        }
    ]
</script>