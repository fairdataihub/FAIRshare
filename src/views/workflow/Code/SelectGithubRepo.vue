<template>
  <div class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium">
        Pick the GitHub repository you want to use
      </span>
      <span class="text-left"> Lets select the GitHub repository that you want to make FAIR. </span>

      <el-divider class="my-4"> </el-divider>

      <div v-if="ready">
        <div v-if="validTokenAvailable">
          <p class="my-5 w-full text-center">
            Pick the GitHub repository you want to use. <br />
            FAIRshare only supports public GitHub repositories.
          </p>

          <div class="py-5">
            <el-select-v2
              v-model="selectedRepo"
              filterable
              :options="githubRepos"
              placeholder="Please select"
              popper-class="github-repo-select"
              @change="showGithubRepoContents('change')"
              size="large"
              class="w-full"
            >
              <template #default="{ item }">
                <el-tag
                  class="min-w-[60px] text-center"
                  :type="item.visibility === 'public' ? '' : 'warning'"
                  size="small"
                  >{{ item.visibility }}</el-tag
                >
                <span class="mx-2">{{ item.label }}</span>
              </template>
            </el-select-v2>
          </div>
        </div>
        <!-- show error message if token is not valid -->
        <div v-else class="flex flex-col items-center justify-center py-10">
          <p class="mb-5">
            We couldn't find your GitHub login details. Please click on the button below to connect
            to your GitHub account.
          </p>

          <ConnectGithub :statusChangeFunction="showConnection"></ConnectGithub>
        </div>
      </div>
      <LoadingFoldingCube v-else></LoadingFoldingCube>

      <div class="flex w-full flex-row justify-center space-x-4 py-2">
        <router-link
          :to="`/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/Code/selectFolder`"
          class=""
        >
          <button class="primary-plain-button">
            <el-icon><d-arrow-left /></el-icon> Back
          </button>
        </router-link>

        <button
          class="secondary-plain-button"
          @click="showGithubRepoContents('click')"
          v-if="selectedRepo !== ''"
        >
          <el-icon><checked-icon /></el-icon>
          View files in repository
        </button>

        <button
          class="primary-button"
          :disabled="disableContinue"
          @click="continueToNextStep"
          v-if="validTokenAvailable"
        >
          Continue
          <el-icon> <d-arrow-right /> </el-icon>
        </button>
      </div>

      <div v-if="showFilePreview" class="py-5">
        <line-divider />
        <p class="text=lg my-5">
          A list of all the files and folders in the selected repository are shown below. Current
          branch is <b>{{ currentBranch }}</b
          >.
        </p>
        <el-tree-v2 :data="fileData" :props="defaultProps">
          <template #default="{ node, data }">
            <el-icon v-if="!node.isLeaf"><folder-icon /></el-icon>
            <el-icon v-if="node.isLeaf"><document-icon /></el-icon>
            <span>{{ node.label }}</span>

            <button
              v-if="node.isLeaf"
              @click="handleNodeClick(data, 'view')"
              class="ml-2 flex items-center rounded-lg bg-primary-100 py-[3px] shadow-sm transition-all hover:bg-primary-200"
            >
              <el-icon><view-icon /></el-icon>
            </button>
          </template>
        </el-tree-v2>
      </div>
    </div>
    <transition name="fade" mode="out-in" appear>
      <div class="fixed bottom-2 right-3" v-show="showSpinner">
        <Vue3Lottie :animationData="$helix_spinner" :width="80" :height="80" />
      </div>
    </transition>
  </div>
</template>

<script>
import LoadingFoldingCube from "@/components/spinners/LoadingFoldingCube";
import ConnectGithub from "@/components/serviceIntegration/ConnectGithub";

import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

import axios from "axios";

import { ElLoading } from "element-plus";

