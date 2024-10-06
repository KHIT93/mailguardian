<template>
    <USlideover v-model="isMobileNavigationSlideoverOpen" side="left">
        <AppNavigation />
    </USlideover>
</template>

<script setup>
    const { isMobileNavigationSlideoverOpen } = useNavigation()
</script>