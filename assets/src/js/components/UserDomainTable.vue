<template>
    <div class="">
        <table class="table text-sm">
            <thead>
                <tr>
                    <th>Domain</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="domain in domains" :key="domain.id" v-if="domains.length > 0">
                    <td>{{ domain.name }}</td>
                    <td class="text-center">
                        <button type="button" class="cursor-pointer" @click="destroy(domain)"><mw-delete-icon class="w-5 h-5"></mw-delete-icon></button>
                    </td>
                </tr>
                <tr v-if="form">
                    <td colspan="2">
                        <form @submit.prevent="add" class="flex justify-between">
                            <v-select class="w-5/6" v-model="form.domain" label="name" :options="allDomains"></v-select>
                            <button type="submit" class="cursor-pointer text-center mx-auto"><mw-checkmark-icon class="w-5 h-5"></mw-checkmark-icon></button>
                        </form>
                    </td>                 
                </tr>
                <tr>
                    <td colspan="2"><button type="button" @click="addForm" class="underline cursor-pointer">Add new domain</button></td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
<script>
import Form from '../classes/Form';
export default {
    props: ['domains'],
    data: () => {
        return {
            form: null,
            allDomains: []
        }
    },
    mounted() {
        this.getDomains();
    },
    methods: {
        addForm() {
            this.form = {
                'domain': null
            };
        },
        async add() {
            if (!this.form.domain) {
                return;
            }
            await this.$emit('submit', this.form.domain);
            this.form = null;
        },
        destroy(domain) {
            this.$emit('destroy', domain);
        },
        getDomains() {
            axios.get('/api/domains/all/').then(response => {
                this.allDomains = response.data;
            }).catch(error => {
                console.log(error);
            })
        }
    }
}
</script>