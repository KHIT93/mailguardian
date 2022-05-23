<template>
    <div class="relative border border-gray-300 rounded-md px-3 py-2 shadow-sm focus-within:ring-1 focus-within:ring-blue-600 focus-within:border-blue-600">
        <select :name="inputId" :id="inputId" class="block peer w-full border-0 p-0 text-gray-900 placeholder-transparent focus:ring-0 sm:text-sm" :value="modelValue" :placeholder="label" @input="$emit('update:modelValue', $event.target.value)">
            <slot name="inputOptions"></slot>
        </select>
        <label :for="inputId"
            class="absolute -top-2 left-2 -mt-px inline-block px-1 bg-white text-xs text-gray-600 transition-all 
            peer-placeholder-shown:text-sm peer-placeholder-shown:text-gray-500 peer-placeholder-shown:top-2 peer-placeholder-shown:cursor-text
            peer-focus:-top-2 peer-focus:left-2 peer-focus:-mt-px peer-focus:text-blue-600 peer-focus:text-xs">{{ label }}</label>
    </div>
</template>

<script>
export default {
    props: ['modelValue', 'label', 'inputId'],
    emits: ['update:modelValue']
}
</script>