import { createApp } from "vue";
import App from "./App.vue";
import { router } from "./router";
import ElementPlus from "element-plus";
import { createPinia } from "pinia";
import Popper from "vue3-popper";

import "element-plus/dist/index.css";
import "./assets/css/index.css";
import "./assets/css/utilities-theme.css";

import LineDivider from "./components/ui/LineDivider.vue";
import WorkflowProgressBarVue from "./components/ui/WorkflowProgressBar.vue";
import FormHelpContent from "./components/ui/FormHelpContent.vue";

let app = createApp(App);

// global variables for use in the app
app.config.globalProperties.$server_url = "http://127.0.0.1:7632";

// register components globally
app.component("line-divider", LineDivider);
app.component("workflow-progress-bar", WorkflowProgressBarVue);
app.component("Popper", Popper);
app.component("form-help-content", FormHelpContent);

// additional vue libraries to be used in the app
app.use(router);
app.use(createPinia());
app.use(ElementPlus);

// Mount application to the root element
app.mount("#app");
