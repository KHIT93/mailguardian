<script setup>
    import MainLayout from '~/components/MainLayout.vue'
    const page = ref(1)
    const pageCount = 50
    const endpoint = computed(() => `/users?page=${page.value}`)
    const { status, data, refresh } = (await useApi(endpoint, {
        watch: [endpoint]
    }))
    const columns = [
        {
            accessorKey: 'email',
            header: 'Email'
        },
        {
            accessorKey: 'first_name',
            header: 'First Name'
        },
        {
            accessorKey: 'last_name',
            header: 'Last Name'
        },
        {
            accessorKey: 'role',
            header: 'Role'
        },
        {
            id: 'actions'
        }
    ]
</script>

<template>
    <MainLayout page-title="Users">
        <UCard>
            <template #header>
                <UButton to="/users/add" size="md" icon="i-heroicons-plus">Add user</UButton>
            </template>
            <UTable :loading="status != 'success'" :columns="columns" :data="data?.items">
                <template #actions-cell="{ row }">
                    <UTooltip text="Edit entry">
                        <UButton color="neutral" variant="ghost" icon="i-heroicons-pencil" :to="`/users/${row.original.uuid}/edit`" />
                    </UTooltip>
                </template>
                <template #role-cell="{ getValue }">
                    <UBadge color="success" variant="subtle" size="md" v-if="getValue() == 'superuser'" label="Administrator"/>
                    <UBadge color="primary" variant="subtle" size="md" v-else-if="getValue() == 'domain_admin'" label="Domain Manager"/>
                    <UBadge color="neutral" variant="subtle" size="md" v-else-if="getValue() == 'user'" label="User"/>
                    <UBadge color="error" variant="solid" size="md" v-else="" label="Unknown"/>
                </template>
            </UTable>
            <div class="flex justify-end px-3 py-3.5 border-t border-gray-200 dark:border-gray-700">
                <UButton color="neutral" leading-icon="i-heroicons-arrow-small-left-20-solid" :disabled="!data?.previous_page" @click="page -= 1" label="Previous"/>
                <UButton color="neutral" trailing-icon="i-heroicons-arrow-small-right-20-solid" :disabled="!data?.next_page" @click="page += 1" label="Next"/>
            </div>
        </UCard>
    </MainLayout>
</template>