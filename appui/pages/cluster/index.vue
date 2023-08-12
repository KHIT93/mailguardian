<template>
    <MainLayout>
        <div class="grid grid-cols-1 gap-5 md:grid-cols-2 2xl:grid-cols-3">
            <UCard v-for="metric in metrics" :key="metric.hostname">
                <template #header>
                    <UBadge v-if="metric.loading" size="md" color="gray"><strong>Connecting...</strong></UBadge>
                    <UBadge v-else-if="metric.active" size="md" color="green"><strong>Online</strong></UBadge>
                    <UBadge v-else size="md" color="red"><strong>Offline</strong></UBadge>
                    {{ metric.hostname }}
                </template>
                <div class="grid grid-cols-2 gap-5">
                    <div>CPU Usage:</div>
                    <div>
                        <template v-if="metric.loading"><USkeleton class="w-1/4 h-4"/></template>
                        <template v-else>{{metric.cpu_usage}}</template>
                    </div>
                </div>
                <div class="grid grid-cols-2 gap-5">
                    <div>Memory Usage:</div>
                    <div>
                        <template v-if="metric.loading"><USkeleton class="w-1/4 h-4"/></template>
                        <template v-else>{{metric.ram_usage}}</template>
                    </div>
                </div>
                <div class="grid grid-cols-2 gap-5">
                    <div>Latency:</div>
                    <div>
                        <template v-if="metric.loading"><USkeleton class="w-1/4 h-4"/></template>
                        <template v-else>20ms</template>
                    </div>
                </div>
                <div class="grid grid-cols-2 gap-5">
                    <div>Queue:</div>
                    <div>
                        <template v-if="metric.loading"><USkeleton class="w-1/4 h-4"/></template>
                        <template v-else>{{metric.queue}}</template>
                    </div>
                </div>
                <template #footer>
                    <template v-if="metric.loading"><USkeleton class="w-1/2 h-4"/></template>
                    <template v-else>Last updated {{metric.timestamp}}</template>
                </template>
            </UCard>
        </div>
    </MainLayout>
</template>
<script setup>
import Metric from '~/classes/Metric';
import MainLayout from '~/components/MainLayout.vue'

const metrics = ref([])
const hosts = ref([])

async function getMetrics() {
    hosts.value.forEach(async (host) => {
        let metric = new Metric(host.hostname, (host.use_tls) ? 'https' : 'http')
        metrics.value.push(metric)
    });
    metrics.value.forEach(async (metric) => {
        metric.get()
    })
}

onMounted(async () => {
    hosts.value = (await useBackendFetch('/api/hosts/')).results
    getMetrics()
})
</script>