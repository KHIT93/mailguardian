<template>
    <div class="flex hover:bg-grey-lighter text-sm cursor-pointer break-words">
        <div class="text-grey-darker w-1/3 sm:w-1/5 border-r p-2">
            <div class="">
                <p>{{ item.from_address }}</p>
            </div>
        </div>
        <div class="text-grey-darker w-1/3 sm:w-1/5 border-r p-2">
            <div class="">
                <p>{{ item.to_address }}</p>
            </div>
        </div>
        <div class="text-grey-darker hidden sm:block sm:w-1/5 border-r p-2">
            <div class="">
                <p>{{ item.subject }}</p>
            </div>
        </div>
        <div class="text-grey-darker w-1/3 sm:w-1/5 border-r p-2">
            <div class="">
                <p>{{ item.timestamp }}</p>
            </div>
        </div>
        <div class="text-grey-darker hidden sm:block sm:w-1/5 p-2">
            <div class="">
                <p>Status</p>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    props: ['item']
}
</script>
