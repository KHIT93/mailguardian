<template>
    <tr class="text-sm cursor-pointer" @click="editing = true">
        <td>
            <div v-if="editing && !saving">
                <input v-model="form.key" class="bg-white appearance-none border border-gray-200 hover:border-blue-500 rounded w-full py-2 px-4 text-gray-700" name="key" id="key" type="text" required>
            </div>
            <div class="" v-else>
                {{ item.key }}
            </div>
        </td>
        <td>
            <div v-if="editing && !saving">
                <input v-model="form.value" class="bg-white appearance-none border border-gray-200 hover:border-blue-500 rounded w-full py-2 px-4 text-gray-700" name="value" id="value" type="text">
            </div>
            <div class="" v-else>
                {{ item.value }}
            </div>
        </td>
        <td>{{ item.filepath }}</td>
        <td>
            <div class="" v-if="editing">
                <button type="button" @click="submit" class="flex-shrink-0 bg-blue-500 hover:bg-blue-600 border-blue-500 hover:border-blue-600 text-xs border-4 text-white py-1 px-1 rounded shadow" :class="{ 'bg-blue-200 hover:bg-blue-200 border-blue-200':saving }" :disabled="saving">
                    <svg class="fill-current w-2 h-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid" v-if="saving">
                        <circle cx="50" cy="50" fill="none" stroke-linecap="round" r="40" stroke-width="4" stroke="#fff" stroke-dasharray="62.83185307179586 62.83185307179586" transform="rotate(66 50 50)">
                            <animateTransform attributeName="transform" type="rotate" calcMode="linear" values="0 50 50;360 50 50" keyTimes="0;1" dur="1s" begin="0s" repeatCount="indefinite"></animateTransform>
                        </circle>
                    </svg>
                    Save
                </button>
            </div>
        </td>
    </tr>
</template>
<script>
import Form from '../classes/Form';
import { mapMutations } from 'vuex';
export default {
    props: ['item'],
    data: () => {
        return {
            form: {},
            editing: false,
            saving: false
        }
    },
    created() {
        this.form = new Form({
            id: this.item.id,
            key: this.item.key,
            value: this.item.value,
            filepath: this.item.filepath
        });
    },
    methods: {
        async submit() {
            this.saving = true;
            await this.form.patch('/api/mailscanner-configuration/'+this.item.id+'/').then(data => {
                this.notify(this.createNotification('Settings saved', `The setting ${data.key} has been saved`, 'success'));                
            }).catch(error => {
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));                
            });
            this.saving = false;
            this.editing = false;
            this.$emit('saved');
        },
        ...mapMutations(['notify'])
    }
}
</script>