<template>
  <el-tooltip effect="dark" :content="content" placement="bottom">
    <div
      class="fixed bottom-28 right-5 rounded-full border border-zinc-50 opacity-30 shadow-sm transition-all hover:opacity-100 hover:shadow-xl"
      @click="openHelpDocs"
    >
      <Vue3Lottie
        animationLink="https://assets5.lottiefiles.com/packages/lf20_tHEtXH.json"
        :width="70"
        :height="70"
        :playOnHover="true"
        class="scale-95 grayscale transition-all hover:scale-100 hover:cursor-help hover:grayscale-0"
      />
    </div>
  </el-tooltip>
</template>

<script>
export default {
  name: "AppDocsLink",
  props: {
    content: {
      type: String,
      required: false,
      default: "Learn more about this feature",
    },
    docs: {
      type: Boolean,
      required: false,
      default: true,
    },
    url: {
      type: String,
      required: false,
      default: "intro",
    },
  },
  data() {
    return {};
  },
  methods: {
    openHelpDocs() {
      const helpURL = `https://docs.fairshareapp.io/docs/${this.url}`;
      window.ipcRenderer.send("open-link-in-browser", helpURL);
    },
  },
  mounted() {},
};
</script>
