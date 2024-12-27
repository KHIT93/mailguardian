<script setup>
    const endpoint = computed(() => '/dashboard/senders')
    const { status, data, refresh } = (await useApi(endpoint))
</script>

<template>
    <UCard class="w-full lg:w-1/2 mb-4">
        <template #header>
            <div class="flex items-start gap-4">
                <div class="inline-flex">
                    <UIcon name="i-heroicons-chart-bar-solid" class="w-10 h-10" />
                </div>
                <div>
                    <p class="text-gray-900 dark:text-white font-semibold text-base">
                        Recent senders
                    </p>
                    <div class="mt-1 text-gray-500 dark:text-gray-400 text-sm">Messages from these domains have recently been processed</div>
                </div>
            </div>
        </template>
        <span v-if="status != 'success'" class="px-3 py-2 -mx-2 last:-mb-2 rounded-md flex items-center gap-3 relative">
            <div class="text-sm flex-1">
                <div>
                    <p class="text-gray-900 dark:text-white font-medium">
                        <USkeleton class="h-4 w-full" />
                    </p>
                </div>
            </div>
        </span>
        <span v-else="" v-for="sender in data" :key="sender.domain" class="px-3 py-2 -mx-2 last:-mb-2 rounded-md hover:bg-gray-50 dark:hover:bg-gray-800/50 flex items-center gap-3 relative">
            <div class="text-sm flex-1">
                <div>
                    <p class="text-gray-900 dark:text-white font-medium">
                        {{ sender.domain }}
                    </p>
                </div>
            </div>

            <p class="text-gray-900 dark:text-white font-medium text-sm">
                {{ sender.count }}
            </p>
        </span>
    </UCard>
</template>