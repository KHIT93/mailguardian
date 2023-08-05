<template>
    <div class="relative border border-gray-300 rounded-md px-3 py-2 shadow-sm focus-within:ring-1 focus-within:ring-blue-600 focus-within:border-blue-600" :class="{ 'cursor-not-allowed bg-gray-100 disabled:bg-gray-100': disabled }">
        <select :name="props.inputId" :id="props.inputId" :aria-disabled="disabled" :disabled="disabled" class="block peer w-full border-0 p-0 text-gray-900 placeholder-transparent focus:ring-0 sm:text-sm" :class="{ 'cursor-not-allowed': disabled }" :value="props.modelValue" :placeholder="props.label" @input="emits('update:modelValue', $event.target.value)">
            <slot name="inputOptions"></slot>
        </select>
        <label :for="props.inputId"
            class="absolute -top-2 left-2 -mt-px inline-block px-1 bg-white text-xs text-gray-600 transition-all 
            peer-placeholder-shown:text-sm peer-placeholder-shown:text-gray-500 peer-placeholder-shown:top-2
            peer-focus:-top-2 peer-focus:left-2 peer-focus:-mt-px peer-focus:text-blue-600 peer-focus:text-xs" :class="[ disabled ? 'cursor-not-allowed' : 'peer-placeholder-shown:cursor-text' ]">{{ props.label }}</label>
    </div>

    <!-- <Listbox :name="props.name" :id="props.inputId" :aria-disabled="props.disabled" :modelValue="modelValue" @update:modelValue="value => emits('update:modelValue', value)">
        <div class="relative border border-gray-300 rounded-md px-3 py-2 shadow-sm focus-within:ring-1 focus-within:ring-blue-600 focus-within:border-blue-600" :class="{ 'cursor-not-allowed bg-gray-100 disabled:bg-gray-100': props.disabled }">
            <ListboxButton class="relative w-full cursor-default bg-white py-2 pl-3 pr-10 text-left focus:outline-none focus-visible:border-blue-500 focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75 focus-visible:ring-offset-2 focus-visible:ring-offset-orange-300 sm:text-sm">
                <span class="block truncate">{{ modelValue }}</span>
                <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                    <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true"/>
                </span>
            </ListboxButton>
            <transition leave-active-class="transition duration-100 ease-in" leave-from-class="opacity-100" leave-to-class="opacity-0">
                <ListboxOptions class="absolute mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                    <ListboxOption v-slot="{ active, selected }" v-for="option in props.inputOptions" :key="option.name" :value="option.name" as="template">
                        <li :class="[ active ? 'bg-blue-100 text-blue-900' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-10 pr-4', ]">
                            <span :class="[ selected ? 'font-medium' : 'font-normal', 'block truncate', ]">
                                {{ option.label }}
                            </span>
                            <span v-if="selected" class="absolute inset-y-0 left-0 flex items-center pl-3 text-blue-600">
                                <CheckIcon class="h-5 w-5" aria-hidden="true" />
                            </span>
                        </li>
                    </ListboxOption>
                </ListboxOptions>
            </transition>
        </div>
    </Listbox> -->
</template>

<script setup>
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from '@headlessui/vue'
import { ChevronUpDownIcon, CheckIcon } from '@heroicons/vue/24/solid'
const props = defineProps(['modelValue', 'label', 'inputId', 'disabled', 'inputOptions'])
const emits = defineEmits(['update:modelValue'])
</script>