import { getGlobal } from "@electron/remote";
import { createApp } from "vue";
import App from "./App.vue";
import { router } from "./router";
import ElementPlus from "element-plus";
import { createPinia } from "pinia";
import Popper from "vue3-popper";
import Vue3Lottie from "vue3-lottie";
import VMdEditor from "@kangc/v-md-editor";

import analytics from "./plugins/analytics";

// plugins for the markdown editor
import githubTheme from "@kangc/v-md-editor/lib/theme/github.js";
import createKatexPlugin from "@kangc/v-md-editor/lib/plugins/katex/npm";
import createTodoListPlugin from "@kangc/v-md-editor/lib/plugins/todo-list/index";
import createAlignPlugin from "@kangc/v-md-editor/lib/plugins/align";
import enUS from "@kangc/v-md-editor/lib/lang/en-US";

import "./assets/css/utilities-theme.css";
import "./assets/css/index.css";
import "element-plus/dist/index.css";
import "vue3-lottie/dist/style.css";

// css for the markdown editor
import "katex/dist/katex.min.css";
import "@kangc/v-md-editor/lib/style/base-editor.css";
import "@kangc/v-md-editor/lib/theme/style/github.css";
import "@kangc/v-md-editor/lib/plugins/todo-list/todo-list.css";

import LineDivider from "./components/ui/LineDivider.vue";
import WorkflowProgressBarVue from "./components/ui/WorkflowProgressBar.vue";
import FormHelpContent from "./components/ui/FormHelpContent.vue";
import AppDocsLink from "./components/ui/AppDocsLink.vue";

import WarningConfirm from "./components/dialogs/confirm/WarningConfirm.vue";
import InfoConfirm from "./components/dialogs/confirm/InfoConfirm.vue";
import ErrorConfirm from "./components/dialogs/confirm/ErrorConfirm.vue";

import WarningPrompt from "./components/dialogs/prompt/WarningPrompt.vue";

import GeneralDialog from "./components/dialogs/general/GeneralDialog.vue";

import FadeTransition from "./components/transitions/FadeTransition.vue";

import HelixSpinnerAnimationData from "./assets/lotties/helixSpinner.json";

// config for the markdown editor
VMdEditor.use(githubTheme, {});
VMdEditor.use(createKatexPlugin());
VMdEditor.use(createTodoListPlugin());
VMdEditor.use(createAlignPlugin());
VMdEditor.lang.use("en-US", enUS); // set language to english

let app = createApp(App);

// global variables for use in the app
app.config.globalProperties.$server_url = `http://127.0.0.1:${getGlobal("PYPORT")}`;
app.config.globalProperties.$helix_spinner = HelixSpinnerAnimationData;

// register components globally
app.component("VuePopper", Popper);

app.component("line-divider", LineDivider);
app.component("workflow-progress-bar", WorkflowProgressBarVue);
app.component("form-help-content", FormHelpContent);
app.component("app-docs-link", AppDocsLink);

app.component("warning-confirm", WarningConfirm);
app.component("info-confirm", InfoConfirm);
app.component("error-confirm", ErrorConfirm);

app.component("warning-prompt", WarningPrompt);

app.component("general-dialog", GeneralDialog);

app.component("fade-transition", FadeTransition);

// import and register icons globally
import {
  ArrowRightBold,
  Back,
  Box,
  ChatDotRound,
  Checked,
  CircleCheckFilled,
  CircleCloseFilled,
  Collection,
  DArrowLeft,
  DArrowRight,
  DataAnalysis,
  DataLine,
  Delete,
  DeleteFilled,
  Document,
  Download,
  Edit,
  EditPen,
  Files,
  Flag,
  Fold,
  Folder,
  Histogram,
  HomeFilled,
  InfoFilled,
  Key,
  List,
  Lock,
  Notebook,
  Monitor,
  PictureFilled,
  Postcard,
  QuestionFilled,
  Reading,
  RemoveFilled,
  Right,
  Select,
  Setting,
  Star,
  Ticket,
  Unlock,
  UploadFilled,
  User,
  UserFilled,
  VideoPlay,
  View,
} from "@element-plus/icons-vue";

app.component("arrow-right-bold", ArrowRightBold);
app.component("back-icon", Back);
app.component("box-icon", Box);
app.component("chat-dot-round", ChatDotRound);
app.component("checked-icon", Checked);
app.component("circle-check-filled", CircleCheckFilled);
app.component("circle-close-filled", CircleCloseFilled);
app.component("collection-icon", Collection);
app.component("d-arrow-left", DArrowLeft);
app.component("d-arrow-right", DArrowRight);
app.component("data-analysis", DataAnalysis);
app.component("data-line", DataLine);
app.component("delete-icon", Delete);
app.component("delete-filled", DeleteFilled);
app.component("document-icon", Document);
app.component("download-icon", Download);
app.component("edit-icon", Edit);
app.component("edit-pen", EditPen);
app.component("files-icon", Files);
app.component("flag-icon", Flag);
app.component("fold-icon", Fold);
app.component("folder-icon", Folder);
app.component("histogram-icon", Histogram);
app.component("home-filled", HomeFilled);
app.component("info-filled", InfoFilled);
app.component("key-icon", Key);
app.component("list-icon", List);
app.component("lock-icon", Lock);
app.component("monitor-icon", Monitor);
app.component("notebook-icon", Notebook);
app.component("picture-filled", PictureFilled);
app.component("postcard-icon", Postcard);
app.component("question-filled", QuestionFilled);
app.component("reading-icon", Reading);
app.component("remove-filled", RemoveFilled);
app.component("right-icon", Right);
app.component("select-icon", Select);
app.component("setting-icon", Setting);
app.component("star-icon", Star);
app.component("ticket-icon", Ticket);
app.component("unlock-icon", Unlock);
app.component("upload-filled", UploadFilled);
app.component("user-icon", User);
app.component("user-filled", UserFilled);
app.component("video-play", VideoPlay);
app.component("view-icon", View);

// additional vue libraries to be used in the app
app.use(router); // vue router
app.use(createPinia()); // pinia
app.use(ElementPlus); // element plus
app.use(VMdEditor); // markdown editor
app.use(Vue3Lottie); // lottie animations
app.use(analytics, {
  trackingID: process.env.VUE_APP_GOOGLE_ANALYTICS_ID,
}); // analytics

// Mount application to the root element
app.mount("#app");
