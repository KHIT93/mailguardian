<template>
    <div>
        <div class="flex text-sm shadow">
            <div class="text-grey-darker w-1/3 p-2">
                <div class="font-semibold">
                    From
                </div>
            </div>
            <div class="text-grey-darker w-1/3 p-2">
                <div class="font-semibold">
                    To
                </div>
            </div>
            <div class="text-grey-darker w-1/3 p-2">
                <div class="font-semibold">
                    Actions
                </div>
            </div>
        </div>
        <div class="shadow">
            <div class="flex hover:bg-grey-lighter text-sm" v-for="item in list.results" :key="item.id">
                <div class="text-grey-darker w-1/3 p-2">
                    <div class="">
                        {{ item._from }}
                    </div>
                </div>
                <div class="text-grey-darker w-1/3 p-2">
                    <div class="">
                        {{ item._to }}
                    </div>
                </div>
                <div class="text-grey-darker w-1/3 p-2">
                    <div class="">
                        <button role="button" @click="confirmDelete(item.id)" class="bg-red hover:bg-red-dark text-white py-1 px-2 border border-red-light rounded shadow text-sm no-underline ml-2">Delete</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: ['list'],
    data: () => {
        return {
            search_key: ""
        }
    },
    methods: {
        confirmDelete(id) {
            this.$emit('confirmDelete', id);
        }
    }
}
</script>
