<script setup>
    const { isMobileNavigationSlideoverOpen } = useNavigation()
</script>

<template>
    <USlideover v-model="isMobileNavigationSlideoverOpen" side="left">
        <AppNavigation />
    </USlideover>
</template>