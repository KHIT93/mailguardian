<script setup>
    import AppNotifications from './AppNotifications'
    import AppMobileNavigation from './AppMobileNavigation'
    import OnlineIndicator from './OnlineIndicator'
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
    useSeoMeta({
        title: () => `${props.pageTitle} - MailGuardian`
    })
</script>

<template>
    <div class="fixed inset-0 text-sm h-screen overflow-hidden flex bg-slate-100 dark:bg-gray-800">
        <AppNavigation class="hidden"/>
        <div class="flex flex-1 w-full min-w-0">
            <div class="flex-col items-stretch relative w-full flex-1 flex">
                <div class="h-16 shrink-0 flex items-center border-b border-gray-200 dark:border-gray-800 px-4 gap-x-4 min-w-0  bg-white dark:bg-gray-900">
                    <div class="flex items-center justify-between flex-1 gap-x-1.5 min-w-0">
                        <div class="flex items-stretch gap-1.5 min-w-0">
                            <!-- Mobile Nav -->
                            <AppMobileNavigation />
                            <!-- Mobile Nav -->
                            <h1 class="flex items-center gap-1.5 font-semibold text-gray-900 dark:text-white min-w-0">
                                {{ props.pageTitle }}
                            </h1>
                        </div>
                        <div class="flex items-stretch shrink-0 gap-1.5">
                            <div class="relative inline-flex">
                                <ClientOnly>
                                    <OnlineIndicator />
                                    <template #fallback>
                                        <div class="w-8 h-8" />
                                    </template>
                                </ClientOnly>
                            </div>
                            <div class="relative inline-flex">
                                <ClientOnly>
                                    <UButton :icon="isDark ? 'i-heroicons-moon-20-solid' : 'i-heroicons-sun-20-solid'" color="neutral" variant="ghost" aria-label="Theme" square @click="isDark = !isDark"/>
                                    <template #fallback>
                                        <div class="w-8 h-8" />
                                    </template>
                                </ClientOnly>
                            </div>
                            <div class="relative inline-flex">
                                <AppNotifications />
                            </div>
                        </div>
                    </div>
                </div>
                <div class="p-4 flex-1 flex flex-col overflow-y-auto">
                    <slot />
                </div>
            </div>
        </div>
    </div>
</template>