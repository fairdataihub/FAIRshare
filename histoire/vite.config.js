import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

const path = require("path");

export default defineConfig({
  plugins: [
    vue({
      template: {
        compilerOptions: {
          isCustomElement: (tag) => tag.startsWith("Vue3Lottie"),
        },
      },
    }),
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
