<template>
    <MainLayout>
        <div class="inline-block w-full p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-2xl">
            <h3 class="text-lg font-medium leading-6 text-gray-900">
                Enable Two-Factor Authentication
            </h3>
            <nav aria-label="Progress" class="my-4">
                <ol role="list" class="flex items-center">
                    <li v-for="(step, stepIdx) in steps" :key="step.name" :class="[stepIdx !== steps.length - 1 ? 'pr-8 sm:pr-20' : '', 'relative']">
                        <template v-if="step.status === 'complete'">
                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                <div class="h-0.5 w-full bg-blue-600" />
                            </div>
                            <a href="#" class="relative w-8 h-8 flex items-center justify-center bg-blue-600 rounded-full hover:bg-blue-900">
                                <CheckIcon class="w-5 h-5 text-white" aria-hidden="true" />
                                <span class="sr-only">{{ step.name }}</span>
                            </a>
                        </template>
                        <template v-else-if="step.status === 'current'" condition="step.status === 'current'">
                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                <div class="h-0.5 w-full bg-gray-200" />
                            </div>
                            <a href="#" class="relative w-8 h-8 flex items-center justify-center bg-white border-2 border-blue-600 rounded-full" aria-current="step">
                                <span class="h-2.5 w-2.5 bg-blue-600 rounded-full" aria-hidden="true" />
                                <span class="sr-only">{{ step.name }}</span>
                            </a>
                        </template>
                        <template v-else>
                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                <div class="h-0.5 w-full bg-gray-200" />
                            </div>
                            <a href="#" class="group relative w-8 h-8 flex items-center justify-center bg-white border-2 border-gray-300 rounded-full hover:border-gray-400">
                                <span class="h-2.5 w-2.5 bg-transparent rounded-full group-hover:bg-gray-300" aria-hidden="true" />
                                <span class="sr-only">{{ step.name }}</span>
                            </a>
                        </template>
                    </li>
                </ol>
            </nav>
            <div v-if="currentStepIndex == 0">
                <div>By following the next steps, you will be able to ewnable two-factor authentication (2FA) on your account. Press <code class="text-blue-700 bg-gray-100 p-1">Next</code> to start</div>
                <div class="pt-5">
                    <div class="flex">
                        <button type="button" @click="nextStep" class="transition duration-300 ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-500 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                            Next
                        </button>
                    </div>
                </div>
            </div>
            <div v-else-if="currentStepIndex == 1">
                <form @submit.prevent="startMfaActivation">
                    <FormSelection input-id="method" v-model="method" label="Validation Method">
                        <template v-slot:inputOptions>
                            <option value="email">Email</option>
                            <option value="app">App</option>
                        </template>
                    </FormSelection>
                    <div class="pt-5">
                        <div class="flex">
                            <button type="submit" class="transition duration-300 ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-500 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                                Next
                            </button>
                        </div>
                    </div>
                </form>
            </div>
            <div v-else-if="currentStepIndex == 2">
                <form @submit.prevent="confirmMfaActivation">
                    <div class="p-4" v-if="qrcode">
                        <QRCode :value="qrcode" render-as="svg" size="400"/>
                    </div>
                    <FormInput v-model="mfaCode" label="Verification code" type="number" autocomplete="one-time-code" input-id="code"/>
                    <div class="pt-5">
                        <div class="flex">
                            <button type="submit" class="transition duration-300 ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-500 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                                Confirm
                            </button>
                        </div>
                    </div>
                </form>
            </div>
            <div v-else-if="currentStepIndex == 3">
                <p>Thank you for completing the setup!</p>
                <p>You are now ready to use 2FA on your account</p>
                <p>Next time you log in, you will required 2FA</p>
                <p>Here is a list of your backup codes. Keep them safe!</p>
                <ul>
                    <li v-for="bCode in backup_codes">
                        {{ bCode }}
                    </li>
                </ul>
                <div class="pt-5">
                    <div class="flex">
                        <NuxtLink href="/mfa/manage" class="transition duration-300 ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-500 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                            Finish
                        </NuxtLink>
                    </div>
                </div>
            </div>
        </div>
    </MainLayout>
</template>
<script setup>
    import MainLayout from '~/components/MainLayout.vue'
    import { CheckIcon } from '@heroicons/vue/24/solid'
    import { computed } from '@vue/reactivity'
    import { onMounted, reactive, ref } from 'vue'
    import FormSelection from '~/components/FormSelection.vue'
    import FormInput from '~/components/FormInput.vue'
    import QRCode from 'qrcode.vue'
    definePageMeta({
        middleware: ['has-no-mfa']
    })
    const steps = reactive([
        { index: 0, name: 'Intro', href:'#', status: 'current' },
        { index: 1, name: 'Method', href:'#', status: 'incomplete' },
        { index: 2, name: 'Setup', href:'#', status: 'incomplete' },
        { index: 3, name: 'Finished', href:'#', status: 'incomplete' },
    ])
    const method = ref('')
    const qrcode = ref('')
    const mfaCode = ref('')
    const backup_codes = reactive([])
    const currentStepIndex = ref(0)
    const currentStep = computed(() => {
        return steps[currentStepIndex]
    })
    function nextStep() {
        let currentStepId = steps.findIndex(step => step.index == currentStepIndex.value)
        steps[currentStepId].status = 'complete'
        steps[currentStepId + 1].status = 'current'
        currentStepIndex.value += 1
    }

    async function startMfaActivation() {
        let res = (await useBackendFetch(`/rest-auth/${method.value}/activate/`, { method: 'POST'}))
        console.log(res)
        if (res.details.startsWith('otpauth://', 0)) {
            qrcode.value = res.details
        }
        nextStep()
    }
    function confirmMfaActivation() {
        useBackendFetch(`/rest-auth/${method.value}/activate/confirm/`, { method: 'POST', body: { code: mfaCode.value }}).then(response => {
            backup_codes.value = response.backup_codes
            nextStep()
        }).catch(error => {
            console.log(error)
        })
    }

</script>