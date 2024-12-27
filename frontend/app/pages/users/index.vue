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
            key: 'actions'
        },
        {
            key: 'email',
            label: 'Email'
        },
        {
            key: 'first_name',
            label: 'First Name'
        },
        {
            key: 'last_name',
            label: 'Last Name'
        },
        {
            key: 'role',
            label: 'Role'
        }
    ]
</script>

<template>
    <MainLayout page-title="Users">
        <UCard>
            <template #header>
                <UButton to="/users/add" size="md" icon="i-heroicons-plus">Add user</UButton>
            </template>
            <UTable :loading="status != 'success'" :columns="columns" :rows="data?.items">
                <template #actions-data="{ row }">
                    <UTooltip text="Edit entry">
                        <UButton color="gray" variant="ghost" icon="i-heroicons-pencil" :to="`/users/${row.uuid}/edit`" />
                    </UTooltip>
                </template>
                <template #role-data="{ row }">
                    <UBadge color="green" variant="subtle" size="md" v-if="row.role == 'superuser'">Administrator</UBadge>
                    <UBadge color="blue" variant="subtle" size="md" v-else-if="row.role == 'domain_admin'">Domain Manager</UBadge>
                    <UBadge color="gray" variant="subtle" size="md" v-else-if="row.role == 'user'">User</UBadge>
                    <UBadge color="red" variant="solid" size="md" v-else="">Unknown</UBadge>
                </template>
            </UTable>
            <div class="flex justify-end px-3 py-3.5 border-t border-gray-200 dark:border-gray-700">
                <UButton color="gray" leading-icon="i-heroicons-arrow-small-left-20-solid" :disabled="!data?.previous_page" @click="page -= 1" label="Previous"/>
                <UButton color="gray" trailing-icon="i-heroicons-arrow-small-right-20-solid" :disabled="!data?.next_page" @click="page += 1" label="Next"/>
            </div>
        </UCard>
    </MainLayout>
</template>