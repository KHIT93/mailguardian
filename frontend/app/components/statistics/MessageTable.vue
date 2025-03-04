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
            id: 'actions'
        },
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
        }
    ]
</script>

<template>
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
</template>