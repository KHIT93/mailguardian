<template>
    <form method="POST" class="space-y-8 sm:space-y-5 divide-y divide-gray-200" @submit.prevent="submit">
        <div class="">
            <p v-if="form.errors.has('non_field_errors')" class="text-red-500">
                {{ form.errors.get('non_field_errors') }}
            </p>
            <UFormGroup label="Hostname" size="md" class="my-4">
                <UInput id="hostname" type="text" v-model="form.hostname"/>
                <p v-if="form.errors.has('hostname')" class="text-red-500 text-xs py-1">
                    {{ form.errors.get('hostname') }}
                </p>
            </UFormGroup>
            <hr class="my-4"/>
            <UFormGroup label="IP Address" size="md" class="my-4">
                <UInput id="ip_address" type="text" v-model="form.ip_address"/>
                <p v-if="form.errors.has('ip_address')" class="text-red-500 text-xs py-1">
                    {{ form.errors.get('ip_address') }}
                </p>
            </UFormGroup>
            <UFormGroup label="Priority" size="md" class="my-4">
                <UInput id="priority" type="text" v-model="form.priority"/>
                <p v-if="form.errors.has('priority')" class="text-red-500 text-xs py-1">
                    {{ form.errors.get('priority') }}
                </p>
            </UFormGroup>
            <hr class="my-4"/>
            <UCheckbox label="Use TLS" id="use_tls" v-model="form.use_tls" help="Communicate with this host using SSL/TLS encryption" name="use_tls" class="my-2"/>
            <UCheckbox label="Passive host" id="passive" v-model="form.passive" help="This host is passive" name="passive" class="my-2"/>
        </div>
        <div class="pt-5">
            <div class="flex justify-end">
                <button type="button" class="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                    Cancel
                </button>
                <button type="submit" class="transition duration-300 ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-500 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                    Save
                </button>
            </div>
        </div>
    </form>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import Form from '~/classes/Form'
const props = defineProps({
    id: String
})
let form = reactive(new Form({
    hostname: '',
    ip_address: '',
    use_tls: false,
    priority: 10,
    passive: false
}))

const toast = useToast()

onMounted(async () => {
    if(props.id) {
        let res = (await useBackendFetch(`/api/hosts/${props.id}/`))
        form.hostname = res.hostname,
        form.ip_address = res.ip_address,
        form.use_tls = res.use_tls,
        form.priority = res.priority,
        form.passive = res.passive
    }
})

async function submit() {
    try {
        if (props.id) {
            await form.put(`/api/hosts/${props.id}/`)
        }
        else {
            await form.post('/api/hosts/')
        }
        toast.add({
            'id': 'hosts_form_submitted',
            'title': (props.id) ? `Host ${res.hostname} updated` : `Host ${res.hostname} created`,
            'description': 'The changes will be active within a few minutes',
            'icon': 'i-heroicons-check-circle',
            'timeout': 5000
        })
        navigateTo('/cluster/nodes')
    }
    catch (error) {
        console.log(error)
    }
}
</script>