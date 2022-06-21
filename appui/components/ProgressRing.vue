<template>
    <svg
        :height="radius * 2"
        :width="radius * 2"
     >
        <circle
            class="rounded-full"
            stroke="currentColor"
            :stroke-dasharray="circumfence + ' ' + circumfence"
            :style="{ strokeDashoffset }"
            :stroke-width="stroke"
            :fill="fillColor"
            :r="normalizedRadius"
            :cx="radius"
            :cy="radius"
        />
    </svg>
</template>

<script setup>
import { ref, computed, toRefs } from 'vue'

const props = defineProps({
    radius: Number,
    progress: Number,
    stroke: Number,
    fillColor: String
})

let { radius, progress, stroke, fillColor } = toRefs(props)
let normalizedRadius = computed(() => {
    return radius.value - stroke.value
})
let circumfence = computed(() => {
    return normalizedRadius.value * 2 * Math.PI
})
let strokeDashoffset = computed(() => {
    return circumfence.value - progress.value / 100 * circumfence.value
})
</script>
<style scoped>
    circle {
        transform: rotate(-180deg);
        transform-origin: 50% 50%;
    }
</style>