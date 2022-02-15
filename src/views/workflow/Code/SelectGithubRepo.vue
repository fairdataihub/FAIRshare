<template>
  <div
    class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 pr-5"
  >
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium">
        Pick the Github repository you want to use
      </span>
      <span class="text-left">
        Lets select the github repository that you want to make FAIR.
      </span>

      <el-divider class="my-4"> </el-divider>

      <div v-if="ready">
        <div v-if="validTokenAvailable">
          <p class="my-5 w-full text-center">
            Pick the Github repository you want to use.
          </p>

          <div class="py-5">
            <el-select-v2
              v-model="selectedRepo"
              filterable
              :options="githubRepos"
              placeholder="Please select"
              popper-class="github-repo-select"
              class="some-random-class w-full"
              @change="handleSelected"
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
            We couldn't find your Github login details. Please click on the
            button below to connect to your Github account.
          </p>

          <ConnectGithub :statusChangeFunction="showConnection"></ConnectGithub>
        </div>
      </div>
      <LoadingFoldingCube v-else></LoadingFoldingCube>

      <div v-if="selectedRepo" class="py-5">
        <line-divider />
        <p class="text=lg my-5">
          A list of all the files in the selected repository. Branch:
          {{ this.currentBranch }}
        </p>
        <el-tree
          :data="fileData"
          :props="defaultProps"
          @node-click="handleNodeClick"
        >
          <template #default="{ node }">
            <el-icon v-if="!node.isLeaf"><folder-icon /></el-icon>
            <el-icon v-if="node.isLeaf"><document-icon /></el-icon>
            <span>{{ node.label }}</span>
          </template>
        </el-tree>
      </div>

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
          class="primary-button"
          :disabled="disableContinue"
          @click="continueToNextStep"
          v-if="validTokenAvailable"
        >
          Continue
          <el-icon> <d-arrow-right /> </el-icon>
        </button>
      </div>
    </div>
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
      ready: false,
      defaultProps: {
        children: "children",
        label: "label",
      },
      fileData: [],
      ownerDictionary: {},
      nameDictionary: {},
      branchDictionary: {},
      tree: [],
      fullNameDictionary: {},
    };
  },
  //el-tree-node__content
  computed: {
    disableContinue() {
      if (this.selectedRepo !== "") {
        return false;
      }
      return true;
    },
    currentBranch() {
      if (
        this.selectedRepo !== "" &&
        this.branchDictionary[this.selectedRepo]
      ) {
        return this.branchDictionary[this.selectedRepo].name;
      }
      return null;
    },
    anyfilePreview() {
      if (
        this.PreviewNewlyCreatedMetadataFile ||
        this.PreviewNewlyCreatedLicenseFile ||
        this.PreviewNewlyCreatedCitationFile
      ) {
        return true;
      } else {
        return false;
      }
    },
  },
  methods: {
    openGithubWebsite(url) {
      window.ipcRenderer.send("open-link-in-browser", url);
    },
    async handleNodeClick(data) {
      this.openGithubWebsite(
        "https://github.com/" +
          this.selectedRepo +
          "/tree/" +
          this.currentBranch +
          "/" +
          this.fullNameDictionary[data.label]
      );
    },
    async handleSelected(selected) {
      let branches = await this.tokens.githubAPI_listCurrentRepoBranches(
        this.GithubAccessToken,
        this.nameDictionary[selected],
        this.ownerDictionary[selected]
      );
      this.branchDictionary[selected] = branches[0];
      let tree = await this.tokens.githubAPI_getTreeFromRepo(
        this.GithubAccessToken,
        this.nameDictionary[selected],
        this.ownerDictionary[selected],
        branches[0].name
      );
      for (let i = 0; i < tree.tree.length; i++) {
        this.tree.push(tree.tree[i]["path"]);
      }
      this.fileData = await this.parseTree();
    },
    async parseTree() {
      let paths = this.tree;
      let result = [];
      let level = { result };
      paths.forEach((path) => {
        this.fullNameDictionary[path.split("/").pop()] = path;
      });
      paths.forEach((path) => {
        path.split("/").reduce((r, label) => {
          if (!r[label]) {
            r[label] = { result: [] };
            r.result.push({ label, children: r[label].result });
          }

          return r[label];
        }, level);
      });
      console.log(result);
      return result;
    },
    createLoading() {
      const loading = ElLoading.service({
        lock: true,
        text: "Loading repositories...",
      });
      return loading;
    },
    async checkToken(token) {
      console.log(token);
      const response = await this.tokens.getDepositions(token);

      if (response.status === 200) {
        this.validTokenAvailable = true;
        this.tokens.saveToken("Github", token);
        return true;
      } else if (response.status === 401) {
        this.errorMessage =
          "Invalid Github access token. Please enter a valid Github access token.";
        this.validTokenAvailable = false;
        return false;
      } else {
        this.errorMessage = "Something went wrong. Please try again.";
        this.validTokenAvailable = false;
        return false;
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

      this.datasetStore.updateCurrentDataset(this.dataset);
      this.datasetStore.syncDatasets();

      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/Code/reviewStandards`;
      if (this.validTokenAvailable) {
        this.$router.push({ path: routerPath });
      }
    },
    async getUserRepos() {
      const response = await axios
        .get(`${process.env.VUE_APP_GITHUB_SERVER_URL}/user/repos`, {
          params: {
            accept: "application/vnd.github.v3+json",
            per_page: 100,
          },
          headers: {
            Authorization: `Bearer ${this.GithubAccessToken}`,
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
          this.githubRepos.push({
            value: repo.full_name,
            label: repo.full_name,
            visibility: repo.visibility,
            originalObject: repo,
          });
          this.ownerDictionary[repo.full_name] = repo.owner.login;
          this.nameDictionary[repo.full_name] = repo.name;
        });
      }

      // console.log(response);
    },
    async showConnection(status) {
      console.log(status);
      if (status === "connected") {
        this.validTokenAvailable = true;
      }
      // this.uploadToGithub(); console.log(this.workflow.licenseText)
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

    console.log(validGithubConnection);

    if (validGithubConnection) {
      this.validTokenAvailable = true;
      this.ready = true;

      const tokenObject = await this.tokens.getToken("github");
      this.GithubAccessToken = tokenObject.token;

      console.log(this.GithubAccessToken);

      await this.getUserRepos();

      if ("github" in this.workflow) {
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
