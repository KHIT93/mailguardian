<template>
    <div>
        <div class="pt-2">

            <div class="pb-1">
                <button @click="whitelist_modal" class="bg-white hover:bg-blue-500 text-blue-600 font-semibold hover:text-white py-1 px-2 border border-blue-500 hover:border-transparent text-xs rounded shadow">
                    <div class="inline-flex content-center">
                        <svg class="fill-current h-3 w-3" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                            <defs>
                                <path d="M0 0h24v24H0V0z" id="a"/>
                            </defs>
                            <clipPath id="b">
                                <use overflow="visible" xlink:href="#a"/>
                            </clipPath>
                            <path clip-path="url(#b)" d="M14 10H2v2h12v-2zm0-4H2v2h12V6zM2 16h8v-2H2v2zm19.5-4.5L23 13l-6.99 7-4.51-4.5L13 14l3.01 3 5.49-5.5z"/>
                        </svg>
                        <span class="pl-1">Add to Whitelist</span>
                    </div>
                </button>
            </div>

            <div>
                <button @click="blacklist_modal" class="bg-white hover:bg-blue-500 text-blue-600 font-semibold hover:text-white py-1 px-2 border border-blue-500 hover:border-transparent text-xs rounded shadow">
                    <div class="inline-flex content-center">
                        <svg class="fill-current h-3 w-3" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path d="M0 0h24v24H0z" fill="none"/>
                            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zM4 12c0-4.42 3.58-8 8-8 1.85 0 3.55.63 4.9 1.69L5.69 16.9C4.63 15.55 4 13.85 4 12zm8 8c-1.85 0-3.55-.63-4.9-1.69L18.31 7.1C19.37 8.45 20 10.15 20 12c0 4.42-3.58 8-8 8z"/>
                        </svg>
                        <span class="pl-1">Add to blacklist</span>
                    </div>
                </button>
            </div>

        </div>
        <mg-modal @close="show_modal = false" :submit-button="false" :show="show_modal" modal-title="View message">
            {{ message_contents }}
        </mg-modal>
    </div>
</template>

<script>
import Form from '../classes/Form';
import { mapMutations } from 'vuex';
export default {
    props: ['uuid', 'direction'],
    data: () => {
        return {
            show_modal: false,
            form: new Form({
                from_address: '',
                to_address: '',
                from_domain: '',
                to_domain: '',
                ip_address: '',
                listing_type: ''
            })
        }
    },
    methods: {
        blacklist_modal() {
            listing_modal('blacklisted');
        },
        whitelist_modal() {
            listing_modal('whitelisted');
        },
        listing_modal(listing_type) {
            
        },
        submit() {
            this.setLoading(true);
            this.form.post('/api/lists/').then(data => {
                this.setLoading(false);
            })
        },
        ...mapMutations(['setLoading'])
    }
}
</script>