<template>
<mg-page>
    <div class="md:container mx-auto md:px-4 pt-6 pb-8 xxl:w-1/2">
        <div class="md:flex">
            <div class="w-full md:mr-1">
                <div class="md:flex">
                    <!-- <div class="md:w-1/2 p-2 bg-white border md:rounded shadow mb-2 md:mb-0 md:mr-1"> -->
                    <div class="md:w-1/2 card card-shadow-md mb-2 md:mb-0 md:mr-1 flex justify-between flex-col">
                        <div>
                            <h2 class="font-normal text-lg text-center">Currently applied filters</h2>
                            <hr>
                            <div class="text-sm text-gray-600" v-if="activeFiltersCount == 0">
                                You have not configured any filters. Please use the options below to set some filters
                            </div>
                            <div class="md:flex hover:bg-gray-200 text-sm pb-1" v-for="(value, key) in activeFilters" :key="key" v-else>
                                <div class="md:w-3/4 pt-1">
                                    {{ key.replace('_', ' ') }}&nbsp;{{ filterOptions[key].operators.filter(operator => operator.value == value.operator)[0].label }}&nbsp;{{ value.value }}
                                </div>
                                <div class="md:w-1/4 text-right">
                                    <button role="button" @click="remove_filter(key)" class="bg-red-500 hover:bg-red-600 text-white py-1 px-2 border border-red-500 rounded shadow text-sm no-underline ml-2">
                                        Remove
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div>
                            <h2 class="font-normal text-lg text-center">Statistics</h2>
                            <hr>
                            <div class="flex hover:bg-gray-200 text-sm">
                                <div class="w-1/2">
                                    First message registered:
                                </div>
                                <div class="w-1/2 text-right">
                                    {{ dates.earliest }}
                                </div>
                            </div>
                            <div class="flex hover:bg-gray-200 text-sm">
                                <div class="w-1/2">
                                    Latest message registered:
                                </div>
                                <div class="w-1/2 text-right">
                                    {{ dates.latest }}
                                </div>
                            </div>
                            <div class="flex hover:bg-gray-200 text-sm">
                                <div class="w-1/2">
                                    Messages registered:
                                </div>
                                <div class="w-1/2 text-right">
                                    {{ message_count }}
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- <div class="md:w-1/2 p-2 bg-white border md:rounded shadow mb-2 md:mb-0 md:ml-1"> -->
                    <div class="md:w-1/2 card card-shadow-md mb-2 md:mb-0 md:ml-1">
                        <h2 class="font-normal text-lg text-center">Add a new filter</h2>
                        <hr>
                        <form @submit.prevent="add_filter">
                            <select v-model="filter_form.filter" class="form-select w-full my-1" required>
                                <option value="">Select field to filter on</option>
                                <option v-for="(value, key) in availableFilters" :key="key" :value="key">{{ key.replace('_', ' ') }}</option>
                            </select>
                            <select v-model="filter_form.operator" class="form-select w-full my-1" required>
                                <option value="">Select filter operator</option>
                                <option v-for="option in selectedFilterOptions.operators" :key="option.value" :value="option.value">{{ option.label }}</option>
                            </select>
                            <input class="form-input w-full my-1" name="value" v-model="filter_form.value" id="value" :type="selectedFilterType" placeholder="Value to filter by">
                            <div class="flex flex-row-reverse">
                                <button type="submit" class="btn btn-blue shadow">
                                    Add
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
        <div class="md:mr-1 mt-2 card">
            <h2 class="font-normal text-lg text-center">Reports</h2>
            <hr>
            <div v-if="message_count == 0"><p class="text-gray-500 text-sm text-center">There are no messages that match your query</p></div>
            <div v-else>
                <router-link class="block border-t px-4 py-2 hover:bg-gray-200 no-underline text-gray-800" to="/reports/messages">
                    See all messages<br/>
                    <span class=" text-xs text-gray-600">View all messages that match your filtering</span>
                </router-link>
                <router-link class="block border-t px-4 py-2 hover:bg-gray-200 no-underline text-gray-800" to="/reports/message-operations">
                    Perform message operations<br/>
                    <span class=" text-xs text-gray-600">Perform operations like marking as spam or releasing multiple messages at one time</span>
                </router-link>
                <router-link class="block border-t px-4 py-2 hover:bg-gray-200 no-underline text-gray-800" to="/reports/messages-by-date">
                    Total messages by date<br/>
                    <span class=" text-xs text-gray-600">Show total messages sorted by date for the selected filtering</span>
                </router-link>
                <router-link class="block border-t px-4 py-2 hover:bg-gray-200 no-underline text-gray-800" to="/reports/messages-per-hour">
                    Messages per hour in the last 24 hours<br/>
                    <span class=" text-xs text-gray-600">Show how many messages that have been processed each hour during the last day</span>
                </router-link>
                <router-link class="block border-t px-4 py-2 hover:bg-gray-200 no-underline text-gray-800" to="/reports/top-mail-relays">
                    Top 10 mail relays<br/>
                    <span class=" text-xs text-gray-600">Show the top 10 mail relays</span>
                </router-link>
                <router-link class="block border-t px-4 py-2 hover:bg-gray-200 no-underline text-gray-800" to="/reports/top-senders-by-quantity">
                    Top 10 senders by quantity<br/>
                    <span class=" text-xs text-gray-600">Show the top 10 senders based on how many emails has been recieved from them</span>
                </router-link>
                <router-link class="block border-t px-4 py-2 hover:bg-gray-200 no-underline text-gray-800" to="/reports/top-senders-by-volume">
                    Top 10 senders by volume<br/>
                    <span class=" text-xs text-gray-600">Show the top 10 senders based on how much data they has been recieved from them</span>
                </router-link>
                <router-link class="block border-t px-4 py-2 hover:bg-gray-200 no-underline text-gray-800" to="/reports/top-recipients-by-quantity">
                    Top 10 recipients by quantity<br/>
                    <span class=" text-xs text-gray-600">Show the top 10 recipients based on how many emails they have recieved</span>
                </router-link>
                <router-link class="block border-t px-4 py-2 hover:bg-gray-200 no-underline text-gray-800" to="/reports/top-recipients-by-volume">
                    Top 10 recipients by volume<br/>
                    <span class=" text-xs text-gray-600">Show the top 10 recipients based on how much data they have recieved</span>
                </router-link>
                <router-link class="block border-t px-4 py-2 hover:bg-gray-200 no-underline text-gray-800" to="/reports/top-sender-domains-by-quantity">
                    Top 10 sender domains by quantity<br/>
                    <span class=" text-xs text-gray-600">Show the top 10 sender domains based on how many emails has been recieved from them</span>
                </router-link>
                <router-link class="block border-t px-4 py-2 hover:bg-gray-200 no-underline text-gray-800" to="/reports/top-sender-domains-by-volume">
                    Top 10 sender domains by volume<br/>
                    <span class=" text-xs text-gray-600">Show the top 10 sender domains based on how much data has been recieved from them</span>
                </router-link>
                <router-link class="block border-t px-4 py-2 hover:bg-gray-200 no-underline text-gray-800" to="/reports/top-recipient-domains-by-quantity">
                    Top 10 recipient domains by quantity<br/>
                    <span class=" text-xs text-gray-600">Show the top 10 recipient domains based on how many emails they have recieved</span>
                </router-link>
                <router-link class="block border-t px-4 py-2 hover:bg-gray-200 no-underline text-gray-800" to="/reports/top-recipient-domains-by-volume">
                    Top 10 recipient domains by volume<br/>
                    <span class=" text-xs text-gray-600">Show the top 10 recipient domains based on how much data they have recieved</span>
                </router-link>
                <!-- <div class="hover:bg-gray-200 text-sm">
                    <router-link to="/reports/sa-score-distribution">SpamAssassin score distribution</router-link>
                </div>
                <div class="hover:bg-gray-200 text-sm">
                    <router-link to="/reports/sa-rule-hits">Spam rule hits</router-link>
                </div> -->
            </div>
        </div>
    </div>
