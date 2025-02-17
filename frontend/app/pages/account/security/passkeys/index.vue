<script setup>
    import TopNavigation from '~/components/account/TopNavigation'
    import MainLayout from '~/components/MainLayout.vue'

    const $auth = useAuth()
    const currentUser = useAuth().$state.user
    const { $backend } = useNuxtApp()

    const loading = ref(true)
</script>

<template>
    <MainLayout page-title="My Account">
        <TopNavigation />
        <UCard>
            <div class="flex items-center p-12" v-if="loading">
                <UProgress animation="carousel" />
            </div>
            <template v-else="">
                
            </template>
        </UCard>
    </MainLayout>
</template>