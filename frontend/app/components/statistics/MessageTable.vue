<script setup>
    const page = ref(1)
    const pageCount = 50
    const { filters } = defineProps(['filters'])

    const endpoint = computed(() => `/statistics/messages`)
    const { status, data, refresh } = (await useApi(endpoint, {
        method: 'POST',
        body: filters
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

<template>
    <UTable :loading="status != 'success'" :columns="columns" :rows="data?.items">
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
</template>