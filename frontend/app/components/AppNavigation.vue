<script setup>
    const $auth = useAuth()
    const currentUser = useAuth().$state.user
    const links = ref([
        [
            {
                label: 'Dashboard',
                to: '/',
                icon: 'i-heroicons-circle-stack'
            },
            {
                label: 'Mail',
                to: '/messages',
                icon: 'i-heroicons-envelope'
            },
            {
                label: 'Allowed senders',
                to: '/lists/allowed',
                icon: 'i-heroicons-check-circle'
            },
            {
                label: 'Blocked senders',
                to: '/lists/blocked',
                icon: 'i-heroicons-x-circle'
            },
            {
                label: 'Statistics',
                to: '/statistics',
                icon: 'i-heroicons-chart-bar'
            },
        ]
    ])
    const adminLinks = ref([
        [
            {
                label: 'Users',
                to: '/users',
                icon: 'i-heroicons-user-group'
            },
            {
                label: 'Domains',
                to: '/domains',
                icon: 'i-heroicons-globe-europe-africa'
            },
        ],
        // [
        //     {
        //         label: 'Cluster Dashboard',
        //         to: '/cluster',
        //         icon: 'i-heroicons-rectangle-group'
        //     },
        //     {
        //         label: 'Cluster Hosts',
        //         to: '/cluster/nodes',
        //         icon: 'i-heroicons-server'
        //     }
        // ],
        [
            {
                label: 'Audit Log',
                to: '/audit/log',
                icon: 'i-heroicons-document-text'
            },
            // {
            //     label: 'Audit Settings',
            //     to: '/audit/settings',
            //     icon: 'i-heroicons-cog'
            // }
        ]
    ])
    const supportLinks = ref([
        {
            label: 'Documentation',
            to: 'https://mailguardian.org',
            icon: 'i-heroicons-question-mark-circle',
            target: '_blank'
        },
    ])
    const userMenuItems = ref([
        [
            {
                label: 'Settings',
                to: '/account',
                icon: 'i-heroicons-adjustments-vertical'
            }
        ],
        [
            {
                label: 'Sign out',
                icon: 'i-heroicons-arrow-left-on-rectangle',
                onSelect: () => $auth.logout()
            }
        ]
    ])
</script>

<template>
    <div class="flex-col items-stretch relative w-full border-b lg:border-r border-gray-200 dark:border-gray-800 lg:w-64 lg:border-b-0 shrink-0 lg:flex bg-white dark:bg-gray-900">
            <div class="h-16 shrink-0 flex items-center border-b border-gray-200 dark:border-gray-800 px-4 gap-x-4 min-w-0">
                <div class="flex items-stretch gap-1.5 min-w-0 flex-1">
                    <UIcon name="i-heroicons-shield-check" class="h-8 w-8 text-blue-500"/>
                    <span class="text-gray-400 text-2xl cursor-default hover:text-gray-800 focus:text-gray-800">MailGuardian</span>
                </div>
            </div>
            <div class="flex flex-col w-full flex-1 relative overflow-hidden">
                <div class="grow flex flex-col min-h-0 gap-y-2 py-2">
                    <div class="flex-1 px-4 flex flex-col gap-y-2 overflow-y-auto">
                        <UNavigationMenu orientation="vertical" :items="links" />
                        <USeparator/>
                        <UNavigationMenu orientation="vertical" v-if="currentUser.role == 'superuser'" :items="adminLinks" />
                        <div class="flex-1"/>
                        <UNavigationMenu orientation="vertical" :items="supportLinks" />
                        <UDropdownMenu
                            :items="userMenuItems"
                            :content="{ align: 'center', collisionPadding: 12 }"
                            :ui="{
                                content: 'w-64'
                            }"
                        >
                            <UButton
                            v-bind="{
                                ...currentUser,
                                label: (currentUser?.first_name && currentUser?.last_name) ? currentUser.first_name + ' ' + currentUser.last_name : currentUser.email,
                                trailingIcon: 'i-heroicons-ellipsis-vertical'
                            }"
                            color="neutral"
                            variant="ghost"
                            block
                            class="data-[state=open]:bg-(--ui-bg-elevated)"
                            :ui="{
                                trailingIcon: 'text-(--ui-text-dimmed) w-5 h-5'
                            }"
                            />
                        </UDropdownMenu>
                    </div>
                </div>
            </div>
        </div>
</template>