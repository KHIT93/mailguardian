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
                <UFormField label="Domain" name="name" size="md" class="my-4">
                    <UInput id="name" type="text" v-model="state.name"/>
                </UFormField>

                <UFormField label="Deliver To" name="destination" size="md" class="my-4" help="This is the hostname/IP-address of the server to which email should be delivered after processing">
                    <UInput id="destination" type="text" v-model="state.destination"/>
                </UFormField>
                <UFormField label="Transport" name="relay_type" size="md" class="my-4" help="The protocol/method used to transport messages to the destination server">
                    <UInputMenu v-model="state.relay_type" :items="relayTypes" value-key="value" label-key="label" placeholder="Select relay type..."/>
                </UFormField>

                <UFormField label="Configuration" name="reception_type" size="md" class="my-4" help="The selected configuration will allow the application to correctly configure DNS to work in the desired configuration">
                    <UInputMenu v-model="state.reception_type" :items="receptionTypes" value-key="value" label-key="label" placeholder="Select relay type..."/>
                </UFormField>

                <UFormField label="Active" name="active" size="md" class="my-4">
                    <USwitch v-model="state.active" />
                </UFormField>

                <template #footer>
                    <UButton type="submit">
                        Save
                    </UButton>
                </template>
            </UCard>
        </UForm>
    </MainLayout>
</template>