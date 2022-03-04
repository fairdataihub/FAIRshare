<template>
  <div
    class="relative flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 px-5"
    v-loading="loading"
  >
    <div class="flex h-full w-full flex-col items-start justify-start">
      <div class="w-full">
        <span class="mb-2 w-full">
          Would you like to upload your dataset to a repository through
          FAIRshare?
        </span>

        <div class="py-1">
          <el-radio v-model="uploadToRepo" label="Yes" size="large">
            Yes
          </el-radio>
          <el-radio v-model="uploadToRepo" label="No" size="large">
            No
          </el-radio>
          <el-radio
            v-model="uploadToRepo"
            label="None"
            size="large"
            border
            class="!hidden"
          >
            None
          </el-radio>
        </div>
      </div>

      <div
        v-if="uploadToRepo !== 'None'"
        class="flex h-full w-full flex-col items-center"
      >
        <transition name="fade" mode="out-in" appear>
          <div
            v-if="uploadToRepo === 'Yes'"
            class="flex h-full w-full flex-col items-center"
          >
            <line-divider class="w-full py-3"></line-divider>

            <span class="text-center">
              Based on your dataset requirements, we suggest uploading your data
              to one of these repositories.
            </span>
            <span class="text-center text-sm">
              Please click one of the following options:
            </span>

            <div class="my-8 grid grid-cols-3 gap-8">
              <div>
                <div class="flex flex-col items-center justify-center">
                  <div
                    class="single-check-box flex h-[200px] w-[200px] cursor-pointer flex-col items-center justify-evenly rounded-lg p-4 shadow-md transition-all"
                    :class="{ 'selected-repo': repoID === 'zenodo' }"
                    @click="selectRepo($event, 'zenodo')"
                  >
                    <img
                      src="https://api.iconify.design/simple-icons/zenodo.svg"
                      alt=""
                      class="mb-3 h-16 w-16"
                    />
                    <span class="mx-5 text-lg"> Zenodo </span>
                  </div>
                  <div
                    class="hover-underline-animation my-5 flex w-max cursor-pointer flex-row items-center text-primary-600"
                    v-if="repoID === 'zenodo'"
                    @click="openWebsite('https://zenodo.org')"
                  >
                    <span class="font-medium"> Learn more... </span>
                    <Icon
                      icon="grommet-icons:form-next-link"
                      class="ml-2 h-5 w-5"
                    />
                  </div>
                </div>
              </div>

              <div>
                <el-popover
                  placement="bottom"
                  trigger="hover"
                  content="Coming soon..."
                >
                  <template #reference>
                    <div>
                      <div
                        class="disabled-card single-check-box pointer-events-none flex h-[200px] w-[200px] cursor-pointer flex-col items-center justify-evenly rounded-lg p-4 text-stone-400 shadow-md transition-all"
                        :class="{ 'selected-repo': repoID === 'figshare' }"
                        @click="selectRepo($event, 'figshare')"
                      >
                        <img
                          src="https://www.digital-science.com/wp-content/uploads/2020/11/Figshare-no-padding.png"
                          alt=""
                          class="mb-3 h-16 opacity-50"
                        />
                        <span class="mx-5 text-lg"> Figshare </span>
                      </div>
                    </div>
                  </template>
                </el-popover>
              </div>

              <div>
                <el-popover
                  placement="bottom"
                  trigger="hover"
                  content="Coming soon..."
                >
                  <template #reference>
                    <div>
                      <div
                        class="disabled-card single-check-box pointer-events-none flex h-[200px] w-[200px] cursor-pointer flex-col items-center justify-evenly rounded-lg p-4 text-stone-400 shadow-md transition-all hover:shadow-lg"
                        :class="{
                          'selected-repo': repoID === 'softwareheritage',
                        }"
                        @click="selectRepo($event, 'softwareheritage')"
                      >
                        <img
                          src="https://www.softwareheritage.org/wp-content/uploads/2015/08/swh-logo.png"
                          alt=""
                          class="mb-3 h-16 opacity-50"
                        />
                        <span class="mx-5 w-full text-center text-lg">
                          Software Heritage
                        </span>
                      </div>
                    </div>
                  </template>
                </el-popover>
              </div>
            </div>

            <!-- This will be enabled in the future. -->
            <!-- change to grid-cols-2 -->
            <!-- <div class="grid grid-cols-1 gap-4">
        <div
          v-for="repo of repositories"
          :key="repo.id"
          class="flex flex-col items-center justify-between p-4 my-5 transition-all bg-gray-200 rounded-lg shadow-md cursor-pointer hover:bg-gray-300 hover:shadow-lg h-30 w-30"
          :class="{ 'selected-repo': repoID === repo.id }"
          @click="selectRepo($event, repo.id)"
        >
          <img :src="repo.imgURL" alt="" class="h-16 mb-3" />
          <span class="mx-5 text-lg"> {{ repo.name }} </span>
        </div>
      </div> -->

            <fade-transition>
              <div v-if="repoID === 'zenodo'" class="mb-8 flex flex-col">
                <p class="mb-4">
                  Is your dataset already published on Zenodo or would you like
                  to create a new Zenodo publication?
                </p>

                <div class="flex flex-row items-center justify-center">
                  <el-radio
                    v-model="newVersion"
                    label="false"
                    size="large"
                    border
                    @change="selectZenodoDeposition"
                  >
                    Create a new Zenodo deposition
                  </el-radio>
                  <el-radio
                    v-model="newVersion"
                    label="true"
                    size="large"
                    border
                    @change="selectZenodoDeposition"
                  >
                    Create a new version of an existing Zenodo deposition
                  </el-radio>
                </div>
              </div>
            </fade-transition>

            <fade-transition>
              <div
                class="h-[300px] w-[600px] pb-20"
                v-if="showSelectZenodoDeposition"
              >
                <Listbox v-model="selectedDeposition">
                  <div class="relative mt-1">
                    <ListboxButton
                      class="relative w-full cursor-default rounded-lg border border-gray-200 bg-white py-2 pl-3 pr-10 text-left shadow-md focus:outline-none sm:text-sm"
                    >
                      <span class="block truncate">{{
                        selectedDeposition.metadata.title
                      }}</span>
                      <!-- <span
                          class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2"
                        >
                          <SelectorIcon
                            class="h-5 w-5 text-gray-400"
                            aria-hidden="true"
                          />
                        </span> -->
                    </ListboxButton>

                    <transition
                      enter-active-class="transition duration-100 ease-in"
                      enter-to-class="opacity-100"
                      enter-from-class="opacity-0"
                      leave-active-class="transition duration-100 ease-in"
                      leave-from-class="opacity-100"
                      leave-to-class="opacity-0"
                    >
                      <ListboxOptions
                        class="absolute mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
                      >
                        <ListboxOption
                          v-slot="{ active, selected }"
                          v-for="deposition in filteredDepositions"
                          :key="deposition.id"
                          :value="deposition"
                          as="template"
                        >
                          <li
                            :class="[
                              active
                                ? 'bg-amber-100 text-amber-900'
                                : 'text-gray-900',
                              'relative cursor-default select-none py-2 pl-10 pr-4',
                            ]"
                          >
                            <span
                              :class="[
                                selected ? 'font-medium' : 'font-normal',
                                'block truncate',
                              ]"
                              >{{ deposition.metadata.title }}</span
                            >
                            <!-- <span
                                v-if="selected"
                                class="absolute inset-y-0 left-0 flex items-center pl-3 text-amber-600"
                              >
                                <CheckIcon class="h-5 w-5" aria-hidden="true" />
                              </span> -->
                          </li>
                        </ListboxOption>
                      </ListboxOptions>
                    </transition>
                  </div>
                </Listbox>
              </div>
            </fade-transition>

            <fade-transition>
              <div
                class="w-max-content flex flex-row justify-center space-x-4 py-6"
                v-if="newVersion === 'false'"
              >
                <router-link
                  :to="`/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/Code/pickLicense`"
                  class=""
                >
                  <button class="primary-plain-button">
                    <el-icon><d-arrow-left /></el-icon> Back
                  </button>
                </router-link>

                <button
                  class="primary-button"
                  @click="addMetadata"
                  :disabled="repoID === ''"
                  id="continue"
                >
                  Continue <el-icon> <d-arrow-right /> </el-icon>
                </button>
              </div>
            </fade-transition>
          </div>
          <div v-else class="flex w-full justify-center space-x-4 px-5 py-4">
            <button
              class="primary-plain-button"
              size="medium"
              @click="saveSkip"
            >
              <el-icon><d-arrow-left /></el-icon>
              Back
            </button>

            <button class="primary-button" @click="showRepoUploadWarning">
              Continue
              <el-icon><d-arrow-right /></el-icon>
            </button>
            <warning-confirm
              ref="warningConfirm"
              title="Warning"
              @messageConfirmed="skipUploadToRepo"
              confirmButtonText="Yes, I want to skip"
            >
              <p class="text-center text-base text-gray-500">
                Are you sure you want to skip uploading this dataset to a data
                repository? This is not recommended according to the FAIR
                guidelines.
              </p>
            </warning-confirm>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access";

