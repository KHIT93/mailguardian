<template>
    <div>
        <div class="sm:container mx-auto px-4">
            <div class="flex justify-between" v-if="page_count > 1">
                <button @click="previous_page" class="bg-grey-light hover:bg-grey text-grey-darkest py-2 px-4 rounded" :class="{'select-none cursor-not-allowed bg-grey-lightest hover:bg-grey-lightest' : current == 1}">
                    Prev
                </button>
                <button @click="next_page" class="bg-grey-light hover:bg-grey text-grey-darkest py-2 px-4 rounded" :class="{'select-none cursor-not-allowed bg-grey-lightest hover:bg-grey-lightest' : current == page_count}">
                    Next
                </button>
            </div>
        </div>
        <mg-message-list :messages="messages" :count="message_count" class="sm:px-4"></mg-message-list>
        <div class="container mx-auto px-4">
            <div class="flex justify-between" v-if="page_count > 1">
                <button @click="previous_page" class="bg-grey-light hover:bg-grey text-grey-darkest py-2 px-4 rounded" :class="{'select-none cursor-not-allowed bg-grey-lightest hover:bg-grey-lightest' : current == 1}">
                    Prev
                </button>
                <button @click="next_page" class="bg-grey-light hover:bg-grey text-grey-darkest py-2 px-4 rounded" :class="{'select-none cursor-not-allowed bg-grey-lightest hover:bg-grey-lightest' : current == page_count}">
                    Next
                </button>
            </div>
        </div>
    </div>
</template>
<script>
import { mapMutations, mapGetters } from 'vuex';
import MessageList from '../../components/MessageList.vue';
import Form from '../../classes/Form';
export default {
    components: {
        'mg-message-list': MessageList
    },
    data: () => {
        return {
            messages: [],
            message_count: 0,
            next: null,
            previous: null,
            current: null,
            page_count: null
        }
    },
    created() {
        this.get();
    },
    computed: {
        activeFilters() {
            return Object.keys(this.filters).filter(key => !!this.filters[key]).reduce((obj, key) => {
                obj[key] = this.filters[key];
                return obj;
            }, {})
        },
        ...mapGetters(['filters'])
    },
    methods: {
        get(page = null) {
            let qs = '';
            if (page) {
                qs = '?page='+page;
            }
            this.toggleLoading();
            (new Form(this.activeFilters)).post('/api/reports/messages/'+qs).then(data => {
                this.messages = data.results;
                this.message_count = data.count;
                this.next = data.next;
                this.previous = data.previous;
                this.current = data.current;
                this.page_count = data.page_count;
                this.toggleLoading();
            }).catch(error => {
                //Handle error
                console.log(error);
                this.toggleLoading();
            });
        },
        next_page() {
            if (this.next) {
                this.get(this.next.split("?page=")[1]);
            }
        },
        previous_page() {
            if (this.previous) {
                this.get(this.previous.split("?page=")[1]);
            }
        },
        ...mapMutations(['toggleLoading'])
    }
}
</script>