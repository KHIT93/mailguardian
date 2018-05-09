<template>
    <div class="table-wrapper">
        <table class="table text-sm cursor-pointer break-words">
            <thead>
                <tr>
                    <th>From</th>
                    <th>To</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="item in list.results" :key="item.id">
                    <td>{{ item._from }}</td>
                    <td>{{ item._to }}</td>
                    <td>
                        <button role="button" @click="confirmDelete(item)" class="bg-red hover:bg-red-dark text-white py-1 px-2 border border-red-light rounded shadow text-sm no-underline ml-2">Delete</button>
                    </td>
                </tr>
            </tbody>
        </table>
        <div class="shadow">
            <div class="flex hover:bg-grey-lighter text-sm" v-for="item in list.results" :key="item.id">
                <div class="text-grey-darker w-1/3 md:w-2/5 p-2">
                    <div class="">
                        {{ item.from_address }}
                    </div>
                </div>
                <div class="text-grey-darker w-1/3 md:w-2/5 p-2">
                    <div class="">
                        {{ item.to_address }}
                    </div>
                </div>
                <div class="text-grey-darker w-1/3 md:w-1/5 p-2">
                    <div class="">
                        <button role="button" @click="confirmDelete(item)" class="bg-red hover:bg-red-dark text-white py-1 px-2 border border-red-light rounded shadow text-sm no-underline ml-2">Delete</button>
                    </div>
                </div>
            </div>
        </div>
        <div class="inline-flex pt-2 rounded">
            <button @click="previous" class="bg-grey-light hover:bg-grey text-grey-darkest py-2 px-4 rounded-l" :class="{'select-none cursor-not-allowed bg-grey-lightest hover:bg-grey-lightest' : list.current == 1}">
                Prev
            </button>
            <!-- <button class="bg-grey-light hover:bg-grey text-grey-darkest py-2 px-4">
                1
            </button>
            <button class="bg-grey-light hover:bg-grey text-grey-darkest py-2 px-4">
                2
            </button>
            <button class="bg-grey-light hover:bg-grey text-grey-darkest py-2 px-4">
                3
            </button> -->
            <button @click="next" class="bg-grey-light hover:bg-grey text-grey-darkest py-2 px-4 rounded-r" :class="{'select-none cursor-not-allowed bg-grey-lightest hover:bg-grey-lightest' : list.current == list.page_count}">
                Next
            </button>
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
        },
        previous() {
            if (this.list.previous) {
                this.$emit('previous');                
            }
        },
        next() {
            if (this.list.next) {
                this.$emit('next');
            }
        }
    }
}
</script>
