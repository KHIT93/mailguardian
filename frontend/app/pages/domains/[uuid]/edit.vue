<script setup>
    import MainLayout from '~/components/MainLayout.vue'
    import { domainSchema } from '~/schemas/domains.ts'
    const { uuid } = useRoute().params
    const pageTitle = computed(() =>  `Domain Details (${uuid})`)
    const { status, data: state } = (await useApi(`/domains/${uuid}`))

    const submissionEndpoint = computed(() => `/domains/${uuid}`)

    const receptionTypes = [
        {
            value: 'failover',
            label: 'Active - Passive'
        },
        {
            value: 'load_balanced',
            label: 'Load Balancing'
        }
    ]

    const relayTypes = [
        {
            value: 'smtp',
            label: 'SMTP'
        },
        {
            value: 'smtps',
            label: 'Secure SMTP'
        }
    ]

    const form = ref()

    async function onSubmit(event) {
        form.value.clear()
        try {
            const response = await useApi(submissionEndpoint, {
                method: 'PATCH',
                body: state
            })
        } catch(error) {
            if (error.statusCode == 422) {
                console.log(error.data)
                form.value.setErrors(error.data.detail.map((err) => ({
                    message: err.msg,
                    path: err.loc
                })))
            }
        }
        
    }
</script>

<template>
    <MainLayout :page-title="pageTitle">
        <UForm ref="form" :schema="domainSchema" :state="state" @submit="onSubmit">
            <UCard>
                <UFormGroup label="Domain" name="name" size="md" class="my-4">
                    <UInput id="name" type="text" v-model="state.name"/>
                </UFormGroup>

                <UFormGroup label="Deliver To" name="destination" size="md" class="my-4" help="This is the hostname/IP-address of the server to which email should be delivered after processing">
                    <UInput id="destination" type="text" v-model="state.destination"/>
                </UFormGroup>
                <UFormGroup label="Transport" name="relay_type" size="md" class="my-4" help="The protocol/method used to transport messages to the destination server">
                    <UInputMenu v-model="state.relay_type" :options="relayTypes" value-attribute="value" option-attribute="label" placeholder="Select relay type..."/>
                </UFormGroup>

                <UFormGroup label="Configuration" name="reception_type" size="md" class="my-4" help="The selected configuration will allow the application to correctly configure DNS to work in the desired configuration">
                    <UInputMenu v-model="state.reception_type" :options="receptionTypes" value-attribute="value" option-attribute="label" placeholder="Select relay type..."/>
                </UFormGroup>

                <UFormGroup label="Active" name="active" size="md" class="my-4">
                    <UToggle v-model="state.active" />
                </UFormGroup>

                <template #footer>
                    <UButton type="submit">
                        Save
                    </UButton>
                </template>
            </UCard>
        </UForm>
    </MainLayout>
</template>