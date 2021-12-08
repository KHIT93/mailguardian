<template>
    <form method="POST" class="space-y-8 sm:space-y-5 divide-y divide-gray-200" @submit.prevent="submit">
        <div class="">
            <p v-if="form.errors.has('non_field_errors')" class="text-red-500">
                {{ form.errors.get('non_field_errors') }}
            </p>
            <div class="relative transition duration-300 border border-gray-300 rounded-md px-3 py-2 shadow-sm focus-within:ring-1 focus-within:ring-blue-600 focus-within:border-blue-600">
                <label for="email" class="absolute -top-2 left-2 -mt-px inline-block px-1 bg-white text-xs font-base text-gray-900">Email</label>
                <input type="email" name="email" id="email" v-model="form.email" class="block w-full border-0 p-0 text-gray-900 placeholder-gray-500 focus:ring-0 sm:text-sm" placeholder="Email" />
                <p v-if="form.errors.has('email')" class="text-red-500 text-xs py-1">
                    {{ form.errors.get('email') }}
                </p>
            </div>
            <hr class="my-4"/>
            <div class="relative transition duration-300 border border-gray-300 rounded-md px-3 py-2 my-4 shadow-sm focus-within:ring-1 focus-within:ring-blue-600 focus-within:border-blue-600">
                <label for="first_name" class="absolute -top-2 left-2 -mt-px inline-block px-1 bg-white text-xs font-base text-gray-900">First name</label>
                <input type="text" name="first_name" id="first_name" v-model="form.first_name" class="block w-full border-0 p-0 text-gray-900 placeholder-gray-500 focus:ring-0 sm:text-sm" placeholder="First name" />
                <p v-if="form.errors.has('first_name')" class="text-red-500 text-xs py-1">
                    {{ form.errors.get('first_name') }}
                </p>
            </div>
            <div class="relative transition duration-300 border border-gray-300 rounded-md px-3 py-2 my-4 shadow-sm focus-within:ring-1 focus-within:ring-blue-600 focus-within:border-blue-600">
                <label for="last_name" class="absolute -top-2 left-2 -mt-px inline-block px-1 bg-white text-xs font-base text-gray-900">Last name</label>
                <input type="text" name="last_name" id="last_name" v-model="form.last_name" class="block w-full border-0 p-0 text-gray-900 placeholder-gray-500 focus:ring-0 sm:text-sm" placeholder="Last name" />
                <p v-if="form.errors.has('last_name')" class="text-red-500 text-xs py-1">
                    {{ form.errors.get('last_name') }}
                </p>
            </div>
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
            <div class="relative transition duration-300 border border-gray-300 rounded-md px-3 py-2 my-4 shadow-sm focus-within:ring-1 focus-within:ring-blue-600 focus-within:border-blue-600">
                <label for="custom_spam_score" class="absolute -top-2 left-2 -mt-px inline-block px-1 bg-white text-xs font-base text-gray-900">Spam Score</label>
                <input type="number" name="custom_spam_score" id="custom_spam_score" v-model="form.custom_spam_score" class="block w-full border-0 p-0 text-gray-900 placeholder-gray-500 focus:ring-0 sm:text-sm" placeholder="Spam Score" />
                <p v-if="form.errors.has('custom_spam_score')" class="text-red-500 text-xs py-1">
                    {{ form.errors.get('custom_spam_score') }}
                </p>
            </div>
            <div class="relative transition duration-300 border border-gray-300 rounded-md px-3 py-2 my-4 shadow-sm focus-within:ring-1 focus-within:ring-blue-600 focus-within:border-blue-600">
                <label for="custom_spam_highscore" class="absolute -top-2 left-2 -mt-px inline-block px-1 bg-white text-xs font-base text-gray-900">Spam HighScore</label>
                <input type="number" name="custom_spam_highscore" id="custom_spam_highscore" v-model="form.custom_spam_highscore" class="block w-full border-0 p-0 text-gray-900 placeholder-gray-500 focus:ring-0 sm:text-sm" placeholder="Spam HighScore" />
                <p v-if="form.errors.has('custom_spam_highscore')" class="text-red-500 text-xs py-1">
                    {{ form.errors.get('custom_spam_highscore') }}
                </p>
            </div>
            
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

<script>
import { toRef, toRefs, ref } from '@vue/reactivity'
import { reactive, onMounted } from 'vue'
import Form from '../classes/Form'
export default {
    props: [
        'id'
    ],
    setup(props) {
        let { id } = props
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
            if(id) {
                let res = (await axios.get(`/api/users/${id}/`)).data
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

        return {
            form,
            id
        }
    },
    methods: {
        async submit() {
            if (this.id) {
                await this.form.patch(`/api/users/${this.id}/`)
            }
            else {
                await this.form.post('/api/users/')
            }
        }
    }
}
</script>