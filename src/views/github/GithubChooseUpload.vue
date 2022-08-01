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
        <p class="mb-2 w-full">
          Would you like to add additional files to your upload? We already have your code from
          GitHub added.
        </p>

        <div class="py-1">
          <el-radio v-model="addAdditionalFiles" label="Yes" size="large"> Yes </el-radio>
          <el-radio v-model="addAdditionalFiles" label="No" size="large"> No </el-radio>
          <el-radio v-model="addAdditionalFiles" label="None" size="large" border class="!hidden">
            None
          </el-radio>
        </div>
      </div>

      <div v-if="addAdditionalFiles !== 'None'" class="flex w-full flex-col">
        <transition name="fade" mode="out-in" appear>
          <div v-if="addAdditionalFiles === 'Yes'" class="flex h-full w-full flex-col">
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

        <div v-if="additionalFilesLocation === 'local'" class="w-full">
          <FileDropZone :fileList="localFileList" multiple @filesUpdated="syncFileList" />
        </div>

        <div
          v-if="additionalFilesLocation === 'github'"
          class="flex h-full w-full flex-col items-center"
        >
          <div class="w-full pt-4 pb-6">
            <!-- <el-select-v2
              v-model="selectedRelease"
              :options="allReleases"
              placeholder="Please select"
              size="large"
              class="w-full"
            >
              <template #default="{ item }">
                <div class="flex flex-col">
                  <span style="margin-right: 8px">{{ item.label }}</span>

                  <span style="color: var(--el-text-color-secondary); font-size: 13px">
                    {{ item.value }}
                  </span>
                </div>
              </template>
            </el-select-v2> -->

            <div class="mb-4">
              <line-divider></line-divider>
              <p class="mb-2">Select the GitHub release you want to use for your Zenodo upload:</p>

              <el-select v-model="selectedRelease" placeholder="Select" class="w-full" size="large">
                <el-option
                  v-for="item in allReleases"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                  class="!h-auto transition-all"
                >
                  <div class="flex flex-col py-2 leading-normal">
                    <div class="flex justify-between">
                      <p class="text-sm font-medium">
                        {{ item.label }}
                      </p>
                      <span class="text-xs font-medium">
                        {{ publishedDate(item.og.published_at) }}
                      </span>
                    </div>
                    <div class="mt-1 flex flex-row">
                      <el-tag class="mr-2" type="warning" size="small" v-if="item.og.prerelease">
                        Pre-release
                      </el-tag>
                      <el-tag class="mr-2" size="small"> {{ item.og.tag_name }} </el-tag>
                    </div>
                  </div>
                </el-option>
              </el-select>
            </div>

            <div v-if="selectedRelease != ''">
              <line-divider></line-divider>

              <p class="mb-2">
                Select the files you want to add from your release to the Zenodo dataset
              </p>

              <el-select
                v-model="addedReleaseAssets"
                multiple
                placeholder="Select"
                class="w-full"
                size="large"
              >
                <el-option
                  v-for="item in releaseAssets"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </div>
          </div>
        </div>

        <div class="flex w-full flex-row justify-center space-x-4 py-2">
          <router-link
            :to="`/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/zenodo/metadata`"
            class=""
          >
            <button class="primary-plain-button">
              <el-icon><d-arrow-left /></el-icon> Back
            </button>
          </router-link>

          <button
            class="primary-button"
            @click="showSummary"
            v-if="localFileList.length > 0 || addedReleaseAssets.length > 0"
          >
            Continue
            <el-icon> <d-arrow-right /> </el-icon>
          </button>
        </div>
      </div>
    </div>
    <app-docs-link url="curate-and-share/connect-github-zenodo" position="bottom-4" />
  </div>
</template>

<script>
import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

import { ElLoading } from "element-plus";
import axios from "axios";
import dayjs from "dayjs";

import FileDropZone from "@/components/files/FileDropZone.vue";

export default {
  name: "GithubChooseUpload",
  components: { FileDropZone },
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
      localFileList: [
        "C:\\Users\\dev\\Desktop\\temp\\taxdmp\\nodes.dmp",
        "C:\\Users\\dev\\Desktop\\temp\\taxdmp\\readme.txt",
      ],
      addAdditionalFiles: "None",
      additionalFilesLocation: "github",
      allReleases: [],
      selectedRelease: "",
      addedReleaseAssets: [],
    };
  },

  computed: {
    releaseAssets() {
      if (this.selectedRelease === "") {
        return [];
      }

      const assets = this.allReleases.find((release) => release.value === this.selectedRelease).og
        .assets;

      console.log(assets);

      return assets.map((asset) => {
        return {
          label: asset.name,
          value: asset.browser_download_url,
        };
      });
    },
  },

  methods: {
    syncFileList(data) {
      this.localFileList = data;
    },

    openWebsite() {
      const url = `${process.env.VUE_APP_ZENODO_URL}/account/settings/github`;
      window.ipcRenderer.send("open-link-in-browser", url);
    },

    publishedDate(date) {
      return dayjs(date).format("MMM DD, YYYY");
    },

    async getReleases() {
      const splitRepoNameOwner = this.selectedRepo.split("/");

      const releaseList = await axios
        .get(`${this.$server_url}/github/repo/releases`, {
          params: {
            access_token: this.GithubAccessToken,
            owner: splitRepoNameOwner[0],
            repo: splitRepoNameOwner[1],
          },
        })
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });

      if (releaseList !== "ERROR") {
        if (releaseList.length > 0) {
          this.allReleases = [];

          for (let release of releaseList) {
            this.allReleases.push({
              label: release.name,
              value: release.id,
              og: release,
            });
          }
        }
      }
    },

    async showSummary() {
      if (this.addAdditionalFiles === "Yes") {
        this.workflow.addAdditionalFiles = true;
      } else {
        this.workflow.addAdditionalFiles = false;
      }

      this.workflow.additionalFilesLocation = this.additionalFilesLocation;

      this.workflow.localFileList = this.localFileList;

      this.workflow.selectedRelease = this.selectedRelease;
      this.workflow.addedReleaseAssets = this.addedReleaseAssets;

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

    if ("localFileList" in this.workflow) {
      this.localFileList = this.workflow.localFileList;
    } else {
      this.localFileList = [];
    }

    const loading = ElLoading.service({
      lock: true,
      text: "Reading GitHub releases...",
      background: "rgba(0, 0, 0, 0.2)",
    });

    await this.getReleases();

    loading.close();

    if ("addAdditionalFiles" in this.workflow) {
      this.addAdditionalFiles = this.workflow.addAdditionalFiles ? "Yes" : "No";
    } else {
      this.addAdditionalFiles = "None";
    }

    if ("additionalFilesLocation" in this.workflow) {
      this.additionalFilesLocation = this.workflow.additionalFilesLocation;
    } else {
      this.additionalFilesLocation = "";
    }

    if ("selectedRelease" in this.workflow) {
      this.selectedRelease = this.workflow.selectedRelease;
    } else {
      this.selectedRelease = "";
    }

    if ("addedReleaseAssets" in this.workflow) {
      this.addedReleaseAssets = this.workflow.addedReleaseAssets;
    } else {
      this.addedReleaseAssets = [];
    }

    this.workflow.currentRoute = this.$route.path;
  },
};
</script>
