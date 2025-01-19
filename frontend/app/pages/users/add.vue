<script setup>
    import MainLayout from '~/components/MainLayout.vue'
    import { userSchema } from '~/schemas/users.ts'

    const submissionEndpoint = computed(() => `/users`)

    const state = reactive({
        email: null,
        first_name: null,
        last_name: null,
        role: null,
    })

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
                method: 'POST',
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
    <MainLayout page-title="Add User">
        <UForm ref="form" :schema="userSchema" :state="state" @submit="onSubmit">
            <UCard>
                <UFormGroup label="Email" name="email" size="md" class="my-4">
                    <UInput id="email" type="email" v-model="state.email"/>
                </UFormGroup>
                <div class="flex justify-between">
                    <UFormGroup label="First Name" name="first_name" size="md" class="my-4 pr-1 w-1/2">
                        <UInput id="first_name" type="text" v-model="state.first_name"/>
                    </UFormGroup>
                    <UFormGroup label="Last Name" name="last_name" size="md" class="my-4 pl-1 w-1/2">
                        <UInput id="last_name" type="text" v-model="state.last_name"/>
                    </UFormGroup>
                </div>

                <UFormGroup label="Role" size="md" class="my-4">
                    <UInputMenu v-model="state.role" :options="userRoles" value-attribute="value" option-attribute="label" placeholder="Select role..."/>
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