<template>
    <v-card>
            <v-card-title>
                <v-icon x-large class="red--text">error_outline</v-icon> Page not found
            </v-card-title>
        <v-card-text>
                Whoops! The page you were looking for does not seem to exist.
        </v-card-text>
    </v-card>
</template>

<script>
    export default {
        mounted() {
            console.log('Page not found.')
        }
    }
</script>