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

<script>
import { ref, computed, toRefs } from 'vue'
export default {
    props: {
        radius: Number,
        progress: Number,
        stroke: Number,
        fillColor: {
            type: String,
            default: 'transparent'
        }
    },
    setup(props) {
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
        return {
            radius,
            stroke,
            normalizedRadius,
            circumfence,
            strokeDashoffset
        }
    }
}
</script>
<style scoped>
    circle {
        transform: rotate(-180deg);
        transform-origin: 50% 50%;
    }
</style>