import { defineConfig } from "histoire";
import { HstVue } from "@histoire/plugin-vue";
import "./src/assets/css/index.css";

export default defineConfig({
  plugins: [HstVue()],
});
