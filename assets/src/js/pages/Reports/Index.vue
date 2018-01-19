<template>
    <div class="container mx-auto sm:px-4 pt-6 pb-8">
        <div class="sm:flex">
            <div class="sm:w-2/3 sm:mr-1">
                <div class="sm:flex">
                    <div class="sm:w-1/2 p-2 bg-white border sm:rounded shadow mb-2 sm:mb-0 sm:mr-1">
                        <h2 class="font-normal text-lg text-center">Currently applied filters</h2>
                        <hr>
                        <div class="text-sm text-grey-dark" v-if="activeFiltersCount == 0">
                            You have not configured any filters. Please use the options below to set some filters
                        </div>
                        <div class="sm:flex hover:bg-grey-lighter text-sm pb-1" v-for="(value, key) in activeFilters" :key="key" v-else>
                            <div class="sm:w-3/4 pt-1">
                                {{ key.replace('_', ' ') }}&nbsp;{{ filterOptions[key].operators.filter(operator => operator.value == value.operator)[0].label }}&nbsp;{{ value.value }}
                            </div>
                            <div class="sm:w-1/4 text-right">
                                <button role="button" @click="remove_filter(key)" class="bg-red hover:bg-red-dark text-white py-1 px-2 border border-red-light rounded shadow text-sm no-underline ml-2">
                                    Remove
                                </button>
                            </div>
                        </div>
                    </div>
                    <div class="sm:w-1/2 p-2 bg-white border sm:rounded shadow mb-2 sm:mb-0 sm:ml-1">
                        <h2 class="font-normal text-lg text-center">Add a new filter</h2>
                        <hr>
                        <form @submit.prevent="add_filter">
                            <div class="relative">
                                <select v-model="filter_form.filter" class="block appearance-none w-full bg-grey-lighter hover:border-blue border border-grey-lighter text-grey-darker py-2 px-4">
                                    <option value="">Select field to filter on</option>
                                    <option v-for="(value, key) in availableFilters" :key="key" :value="key">{{ key.replace('_', ' ') }}</option>
                                </select>
                                <div class="pointer-events-none absolute pin-y pin-r flex items-center px-2 text-grey-darker">
                                    <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                                </div>
                            </div>
                            <hr>
                            <div class="relative">
                                <select v-model="filter_form.operator" class="block appearance-none w-full bg-grey-lighter hover:border-blue border border-grey-lighter text-grey-darker py-2 px-4">
                                    <option value="">Select filter operator</option>
                                    <option v-for="option in selectedFilterOptions.operators" :key="option.value" :value="option.value">{{ option.label }}</option>
                                </select>
                                <div class="pointer-events-none absolute pin-y pin-r flex items-center px-2 text-grey-darker">
                                    <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                                </div>
                            </div>
                            <hr>
                            <div class="">
                                <input class="bg-grey-lighter appearance-none border border-grey-lighter hover:border-blue rounded w-full py-2 px-4 text-grey-darker" name="value" v-model="filter_form.value" id="value" :type="selectedFilterType" placeholder="Value to filter by">
                            </div>
                            <hr>
                            <div class="flex flex-row-reverse">
                                <button type="submit" class="flex-no-shrink bg-blue hover:bg-blue-dark border-blue hover:border-blue-dark text-sm border-4 text-white py-1 px-2 rounded shadow">
                                    Add
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
            <div class="sm:w-1/3 p-2 bg-white border sm:rounded shadow mb-2 sm:mb-0 sm:ml-1">
                <h2 class="font-normal text-lg text-center">Statistics</h2>
                <hr>
                <div class="sm:flex hover:bg-grey-lighter text-sm">
                    <div class="sm:w-1/2">
                        First message registered:
                    </div>
                    <div class="sm:w-1/2 text-right">
                        {{ dates.earliest }}
                    </div>
                </div>
                <div class="sm:flex hover:bg-grey-lighter text-sm">
                    <div class="sm:w-1/2">
                        Latest message registered:
                    </div>
                    <div class="sm:w-1/2 text-right">
                        {{ dates.latest }}
                    </div>
                </div>
                <div class="sm:flex hover:bg-grey-lighter text-sm">
                    <div class="sm:w-1/2">
                        Messages registered:
                    </div>
                    <div class="sm:w-1/2 text-right">
                        {{ message_count }}
                    </div>
                </div>
                <hr>
                <h2 class="font-normal text-lg text-center">Reports</h2>
                <hr>
                <div class="hover:bg-grey-lighter text-sm">
                    <router-link to="/reports/messages">See all messages</router-link>
                </div>
                <div class="hover:bg-grey-lighter text-sm">
                    <router-link to="/reports/message-operations">Perform message operations</router-link>
                </div>
                <div class="hover:bg-grey-lighter text-sm">
                    <router-link to="/reports/messages-by-date">Total messages by date</router-link>
                </div>
                <div class="hover:bg-grey-lighter text-sm">
                    <router-link to="/reports/top-mail-relays">Top 10 mail relays</router-link>
                </div>
                <div class="hover:bg-grey-lighter text-sm">
                    <router-link to="/reports/sa-rule-hits">Spam rule hits</router-link>
                </div>
            </div>
        </div>
    </div>
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
    mounted() {
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
        ...mapGetters(['filters', 'filterOptions', 'isLoggedIn', 'loading'])
    },
    methods: {
        get() {
            this.toggleLoading();
            (new Form(this.activeFilters)).post('/api/reports/summary/').then(data => {
                this.dates.latest = data.latest;
                this.dates.earliest = data.earliest;
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
            //this.get();
        },
        ...mapMutations(['toggleLoading', 'resetFilters', 'setFilter', 'removeFilter'])
    }
}
</script>
