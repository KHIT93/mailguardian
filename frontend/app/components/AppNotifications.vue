<template>
    <USlideover v-model="isNotificationsSlideoverOpen">
        <div class="p-4 flex-1">
            <USkeleton class="h-full" />
        </div>
    </USlideover>
</template>

<script setup>
    const { isNotificationsSlideoverOpen } = useNotifications()
</script>