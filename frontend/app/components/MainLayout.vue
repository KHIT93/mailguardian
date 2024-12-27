<script setup>
    import AppNotifications from './AppNotifications'
    import AppMobileNavigation from './AppMobileNavigation'
    const props = defineProps(['pageTitle'])
    const { isNotificationsSlideoverOpen } = useNotifications()
    const { isMobileNavigationSlideoverOpen } = useNavigation()
    const colorMode = useColorMode()
    const isDark = computed({
        get () {
            return colorMode.value === 'dark'
        },
        set () {
            colorMode.preference = colorMode.value === 'dark' ? 'light' : 'dark'
        }
    })
</script>

<template>
    <div class="fixed inset-0 text-sm h-screen overflow-hidden flex bg-slate-100 dark:bg-gray-800">
        <AppNavigation class="hidden"/>
        <div class="flex flex-1 w-full min-w-0">
            <div class="flex-col items-stretch relative w-full flex-1 flex">
                <div class="h-16 flex-shrink-0 flex items-center border-b border-gray-200 dark:border-gray-800 px-4 gap-x-4 min-w-0  bg-white dark:bg-gray-900">
                    <div class="flex items-center justify-between flex-1 gap-x-1.5 min-w-0">
                        <div class="flex items-stretch gap-1.5 min-w-0">
                            <!-- Mobile Nav -->
                            <UButton color="gray" variant="ghost" class="lg:hidden" square @click="isMobileNavigationSlideoverOpen = true" aria-label="Open Main Menu">
                                <UIcon name="i-heroicons-bars-3-20-solid" class="h-5 w-5" />
                            </UButton>
                            <!-- Mobile Nav -->
                            <h1 class="flex items-center gap-1.5 font-semibold text-gray-900 dark:text-white min-w-0">
                                {{ props.pageTitle }}
                            </h1>
                        </div>
                        <div class="flex items-stretch flex-shrink-0 gap-1.5">
                            <div class="relative inline-flex">
                                <ClientOnly>
                                    <UButton :icon="isDark ? 'i-heroicons-moon-20-solid' : 'i-heroicons-sun-20-solid'" color="gray" variant="ghost" aria-label="Theme" square @click="isDark = !isDark"/>
                                    <template #fallback>
                                        <div class="w-8 h-8" />
                                    </template>
                                </ClientOnly>
                            </div>
                            <div class="relative inline-flex">
                                <UButton color="gray" variant="ghost" square @click="isNotificationsSlideoverOpen = true">
                                    <UChip color="red" inset>
                                        <UIcon name="i-heroicons-bell" class="w-5 h-5" />
                                    </UChip>
                                </UButton>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="p-4 flex-1 flex flex-col overflow-y-auto">
                    <slot />
                </div>
            </div>
        </div>
        <AppMobileNavigation />
        <AppNotifications />
    </div>
</template>