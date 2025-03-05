<script setup>
    import MainLayout from '~/components/MainLayout.vue'
    import { userSchema } from '~/schemas/users.ts'
    const { uuid } = useRoute().params
    const pageTitle = computed(() =>  `User Details (${uuid})`)
    const { status, data: state } = (await useApi(`/users/${uuid}`))

    const submissionEndpoint = computed(() => `/users/${uuid}`)

    const userRoles = [
        {
            value: 'user',
            label: 'User'
        },
        {
            value: 'domain_admin',
            label: 'Domain Administrator'
        },
        {
            value: 'superuser',
            label: 'Application Administrator'
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
        <UForm ref="form" :schema="userSchema" :state="state" @submit="onSubmit">
            <UCard>
                <UFormField label="Email" name="email" size="md" class="my-4">
                    <UInput class="w-full" id="email" type="email" v-model="state.email"/>
                </UFormField>
                <div class="flex justify-between">
                    <UFormField label="First Name" name="first_name" size="md" class="my-4 pr-1 w-1/2">
                        <UInput class="w-full" id="first_name" type="text" v-model="state.first_name"/>
                    </UFormField>
                    <UFormField label="Last Name" name="last_name" size="md" class="my-4 pl-1 w-1/2">
                        <UInput class="w-full" id="last_name" type="text" v-model="state.last_name"/>
                    </UFormField>
                </div>

                <UFormField label="Role" size="md" class="my-4">
                    <UInputMenu class="w-full" v-model="state.role" :items="userRoles" value-key="value" label-key="label" placeholder="Select role..."/>
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