<template>
    <UCard class="mb-4">
        <template #header>
            Traffic
        </template>
        <VisXYContainer :data="data":padding="{ top: 10 }" class="h-96">
            <VisLine
                :x="x"
                :y="y"
                color="rgb(var(--color-primary-DEFAULT))"
            />
            <VisArea
                :x="x"
                :y="y"
                color="rgb(var(--color-primary-DEFAULT))"
                :opacity="0.1"
            />
            <VisAxis
                type="x"
                :x="x"
                :tick-format="xTicks"
            />
            <VisAxis type="y" />
            <VisCrosshair
                color="rgb(var(--color-primary-DEFAULT))"
                :template="template"
            />
            <VisTooltip />
        </VisXYContainer>
    </UCard>
</template>

<script setup>
    import { format } from 'date-fns'
    import { VisXYContainer, VisLine, VisAxis, VisArea, VisTooltip, VisCrosshair } from '@unovis/vue'
    const endpoint = computed(() => '/dashboard/traffic')
    const { status, data, refresh } = (await useApi(endpoint))
    const x = (_, i) => i
    const y = (d) => d.count

    const formatDate = (date) => {
        return format(date, 'do MMMM y')
    }

    const xTicks = (i) => {
        if (i === 0 || i === data.value.length - 1 || !data.value[i]) {
            return ''
        }

        return formatDate(data.value[i].date)
    }

    const template = (d) => `${formatDate(d.date)}: ${d.count} messages`
</script>

<style scoped>
.unovis-xy-container {
  --vis-crosshair-line-stroke-color: rgb(var(--color-primary-500));
  --vis-crosshair-circle-stroke-color: #fff;

  --vis-axis-grid-color: rgb(var(--color-gray-200));
  --vis-axis-tick-color: rgb(var(--color-gray-200));
  --vis-axis-tick-label-color: rgb(var(--color-gray-400));

  --vis-tooltip-background-color: #fff;
  --vis-tooltip-border-color: rgb(var(--color-gray-200));
  --vis-tooltip-text-color: rgb(var(--color-gray-900));
}

.dark {
  .unovis-xy-container {
    --vis-crosshair-line-stroke-color: rgb(var(--color-primary-400));
    --vis-crosshair-circle-stroke-color: rgb(var(--color-gray-900));

    --vis-axis-grid-color: rgb(var(--color-gray-800));
    --vis-axis-tick-color: rgb(var(--color-gray-800));
    --vis-axis-tick-label-color: rgb(var(--color-gray-500));

    --vis-tooltip-background-color: rgb(var(--color-gray-900));
    --vis-tooltip-border-color: rgb(var(--color-gray-800));
    --vis-tooltip-text-color: #fff;
  }
}
</style>