<script setup>
    
    import MainLayout from '~/components/MainLayout.vue'
    import TrafficGraph from '~/components/dashboard/TrafficGraph'
    import RecentSenders from '~/components/dashboard/RecentSenders'
    import SpamHits from '~/components/dashboard/SpamHits'

</script>

<template>
    <MainLayout page-title="Dashboard">
        <TrafficGraph />
        <div class="lg:flex lg:space-x-4">
            <RecentSenders />
            <SpamHits />
        </div>
        
    </MainLayout>
</template>