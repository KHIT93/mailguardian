<template>
    <div>
        <div class="sm:container mx-auto px-4">
            <div class="flex justify-between" v-if="page_count > 1">
                <button @click="previous_page" class="hidden sm:block bg-grey-light hover:bg-grey text-grey-darkest py-2 px-4 rounded" :class="{'select-none cursor-not-allowed bg-grey-lightest hover:bg-grey-lightest' : current == 1}">
                    Prev
                </button>
                <div v-if="selectedMessages.length > 0">
                    <button @click="mark_spam" type="button" class="flex-no-shrink bg-orange hover:bg-orange-dark border-orange hover:border-orange-dark text-sm border-4 text-white py-1 px-2 rounded shadow">
                        Mark as spam
                    </button>
                    <button @click="mark_non_spam" type="button" class="flex-no-shrink bg-orange hover:bg-orange-dark border-orange hover:border-orange-dark text-sm border-4 text-white py-1 px-2 rounded shadow">
                        Mark as not spam
                    </button>
                    <button @click="release_messages" type="button" class="flex-no-shrink bg-green hover:bg-green-dark border-green hover:border-green-dark text-sm border-4 text-white py-1 px-2 rounded shadow">
                        Release
                    </button>
                </div>
                <button @click="next_page" class="hidden sm:block bg-grey-light hover:bg-grey text-grey-darkest py-2 px-4 rounded" :class="{'select-none cursor-not-allowed bg-grey-lightest hover:bg-grey-lightest' : current == page_count}">
                    Next
                </button>
            </div>
        </div>
        <div class="container mx-auto px-4">
            <div class="bg-white border sm:rounded shadow">
                <mw-message-list-header></mw-message-list-header>
                <div class="flex text-sm break-words items-center p-2" v-if="message_count == 0">
                    <p>There are currently no messages to display</p>
                </div>
                <mw-message-list-entry v-for="item in messages" :key="item.id" :item="item" @click="item.selected = !item.selected" v-else :class="{ 'bg-blue-lighter hover:bg-blue-light': item.selected }"></mw-message-list-entry>
            </div>
        </div>
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
import MessageListHeader from '../../components/MessageListHeader.vue';
import MessageListEntry from '../../components/MessageListEntry.vue';
import Form from '../../classes/Form';
import OperatableMessage from '../../classes/OperatableMessage';
export default {
    components: {
        'mw-message-list-entry': MessageListEntry,
        'mw-message-list-header': MessageListHeader
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
        selectedMessages() {
            return this.messages.filter(message => message.selected == true);
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
            this.messages = [];
            (new Form(this.activeFilters)).post('/api/reports/messages/'+qs).then(data => {
                data.results.forEach(message => {
                    this.messages.push(new OperatableMessage(message));
                });
                
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
        mark_spam() {
            this.toggleLoading();
            axios.post('/api/message-actions/', {action: 'spam', data: this.selectedMessages}).then(response => {
                this.toggleLoading();
                this.get();
            }).catch(error => {
                this.toggleLoading();
                console.log(error);
            });
        },
        mark_non_spam() {
            this.toggleLoading();
            axios.post('/api/message-actions/', {action: 'ham', data: this.selectedMessages}).then(response => {
                this.toggleLoading();
                this.get();
            }).catch(error => {
                this.toggleLoading();
                console.log(error);
            });
        },
        release_messages() {
            this.toggleLoading();
            axios.post('/api/message-actions/', {action: 'release', data: this.selectedMessages}).then(response => {
                this.toggleLoading();
                this.get();
            }).catch(error => {
                this.toggleLoading();
                console.log(error);
            });
        },
        ...mapMutations(['toggleLoading'])
    }
}
</script>
