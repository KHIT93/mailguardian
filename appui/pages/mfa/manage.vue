<template>
    <MainLayout>
        <div class="inline-block w-full p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-2xl" >
            <h3 class="text-lg font-medium leading-6 text-gray-900">
                Manage Two-Factor Authentication
            </h3>
            <div>
                <dl class="divide-y divide-gray-200">
                    <template v-for="method in mfaMethods">
                        <SwitchGroup as="div" class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:pt-5">
                            <SwitchLabel as="dt" class="text-sm font-medium text-gray-500" passive>
                                {{ method.name }}
                            </SwitchLabel>
                            <dd class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                <svg v-if="primaryMfaMethodToggle" class="relative inline-flex shrink-0 sm:ml-auto animate-spin mr-3 h-6 w-6 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                <template v-else>
                                    <Switch v-if="method.is_primary" v-model="method.is_primary" disabled :class="[method.is_primary ? 'bg-blue-300' : 'bg-gray-200', 'relative inline-flex shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-not-allowed transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-auto']">
                                        <span aria-hidden="true" :class="[method.is_primary ? 'translate-x-5' : 'translate-x-0', 'inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200']" />
                                    </Switch>
                                    <Switch v-else v-model="method.is_primary" @click="toggleConfirmationModal(method.name)" :class="[method.is_primary ? 'bg-blue-600' : 'bg-gray-200', 'relative inline-flex shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-auto']">
                                        <span aria-hidden="true" :class="[method.is_primary ? 'translate-x-5' : 'translate-x-0', 'inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200']" />
                                    </Switch>
                                    <NuxtLink v-if="! method.is_primary" class="bg-white mx-2 rounded-md font-medium text-red-600 hover:text-red-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500" :href="`/mfa/disable/${method.name}`">
                                        <TrashIcon class="w-6 h-6"/>
                                        <span class="sr-only">Delete</span>
                                    </NuxtLink>
                                    <div v-else class="bg-white mx-2 rounded-md font-medium text-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-300 cursor-not-allowed" :href="`/mfa/disable/${method.name}`">
                                        <TrashIcon class="w-6 h-6"/>
                                        <span class="sr-only">Delete</span>
                                    </div>
                                </template>
                            </dd>
                        </SwitchGroup>
                    </template>
                </dl>
            </div>
        </div>
        <TransitionRoot appear :show="showConfirmationModal" as="template">
            <Dialog as="div" @close="showConfirmationModal = false">
                <div class="fixed inset-0 z-10 overflow-y-auto">
                    <div class="min-h-screen px-4 text-center">
                        <TransitionChild
                            as="template"
                            enter="duration-300 ease-out"
                            enter-from="opacity-0"
                            enter-to="opacity-100"
                            leave="duration-200 ease-in"
                            leave-from="opacity-100"
                            leave-to="opacity-0"
                            >
                            <div class="fixed inset-0 bg-black opacity-30" />
                        </TransitionChild>
                        <span class="inline-block h-screen align-middle" aria-hidden="true">
                        &#8203;
                        </span>
                        <TransitionChild
                            as="template"
                            enter="duration-300 ease-out"
                            enter-from="opacity-0 scale-95"
                            enter-to="opacity-100 scale-100"
                            leave="duration-200 ease-in"
                            leave-from="opacity-100 scale-100"
                            leave-to="opacity-0 scale-95"
                            >
                            <DialogPanel class="inline-block w-full sm:max-w-xl p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-2xl" >
                                <h3 class="text-lg font-medium leading-6 text-gray-900">
                                    Chnage Two-Factor Authentication method
                                </h3>
                                <div>
                                    <p class="my-2">Please confirm switching to the <code class="text-blue-700 bg-gray-100 p-1">{{ newMethod }}</code> method by entering a validation code from your current 2FA method</p>
                                    <FormInput v-model="mfaCode" label="Verification code" autocomplete="one-time-code" type="number" input-id="mfaCode"/>
                                    <div class="pt-5">
                                        <div class="flex">
                                            <button type="button" @click="switchPrimaryMethod" class="transition duration-300 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-500 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                                                Confirm
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </DialogPanel>
                        </TransitionChild>
                    </div>
                </div>
            </Dialog>
        </TransitionRoot>
    </MainLayout>
</template>
<script setup>
    import MainLayout from '~/components/MainLayout.vue'
    import {
        Switch,
        SwitchGroup,
        SwitchLabel,
        TransitionRoot,
        TransitionChild,
        Dialog,
        DialogPanel,
    } from '@headlessui/vue'
    import { TrashIcon } from '@heroicons/vue/24/outline'
    definePageMeta({
        middleware: ['has-mfa']
    })
    const { $auth } = useNuxtApp()
    const mfaMethods = ref([])
    const showConfirmationModal = ref(false)
    const primaryMfaMethodToggle = ref(false)
    const newMethod = ref('')
    const mfaCode = ref('')
    onMounted(async () => {
        await fetchMfaMethods()
    })
    async function fetchMfaMethods() {
        primaryMfaMethodToggle.value = true
        mfaMethods.value = (await $auth().fetch()).mfa_methods
        primaryMfaMethodToggle.value = false
    }
    async function switchPrimaryMethod() {
        primaryMfaMethodToggle.value = true
        await useBackendFetch('/rest-auth/mfa/change-primary-method/', {
            method: 'POST',
            body: {
                method: newMethod.value,
                code: mfaCode.value
            }
        })
        primaryMfaMethodToggle.value = false
        showConfirmationModal.value = false
        fetchMfaMethods()
    }
    function toggleConfirmationModal(methodName) {
        newMethod.value = methodName
        useBackendFetch('/rest-auth/code/request/', {
            method: 'POST'
        })
        primaryMfaMethodToggle.value = true
        showConfirmationModal.value = true
    }

</script>