<template>
<mg-page>
    <div>
        <div class="sm:container mx-auto px-4">
            <div class="flex justify-between">
                <button @click="previous_page" v-if="page_count > 1" class="hidden sm:block bg-gray-400 hover:bg-gray-500 text-gray-800 py-2 px-4 rounded" :class="{'select-none cursor-not-allowed bg-gray-100 hover:bg-gray-100' : current == 1}">
                    Prev
                </button>
                <div v-if="selectedMessages.length > 0">
                    <button @click="mark_spam" type="button" class="flex-shrink-0 bg-orange-500 hover:bg-orange-600 border-orange-500 hover:border-orange-600 text-sm border-4 text-white py-1 px-2 rounded shadow">
                        Mark as spam
                    </button>
                    <button @click="mark_non_spam" type="button" class="flex-shrink-0 bg-orange-500 hover:bg-orange-600 border-orange-500 hover:border-orange-600 text-sm border-4 text-white py-1 px-2 rounded shadow">
                        Mark as not spam
                    </button>
                    <button @click="release_messages" type="button" class="flex-shrink-0 bg-green-500 hover:bg-green-600 border-green-500 hover:border-green-600 text-sm border-4 text-white py-1 px-2 rounded shadow">
                        Release
                    </button>
                </div>
                <button @click="next_page" v-if="page_count > 1" class="hidden sm:block bg-gray-400 hover:bg-gray-500 text-gray-800 py-2 px-4 rounded" :class="{'select-none cursor-not-allowed bg-gray-100 hover:bg-gray-100' : current == page_count}">
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
                        <tr v-for="item in messages" :key="item.id" class="text-gray-700" @click="item.selected = !item.selected" v-else :class="{ 'bg-blue-200 hover:bg-blue-500': item.selected, 'bg-red-500': item.is_spam, 'bg-orange-500': item.is_rbl_listed, 'bg-gray-900 text-white': item.blocked, 'bg-green-200': item.allowed }">
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
                                <span v-if="item.blocked">blocked</span>
                                <span v-if="item.allowed">allowed</span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <div class="container mx-auto px-4">
            <div class="flex justify-between" v-if="page_count > 1">
                <button @click="previous_page" class="bg-gray-400 hover:bg-gray-500 text-gray-800 py-2 px-4 rounded" :class="{'select-none cursor-not-allowed bg-gray-100 hover:bg-gray-100' : current == 1}">
                    Prev
                </button>
                <button @click="next_page" class="bg-gray-400 hover:bg-gray-500 text-gray-800 py-2 px-4 rounded" :class="{'select-none cursor-not-allowed bg-gray-100 hover:bg-gray-100' : current == page_count}">
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
