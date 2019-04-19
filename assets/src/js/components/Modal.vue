<template>
    <!-- show container -->
    <div class="fixed pin z-40 overflow-auto bg-smoke-500" :class="{'hidden' : !show, 'flex': show}">
        <!-- show dialog -->
        <div class="relative bg-white w-full max-w-md m-auto flex-col flex rounded">
            <!-- show content -->
            <div class="px-6 py-4">
                <!-- show header -->
                <div class="font-bold text-xl mb-2">
                    {{modalTitle}}
                </div>
                <!-- show body -->
                <p class="text-gray-700 text-base">
                    <slot>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus quia, nulla! Maiores et perferendis eaque, exercitationem praesentium nihil.</slot>
                </p>
            </div>
            <!-- show footer -->
            <div class="px-6 py-4 border-t bg-gray-100 rounded-b">
                <div class="flex flex-row-reverse">
                    <slot name="footer">
                        <button v-if="closeButton" type="button" @click="close" class="bg-white hover:bg-gray-200 text-gray-800 py-2 px-4 border border-gray-400 rounded shadow ml-1">{{closeButtonText}}</button>
                        <button v-if="submitButton" type="button" @click="submit" class="bg-blue-500 hover:bg-blue-500 text-white py-2 px-4 border border-gray-400 rounded shadow mr-1">{{submitButtonText}}</button>
                    </slot>
                </div>
            </div>
            <span class="absolute top-0 bottom-0 right-0 p-4" @click="close" v-if="closeIcon">
                <svg class="h-4 w-4 text-gray-500 hover:text-gray-800" role="button" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                    <path d="M0 0h24v24H0z" fill="none"/>
                </svg>
            </span>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        closeIcon: {
            type: Boolean,
            default: () => {
                return false;
            }
        },
        closeButton: {
            type: Boolean,
            default: () => {
                return true;
            }
        },
        submitButton: {
            type: Boolean,
            default: () => {
                return true;
            }
        },
        modalTitle: {
            type: String,
            default: () => {
                return "Modal";
            }
        },
        closeButtonText: {
            type: String,
            default: () => {
                return "Close";
            }
        },
        submitButtonText: {
            type: String,
            default: () => {
                return "Submit";
            }
        },
        show: Boolean
    },
    methods: {
        close() {
            this.$emit('close');
        },
        submit() {
            this.$emit('submit');
        }
    }
}
</script>

