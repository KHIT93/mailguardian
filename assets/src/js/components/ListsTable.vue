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
                    <td>{{ item.from_address }}</td>
                    <td>{{ item.to_address }}</td>
                    <td>
                        <button role="button" @click="confirmDelete(item)" class="btn btn-red btn-sm shadow no-underline ml-2">Delete</button>
                    </td>
                </tr>
            </tbody>
        </table>
        <div class="inline-flex pt-2 rounded">
            <button @click="previous" class="btn rounded-none rounded-l" :class="{'select-none cursor-not-allowed btn-gray-lightest' : list.current == 1, 'btn-gray-400' : list.current != 1}">
                Prev
            </button>
            <!-- <button class="bg-gray-400 hover:bg-gray-500 text-gray-800 py-2 px-4">
                1
            </button>
            <button class="bg-gray-400 hover:bg-gray-500 text-gray-800 py-2 px-4">
                2
            </button>
            <button class="bg-gray-400 hover:bg-gray-500 text-gray-800 py-2 px-4">
                3
            </button> -->
            <button @click="next" class="btn rounded-none rounded-r" :class="{'select-none cursor-not-allowed btn-gray-lightest' : list.current == list.page_count, 'btn-gray-400' : list.current != list.page_count}">
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
