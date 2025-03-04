<script setup>
    const { isNotificationsSlideoverOpen } = useNotifications()
</script>

<template>
    <USlideover title="Notifications" description="Show Notifications">
        <UButton color="neutral" variant="ghost" square>
            <UChip color="red" inset>
                <UIcon name="i-heroicons-bell" class="w-5 h-5" />
            </UChip>
        </UButton>

        <template #body>
            <div class="p-4 flex-1">
                <USkeleton class="h-full" />
            </div>
        </template>
    </USlideover>
</template>