export default {
  name: "SelectGithubRepo",
  components: { LoadingFoldingCube, ConnectGithub },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      tokens: useTokenStore(),
      dataset: {},
      folderPath: "",
      workflowID: this.$route.params.workflowID,
      workflow: {},
      validTokenAvailable: false,
      errorMessage: "",
      GithubAccessToken: "",
      githubRepos: [],
      selectedRepo: "",
      currentBranch: "",
      showFilePreview: false,
      ready: false,
      defaultProps: {
        value: "id",
        children: "children",
        label: "label",
      },
      fileData: [],
      showSpinner: false,
    };
  },
  computed: {
    disableContinue() {
      if (this.selectedRepo !== "") {
        return false;
      }
      return true;
    },
  },
  methods: {
    createLoading() {
      const loading = ElLoading.service({
        lock: true,
        text: "Loading repositories...",
      });
      return loading;
    },

    async showGithubRepoContents(type) {
      if (type === "click") {
        this.showFilePreview = !this.showFilePreview;
      }

      if (this.showFilePreview) {
        this.showSpinner = true;
        this.fileData = [];
        const response = await this.getGithubRepoContents();
        this.showSpinner = false;

        if (response !== "ERROR") {
          this.fileData = JSON.parse(response);
        } else {
          this.$message({
            message: "Could not get the contents of the repository",
            type: "error",
          });
        }
      }
    },

    async getGithubRepoContents() {
      const repoObject = this.githubRepos.find((repo) => repo.value === this.selectedRepo);

      const fullRepoName = repoObject.label.split("/");
      this.currentBranch = repoObject.default_branch;

      const response = await axios
        .get(`${this.$server_url}/github/repo/tree`, {
          params: {
            access_token: this.GithubAccessToken,
            owner: fullRepoName[0],
            repo: fullRepoName[1],
          },
        })
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });

      return response;
    },

    async handleNodeClick(data, _action) {
      const githubURL = `https://github.com/${this.selectedRepo}/tree/${this.currentBranch}/${data.path}`;
      if (data.isLeaf) {
        window.ipcRenderer.send("open-link-in-browser", githubURL);
      }
    },

    async continueToNextStep() {
      const repoObject = this.githubRepos.find((repo) => {
        return repo.full_name === this.selectedRepo;
      });

      if ("github" in this.workflow) {
        this.workflow.github.repo = this.selectedRepo;
        this.workflow.github.fullObject = repoObject;
      } else {
        this.workflow.github = {
          repo: this.selectedRepo,
          fullObject: repoObject,
        };
      }

      this.dataset.meta.locationPath = this.selectedRepo;

      this.datasetStore.updateCurrentDataset(this.dataset);
      this.datasetStore.syncDatasets();

      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/Code/reviewStandards`;
      if (this.validTokenAvailable) {
        this.$router.push({ path: routerPath });
      }
    },

    async getUserRepos() {
      const response = await axios
        .get(`${this.$server_url}/github/user/repos`, {
          params: {
            access_token: this.GithubAccessToken,
          },
        })
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });

      if (response === "ERROR") {
        this.errorMessage = "Something went wrong. Please try again.";
        this.validTokenAvailable = false;
      } else {
        response.forEach((repo) => {
          const selectionDisabled = repo.visibility === "private" ? true : false;
          this.githubRepos.push({
            value: repo.full_name,
            label: repo.full_name,
            visibility: repo.visibility,
            originalObject: repo,
            default_branch: repo.default_branch,
            disabled: selectionDisabled,
          });
        });
      }
    },
    async showConnection(status, token = "") {
      console.log(status);
      if (status === "connected") {
        this.validTokenAvailable = true;

        if (token !== "") {
          this.GithubAccessToken = token;
          await this.getUserRepos();
        }
      }
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    let spinner = this.createLoading();

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(1);

    this.workflow.currentRoute = this.$route.path;

    const validGithubConnection = await this.tokens.verifyGithubConnection();

    if (validGithubConnection) {
      this.validTokenAvailable = true;
      this.ready = true;

      const tokenObject = await this.tokens.getToken("github");
      this.GithubAccessToken = tokenObject.token;

      await this.getUserRepos();

      if ("github" in this.workflow && "repo" in this.workflow.github) {
        this.selectedRepo = this.workflow.github.repo;
      }

      spinner.close();
    } else {
      this.validTokenAvailable = false;
      this.ready = true;

      spinner.close();
    }
  },
};
</script>
