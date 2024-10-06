<template>
    <div class="flex-col items-stretch relative w-full border-b lg:border-r border-gray-200 dark:border-gray-800 lg:w-64 lg:border-b-0 flex-shrink-0 lg:flex bg-white dark:bg-gray-900">
            <div class="h-16 flex-shrink-0 flex items-center border-b border-gray-200 dark:border-gray-800 px-4 gap-x-4 min-w-0 !border-transparent">
                <div class="flex items-stretch gap-1.5 min-w-0 flex-1">
                    <UIcon name="i-heroicons-shield-check" class="h-8 w-8 text-blue-500"/>
                    <span class="text-gray-400 text-2xl cursor-default hover:text-gray-800 focus:text-gray-800">MailGuardian</span>
                </div>
            </div>
            <div class="flex flex-col w-full flex-1 relative overflow-hidden">
                <div class="flex-grow flex flex-col min-h-0 gap-y-2 py-2">
                    <div class="flex-1 px-4 flex flex-col gap-y-2 overflow-y-auto">
                        <UVerticalNavigation :links="links" />
                        <UDivider/>
                        <UVerticalNavigation :links="adminLinks" />
                        <div class="flex-1"/>
                        <UVerticalNavigation :links="supportLinks" />
                        <UDropdown mode="hover" :items="userMenuItems" :ui="{ width: 'w-full', item: { disabled: 'cursor-text select-text' } }" :popper="{ strategy: 'absolute', placement: 'top' }" class="w-full">
                            <template #default="{ open }">
                                <UButton color="white" variant="ghost" class="w-full" :label="(currentUser?.first_name && currentUser?.last_name) ? currentUser.first_name + ' ' + currentUser.last_name : currentUser.email" icon="i-heroicons-user-circle" :class="[open && 'bg-gray-50 dark:bg-gray-800']">
                                    <template #trailing>
                                        <UIcon name="i-heroicons-ellipsis-vertical" class="w-5 h-5 ml-auto" />
                                    </template>
                                </UButton>
                            </template>
                            <template #account>
                                <div class="text-left">
                                    <p>
                                    Signed in as
                                    </p>
                                    <p class="truncate font-medium text-gray-900 dark:text-white">
                                    {{ currentUser.email }}
                                    </p>
                                </div>
                            </template>
                        </UDropdown>
                    </div>
                </div>
            </div>
        </div>
</template>

<script setup>
    const $auth = useAuth()
    const currentUser = useAuth().$state.user
    const links = [
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
    ]
    const adminLinks = [
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
        [
            {
                label: 'Cluster Dashboard',
                to: '/cluster',
                icon: 'i-heroicons-rectangle-group'
            },
            {
                label: 'Cluster Hosts',
                to: '/cluster/nodes',
                icon: 'i-heroicons-server'
            }
        ],
        [
            {
                label: 'Audit Log',
                to: '/audit/log',
                icon: 'i-heroicons-document-text'
            },
            {
                label: 'Audit Settings',
                to: '/audit/settings',
                icon: 'i-heroicons-cog'
            }
        ]
    ]
    const supportLinks = [
        {
            label: 'Documentation',
            to: 'https://mailguardian.org',
            icon: 'i-heroicons-question-mark-circle',
            target: '_blank'
        },
    ]
    const userMenuItems = [
        [
            {
                slot: 'account',
                label: '',
                disabled: true
            }
        ],
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
                click: () => $auth.logout()
            }
        ]
    ]
</script>