<template>
    <div class="sm:container mx-auto sm:px-4 pt-6 pb-8">
        <div class="sm:flex">
            <div class="bg-white border sm:rounded shadow min-w-full">
                <div class="flex shadow">
                    <div class="text-grey-darker w-1/2 border-r px-2 py-2 font-semibold">
                        <div class="">
                            Date
                        </div>
                    </div>
                    <div class="text-grey-darker w-1/2 border-r px-2 py-2 font-semibold">
                        <div class="">
                            Number of messages
                        </div>
                    </div>
                </div>
                <div class="flex hover:bg-grey-lighter text-sm" v-for="item in dates" :key="item.date">
                    <div class="text-grey-darker w-1/2 border-r p-2">
                        <div class="">
                            <p>{{ item.date }}</p>
                        </div>
                    </div>
                    <div class="text-grey-darker w-1/2 border-r p-2">
                        <div class="">
                            <p>{{ item.id__count }}</p>
                        </div>
                    </div>
                </div>
                <div class="flex shadow border-t-2">
                    <div class="text-grey-darker w-1/2 border-r px-2 py-2 font-semibold">
                        <div class="">
                            Total
                        </div>
                    </div>
                    <div class="text-grey-darker w-1/2 border-r px-2 py-2 font-semibold">
                        <div class="">
                            {{ messageTotalCount }}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import { mapMutations, mapGetters } from 'vuex';
import Form from '../../classes/Form';
export default {
    data: () => {
        return {
            dates: [],
        }
    },
    mounted() {
        this.get();
    },
    computed: {
        activeFilters() {
            return Object.keys(this.filters).filter(key => !!this.filters[key]).reduce((obj, key) => {
                obj[key] = this.filters[key];
                return obj;
            }, {})
        },
        messageTotalCount() {
            let total = 0;
            this.dates.forEach(item => {
                total += item.id__count;
            });
            return total;
        },
        ...mapGetters(['filters'])
    },
    methods: {
        get() {
            this.toggleLoading();
            (new Form(this.activeFilters)).post('/api/reports/messages-by-date/').then(data => {
                this.dates = data;
                this.toggleLoading();
            }).catch(error => {
                //Handle error
                console.log(error);
                this.toggleLoading();
            });
        },
        ...mapMutations(['toggleLoading'])
    }
}
</script>