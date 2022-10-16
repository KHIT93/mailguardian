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
</template>

<script setup>
const props = defineProps(['modelValue', 'label', 'inputId', 'disabled'])
const emits = defineEmits(['update:modelValue'])
</script>