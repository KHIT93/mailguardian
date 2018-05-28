<template>
    <div class="justify-center flex pt-8">
        <div class="w-full max-w-lg">
            <div class="bg-white shadow-lg sm:rounded">
                <div class="flex bg-grey-light justify-between items-center border-b shadow-inner rounded-t">
                    <div class="flex">
                        <div v-for="(step, index) in steps" :key="step.order" :class="{ 'bg-blue-lighter text-black' : currentStepIndex == index, 'bg-green text-white': step.completed, 'bg-red text-white': step.error, 'rounded-tl': index == 0 }"  class="text-sm p-4">
                            {{ step.order }} {{ step.name }}
                        </div>
                    </div>
                    <div class="flex mr-2">
                        <button @click="previous" type="button" :disabled="currentStepIndex <= 0" :class="{ 'cursor-not-allowed bg-grey-light border-grey-light hover:bg-grey-light hover:border-grey-light': currentStepIndex <= 0, 'bg-grey-lighter hover:bg-grey border-grey-lighter hover:border-grey shadow': currentStepIndex > 0 }" class="flex-no-shrink text-sm border-4 text-black py-1 px-2 rounded mr-2">
                            <mw-navigate-before-icon class="w-3 h-3"></mw-navigate-before-icon>
                            Previous
                        </button>
                        <button @click="next" v-if="currentStepIndex < steps.length-1" type="button" class="flex-no-shrink bg-blue hover:bg-blue-dark border-blue hover:border-blue-dark text-sm border-4 text-white py-1 px-2 rounded shadow" :class="{ 'cursor-not-allowed bg-blue-lighter border-blue-lighter hover:bg-blue-lighter hover:border-blue-lighter shadow-none': !steps[currentStepIndex].completed && currentStepIndex > 0 }" :disabled="!steps[currentStepIndex].completed && currentStepIndex > 0">
                            Next
                            <mw-navigate-next-icon class="w-3 h-3"></mw-navigate-next-icon>
                        </button>
                        <button v-else type="button" @click="finish" class="flex-no-shrink bg-green hover:bg-green-dark border-green hover:border-green-dark text-sm border-4 text-white py-1 px-2 rounded shadow">
                            <mw-checkmark-icon class="w-3 h-3"></mw-checkmark-icon>
                            Finish
                        </button>
                    </div>
                </div>
                <div class="px-8 pt-6 pb-8 mb-4 text-grey-dark text-sm">
                    <component :is="currentStep.component" @complete="markCompleted" @error="markError" />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Welcome from './Welcome.vue';
import License from './License.vue';
import InitialData from './InitialData.vue';
import Installation from './Installation.vue';
import Finished from './Finished.vue';
import { mapMutations } from 'vuex';
export default {
    data: () =>  {
        return {
            steps: [
                { order: 1, name: 'Welcome', completed: false, error: false, component: Welcome },
                { order: 2, name: 'License Agreement', completed: false, error: false, component: License },
                { order: 3, name: 'Initial data', completed: false, error: false, component: InitialData },
                { order: 4, name: 'Installation', completed: false, error: false, component: Installation },
                { order: 5, name: 'Finished', completed: false, error: false, component: Finished },
            ],
            currentStepIndex: 0,
        }
    },
    mounted() {
        axios.post('/api/installed/').then(response => {
            if (response.status == 403) {
                window.location.href = '/';
            }
        }).catch(error => {
            if (error.response.status == 403) {
                window.location.href = '/';
            }
        })
    },
    computed: {
        nextStep() {
            let next = this.steps[this.currentStepIndex].order+1;
            if (next > this.steps[this.steps.length-1].order) {
                return this.currentStepIndex;
            }
            return this.steps.findIndex(s => s.order == next);
        },
        previousStep() {
            let previous = this.steps[this.currentStepIndex].order-1;
            if (previous < 1) {
                return 0;
                
            }
            return this.steps.findIndex(s => s.order == previous);
        },
        currentStep() {
            return this.steps[this.currentStepIndex];
        }
    },
    methods: {
        next() {
            if (this.currentStepIndex == 0) {
                this.steps[0].completed = true;
            }
            if (!this.currentStep.completed) {
                return;
            }
            this.currentStepIndex = this.nextStep;
        },
        previous() {
            this.currentStepIndex = this.previousStep;
        },
        finish() {
            console.log('finish is called')
            this.setWizardPayload(null);
            window.location.href = '/';
        },
        markCompleted(e) {
            this.steps[this.currentStepIndex].completed = e.completed;
            if (e.action == 'auto') {
                this.next();
            }
        },
        markError() {
            this.steps[this.currentStepIndex].error = true;
        },
        ...mapMutations(['setWizardPayload'])
    }
}
</script>