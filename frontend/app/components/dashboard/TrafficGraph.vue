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

<template>
    <UCard class="mb-4">
        <template #header>
            Traffic
        </template>
        <VisXYContainer :data="data":padding="{ top: 10 }" class="h-96">
            <VisLine
                :x="x"
                :y="y"
                color="rgb(var(--ui-primary))"
            />
            <VisArea
                :x="x"
                :y="y"
                color="rgb(var(--ui-primary))"
                :opacity="0.1"
            />
            <VisAxis
                type="x"
                :x="x"
                :tick-format="xTicks"
            />
            <VisAxis type="y" />
            <VisCrosshair
                color="rgb(var(--ui-primary))"
                :template="template"
            />
            <VisTooltip />
        </VisXYContainer>
    </UCard>
</template>

<style scoped>
.unovis-xy-container {
  --vis-crosshair-line-stroke-color: var(--ui-primary);
  --vis-crosshair-circle-stroke-color: var(--ui-bg);

  --vis-axis-grid-color: var(--ui-border);
  --vis-axis-tick-color: var(--ui-border);
  --vis-axis-tick-label-color: var(--ui-text-dimmed);

  --vis-tooltip-background-color: var(--ui-bg);
  --vis-tooltip-border-color: var(--ui-border);
  --vis-tooltip-text-color: var(--ui-text-highlighted);
}
</style>