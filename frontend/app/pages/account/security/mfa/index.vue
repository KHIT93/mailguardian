<script setup>
    import { format } from 'date-fns'
    import TopNavigation from '~/components/account/TopNavigation'
    import MainLayout from '~/components/MainLayout.vue'

    const $auth = useAuth()
    const currentUser = useAuth().$state.user
    const { $backend } = useNuxtApp()

    const loading = ref(false)

    const endpoint = computed(() => `/totp/devices`)
    const { status, data, refresh } = (await useApi(endpoint))
    const columns = [
        {
            key: 'name',
            label: 'Name'
        },
        {
            key: 'created_at',
            label: 'Created'
        },
        {
            key: 'actions'
        },
    ]

    async function revokeTotpDevice(device) {
        let removalEndpoint = `/totp/devices/${device.uuid}`
        try {
            await $backend(removalEndpoint, {
                method: 'DELETE'
            })
            refresh()
        } catch(error) {
            console.log(error.statusCode)
            console.log(error.data)
            console.log(error.message)
        }
        finally {
            loading.value = false
        }
    }

    const formatDate = (date) => {
        return format(date, 'do MMMM y HH:mm:ss')
    }


</script>

<template>
    <MainLayout page-title="My Account">
        <TopNavigation />
        <UCard>
            <UButton to="/account/security/mfa/enable" size="md" icon="i-heroicons-plus">Add TOTP Device</UButton>
            <UTable :loading="status != 'success'" :columns="columns" :rows="data">
                <template #created_at-data="{row}">
                    {{ formatDate(row.created_at) }}
                </template>
                <template #actions-data="{ row }">
                    <UTooltip text="Revoke TOTP">
                        <UButton color="red" variant="ghost" icon="i-heroicons-trash" @click="revokeTotpDevice(row)" />
                    </UTooltip>
                </template>
            </UTable>
        </UCard>
    </MainLayout>
</template>