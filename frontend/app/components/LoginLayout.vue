<template>
    <UContainer class="w-full h-screen flex flex-col gap-y-4 pt-36 dark:bg-gray-800">
        <UCard :ui="{ body: { base: 'lg:grid lg:grid-cols-2' } }" class="py-3">
            <div class="space-y-8>">
                <div class="flex items-stretch gap-1.5 min-w-0 flex-1">
                    <UIcon name="i-heroicons-shield-check" class="h-8 w-8 text-blue-500"/>
                    <span class="text-gray-400 text-2xl cursor-default hover:text-gray-800 focus:text-gray-800">MailGuardian</span>
                </div>
                <div class="py-8 lg:py-4">
                    <span class="text-2xl block">Sign In</span>
                    <span class="block pt-2">Continue by signing in your account</span>
                </div>
            </div>

            <slot />
        </UCard>
    </UContainer>
</template>

<script setup>

</script>