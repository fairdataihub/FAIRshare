<template>
  <div
    class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 pr-5"
  >
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-semibold">
        Publish your work to Zenodo
      </span>
      <span class="text-left">
        All your metadata files have been uploaded to GitHub. It's now time to
        publish your work to Zenodo by creating a release on GitHub.
      </span>

      <el-divider class="my-4"> </el-divider>

      <div
        class="flex h-full flex-col items-center justify-start"
        :class="{
          'justify-center': showReleasePrompt || showDeclinedInstructions,
          'justify-start': showApprovedInstructions,
        }"
        v-if="!showFinalInstructions"
      >
        <div
          class="flex items-center justify-center space-x-4 pb-20"
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

        <div
          v-if="showDeclinedInstructions"
          class="flex flex-col items-center justify-center"
        >
          <p class="pb-10 text-center text-lg">
            No worries. You can always come back to this page and let FAIRshare
            create your release for you.
          </p>
          <button class="primary-button" @click="approveRelease">
            <el-icon><edit-icon /></el-icon>
            I changed my mind. Create a release for me
          </button>
        </div>

        <div
          class="flex w-full flex-col space-x-4 pb-5"
          v-if="showApprovedInstructions"
        >
          <div class="w-full px-2">
            <div class="flex w-full flex-row items-center py-1">
              <p class="w-[200px] px-2 text-[15px] font-semibold text-zinc-600">
                Create a tag <span class="text-red-600">*</span>
              </p>

              <div class="grow">
                <el-dropdown
                  ref="dropdown1"
                  trigger="click"
                  size="large"
                  max-height="350px"
                >
                  <el-input
                    v-model="selectedTag"
                    size="large"
                    placeholder="v4.5.8 or v4.5.8-beta "
                    clearable
                    class="flex px-2"
                  />
                  <template #dropdown>
                    <div class="w-full px-5 pt-3">
                      <p class="text-sm">Your previous tags are shown below</p>
                    </div>
                    <el-dropdown-menu class="w-full">
                      <el-dropdown-item
                        v-for="(item, index) in retrievedTags"
                        :key="item.value"
                        :disabled="item.disabled"
                        :divided="index === 0"
                      >
                        {{ item.label }}
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </div>

            <div class="flex flex-row items-center py-1">
              <p class="w-[200px] px-2 text-[15px] font-semibold text-zinc-600">
                Choose a target branch <span class="text-red-600">*</span>
              </p>
              <el-select
                v-model="selectedBranch"
                class="m-2"
                placeholder="Find or create a new tag"
                size="large"
                :filterable="true"
              >
                <el-option
                  v-for="item in retrievedBranches"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                >
                </el-option>
              </el-select>
            </div>

            <div class="flex flex-row items-center py-1">
              <p class="w-[200px] px-2 text-[15px] font-semibold text-zinc-600">
                Release title <span class="text-red-600">*</span>
              </p>

              <div class="grow">
                <el-input
                  v-model="releaseTitle"
                  size="large"
                  placeholder="Please input"
                  clearable
                  class="px-2"
                />
              </div>
            </div>

            <div class="my-2 flex flex-col py-3">
              <div class="flex items-end justify-between px-2 pb-2">
                <p class="text-[15px] font-semibold text-zinc-600">
                  Release description <span class="text-red-600">*</span>
                </p>
                <button
                  class="secondary-plain-button py-1 px-2"
                  @click="autoGenerateReleaseNotes"
                  :disabled="disableAutoGenerateReleaseNotes"
                >
                  <Icon icon="ic:baseline-auto-fix-high" class="mx-2 h-5 w-5" />
                  Auto generate release notes
                </button>
              </div>
              <div class="px-3">
                <v-md-editor
                  v-model="releaseBody"
                  height="400px"
                  left-toolbar="undo redo clear | h bold italic strikethrough quote | ul ol table hr | link"
                  right-toolbar="sync-scroll preview fullscreen"
                ></v-md-editor>
              </div>
            </div>

            <div class="flex items-start justify-start py-4">
              <div class="flex flex-col">
                <div class="flex items-center">
                  <p class="px-2 text-[15px] font-semibold text-zinc-600">
                    Is this a pre-release?
                  </p>
                  <el-tooltip
                    :content="prerelease ? 'Yes' : 'No'"
                    placement="right"
                  >
                    <el-switch
                      v-model="prerelease"
                      class="ml-2"
                      active-color="#2563eb"
                      inactive-color="#fdba74"
                    />
                  </el-tooltip>
                </div>
                <p
                  class="px-2 text-[14px] font-medium text-zinc-600"
                  v-if="prerelease"
                >
                  We will mark the release as non-production ready.
                </p>
              </div>
            </div>
          </div>

          <div class="py-5">
            <div class="flex items-center justify-center space-x-4">
              <button
                class="primary-plain-button"
                @click="createRelease('publish')"
                :disabled="disablePublish"
              >
                Publish release
              </button>
              <button
                class="primary-button"
                @click="createRelease('draft')"
                :disabled="disablePublish"
              >
                Create a draft release
              </button>
            </div>
          </div>
        </div>
      </div>
      <div
        class="flex h-full flex-col items-center justify-center"
        v-if="showFinalInstructions"
      >
        <Vue3Lottie
          animationLink="https://assets4.lottiefiles.com/packages/lf20_lg6lh7fp.json"
          class="pointer-events-none absolute top-0 left-0 h-full w-full"
          :loop="1"
        />
        <div v-if="draftReleaseURL !== ''">
          <p class="pb-10 text-center font-medium">
            Your draft release is now on GitHub. You can go in and add
            additional files or edit items before publishing. <br />
            You will also be able to directly publish your draft from GitHub.
            <br />
            <span class="font-medium text-secondary-500">
              This will automatically push your release to Zenodo.
            </span>
          </p>
        </div>
        <div v-if="publishedReleaseURL !== ''">
          <p class="pb-10 text-center text-lg font-medium">
            Your release was published successfully. <br />
            You can view it on Zenodo and get your DOI.
          </p>
        </div>
        <div class="flex space-x-4">
          <button class="primary-plain-button" @click="openCommitList">
            <el-icon><fold-icon /></el-icon>
            View commits
          </button>
          <button class="primary-plain-button" @click="openAllReleases">
            <el-icon><box-icon /></el-icon>
            View all releases
          </button>
          <button
            class="primary-button"
            @click="openDraftRelease(draftReleaseURL)"
            v-if="draftReleaseURL !== ''"
          >
            <el-icon><flag-icon /></el-icon>
            View draft release on GitHub
          </button>
          <button
            class="secondary-plain-button"
            @click="openDraftRelease(publishedReleaseURL)"
            v-if="publishedReleaseURL !== ''"
          >
            <el-icon><upload-filled /></el-icon>
            View release on GitHub
          </button>
          <button
            class="primary-button"
            @click="viewZenodoRelease"
            v-if="publishedReleaseURL !== ''"
          >
            <el-icon><star-icon /></el-icon>
            View release on Zenodo
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ElLoading, ElNotification } from "element-plus";
import { Icon } from "@iconify/vue";