</mg-page>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex';
import Form from '../../classes/Form';
export default {
    data: () => {
        return {
            dates: {
                latest: null,
                earliest: null
            },
            message_count: 0,
            filter_form: new Form({
                filter: '',
                operator: '',
                value: ''
            })
        }
    },
    created() {
        this.get();
    },
    computed: {
        activeFiltersCount() {
            return Object.keys(this.activeFilters).length;
        },
        activeFilters() {
            return Object.keys(this.filters).filter(key => !!this.filters[key]).reduce((obj, key) => {
                obj[key] = this.filters[key];
                return obj;
            }, {})
        },
        availableFilters() {
            return Object.keys(this.filters).filter(key => this.filters[key] == null ).reduce((obj, key) => {
                obj[key] = this.filters[key];
                return obj;
            }, {})
        },
        selectedFilterOptions() {
            if (this.filter_form.filter == '') {
                return {};
            }
            else {
                return this.filterOptions[this.filter_form.filter];
            }
        },
        selectedFilterType() {
            if (this.selectedFilterOptions.field_type == 'boolean') {
                return 'hidden';
            }
            else {
                return this.selectedFilterOptions.field_type;
            }
        },
        ...mapGetters(['filters', 'filterOptions', 'isLoggedIn', 'loading', 'user'])
    },
    methods: {
        get() {
            this.setLoading(true);
            (new Form(this.activeFilters)).post('/api/reports/summary/').then(data => {
                this.dates.latest = new Date(data.latest).toLocaleDateString();
                this.dates.earliest = new Date(data.earliest).toLocaleDateString();
                this.message_count = data.count;
                this.toggleLoading();
            }).catch(error => {
                //Handle error
                console.log(error);
                this.toggleLoading();
            });
        },
        add_filter() {
            console.log('Adding filter');
            this.$store.commit('setFilter', {
                field: this.filter_form.filter,
                operator: this.filter_form.operator,
                value: this.filter_form.value 
            });
            this.filter_form.reset();
            this.get();
        },
        remove_filter(filter) {
            this.removeFilter(filter);
            this.get();
        },
        ...mapMutations(['toggleLoading', 'resetFilters', 'setFilter', 'removeFilter', 'setLoading'])
    }
}
</script>
