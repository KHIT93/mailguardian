<script setup>
    import MainLayout from '~/components/MainLayout.vue'
    import MessageTable from '~/components/statistics/MessageTable'

    const $auth = useAuth()
    const currentUser = useAuth().$state.user
    const toast = useToast()

    const filters = reactive([])
    const state = reactive({
        field: undefined,
        operator: undefined,
        query: undefined
    })

    const showResults = ref(false)

    const fieldOptions = [
        {
            value: 'from_address',
            label: 'From Address'
        },
        {
            value: 'from_domain',
            label: 'From Domain'
        },
        {
            value: 'to_address',
            label: 'To Address'
        },
        {
            value: 'to_domain',
            label: 'To Domain'
        },
        {
            value: 'subject',
            label: 'Message Subject'
        },
        {
            value: 'date',
            label: 'Date Recieved'
        },
        {
            value: 'client_ip',
            label: 'Recieved From'
        },
        {
            value: 'mailscanner_hostname',
            label: 'Processed by'
        }
    ]

    const operatorOptions = [
        {
            value: '=',
            label: 'Equals'
        },
        {
            value: '!=',
            label: 'Does not equal'
        },
        {
            value: '>',
            label: 'Greater than'
        },
        {
            value: '<',
            label: 'Less than'
        },
        {
            value: 'in',
            label: 'Contains'
        },
        {
            value: 'not in',
            label: 'Does not contain'
        }
    ]

    const fieldTypes = {
        from_address: 'text',
        from_domain: 'text',
        to_address: 'text',
        to_domain: 'text',
        subject: 'text',
        date: 'date',
        client_ip: 'text',
        mailscanner_hostname: 'text'
    }

    const columns = [
        {
            accessorKey: 'field',
            header: 'Field'
        },
        {
            accessorKey: 'operator',
            header: 'Matches'
        },
        {
            accessorKey: 'value',
            header: 'Value'
        },
        {
            id: 'actions'
        }
    ]

    async function addFilter(event) {
        if (filters.find(f => f.field == state.field) == undefined) {
            filters.push({
                field: state.field,
                operator: state.operator,
                value: state.query
            })

            state.field = undefined
            state.operator = undefined
            state.query = undefined
        }
        else {
            toast.add({
                title: 'Failed to add filter',
                description: `Filter for ${fieldOptions.find(f => f.value == state.field).label} has already been created`,
                timeout: 10000,
                icon: 'i-heroicons-exclamation-circle-solid',
                color: 'error'
            })   
            
        }
    }
</script>

<template>
    <MainLayout page-title="Statistics">
        <div class="lg:flex">
            <UCard class="w-full lg:w-1/2 lg:mx-1">
                <template #header>
                    Message filters
                </template>
                <UForm :state="state" @submit="addFilter">
                    <UFormField label="Field" name="field" size="md" required class="my-4" help="Select what field/information you want to search in">
                        <UInputMenu class="w-full" v-model="state.field" :items="fieldOptions" required value-key="value" label-key="label" placeholder="Select field..."/>
                    </UFormField>
                    <UFormField label="Matches" name="operator" required size="md" class="my-4" help="Select how you want to search the selected field/information">
                        <UInputMenu class="w-full" v-model="state.operator" :items="operatorOptions" required value-kye="value" label-key="label" placeholder="Select relay type..."/>
                    </UFormField>
                    <UFormField label="Value" name="query" required size="md" help="Type/Select the value to search for">
                        <UInput class="w-full" v-model="state.query" :type="fieldTypes[state.field]" />
                    </UFormField>
                    <USeparator class="my-4" />
                    <UButton type="submit" size="md" icon="i-heroicons-plus-solid">
                        Add Filter
                    </UButton>
                </UForm>
            </UCard>

            <UCard class="w-full lg:w-1/2 my-2 lg:my-0 lg:mx-1">
                <template #header>
                    Applied filters
                </template>
                <UTable :columns="columns" :data="filters">
                    <template #field-cell="{ getValue }">
                        {{ fieldOptions.find(f => f.value == getValue()).label }}
                    </template>
                    <template #operator-cell="{ getValue }">
                        {{ operatorOptions.find(f => f.value == getValue()).label }}
                    </template>
                    <template #actions-cell="{ row }">
                        <UTooltip text="Remove filter">
                            <UButton color="error" variant="ghost" icon="i-heroicons-trash" @click="filters.splice(filters.findIndex(f => f.field == row.original.field), 1)" />
                        </UTooltip>
                    </template>
                </UTable>
                <template #footer v-if="filters.length">
                    {{ filters }}
                    <UButton icon="i-heroicons-magnifying-glass" size="md" @click="showResults = true">
                        Show results
                    </UButton>
                </template>
            </UCard>
        </div>
        
        <UModal v-model:open="showResults" fullscreen>
            <template #content>
                <UCard>
                    <template #header>
                        <div class="flex items-center justify-between">
                            <h3 class="text-base font-semibold leading-6 text-gray-900 dark:text-white">
                                Query Results
                            </h3>
                            <UTooltip text="Close">
                                <UButton color="neutral" variant="ghost" icon="i-heroicons-x-mark-20-solid" class="-my-1" @click="showResults = false" />
                            </UTooltip>
                        </div>
                    </template>
                    <MessageTable :filters="filters"></MessageTable>
                </UCard>
            </template>
        </UModal>
    </MainLayout>
</template>