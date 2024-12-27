import { createSharedComposable } from '@vueuse/core'

const _useNotifications = () => {
    const route = useRoute()
    const isNotificationsSlideoverOpen = ref(false)

    watch(() => route.fullPath, () => {
        isNotificationsSlideoverOpen.value = false
    })

    return {
        isNotificationsSlideoverOpen
    }
}

export const useNotifications = createSharedComposable(_useNotifications)