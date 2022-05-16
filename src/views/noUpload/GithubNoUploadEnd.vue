<template>
  <div class="flex h-full w-full flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium"> Final step </span>
      <span class="text-left"> All your requested data has been generated and uploaded. </span>

      <el-divider class="my-4"> </el-divider>

      <div class="flex h-full flex-col items-center justify-center px-2">
        <p class="pb-5 text-center">
          It does not look like you have selected a data repository to upload your files to. This is
          not recommended if you are trying to make your dataset FAIR. You can come back to this
          page later and select a data sharing repository to make your dataset completely FAIR.
        </p>
        <div class="flex space-x-4">
          <router-link :to="`/datasets`" class="">
            <button class="primary-plain-button">
              <el-icon><data-line /></el-icon> Go to the homepage
            </button>
          </router-link>
          <button class="secondary-plain-button" @click="openRepository">
            <el-icon><fold-icon /></el-icon>
            View GitHub repository
          </button>
          <button class="secondary-plain-button" @click="showBadges">
            <el-icon><chat-line-square /></el-icon> Add a badge to your README
          </button>
          <button class="primary-button blob transition-all" @click="navigateToBioToolsPublishing">
            <el-icon><suitcase-icon /></el-icon> Register on bio.tools
          </button>
        </div>
        <general-dialog
          ref="showBadgesDialog"
          title="Add this badge to your GitHub repository readme to showcase your FAIRness"
        >
          <div class="mt-4 flex flex-col">
            <div class="py-2">
              <img :src="$fairshare_badge_image_url" alt="" />
            </div>
            <div class="divide-y divide-gray-200">
              <div class="py-2">
                <p class="pb-2 text-base font-semibold text-gray-700">Markdown</p>
                <div
                  class="relative w-full break-normal rounded-lg border border-zinc-300 bg-zinc-100 py-2 px-3"
                >
                  <div
                    class="badge-container h-[50px] overflow-x-auto overflow-y-hidden whitespace-nowrap text-left font-mono text-sm"
                  >
                    <code>
                      [![{{ $fairshare_badge_text }}]({{
                        $fairshare_badge_image_url
                      }})](https://fairdataihub.org/fairshare)
                    </code>
                  </div>
                  <div
                    class="absolute bottom-2 right-2 rounded-lg bg-transparent opacity-40 transition-all hover:bg-zinc-200 hover:opacity-95"
                    @click="copyToClipboard('markdown')"
                  >
                    <el-tooltip
                      class="box-item"
                      effect="dark"
                      content="Copy to clipboard"
                      placement="bottom"
                    >
                      <button class="flex items-center justify-center p-1">
                        <el-icon :size="20"><copy-document /></el-icon>
                      </button>
                    </el-tooltip>
                  </div>
                </div>
              </div>
              <div class="py-2">
                <p class="pb-2 text-base font-semibold text-gray-700">HTML</p>
                <div
                  class="relative w-full break-normal rounded-lg border border-zinc-300 bg-zinc-100 py-2 px-3"
                >
                  <div
                    class="badge-container h-[50px] overflow-x-auto overflow-y-hidden whitespace-nowrap text-left font-mono text-sm"
                  >
                    <code>
                      &lt;a href="https://fairdataihub.org/fairshare"&gt;&lt;img src="{{
                        $fairshare_badge_image_url
                      }}" alt="{{ $fairshare_badge_text }}"/&gt;&lt;/a&gt;
                    </code>
                  </div>
                  <div
                    class="absolute bottom-2 right-2 rounded-lg bg-transparent opacity-40 transition-all hover:bg-zinc-200 hover:opacity-95"
                    @click="copyToClipboard('html')"
                  >
                    <el-tooltip
                      class="box-item"
                      effect="dark"
                      content="Copy to clipboard"
                      placement="bottom"
                    >
                      <button class="flex items-center justify-center p-1">
                        <el-icon :size="20"><copy-document /></el-icon>
                      </button>
                    </el-tooltip>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </general-dialog>
      </div>
    </div>
  </div>
</template>

<script>
import { useDatasetsStore } from "@/store/datasets";

export default {
  name: "LocalNoUploadEnd",
  data() {
    return {
      datasetStore: useDatasetsStore(),
      dataset: {},
      folderPath: "",
      datasetID: this.$route.params.datasetID,
      workflowID: this.$route.params.workflowID,
      workflow: {},
      zenodoToken: "",
      published: false,
      zenodoDatasetID: "",
    };
  },
  computed: {},
  methods: {
    async sleep(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    },
    navigateToBioToolsPublishing() {
      this.$router.push(`/datasets/${this.datasetID}/${this.workflowID}/biotools/login`);
    },
    async openRepository() {
      const githubURL = `https://github.com/${this.dataset.meta.locationPath}`;
      window.ipcRenderer.send("open-link-in-browser", githubURL);
    },
    showBadges() {
      this.$refs.showBadgesDialog.show();
    },
    copyToClipboard(type) {
      this.$track("Badges", "Curated with FAIRshare", type);
      if (type === "markdown") {
        const text = `[![${this.$fairshare_badge_text}](${this.$fairshare_badge_image_url})](https://fairdataihub.org/fairshare)`;
        window.ipcRenderer.send("write-to-clipboard", text, "text");
        this.$notify({
          title: "Copied to clipboard",
          message: "Markdown badge code copied to clipboard",
          type: "success",
          duration: 2000,
          position: "bottom-right",
        });
      }
      if (type === "html") {
        const html = `<a href="https://fairdataihub.org/fairshare"><img src="${this.$fairshare_badge_image_url}" alt="${this.$fairshare_badge_text}"/></a>`;
        window.ipcRenderer.send("write-to-clipboard", html, "text");
        this.$notify({
          title: "Copied to clipboard",
          message: "HTML badge code copied to clipboard",
          type: "success",
          duration: 2000,
          position: "bottom-right",
        });
      }
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(7);

    this.workflow.currentRoute = this.$route.path;

    this.showBadges();
  },
};
</script>

<style lang="postcss" scoped>
.blob {
  box-shadow: 0 0 0 0 rgba(52, 172, 224, 1);
  animation: pulse-blue 2s infinite;
}

@keyframes pulse-blue {
  0% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(52, 172, 224, 0.7);
  }

  70% {
    transform: scale(1);
    box-shadow: 0 0 0 10px rgba(52, 172, 224, 0);
  }

  100% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(52, 172, 224, 0);
  }
}
</style>
