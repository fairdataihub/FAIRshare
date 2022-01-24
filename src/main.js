import { createApp } from "vue";
import App from "./App.vue";
import { router } from "./router";
import ElementPlus from "element-plus";
import { createPinia } from "pinia";
import Popper from "vue3-popper";

import "./assets/css/utilities-theme.css";
import "./assets/css/index.css";
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
app.component("VuePopper", Popper);
app.component("form-help-content", FormHelpContent);

// import and register icons globally
import {
  ArrowRightBold,
  Back,
  ChatDotRound,
  CircleCheckFilled,
  CircleCloseFilled,
  Collection,
  DArrowLeft,
  DArrowRight,
  DataAnalysis,
  DataLine,
  Delete,
  Document,
  Edit,
  Histogram,
  HomeFilled,
  InfoFilled,
  Key,
  Lock,
  Notebook,
  Monitor,
  PictureFilled,
  QuestionFilled,
  Reading,
  RemoveFilled,
  Right,
  Setting,
  Star,
  Unlock,
  User,
  UserFilled,
  VideoPlay,
} from "@element-plus/icons-vue";

app.component("arrow-right-bold", ArrowRightBold);
app.component("back-icon", Back);
app.component("chat-dot-round", ChatDotRound);
app.component("circle-check-filled", CircleCheckFilled);
app.component("circle-close-filled", CircleCloseFilled);
app.component("collection-icon", Collection);
app.component("d-arrow-left", DArrowLeft);
app.component("d-arrow-right", DArrowRight);
app.component("data-analysis", DataAnalysis);
app.component("data-line", DataLine);
app.component("delete-icon", Delete);
app.component("document-icon", Document);
app.component("edit-icon", Edit);
app.component("histogram-icon", Histogram);
app.component("home-filled", HomeFilled);
app.component("info-filled", InfoFilled);
app.component("key-icon", Key);
app.component("lock-icon", Lock);
app.component("monitor-icon", Monitor);
app.component("notebook-icon", Notebook);
app.component("picture-filled", PictureFilled);
app.component("question-filled", QuestionFilled);
app.component("reading-icon", Reading);
app.component("remove-filled", RemoveFilled);
app.component("right-icon", Right);
app.component("setting-icon", Setting);
app.component("star-icon", Star);
app.component("unlock-icon", Unlock);
app.component("user-icon", User);
app.component("user-filled", UserFilled);
app.component("video-play", VideoPlay);

// additional vue libraries to be used in the app
app.use(router); // vue router
app.use(createPinia()); // pinia
app.use(ElementPlus); // element plus

// Mount application to the root element
app.mount("#app");