import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

export default {
  name: "GithubPublish",
  components: { Icon },
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
      repoName: "",
      showReleasePrompt: true,
      showDeclinedInstructions: false,
      showApprovedInstructions: false,
      retrievedTags: [],
      selectedTag: "",
      retrievedBranches: [],
      selectedBranch: "",
      releaseTitle: "",
      releaseBody: "# Your release notes here",
      prerelease: false,
      draftReleaseURL: "",
      publishedReleaseURL: "",
      showFinalInstructions: false,
    };
  },
  computed: {
    disableAutoGenerateReleaseNotes() {
      if (this.selectedTag === "") {
        return true;
      }
      if (this.selectedBranch === "") {
        return true;
      }
      return false;
    },
    disablePublish() {
      const valid = this.validateReleaseForm();
      if (valid) {
        return false;
      } else {
        return true;
      }
    },
  },
  methods: {
    async sleep(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    },
    selectEvent(type) {
      console.log(type, this.selectedTag);
    },
    openDropdown() {
      this.$refs.dropdown1.handleOpen();
    },
    createLoading() {
      const loading = ElLoading.service({
        lock: true,
        text: "Reading GitHub repository...",
      });
      return loading;
    },
    validateReleaseForm() {
      if (this.selectedTag === "") {
        return false;
      }

      if (this.selectedBranch === "") {
        return false;
      }

      if (this.releaseTitle === "") {
        return false;
      }

      if (this.releaseBody === "") {
        return false;
      }

      return true;
    },
    async openCommitList() {
      const githubURL = `https://github.com/${this.repoName}/commits`;

      window.ipcRenderer.send("open-link-in-browser", githubURL);
    },
    async openAllReleases() {
      const githubURL = `https://github.com/${this.repoName}/releases`;

      window.ipcRenderer.send("open-link-in-browser", githubURL);
    },
    async openDraftRelease(githubURL) {
      window.ipcRenderer.send("open-link-in-browser", githubURL);
    },
    async viewZenodoRelease() {
      const zenodoURL = `${process.env.VUE_APP_ZENODO_URL}/deposit`;
      window.ipcRenderer.send("open-link-in-browser", zenodoURL);
    },
    declineRelease() {
      this.showReleasePrompt = false;
      this.showApprovedInstructions = false;
      this.showDeclinedInstructions = true;
    },
    approveRelease() {
      this.showReleasePrompt = false;
      this.showDeclinedInstructions = false;
      this.showApprovedInstructions = true;
    },
    async pushRelease(config) {
      return await axios(config)
        .then((response) => {
          if (response.status === 201) {
            if ("html_url" in response.data) {
              return response.data.html_url;
            } else {
              return `https://github.com/${this.repoName}/releases`;
            }
          } else {
            throw new Error(
              `Error creating release: ${response.status} ${response.statusText}`
            );
          }
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });
    },
    async createRelease(releaseType) {
      let errorMessage = "";
      let successMessage = "";

      let requestBody = {
        tag_name: this.selectedTag,
        target_commitish: this.selectedBranch,
        name: this.releaseTitle,
        body: this.releaseBody,
        prerelease: this.prerelease,
      };

      if (releaseType === "publish") {
        let response = "";

        try {
          response = await this.$confirm(
            "Once a release has been made you will not be able to remove it from Zenodo. Are you sure you want to continue?",
            "Confirm publish",
            {
              confirmButtonText: "Publish",
              cancelButtonText: "Cancel",
              type: "warning",
            }
          );
        } catch (error) {
          response = error;
        }

        if (response !== "confirm") {
          return;
        }

        errorMessage = "Error publishing release";
        successMessage = "Release published successfully";
        requestBody.draft = false;
      }
      if (releaseType === "draft") {
        errorMessage = "There was an error with creating the draft release";
        successMessage = "Draft release created successfully";
        requestBody.draft = true;
      }

      const config = {
        method: "post",
        url: `${process.env.VUE_APP_GITHUB_SERVER_URL}/repos/${this.repoName}/releases`,
        headers: {
          Accept: "application/vnd.github.v3+json",
          Authorization: `Bearer ${this.githubToken}`,
          "Content-Type": "application/json",
        },
        data: JSON.stringify(requestBody),
      };

      const response = await this.pushRelease(config);

      if (response === "ERROR") {
        ElNotification({
          title: "Error",
          message: errorMessage,
          type: "error",
          position: "bottom-right",
        });
      } else {
        if (releaseType === "publish") {
          this.publishedReleaseURL = response;
        }
        if (releaseType === "draft") {
          this.draftReleaseURL = response;
        }

        ElNotification({
          title: "Success",
          message: successMessage,
          type: "success",
          position: "bottom-right",
        });

        this.showApprovedInstructions = false;
        this.showFinalInstructions = true;
      }
    },
    async autoGenerateReleaseNotes() {
      let response = "";

      const data = JSON.stringify({
        tag_name: this.selectedTag,
        target_commitish: this.selectedBranch,
      });

      const config = {
        method: "post",
        url: `${process.env.VUE_APP_GITHUB_SERVER_URL}/repos/${this.repoName}/releases/generate-notes`,
        headers: {
          Accept: "application/vnd.github.v3+json",
          Authorization: `Bearer ${this.githubToken}`,
          "Content-Type": "application/json",
        },
        data: data,
      };

      response = await axios(config)
        .then((response) => {
          console.log(response);
          if (response.status === 200) {
            console.log("response.data", response.data.body);
            this.releaseBody = response.data.body;
            return true;
          } else {
            return false;
          }
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });

      if (response !== "ERROR") {
        return response;
      } else {
        return false;
      }
    },
    async prefillGithubEntries() {
      let response = "";

      response = await axios
        .get(
          `${process.env.VUE_APP_GITHUB_SERVER_URL}/repos/${this.repoName}/tags`,
          {
            params: {
              per_page: 100,
            },
            headers: {
              Accept: "application/vnd.github.v3+json",
              Authorization: `Bearer ${this.githubToken}`,
            },
          }
        )
        .then((res) => {
          return res.data;
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });

      if (response !== "ERROR") {
        this.retrievedTags = response.map((tag) => {
          return {
            label: tag.name,
            value: tag.name,
            commit: tag.commit.sha,
            url: tag.commit.url,
            disabled: true,
          };
        });
      }

      response = await axios
        .get(
          `${process.env.VUE_APP_GITHUB_SERVER_URL}/repos/${this.repoName}/branches`,
          {
            params: {
              per_page: 100,
            },
            headers: {
              Accept: "application/vnd.github.v3+json",
              Authorization: `Bearer ${this.githubToken}`,
            },
          }
        )
        .then((res) => {
          return res.data;
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });

      if (response !== "ERROR") {
        this.retrievedBranches = response.map((branch) => {
          return {
            label: branch.name,
            value: branch.name,
            commit: branch.commit.sha,
            url: branch.commit.url,
          };
        });
      }

      response = await axios
        .get(
          `${process.env.VUE_APP_GITHUB_SERVER_URL}/repos/${this.repoName}`,
          {
            params: {},
            headers: {
              Accept: "application/vnd.github.v3+json",
              Authorization: `Bearer ${this.githubToken}`,
            },
          }
        )
        .then((res) => {
          return res.data;
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });

      if (response !== "ERROR") {
        this.selectedBranch = response.default_branch;
      }

      return;
    },
  },
  async mounted() {
    let spinner = this.createLoading();
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(7);

    this.workflow.currentRoute = this.$route.path;

    const tokenObject = await this.tokens.getToken("github");
    this.githubToken = tokenObject.token;

    this.repoName = this.workflow.github.repo;
    // this.repoName = "fairdataihub/Custom-Hook";
    // this.repoName = "fairdataihub/FAIRshare";

    await this.prefillGithubEntries();

    spinner.close();
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
