<template>
    <div class="table-wrapper">
        <table class="table text-sm">
            <thead>
                <tr>
                    <th>Key</th>
                    <th>Value</th>
                    <th>File</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <mg-mailscanner-configuration-item :item="item" v-for="item in list.results" :key="item.id" @saved="saved()"></mg-mailscanner-configuration-item>
            </tbody>
        </table>
        <div class="inline-flex pt-2 rounded">
            <button @click="previous" class="btn rounded-none rounded-l" :class="{'select-none cursor-not-allowed btn-grey-lightest' : list.current == 1, 'btn-grey-light' : list.current != 1}">
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
            <button @click="next" class="btn rounded-none rounded-r" :class="{'select-none cursor-not-allowed btn-grey-lightest' : list.current == list.page_count, 'btn-grey-light' : list.current != list.page_count}">
                Next
            </button>
        </div>
    </div>
</template>

<script>
import router from '../routing/router';
import MailScannerConfigurationItem from './MailScannerConfigurationItem.vue';
export default {
    props: ['list'],
    data: () => {
        return {
            search_key: ""
        }
    },
    components: {
        'mg-mailscanner-configuration-item': MailScannerConfigurationItem
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
        saved() {
            this.$emit('saved');
        }
    }
}
</script>
