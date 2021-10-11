import { createApp } from "vue";
import App from "./App.vue";
import { router } from "./router";
// import store from '@/store'
import ElementPlus from "element-plus";
import { createPinia } from "pinia";

import "element-plus/dist/index.css";
import "./index.css";

let app = createApp(App);

// global variables are defined in main.js
app.config.globalProperties.SERVERURL = "http://127.0.0.1:5000";

// additional vue libraries
app.use(router);
// app.use(store)
app.use(createPinia())
app.use(ElementPlus);

// Mount application
app.mount("#app");
