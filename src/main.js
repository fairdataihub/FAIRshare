import { createApp } from "vue";
import App from "./App.vue";
import { router } from "./router";
import ElementPlus from "element-plus";
import { createPinia } from "pinia";
import Popper from "vue3-popper";

import "./assets/css/tailwind.css";
import "./assets/css/utilities-theme.css";
import "element-plus/dist/index.css";

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

// import and register icons globally
import {
  ArrowRightBold,
  Back,
  CircleCheckFilled,
  CircleCloseFilled,
  DArrowLeft,
  DArrowRight,
  DataLine,
  Delete,
  Edit,
  HomeFilled,
  Key,
  Lock,
  QuestionFilled,
  RemoveFilled,
  Right,
  Setting,
  Star,
  Unlock,
  User,
} from "@element-plus/icons-vue";

app.component("arrow-right-bold", ArrowRightBold);
app.component("back", Back);
app.component("circle-check-filled", CircleCheckFilled);
app.component("circle-close-filled", CircleCloseFilled);
app.component("d-arrow-left", DArrowLeft);
app.component("d-arrow-right", DArrowRight);
app.component("data-line", DataLine);
app.component("delete", Delete);
app.component("edit", Edit);
app.component("home-filled", HomeFilled);
app.component("key", Key);
app.component("lock", Lock);
app.component("question-filled", QuestionFilled);
app.component("remove-filled", RemoveFilled);
app.component("right", Right);
app.component("setting", Setting);
app.component("star", Star);
app.component("unlock", Unlock);
app.component("user", User);

// additional vue libraries to be used in the app
app.use(router); // vue router
app.use(createPinia()); // pinia
app.use(ElementPlus); // element plus

// Mount application to the root element
app.mount("#app");
