<template>
    <div
        class="inline-block w-full sm:max-w-xl p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-2xl"
        >
        <DialogTitle
            as="h3"
            class="text-lg font-medium leading-6 text-gray-900"
            >
            Enable Two-Factor Authentication
        </DialogTitle>
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
            <MfaWizardIndex @complete="nextStep" />
        </div>
        <div v-else-if="currentStepIndex == 1">
            <MfaWizardMethod @complete="nextStep" />
        </div>
        <div v-else-if="currentStepIndex == 2">
            <MfaWizardSetup @complete="nextStep" :method="method" />
        </div>
        <div v-else-if="currentStepIndex == 3">
            <p>Thank you for completing the setup!</p>
            <p>You are now ready to use 2FA on your account</p>
            <p>Next time you log in, you will required 2FA</p>
            <p>Here is a list of your backup codes. Keep them safe!</p>
            <ul>
                <li v-for="code in backup_codes">
                    {{ code }}
                </li>
            </ul>
            <div class="pt-5">
                <div class="flex">
                    <button type="button" @click="close" class="transition duration-300 ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-500 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                        Finish
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import { DialogTitle } from '@headlessui/vue'
import { CheckIcon } from '@heroicons/vue/solid/esm/index.js'
import { computed } from '@vue/reactivity'
import { onMounted, reactive, ref } from 'vue'
import MfaWizardIndex from './MfaWizard/index.vue'
import MfaWizardMethod from './MfaWizard/method.vue'
import MfaWizardSetup from './MfaWizard/setup.vue'
export default {
    props: ['show'],
    components: {
        DialogTitle,
        CheckIcon,
        MfaWizardIndex,
        MfaWizardMethod,
        MfaWizardSetup
    },
    setup(props) {
        let { show } = props
        const steps = reactive([
            { index: 0, name: 'Intro', href:'#', status: 'current' },
            { index: 1, name: 'Method', href:'#', status: 'incomplete' },
            { index: 2, name: 'Setup', href:'#', status: 'incomplete' },
            { index: 3, name: 'Finished', href:'#', status: 'incomplete' },
        ])
        const method = ref('')
        const backup_codes = reactive([])
        const currentStepIndex = computed(() => {
            return steps.findIndex(step => step.status == 'current')
        })
        const currentStep = computed(() => {
            return steps.find(step => step.status == 'current')
        })
        return {
            show,
            steps,
            currentStep,
            currentStepIndex,
            method,
            backup_codes
        }
    },
    methods: {
        close() {
            this.$emit('close')
        },
        nextStep(event) {
            console.log(event)
            let currentStep = this.steps.findIndex(step => step.status == 'current')
            this.steps[currentStep].status = 'complete'
            if (this.steps[currentStep].index == 1) {
                this.method = event
            }
            else if (this.steps[currentStep].index == 2) {
                this.backup_codes = event.backup_codes
            }
            this.steps[currentStep + 1].status = 'current'
        }
    }
}
</script>