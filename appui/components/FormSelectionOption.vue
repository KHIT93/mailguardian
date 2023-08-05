<template>
    <ListboxOption v-slot="{ active, selected }" :value="props.value" as="template">
        <li :class="[ active ? 'bg-amber-100 text-amber-900' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-10 pr-4', ]">
            <span :class="[ selected ? 'font-medium' : 'font-normal', 'block truncate', ]">
                <slot></slot>
            </span>
            <span v-if="selected" class="absolute inset-y-0 left-0 flex items-center pl-3 text-amber-600">
                <CheckIcon class="h-5 w-5" aria-hidden="true" />
            </span>
        </li>
    </ListboxOption>
</template>
<script setup>
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from '@headlessui/vue'
import { ChevronUpDownIcon, CheckIcon } from '@heroicons/vue/24/solid'
const props = defineProps(['value'])
</script>