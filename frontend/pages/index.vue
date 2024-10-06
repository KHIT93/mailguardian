<template>
    <MainLayout page-title="Dashboard">
        <UCard class="mb-4">
            <template #header>
                Traffic
            </template>
        </UCard>
        <div class="flex space-x-4">
            <UCard class="w-1/2">
                <template #header>
                    Recent senders
                </template>
            </UCard>
            <UCard class="w-1/2">
                <template #header>
                    Recent spam hits
                </template>
            </UCard>
        </div>
        
    </MainLayout>
</template>

<script setup>
    import MainLayout from '~/components/MainLayout.vue'
</script>