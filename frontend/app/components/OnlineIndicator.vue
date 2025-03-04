<script setup>
    const online = ref(false)

    function checkOnline() {
        useNuxtApp().$backend('/status/ping').then(() => online.value = true).catch(() => online.value = false)
    }

    let interval = setInterval(() => {
        checkOnline()
    }, 1000 * 60 * 5)

    onMounted(() => checkOnline())
    onUnmounted(() => clearInterval(interval))
</script>

<template>
    <div class="focus:outline-hidden focus-visible:outline-0 shrink-0 text-sm gap-x-1.5 p-1.5 focus-visible:ring-inset focus-visible:ring-2 focus-visible:ring-primary-500 dark:focus-visible:ring-primary-400 inline-flex items-center">
        <UIcon v-if="online"name="i-heroicons-signal-solid" class="h-5 w-5 text-green-700 dark:text-green-400" title="Application is online" />
        <UIcon v-else="" name="i-heroicons-signal-slash-solid" class="h-5 w-5 text-red-700 dark:text-red-400" title="Application is unavailable" />
    </div>
</template>