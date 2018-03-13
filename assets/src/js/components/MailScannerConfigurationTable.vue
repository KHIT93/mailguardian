<template>
    <div>
        <div class="flex text-sm shadow">
            <div class="text-grey-darker w-1/3 p-2">
                <div class="font-semibold">
                    Key
                </div>
            </div>
            <div class="text-grey-darker w-1/3 p-2">
                <div class="font-semibold">
                    Value
                </div>
            </div>
            <div class="text-grey-darker w-1/3 p-2">
                <div class="font-semibold">
                    File
                </div>
            </div>
        </div>
        <div class="shadow">
            <div class="flex hover:bg-grey-lighter text-sm cursor-pointer" v-for="item in list.results" :key="item.id" @click="details(item.id)">
                <div class="text-grey-darker w-1/3 p-2 overflow-hidden">
                    <div class="">
                        {{ item.key }}
                    </div>
                </div>
                <div class="text-grey-darker w-1/3 p-2 overflow-hidden">
                    <div class="">
                        {{ item.value }}
                    </div>
                </div>
                <div class="text-grey-darker w-1/3 p-2 overflow-hidden">
                    <div class="">
                        {{ item.filepath }}
                    </div>
                </div>
            </div>
        </div>
        <div class="inline-flex pt-2 rounded">
            <button @click="previous" class="bg-grey-light hover:bg-grey text-grey-darkest py-2 px-4 rounded-l" :class="{'select-none cursor-not-allowed bg-grey-lightest hover:bg-grey-lightest' : list.current == 1}">
                Prev
            </button>
            <!-- <button class="bg-grey-light hover:bg-grey text-grey-darkest py-2 px-4">
                1
            </button>
            <button class="bg-grey-light hover:bg-grey text-grey-darkest py-2 px-4">
                2
            </button>
            <button class="bg-grey-light hover:bg-grey text-grey-darkest py-2 px-4">
                3
            </button> -->
            <button @click="next" class="bg-grey-light hover:bg-grey text-grey-darkest py-2 px-4 rounded-r" :class="{'select-none cursor-not-allowed bg-grey-lightest hover:bg-grey-lightest' : list.current == list.page_count}">
                Next
            </button>
        </div>
    </div>
</template>

<script>
import router from '../routing/router';
export default {
    props: ['list'],
    data: () => {
        return {
            search_key: ""
        }
    },
    methods: {
        previous() {
            if (this.list.previous) {
                this.$emit('previous');                
            }
        },
        next() {
            if (this.list.next) {
                this.$emit('next');
            }
        },
        details(id) {
            router.push('/admin/mailscanner/configuration/'+id);
        }
    }
}
</script>
