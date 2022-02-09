<template>
  <div
    class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 pr-5"
  >
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium">
        Publish your work to Zenodo
      </span>
      <span class="text-left">
        All your metadata files have been uploaded to GitHub. It's now time to
        publish your work to Zenodo.
      </span>

      <el-divider class="my-4"> </el-divider>

      <div class="flex h-full flex-col items-center justify-start">
        <p class="pb-5 font-medium">
          To publish the dataset to Zenodo all you need to do is publish a new
          release.
          <!-- Once the record is published you will no longer be able to change the
          files in this upload. This is because a Digital Object Identifier
          (DOI) will be registered immediately after publishing. You will still
          be able to update the record's metadata later. -->
        </p>

        <div
          class="flex items-center justify-center space-x-4"
          v-if="showReleasePrompt"
        >
          <p class="text-center">Do you want us to create a release for you?</p>
          <button class="danger-plain-button" @click="declineRelease">
            No, I'll do it myself
          </button>
          <button class="primary-button" @click="approveRelease">
            Yes, Create a release
          </button>
        </div>

        <div class="" v-if="showDeclinedInstructions">
          <p class="text-center">
            If you would like to use Fair Share to complete this step you can
            always come back to this page and create to create releases.
          </p>
        </div>

        <div
          class="flex w-full flex-col space-x-4 py-5"
          v-if="showApprovedInstructions"
        >
          <div>
            <el-form
              ref="releaseForm"
              :model="releaseForm"
              label-width="170px"
              @submit.prevent
              :rules="rules"
              class="rounded-lg border-2 border-slate-100 p-4"
            >
              <el-form-item label="Tag name" prop="tagName">
                <div class="flex flex-row items-center">
                  <el-input
                    v-model="releaseForm.tagName"
                    placeholder="v1.0.0 or v0.2.0-alpha or v5.9-beta.3"
                  ></el-input>
                  <form-help-content
                    popoverContent="It's common practice to prefix your version names with the letter 'v'. If the tag isn't meant for production use, add a pre-release version after the version name."
                  />
                </div>
              </el-form-item>

              <el-form-item label="Release title" prop="name">
                <el-input v-model="releaseForm.name"></el-input>
              </el-form-item>

              <el-form-item label="Is this ">
                <el-switch v-model="releaseForm.prerelease"></el-switch>
              </el-form-item>

              <el-form-item label="Release description">
                <el-popover
                  ref="popover"
                  placement="bottom"
                  :width="300"
                  trigger="manual"
                >
                  <template #reference>
                    <el-input
                      v-model="releaseForm.body"
                      type="textarea"
                    ></el-input>
                  </template>

                  <span class="break-normal text-left text-sm">
                    Use a description that is easily identifiable. This will be
                    shown in the dataset selection screen and is not part of
                    your submitted metadata.
                  </span>
                </el-popover>
              </el-form-item>

              <!-- <div class="flex flex-row justify-center space-x-4 py-4">
          <button class="danger-plain-button" @click="cancelNewDataset">
            <el-icon><circle-close-filled /></el-icon> Cancel
          </button>

          <button class="primary-button" @click="submitForm('datasetForm')">
            Create new project <el-icon><d-arrow-right /></el-icon>
          </button>
        </div> -->
            </el-form>
          </div>

          <div class="flex items-center justify-center py-5">
            <p>
              Do you want to create a
              <span class="font-semibold">published</span> or a
              <span class="font-semibold">draft</span> release?
            </p>
            <form-help-content popoverContent="Helpful text here" />
          </div>

          <div class="flex items-center justify-center space-x-4">
            <button
              class="secondary-plain-button"
              @click="createRelease('publish')"
            >
              Create a published release
            </button>
            <button
              class="primary-plain-button"
              @click="createRelease('draft')"
            >
              Create a draft release
            </button>
          </div>
        </div>

        <div class="flex hidden space-x-4">
          <button class="primary-plain-button" @click="openCommitList">
            View commits
          </button>
          <button class="primary-plain-button" @click="openDraftRelease">
            View all releases
          </button>
          <button
            class="blob primary-button transition-all"
            @click="publishDeposition"
          >
            Publish <el-icon><star-icon /></el-icon>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import axios from "axios";
// import { ElMessageBox, ElLoading } from "element-plus";

import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

export default {
  name: "GithubPublish",
  data() {
    return {
      datasetStore: useDatasetsStore(),
      tokens: useTokenStore(),
      dataset: {},
      folderPath: "",
      datasetID: this.$route.params.datasetID,
      workflowID: this.$route.params.workflowID,
      workflow: {},
      githubToken: "",
      showReleasePrompt: false,
      showDeclinedInstructions: false,
      showApprovedInstructions: true,
      releaseForm: {
        tagName: "",
        name: "",
        body: "",
        prerelease: false,
        generateReleaseNotes: false,
      },
      rules: {
        tagName: [
          {
            required: true,
            message: "Please provide a tag name",
            trigger: "blur",
          },
        ],
        name: [
          {
            required: true,
            message: "Please provide a name for the release",
            trigger: "blur",
          },
        ],
      },
    };
  },
  computed: {},
  methods: {
    async sleep(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    },

    async openCommitList() {
      const repoName = this.workflow.github.repo;
      const githubURL = `https://github.com/${repoName}/commits`;

      window.ipcRenderer.send("open-link-in-browser", githubURL);
    },
    async openDraftRelease() {
      const repoName = this.workflow.github.repo;
      const githubURL = `https://github.com/${repoName}/releases`;

      window.ipcRenderer.send("open-link-in-browser", githubURL);
    },
    declineRelease() {
      this.showReleasePrompt = false;
      this.showDeclinedInstructions = true;
    },
    approveRelease() {
      this.showReleasePrompt = false;
      this.showApprovedInstructions = true;
    },
    createRelease(releaseType) {
      console.log("createRelease", releaseType);
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(7);

    this.workflow.currentRoute = this.$route.path;

    const tokenObject = await this.tokens.getToken("github");
    this.githubToken = tokenObject.token;

    //change this to look more like the github ui
    // console.log(this.zenodoToken);
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
