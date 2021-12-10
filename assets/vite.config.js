import { resolve } from 'path';
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
    build: {
        manifest: true, // adds a manifest.json
        rollupOptions: {
            input: [
                resolve(__dirname, './src/main.js'),
            ]
        },
        outDir: './dist',
        emptyOutDir: true,
        assetsDir: '',
    },
    plugins: [vue()],
});