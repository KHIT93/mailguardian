<template>
<div class="container mx-auto sm:px-4 pt-6 pb-8">
    <div class="bg-white border sm:rounded shadow">
        <div class="sm:flex sm:justify-between">
            <div class="sm:w-1/3 text-center text-grey-darker py-6">
                <div class="sm:border-r">
                    <div class="mb-2">
                        <span class="text-5xl">300</span>
                    </div>
                    <div class="uppercase">
                        Total emails recieved
                    </div>
                </div>
            </div>
            <div class="sm:w-1/3 text-center text-grey-darker py-6">
                <div class="sm:border-r">
                    <div class="mb-2">
                        <span class="text-5xl">30</span>
                    </div>
                    <div class="uppercase">
                        Spam emails recieved
                    </div>
                </div>
            </div>
            <div class="sm:w-1/3 text-center text-grey-darker py-6">
                <div>
                    <div class="mb-2">
                        <span class="text-5xl">5</span>
                    </div>
                    <div class="uppercase">
                        Viruses recieved
                    </div>
                </div>
            </div>
        </div>
        <!-- Chart.js graph here for showing message stats -->
    </div>
</div>
</template>

<<script>
    export default {
        data: () => {
            return {
                chartdata: [],
            }
        }
    }
</script>
