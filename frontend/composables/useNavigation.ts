import { createSharedComposable } from '@vueuse/core'

const _useNavigation = () => {
    const route = useRoute()
    const isMobileNavigationSlideoverOpen = ref(false)

    watch(() => route.fullPath, () => {
        isMobileNavigationSlideoverOpen.value = false
    })

    return {
        isMobileNavigationSlideoverOpen
    }
}

export const useNavigation = createSharedComposable(_useNavigation)