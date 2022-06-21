<template>
    <form method="POST" class="space-y-8 sm:space-y-5 divide-y divide-gray-200" @submit.prevent="submit">
        <div class="">
            <p v-if="form.errors.has('non_field_errors')" class="text-red-500">
                {{ form.errors.get('non_field_errors') }}
            </p>
            <FormInput inputId="email" label="Email" type="email" v-model="form.email"/>
            <p v-if="form.errors.has('email')" class="text-red-500 text-xs py-1">
                {{ form.errors.get('email') }}
            </p>
            <hr class="my-4"/>
            <FormInput inputId="first_name" label="First name" type="text" v-model="form.first_name" class="my-4"/>
            <p v-if="form.errors.has('first_name')" class="text-red-500 text-xs py-1">
                {{ form.errors.get('first_name') }}
            </p>
            <FormInput inputId="last_name" label="Last name" type="text" v-model="form.last_name"/>
            <p v-if="form.errors.has('last_name')" class="text-red-500 text-xs py-1">
                {{ form.errors.get('last_name') }}
            </p>
            <hr class="my-4"/>
            <div class="flex my-4 items-center">
                <input id="is_domain_admin" v-model="form.is_domain_admin" name="is_domain_admin" type="checkbox" class="transition duration-300 h-4 w-4 text-blue-600 focus:ring-blue-500 border-2 border-gray-300 rounded" />
                <label for="is_domain_admin" class="ml-2 block text-sm text-gray-900">
                    Domain Administrator
                </label>
            </div>
            <div class="flex my-4 items-center">
                <input id="is_staff" v-model="form.is_staff" name="is_staff" type="checkbox" class="transition duration-300 h-4 w-4 text-blue-600 focus:ring-blue-500 border-2 border-gray-300 rounded" />
                <label for="is_staff" class="ml-2 block text-sm text-gray-900">
                    Application Administrator
                </label>
            </div>
            <hr class="my-4"/>
            <FormInput inputId="custom_spam_score" label="Spam Score" type="number" v-model="form.custom_spam_score" class="my-4"/>
            <p v-if="form.errors.has('custom_spam_score')" class="text-red-500 text-xs py-1">
                {{ form.errors.get('custom_spam_score') }}
            </p>
            <FormInput inputId="custom_spam_highscore" label="Spam HighScore" type="number" v-model="form.custom_spam_highscore" class="my-4"/>
            <p v-if="form.errors.has('custom_spam_highscore')" class="text-red-500 text-xs py-1">
                {{ form.errors.get('custom_spam_highscore') }}
            </p>
            
        </div>
        <div class="pt-5">
            <div class="flex justify-end">
                <button type="button" class="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                    Cancel
                </button>
                <button type="submit" @click="submit" class="transition duration-300 ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-500 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                    Save
                </button>
            </div>
        </div>
    </form>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import FormInput from './FormInput.vue'
import Form from '~/classes/Form'
const props = defineProps({
    id: String
})
let form = reactive(new Form({
    email: '',
    first_name: '',
    last_name: '',
    is_active: true,
    is_domain_admin: false,
    is_staff: false,
    skip_scan: false,
    custom_spam_score: 5.0,
    custom_spam_highscore: 15.0
}))

onMounted(async () => {
    if(props.id) {
        let { data: res } = await useBackendFetch(`/api/users/${props.id}/`)
        form.email = res.email,
        form.first_name = res.first_name,
        form.last_name = res.last_name,
        form.is_active = res.is_active,
        form.is_domain_admin = res.is_domain_admin,
        form.is_staff = res.is_staff,
        form.skip_scan = res.skip_scan,
        form.custom_spam_score = res.custom_spam_score,
        form.custom_spam_highscore = res.custom_spam_highscore
    }
})

async function submit() {
    if (props.id) {
        await form.patch(`/api/users/${props.id}/`)
    }
    else {
        await form.post('/api/users/')
    }
}
</script>