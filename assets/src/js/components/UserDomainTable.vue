<template>
    <div class="">
        <table class="table text-sm">
            <tbody>
                <tr v-for="domain in domains" :key="domain.id" v-if="domains.length > 0">
                    <td>{{ domain.name }}</td>
                    <td class="text-center">
                        <button type="button" class="cursor-pointer" @click="destroy(domain)"><mg-delete-icon class="w-5 h-5"></mg-delete-icon></button>
                    </td>
                </tr>
                <tr v-if="form">
                    <td colspan="2">
                        <form @submit.prevent="add" class="flex justify-between">
                            <v-select class="w-5/6" v-model="form.domain" label="name" :options="allDomains"></v-select>
                            <button type="submit" class="cursor-pointer text-center mx-auto"><mg-checkmark-icon class="w-5 h-5"></mg-checkmark-icon></button>
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
import { mapMutations } from 'vuex';
export default {
    props: ['domains'],
    data: () => {
        return {
            form: null,
            allDomains: []
        }
    },
    created() {
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
            this.setLoading(true);
            axios.get('/api/domains/all/').then(response => {
                this.allDomains = response.data;
                this.setLoading(false);
            }).catch(error => {
                this.setLoading(false);
                console.log(error);
            })
        },
        ...mapMutations(['setLoading'])
    }
}
</script>