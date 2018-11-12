<template>
    <form @submit.prevent="submit_list" class="h-full">
        <h2 class="p-2 text-center">Add {{listingType}} entry</h2>
        <div class="px-4">
            <div class="md:flex md:items-center mb-6">
                <div class="md:w-1/4">
                    <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="from_select">
                        I want to make a listing based on
                    </label>
                </div>
                <div class="md:w-3/4">
                    <div class="relative">
                        <select v-model="listing_choice_from" @change="from_reset" name="from_select" class="form-select">
                            <option value="">-- Select --</option>
                            <option value="from_address">Senders email address or domain</option>
                            <option value="from_ip_address">Senders IP-address</option>
                        </select>
                        <div class="form-select-icon">
                            <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="md:flex md:items-center mb-6 px-4" v-if="listing_choice_from == 'from_address'">
            <div class="md:w-1/4">
                <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="from_address">
                    From
                </label>
            </div>
            <div class="md:w-3/4 inline-flex">
                <input class="bg-grey-lighter appearance-none border border-grey-lighter hover:border-blue rounded py-2 px-4 text-grey-darker" name="from_address" v-model="from" id="from_address" type="text" placeholder="JaneDoe">
                <span class="select-none bg-grey-lighter appearance-none border border-grey-lighter py-2 px-4 text-grey-darker">@</span>
                <input class="bg-grey-lighter appearance-none border border-grey-lighter hover:border-blue w-full rounded py-2 px-4 text-grey-darker" name="from_domain" v-model="from_domain" id="from_domain" type="text" placeholder="example.com">
            </div>
        </div>

        <div class="md:flex md:items-center mb-6 px-4" v-if="listing_choice_from == 'from_ip_address'">
            <div class="md:w-1/4">
                <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="from_ip_address">
                    From
                </label>
            </div>
            <div class="md:w-3/4">
                <input class="form-input" name="from_ip_address" v-model="from_ip_address" id="from_ip_address" type="text" placeholder="111.222.333.444">
            </div>
        </div>

        <div class="px-4">
            <div class="md:flex md:items-center mb-6">
                <div class="md:w-1/4">
                    <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="to_select">
                        I want to make a listing based on
                    </label>
                </div>
                <div class="md:w-3/4">
                    <div class="relative">
                        <select v-model="listing_choice_to" @change="to_reset" name="to_select" class="form-select">
                            <option value="">-- Select --</option>
                            <option value="to_address">Recipients email address or domain</option>
                            <option value="to_ip_address">Recipients IP-address</option>
                        </select>
                        <div class="form-select-icon">
                            <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="md:flex md:items-center mb-6 px-4" v-if="listing_choice_to == 'to_address'">
            <div class="md:w-1/4">
                <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="to_address">
                    To
                </label>
            </div>
            <div class="md:w-3/4 inline-flex">
                <input class="bg-grey-lighter appearance-none border border-grey-lighter hover:border-blue rounded py-2 px-4 text-grey-darker" name="to_address" v-model="to" id="to_address" type="text" placeholder="JohnDoe">
                <span class="select-none bg-grey-lighter appearance-none border border-grey-lighter py-2 px-4 text-grey-darker">@</span>
                <input class="form-input" name="to_domain" v-model="to_domain" id="to_domain" type="text" placeholder="example.com">                    
            </div>
        </div>

        <div class="md:flex md:items-center mb-6 px-4" v-if="listing_choice_to == 'to_ip_address'">
            <div class="md:w-1/4">
                <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="to_ip_address">
                    To
                </label>
            </div>
            <div class="md:w-3/4">
                <input class="form-input" name="to_ip_address" v-model="to_ip_address" id="to_ip_address" type="text" placeholder="111.222.333.444">
            </div>
        </div>
        <div class="px-6 py-4 border-t bg-grey-lightest rounded-b">
            <div class="flex flex-row-reverse">
                <button type="button" @click.prevent="$emit('close')" class="btn btn-grey-lightest shadow">Cancel</button>
                <button type="submit" class="btn btn-blue shadow mr-2">Save</button>
            </div>
        </div>
    </form>
</template>
<script>
import Form from '../classes/Form';
import { mapMutations } from 'vuex';
export default {
    props: {
        listingType: {
            type: String,
            required: true
        },
        fromAddress: {
            type: String,
            default: ''
        },
        toAddress: {
            type: String,
            default: ''
        },
        fromChoice: {
            default: ''
        },
        toChoice: {
            default: ''
        }
    },
    data: () => {
        return {
            form: new Form({
                from_address: '',
                to_address: '',
                listing_type: this.listingType
            }),
            listing_choice_from: '',
            listing_choice_to: '',
            from_ip_address: '',
            to_ip_address: '',
            from_domain: '',
            to_domain: '',
            from: '',
            to: ''
        }
    },
    mounted() {
        this.listing_choice_from = (this.fromChoice && this.fromChoice != '') ? this.fromChoice : '';
        this.listing_choice_to = (this.toChoice && this.toChoice != '') ? this.toChoice : '';
        this.from_domain = (this.fromAddress && this.fromAddress.includes('@')) ? this.fromAddress.split('@')[1] : '';
        this.from = (this.fromAddress && this.fromAddress.includes('@')) ? this.fromAddress.split('@')[0] : '';
        this.to_domain = (this.toAddress && this.toAddress.includes('@')) ? this.toAddress.split('@')[1] : '';
        this.to = (this.toAddress && this.toAddress.includes('@')) ? this.toAddress.split('@')[0] : '';
    },
    computed: {
        from_address() {
            if (this.from_ip_address && this.from_ip_address != '') {
                return this.from_ip_address;
            }
            else {
                return this.from + '@' + this.from_domain;
            }
        },
        to_address() {
            if (this.to_ip_address && this.to_ip_address != '') {
                return this.to_ip_address;
            }
            else {
                return this.to + '@' + this.to_domain;
            }
        }
    },
    methods: {
        submit_list() {
            this.form.from_address = this.from_address;
            this.form.to_address = this.to_address;
            this.form.listing_type = this.listingType;
            this.form.post('/api/lists/').then(() => {
                this.$emit('close');
                this.notify(this.createNotification('Entry created', `A ${this.listingType} entry has been created for email from ${this.form.from_address} to ${this.form.to_address}`, 'success'));
            }).catch(error => {
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        from_reset() {
            this.from_ip_address = '';
            this.from_domain = '';
            this.from = '';
        },
        to_reset() {
            this.to_ip_address = '';
            this.to_domain = '';
            this.to = '';
        },
        ...mapMutations(['notify'])
    }
}
</script>
