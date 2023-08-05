<template>
    <MainLayout>
        <div class="grid grid-cols-1 gap-5 md:grid-cols-2 2xl:grid-cols-3">
            <UCard>
                <template #header>
                    <UBadge size="md" color="green"><strong>Online</strong></UBadge> mx01.fr.kitecluster.cloud
                </template>
                <div class="grid grid-cols-2 gap-5">
                    <div>CPU Usage:</div>
                    <div>43%</div>
                </div>
                <div class="grid grid-cols-2 gap-5">
                    <div>Memory Usage:</div>
                    <div>72%</div>
                </div>
                <div class="grid grid-cols-2 gap-5">
                    <div>Latency:</div>
                    <div>20ms</div>
                </div>
                <div class="grid grid-cols-2 gap-5">
                    <div>Queue:</div>
                    <div>0</div>
                </div>
                <template #footer>
                    Last updated Mon May 22nd 2023 21:00
                </template>
            </UCard>
            <UCard>
                <template #header>
                    <UBadge size="md" color="red"><strong>Offline</strong></UBadge> mx02.pl.kitecluster.cloud
                </template>
                <div class="grid grid-cols-2 gap-5">
                    <div>CPU Usage:</div>
                    <div>N/A</div>
                </div>
                <div class="grid grid-cols-2 gap-5">
                    <div>Memory Usage:</div>
                    <div>N/A</div>
                </div>
                <div class="grid grid-cols-2 gap-5">
                    <div>Latency:</div>
                    <div>N/A</div>
                </div>
                <div class="grid grid-cols-2 gap-5">
                    <div>Queue:</div>
                    <div>N/A</div>
                </div>
                <template #footer>
                    Last updated Mon May 22nd 2023 21:00
                </template>
            </UCard>
        </div>
    </MainLayout>
</template>
<script setup>
import MainLayout from '~/components/MainLayout.vue'
</script>