import { Icon } from "@iconify/vue";
import axios from "axios";
import {
  Listbox,
  ListboxButton,
  ListboxOptions,
  ListboxOption,
} from "@headlessui/vue";

export default {
  name: "SelectRepositoryDestination",
  components: { Icon, Listbox, ListboxButton, ListboxOptions, ListboxOption },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      tokens: useTokenStore(),
      dataset: {},
      workflowID: this.$route.params.workflowID,
      datasetID: this.$route.params.datasetID,
      workflow: {},
      zenodoToken: "",
      loading: false,
      repoID: "",
      showSelectZenodoDeposition: false,
      filteredDepositions: [],
      selectedDeposition: {},
      uploadToRepo: "None",
      newVersion: "",
      repositories: [
        {
          id: "zenodo",
          name: "Zenodo",
          imgURL: "https://api.iconify.design/simple-icons/zenodo.svg",
        },
        {
          id: "figshare",
          name: "Figshare",
          imgURL: "https://api.iconify.design/simple-icons/figshare.svg",
        },
      ],
    };
  },
  computed: {},
  methods: {
    selectRepo(event, repoID) {
      this.repoID = repoID;
      if (event && event.detail === 2) {
        this.addMetadata();
      }
    },
    async getAllDepositions() {
      const response = await axios
        .get(`${this.$server_url}/zenodo/depositions`, {
          params: {
            access_token: this.zenodoToken,
          },
        })
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });

      this.filteredDepositions = response.filter((deposition) => {
        return deposition.submitted === true;
      });

      console.log(this.filteredDepositions);
      this.selectedDeposition = this.filteredDepositions[0];
      this.showSelectZenodoDeposition = true;
    },
    async selectZenodoDeposition() {
      if (this.newVersion === "true") {
        await this.getAllDepositions();
      } else {
        this.showSelectZenodoDeposition = false;
      }
    },
    openWebsite(url) {
      window.ipcRenderer.send("open-link-in-browser", url);
    },
    addMetadata() {
      this.dataset.destinationSelected = true;

      if (!("destination" in this.workflow)) {
        this.workflow.destination = {};
      }

      if (!this.workflow.destination[this.repoID]) {
        this.workflow.destination[this.repoID] = {
          id: this.repoID,
          questions: {},
          status: {},
        };
      }

      if (this.workflow.destination.name === this.repoID) {
        //do nothing
        this.workflow.destination.name = this.repoID;
      } else {
        // warn the user that they are changing repos (add a sweetalert or something)
        this.workflow.destination.name = this.repoID;
      }

      this.dataset.meta.destination = this.repoID;

      if (this.uploadToRepo === "Yes") {
        this.workflow.uploadToRepo = true;
      } else {
        this.workflow.uploadToRepo = false;
      }

      this.datasetStore.updateCurrentDataset(this.dataset);
      this.datasetStore.syncDatasets();

      // using the zenodo one here. I don't think this matters since we aren't uploading anything
      // Might change it to its own page later
      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/zenodo/metadata`;
      this.$router.push(routerPath);
    },
    async saveSkip() {
      if (this.uploadToRepo === "Yes") {
        this.workflow.uploadToRepo = true;
      } else {
        this.workflow.uploadToRepo = false;
      }

      await this.datasetStore.updateCurrentDataset(this.dataset);
      await this.datasetStore.syncDatasets();

      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/Code/pickLicense`;
      this.$router.push(routerPath);
    },
    showRepoUploadWarning() {
      this.$refs.warningConfirm.show();
    },
    async skipUploadToRepo() {
      if (this.uploadToRepo === "Yes") {
        this.workflow.uploadToRepo = true;
      } else {
        this.workflow.uploadToRepo = false;
      }

      await this.datasetStore.updateCurrentDataset(this.dataset);
      await this.datasetStore.syncDatasets();

      let routerPath = "";

      if ("source" in this.workflow) {
        if (this.workflow.source.type === "github") {
          routerPath = `/datasets/${this.datasetID}/${this.workflowID}/github/upload`;
        }
        if (this.workflow.source.type === "local") {
          routerPath = `/datasets/${this.dataset.id}/${this.workflowID}/localNoUpload/generate`;
        }
      } else {
        routerPath = `/datasets/${this.dataset.id}/${this.workflowID}/localNoUpload/generate`;
      }

      this.$router.push({ path: routerPath });
    },
  },
  async mounted() {
    this.loading = true;

    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    const tokenObject = await this.tokens.getToken("zenodo");
    this.zenodoToken = tokenObject.token;

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(5);

    this.workflow.currentRoute = this.$route.path;

    if ("uploadToRepo" in this.workflow) {
      this.uploadToRepo = this.workflow.uploadToRepo ? "Yes" : "No";
    } else {
      this.uploadToRepo = "None";
    }

    if (this.workflow.destination) {
      this.repoID = this.workflow.destination.name;
    }

    this.loading = false;
  },
};
</script>

<style scoped>
.single-check-box {
  @apply flex h-48 w-48 items-center justify-center transition-all;
}

.single-check-box:not(.disabled-card, .selected-repo):hover {
  @apply border border-secondary-500 shadow-lg shadow-secondary-500/50 transition-all;
}
</style>
