import { createApp } from "vue";
import App from "./App.vue";
import { router } from "./router";
// import store from '@/store'
import ElementPlus from "element-plus";
import { createPinia } from "pinia";

import "element-plus/dist/index.css";
import "./index.css";

import LineDivider from "./components/ui/LineDivider.vue";

let app = createApp(App);

// global variables for use in the app
app.config.globalProperties.SERVERURL = "http://127.0.0.1:5000";

// register components globally
app.component("line-divider", LineDivider);

// additional vue libraries to be used in the app
app.use(router);
app.use(createPinia());
app.use(ElementPlus);

// Mount application to the root element
app.mount("#app");
