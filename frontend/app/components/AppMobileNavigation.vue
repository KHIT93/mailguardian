<script setup>
    const { isMobileNavigationSlideoverOpen } = useNavigation()
</script>

<template>
    <USlideover side="left">
        <UButton color="neutral" variant="ghost" class="lg:hidden" square aria-label="Open Main Menu">
            <UIcon name="i-heroicons-bars-3-20-solid" class="h-5 w-5" />
        </UButton>
        
        <template #body>
            <AppNavigation />
        </template>
    </USlideover>
</template>