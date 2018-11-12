<template>
<mg-page>
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
            <div class="card table-wrapper">
                <table class="table text-sm cursor-pointer break-words">
                    <thead>
                        <tr>
                            <th>From</th>
                            <th>To</th>
                            <th class="hidden md:table-cell">Subject</th>
                            <th>Recieved</th>
                            <th class="hidden md:table-cell">Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-if="message_count == 0">
                            <td colspan="5">
                                There are currently no messages to display
                            </td>
                        </tr>
                        <tr v-for="item in messages" :key="item.id" class="text-grey-darker" @click="item.selected = !item.selected" v-else :class="{ 'bg-blue-lighter hover:bg-blue-light': item.selected, 'bg-red': item.is_spam, 'bg-orange': item.is_rbl_listed, 'bg-black text-white': item.blacklisted, 'bg-green-lighter': item.whitelisted }">
                            <td>{{ item.from_address }}</td>
                            <td>{{ item.to_address }}</td>
                            <td class="hidden md:table-cell">{{ item.subject }}</td>
                            <td>{{ item.timestamp }}</td>
                            <td class="hidden md:table-cell">
                                <span v-if="item.is_clean">Clean</span>
                                <template v-else>
                                    <span v-if="item.is_spam">Spam</span>
                                    <span v-if="item.is_rbl_listed">RBL</span>
                                    <span v-if="item.infected">Infected</span>
                                </template>
                                <span v-if="item.blacklisted">Blacklisted</span>
                                <span v-if="item.whitelisted">Whitelisted</span>
                            </td>
                        </tr>
                    </tbody>
                </table>
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
</mg-page>
</template>
<script>
import { mapMutations, mapGetters } from 'vuex';
import Form from '../../classes/Form';
import OperatableMessage from '../../classes/OperatableMessage';
export default {
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
        selectedMessages() {
            return this.messages.filter(message => message.selected == true);
        },
        ...mapGetters(['filters'])
    },
    methods: {
        get(page = null) {
            this.setLoading(true);
            let qs = '';
            if (page) {
                qs = '?page='+page;
            }
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
            axios.post('/api/messages/mark-spam/', { 'messages': this.selectedMessages.map(m => m.id)}).then(response => {
                this.toggleLoading();
                this.get();
            }).catch(error => {
                this.toggleLoading();
                console.log(error);
            });
        },
        mark_non_spam() {
            this.toggleLoading();
            axios.post('/api/messages/mark-nonspam/', { 'messages': this.selectedMessages.map(m => m.id)}).then(response => {
                this.toggleLoading();
                this.get();
            }).catch(error => {
                this.toggleLoading();
                console.log(error);
            });
        },
        release_messages() {
            this.toggleLoading();
            axios.post('/api/messages/release/', { 'messages': this.selectedMessages.map(m => m.id)}).then(response => {
                this.toggleLoading();
                this.get();
            }).catch(error => {
                this.toggleLoading();
                console.log(error);
            });
        },
        ...mapMutations(['toggleLoading', 'setLoading'])
    }
}
</script>
