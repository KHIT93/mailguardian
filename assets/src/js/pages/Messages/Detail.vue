<template>
<mg-page>
    <div class="sm:container mx-auto sm:px-4 pt-6 pb-8">
        <div class="card sm:p-2">
            <h2 class="border-b">Details for message <em>{{ uuid }}</em></h2>
            <mg-message-actions @view="showMessage" @release="release" @spam="spam" @nonspam="nonspam" class="border-b" :uuid="uuid" v-if="file_exists"></mg-message-actions>
            <div class="sm:flex">
                <div class="sm:w-1/2 sm:border-r border-b">
                    <div class="flex hover:bg-gray-200 text-sm">
                        <div class="text-gray-700 w-1/2 sm:w-1/6 p-2">
                            <div class="font-semibold">
                                From:
                            </div>
                        </div>
                        <div class="text-gray-700 w-1/2 sm:w-5/6 p-2">
                            <div class="flex hover:bg-gray-200 text-sm">
                                <div class="text-gray-700">
                                    {{ message.from_address }}
                                </div>
                            </div>
                            <div class="sm:flex hover:bg-gray-200 text-sm pt-2">
                                <div class="text-gray-700 sm:w-1/2">
                                    <div class="font-semibold">
                                        Recieved from:
                                    </div>
                                </div>
                                <div class="text-gray-700 sm:w-1/2">
                                    <div class="">
                                        {{ message.client_ip }}<br/>
                                        <span v-if="client_country">({{ client_country }})</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="py-2 flex">
                        <div class="pr-1">
                            <button @click="createListing(message.from_address, message.to_address, 'allowed')" class="btn btn-xs btn-blue-outline font-semibold shadow">
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
                                    <span class="pl-1">Add to allowlist</span>
                                </div>
                            </button>
                        </div>

                        <div>
                            <button @click="createListing(message.from_address, message.to_address, 'blocked')" class="btn btn-xs btn-blue-outline font-semibold shadow">
                                <div class="inline-flex content-center">
                                    <svg class="fill-current h-3 w-3" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M0 0h24v24H0z" fill="none"/>
                                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zM4 12c0-4.42 3.58-8 8-8 1.85 0 3.55.63 4.9 1.69L5.69 16.9C4.63 15.55 4 13.85 4 12zm8 8c-1.85 0-3.55-.63-4.9-1.69L18.31 7.1C19.37 8.45 20 10.15 20 12c0 4.42-3.58 8-8 8z"/>
                                    </svg>
                                    <span class="pl-1">Add to blocklist</span>
                                </div>
                            </button>
                        </div>
                    </div>
                </div>

                <div class="sm:w-1/2 border-b">
                    <div class="flex hover:bg-gray-200 text-sm">
                        <div class="text-gray-700 w-1/2 sm:w-1/6 p-2">
                            <div class="font-semibold">
                                To:
                            </div>
                        </div>
                        <div class="text-gray-700 w-1/2 sm:w-5/6 p-2">
                            <div class="flex hover:bg-gray-200 text-sm">
                                <div class="text-gray-700">
                                    {{ message.to_address }}
                                </div>
                            </div>
                            <div class="sm:flex hover:bg-gray-200 text-sm pt-2">
                                <div class="text-gray-700 sm:w-1/2">
                                    <div class="font-semibold">
                                        Processed by:
                                    </div>
                                </div>
                                <div class="text-gray-700 sm:w-1/2">
                                    <div class="">
                                        {{ message.mailscanner_hostname }}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="py-2 flex">
                        <div class="pr-1">
                            <button @click="createListing(message.to_address, message.from_address, 'allowed')" class="btn btn-xs btn-blue-outline font-semibold shadow">
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
                                    <span class="pl-1">Add to allowlist</span>
                                </div>
                            </button>
                        </div>

                        <div>
                            <button @click="createListing(message.to_address, message.from_address, 'blocked')" class="btn btn-xs btn-blue-outline font-semibold shadow">
                                <div class="inline-flex content-center">
                                    <svg class="fill-current h-3 w-3" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M0 0h24v24H0z" fill="none"/>
                                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zM4 12c0-4.42 3.58-8 8-8 1.85 0 3.55.63 4.9 1.69L5.69 16.9C4.63 15.55 4 13.85 4 12zm8 8c-1.85 0-3.55-.63-4.9-1.69L18.31 7.1C19.37 8.45 20 10.15 20 12c0 4.42-3.58 8-8 8z"/>
                                    </svg>
                                    <span class="pl-1">Add to blocklist</span>
                                </div>
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="sm:flex">
                <div class="sm:w-1/2 sm:border-r border-b">
                    <div class="flex hover:bg-gray-200 text-sm">
                        <div class="text-gray-700 w-1/2 sm:w-1/4 p-2">
                            <div class="font-semibold">
                                Subject:
                            </div>
                        </div>
                        <div class="text-gray-700 w-1/2 sm:w-3/4 p-2">
                            <div class="">
                                {{ message.subject }}
                            </div>
                        </div>
                    </div>

                    <div class="flex hover:bg-gray-200 text-sm">
                        <div class="text-gray-700 w-1/2 sm:w-1/4 p-2">
                            <div class="font-semibold">
                                Recieved:
                            </div>
                        </div>
                        <div class="text-gray-700 w-1/2 sm:w-3/4 p-2">
                            <div class="">
                                {{ new Date(message.timestamp).toLocaleString() }}
                            </div>
                        </div>
                    </div>

                    <div class="flex hover:bg-gray-200 text-sm">
                        <div class="text-gray-700 w-1/2 sm:w-1/4 p-2">
                            <div class="font-semibold">
                                Size:
                            </div>
                        </div>
                        <div class="text-gray-700 w-1/2 sm:w-3/4 p-2">
                            <div class="">
                                {{ message.size | byte_display }}
                            </div>
                        </div>
                    </div>

                    <div class="flex hover:bg-gray-200 text-sm">
                        <div class="text-gray-700 w-1/2 sm:w-1/4 p-2">
                            <div class="font-semibold">
                                Spam score:
                            </div>
                        </div>
                        <div class="text-gray-700 w-1/2 sm:w-3/4 p-2">
                            <div class="">
                                {{ message.spam_score }}
                            </div>
                        </div>
                    </div>
                    <div class="flex hover:bg-gray-200 text-sm">
                        <div class="text-gray-700 w-1/2 sm:w-1/4 p-2">
                            <div class="font-semibold">
                                Queue ID:
                            </div>
                        </div>
                        <div class="text-gray-700 w-1/2 sm:w-3/4 p-2">
                            <div class="">
                                {{ message.mailq_id }}
                            </div>
                        </div>
                    </div>
                </div>

                <div class="sm:w-1/2 border-b">
                    <div class="sm:flex text-sm">
                        <div class="sm:w-1/2 hover:bg-gray-200">
                            <div class="flex">
                                <div class="text-gray-700 bg-gray-300 w-1/2 p-3">
                                    Allowed:
                                </div>
                                <div class="text-gray-700 w-1/2 p-2">
                                    <div class="items-center text-white leading-none lg:rounded-full flex lg:inline-flex">
                                        <span class="flex rounded-full uppercase px-2 py-1 text-xs font-bold" :class="{ 'bg-green-500': message.allowed, 'bg-gray-500': !message.allowed }" >
                                            {{ message.allowed | yesno }}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="sm:w-1/2 hover:bg-gray-200">
                            <div class="flex">
                                <div class="text-gray-700 bg-gray-300 w-1/2 p-3">
                                    Blocked:
                                </div>
                                <div class="text-gray-700 w-1/2 p-2">
                                    <div class="items-center text-white leading-none lg:rounded-full flex lg:inline-flex">
                                        <span class="flex rounded-full uppercase px-2 py-1 text-xs font-bold" :class="{ 'bg-red-500': message.blocked, 'bg-gray-500': !message.blocked }" >
                                            {{ message.blocked | yesno }}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="sm:flex text-sm">
                        <div class="sm:w-1/2 hover:bg-gray-200">
                            <div class="flex">
                                <div class="text-gray-700 bg-gray-300 w-1/2 p-3">
                                    Stored:
                                </div>
                                <div class="text-gray-700 w-1/2 p-2">
                                    <div class="items-center text-white leading-none lg:rounded-full flex lg:inline-flex">
                                        <span class="flex rounded-full uppercase px-2 py-1 text-xs font-bold bg-gray-500">
                                            {{ message.stored | yesno }}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="sm:w-1/2 hover:bg-gray-200">
                            <div class="flex">
                                <div class="text-gray-700 bg-gray-300 w-1/2 p-3">
                                    Spam:
                                </div>
                                <div class="text-gray-700 w-1/2 p-2">
                                    <div class="items-center text-white leading-none lg:rounded-full flex lg:inline-flex">
                                        <span class="flex rounded-full uppercase px-2 py-1 text-xs font-bold" :class="{ 'bg-red-500': message.is_spam, 'bg-green-500': !message.is_spam }" >
                                            {{ message.is_spam | yesno }}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="sm:flex text-sm">
                        <div class="sm:w-1/2 hover:bg-gray-200">
                            <div class="flex">
                                <div class="text-gray-700 bg-gray-300 w-1/2 p-3">
                                    Infected:
                                </div>
                                <div class="text-gray-700 w-1/2 p-2">
                                    <div class="items-center text-white leading-none lg:rounded-full flex lg:inline-flex">
                                        <span class="flex rounded-full uppercase px-2 py-1 text-xs font-bold" :class="{ 'bg-red-500': message.infected, 'bg-green-500': !message.infected }" >
                                            {{ message.infected | yesno }}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="sm:w-1/2 hover:bg-gray-200">
                            <div class="flex">
                                <div class="text-gray-700 bg-gray-300 w-1/2 p-3">
                                    RBL listed:
                                </div>
                                <div class="text-gray-700 w-1/2 p-2">
                                    <div class="items-center text-white leading-none lg:rounded-full flex lg:inline-flex">
                                        <span class="flex rounded-full uppercase px-2 py-1 text-xs font-bold" :class="{ 'bg-red-500': message.is_rbl_listed, 'bg-green-500': !message.is_rbl_listed }" >
                                            {{ message.is_rbl_listed | yesno }}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="sm:flex mb-2">
                <div class="sm:w-1/2 sm:border-r">
                    <div class="text-center font-bold bg-gray-100">Message Headers</div>
                    <div class="flex hover:bg-gray-200 text-xs" v-for="(value, key) in headers.headers" :key="key">
                        <div class="w-1/4">
                            {{ key }}
                        </div>
                        <div class="w-3/4 break-words">
                            <nl2br tag="p" :text="value" />
                        </div>
                    </div>
                </div>
                <div class="sm:w-1/2">
                    <div>
                        <div class="text-center font-bold bg-gray-100" v-show="spamreport.id">Spam report</div>
                        <div class="flex hover:bg-gray-200 text-sm" v-for="(value, key) in spamreport.report" :key="key">
                            <div class="w-3/4">
                                <a class="text-gray-900 no-underline" :href="'http://wiki.apache.org/spamassassin/Rules/' + key" target="_blank">
                                    <span v-if="value.description">{{ value.description }}</span>
                                    <span v-else>{{ key }}</span>
                                </a>
                            </div>
                            <div class="w-1/4 text-right">
                                {{ value.value }}
                            </div>
                        </div>
                        <div class="text-center font-bold bg-gray-100" v-show="mcpreport.id">MCP report</div>
                        <div class="flex hover:bg-gray-200 text-sm" v-for="(value, key) in mcpreport.report" :key="key">
                            <div class="w-3/4">
                                <a :href="'http://wiki.apache.org/spamassassin/Rules/' + key" target="_blank">{{ key }}</a>
                            </div>
                            <div class="w-1/4 text-right">
                                {{ value }}
                            </div>
                        </div>
                    </div>
                    <div class="hover:bg-gray-200">
                        <div class="text-center font-bold bg-gray-100" v-show="mailscanner_report.id">MailScanner report</div>
                        <div class=" text-sm"><p>{{ mailscanner_report.contents }}</p></div>
                    </div>
                </div>
            </div>
            <div class="w-full" v-if="transport_log.length">
                <div class="text-center font-bold bg-gray-100">Transport log</div>
                <div class="table-wrapper">
                    <table class="table text-sm">
                        <thead>
                            <tr>
                                <th>Timestamp</th>
                                <th>DSN</th>
                                <th>Message</th>
                                <th>From</th>
                                <th>To</th>
                                <th>Type</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="log in transport_log" :key="log.id">
                                <td>{{ log.timestamp }}</td>
                                <td>{{ log.dsn }}</td>
                                <td>{{ log.dsn_message }}</td>
                                <td>{{ log.transport_host }}</td>
                                <td>{{ log.relay_host }}</td>
                                <td>{{ log.transport_type }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <mg-message-actions @view="showMessage" @release="release" @spam="spam" @nonspam="nonspam" class="border-t" :uuid="uuid" v-if="file_exists"></mg-message-actions>
            <mg-modal @close="show_modal = false" :submit-button="false" :show="show_modal" modal-title="View message" v-if="file_exists">
                {{ message_contents }}
            </mg-modal>
        </div>
    </div>
</mg-page>
</template>
<script>
import MessageActions from '../../components/MessageActions.vue';
import ListEntryForm from '../../components/ListEntryForm.vue';
import router from '../../routing/router';
import { mapMutations, mapGetters } from 'vuex';
export default {
    props: ['uuid'],
    data: () => {
        return {
            message: {},
            headers: {},
            spamreport: {},
            rblreport: {},
            mcpreport: {},
            mailscanner_report: {},
            transport_log: [],
            show_modal: false,
            show_listing_modal: false,
            listing_type: '',
            message_contents: '',
            file_exists: false,
            client_country: false
        }
    },
    methods: {
        async getMessage() {
            await axios.get('/api/messages/' + this.uuid + '/').then(response => {
                this.message = response.data;
            }).catch(error => {
                if (error.response.status == 404) {
                    router.push({ name: 'not_found' });
                }
                else if (error.response.status == 403) {
                    router.push({ name: 'access_denied' });
                }
            })
            axios.post('/api/geoip/lookup/', { 'ip_addr': this.message.client_ip }).then(response => {
                this.client_country = response.data.country;
            }).catch(error => {
                this.notify(this.createNotification('GeoIP Status', 'Query failed', 'error'));
            })
        },
        getMessageHeaders() {
            axios.get('/api/messages/' + this.uuid + '/headers/').then(response => {
                this.headers = response.data;
            }).catch(error => {
                if (error.response.status !== 404) {
                    this.notify(this.createNotification('An error occurred whle getting the message headers', `${error}`, 'error'));
                }
            })
        },
        getSpamReport() {
            axios.get('/api/messages/' + this.uuid + '/spam-report/').then(response => {
                this.spamreport = response.data;
            }).catch(error => {
                if (error.response.status !== 404) {
                    this.notify(this.createNotification('An error occurred while getting the spam report', `${error}`, 'error'));
                }
            })
        },
        getRblReport() {
            axios.get('/api/messages/' + this.uuid + '/rbl-report/').then(response => {
                this.rblreport = response.data;
            }).catch(error => {
                if (error.response.status !== 404) {
                    this.notify(this.createNotification('An error occurred while getting the RBL report', `${error}`, 'error'));
                }
            })
        },
        getMcpReport() {
            axios.get('/api/messages/' + this.uuid + '/mcp-report/').then(response => {
                this.mcpreport = response.data;
            }).catch(error => {
                if (error.response.status !== 404) {
                    this.notify(this.createNotification('An error occurred while getting the MCP report', `${error}`, 'error'));
                }
            })
        },
        getMailscannerReport() {
            axios.get('/api/messages/' + this.uuid + '/mailscanner-report/').then(response => {
                this.mailscanner_report = response.data;
            }).catch(error => {
                if (error.response.status !== 404) {
                    this.notify(this.createNotification('An error occurred while getting the Mailscanning report', `${error}`, 'error'));
                }
            })
        },
        getTransportLog() {
            axios.get('/api/messages/'+this.uuid+'/transport-log/').then(response => {
                this.transport_log = response.data;
            }).catch(error => {
                if (error.response.status !== 404) {
                    this.notify(this.createNotification('An error occurred while getting the Transport log', `${error}`, 'error'));
                }
            });
        },
        getQueueFileStatus() {
            axios.get('/api/messages/'+this.uuid+'/file-exists/').then(response => {
                this.file_exists = response.data.file_exists;
            }).catch(error => {
                console.log(error.response);
            });
        },
        showMessage() {
            router.push('/messages/'+this.uuid+'/content');
        },
        async getMessageContents() {
            if (this.message.queue_file_exists) {
                axios.get('/api/messages/' + this.uuid + '/contents/').then(response => {
                    this.message_contents = response.data.message_contents;
                }).catch(error => {
                    if (error.response.status !== 404) {
                        this.notify(this.createNotification('An error occurred while getting the message contents', `${error}`, 'error'));
                    }
                });
            }
            else {
                this.message_contents = 'Message contents are no longer available on this server';
            }
        },
        createListing(from_address, to_address, listing_type) {
            this.$modal.show(ListEntryForm,{
                listingType: listing_type,
                fromAddress: from_address,
                toAddress: to_address,
                fromChoice: 'from_address',
                toChoice: 'to_address'
            },
            {
                clickToClose: false,
                adaptive: true,
                height: 'auto'
            });
        },
        release() {
            axios.post('/api/messages/release/', { 'messages': [this.uuid]}).then(response => {
                this.notify(this.createNotification('Message release', `The message has been release from quarantine and should be delivered soon`, 'success'));
            }).catch(error => {
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        spam() {
            axios.post('/api/messages/mark-spam/', { 'messages': [this.uuid]}).then(response => {
                this.notify(this.createNotification('Message marked as spam', `The message has been marked as spam in our system. In the future you should recieve less messages like this`, 'success'));
            }).catch(error => {
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        nonspam() {
            axios.post('/api/messages/mark-nonspam/', { 'messages': [this.uuid]}).then(response => {
                this.notify(this.createNotification('Message marked as nonspam', `The message has been marked as not being harmful in our system. In the future you should recieve messages like this`, 'success'));
            }).catch(error => {
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        ...mapMutations(['notify', 'setLoading'])
    },
    created() {
        this.getMessage().then(() => {
            this.getMessageHeaders();
            this.getSpamReport();
            this.getRblReport();
            this.getMcpReport();
            this.getMailscannerReport();
            this.getTransportLog();
            this.getQueueFileStatus();
            this.setLoading(false);
        });
    },
    components: {
        'mg-message-actions': MessageActions
    }
}
</script>
