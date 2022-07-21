<template>
  <div class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <h1 class="pb-1 text-left text-lg font-medium">Let's decide what to upload</h1>
      <p class="text-left">
        In this step you can decide what to upload to the data repository. Your source code will be
        automatically saved but you can also add additional files.
      </p>

      <line-divider />

      <div class="w-full">
        <span class="mb-2 w-full">
          Would you like to add additional files to your upload? We will handle all your source code
          from the GitHub repository.
        </span>

        <div class="py-1">
          <el-radio v-model="addAdditionalFiles" label="Yes" size="large"> Yes </el-radio>
          <el-radio v-model="addAdditionalFiles" label="No" size="large"> No </el-radio>
          <el-radio v-model="addAdditionalFiles" label="None" size="large" border class="!hidden">
            None
          </el-radio>
        </div>
      </div>

      <div v-if="addAdditionalFiles !== 'None'" class="flex h-full w-full flex-col items-center">
        <transition name="fade" mode="out-in" appear>
          <div v-if="addAdditionalFiles === 'Yes'" class="flex h-full w-full flex-col items-center">
            <line-divider class="w-full"></line-divider>

            <div class="w-full">
              <span class="mb-4 w-full">
                Are these files stored on your computer or do you want the files to be downloaded
                from a GitHub release?
              </span>

              <div class="mt-3 flex flex-row justify-start py-1">
                <el-radio-group v-model="additionalFilesLocation" size="large">
                  <el-radio-button label="local"> On my computer </el-radio-button>
                  <el-radio-button label="github"> Pick a GitHub release </el-radio-button>
                </el-radio-group>
              </div>
            </div>
          </div>
        </transition>

        <div
          v-if="additionalFilesLocation === 'local'"
          class="flex h-full w-full flex-col items-center"
        >
          <el-upload
            class="upload-demo"
            drag
            multiple
            :auto-upload="false"
            show-file-list
            ref="fileUploadThing"
          >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">Drop file here or <em>click to select</em></div>
            <template #tip>
              <div class="el-upload__tip">jpg/png files with a size less than 500kb</div>
            </template>
          </el-upload>
        </div>

        <pre>{{ this.$refs.fileUploadThing.files }}</pre>

        <div
          v-if="additionalFilesLocation === 'github'"
          class="flex h-full w-full flex-col items-center"
        >
          github selector
        </div>
      </div>
    </div>
    <app-docs-link url="curate-and-share/connect-github-zenodo" position="bottom-4" />
  </div>
</template>

<script>
import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

export default {
  name: "GithubChooseUpload",
  components: {},
  data() {
    return {
      datasetStore: useDatasetsStore(),
      tokens: useTokenStore(),
      dataset: {},
      folderPath: "",
      workflowID: this.$route.params.workflowID,
      workflow: {},
      GithubAccessToken: "",
      selectedRepo: "",
      fileList: [],
      addAdditionalFiles: "Yes",
      additionalFilesLocation: "local",
    };
  },

  methods: {
    openWebsite() {
      const url = `${process.env.VUE_APP_ZENODO_URL}/account/settings/github`;
      window.ipcRenderer.send("open-link-in-browser", url);
    },

    async cancelUpload(files) {
      console.log(files);
      return false;
    },

    async showSummary() {
      if (this.addAdditionalFiles === "Yes") {
        this.workflow.addAdditionalFiles = true;
      } else {
        this.workflow.addAdditionalFiles = false;
      }

      await this.datasetStore.updateCurrentDataset(this.dataset);
      await this.datasetStore.syncDatasets();

      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/github/summary`;

      this.$router.push({ path: routerPath });
    },
  },

  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    this.selectedRepo = this.workflow.github.repo;

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(6);

    const tokenObject = await this.tokens.getToken("github");
    this.GithubAccessToken = tokenObject.token;

    // }

    this.workflow.currentRoute = this.$route.path;
  },
};
</script>
