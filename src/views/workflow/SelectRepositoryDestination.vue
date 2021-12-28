<template>
  <div
    class="h-full w-full flex flex-row justify-center items-center p-3"
    v-loading="loading"
  >
    <div class="h-full flex flex-col justify-center items-center">
      <span class="text-center">
        Based on your data requirements, we suggest uploading your data to one
        of these repositories.
      </span>
      <span class="text-sm text-center">
        Please click one of the following options:
      </span>

      <div class="grid grid-cols-3 my-8 gap-8">
        <div
          class="flex flex-col justify-between items-center bg-gray-200 p-4 shadow-md rounded-lg hover:bg-stone-200 hover:shadow-lg transition-all cursor-pointer h-[150px] w-[200px]"
          :class="{ 'selected-repo': repoID === 'zenodo' }"
          @click="selectRepo($event, 'zenodo')"
        >
          <img
            src="https://api.iconify.design/simple-icons/zenodo.svg"
            alt=""
            class="h-16 w-16 mb-3"
          />
          <span class="text-lg mx-5"> Zenodo </span>
        </div>
        <el-popover placement="bottom" trigger="hover" content="Coming soon...">
          <template #reference>
            <div>
              <div
                class="flex flex-col justify-between items-center bg-gray-100 p-4 shadow-md rounded-lg hover:bg-gray-300 transition-all cursor-pointer h-[150px] w-[200px] pointer-events-none text-stone-400"
                :class="{ 'selected-repo': repoID === 'figshare' }"
                @click="selectRepo($event, 'figshare')"
              >
                <img
                  src="https://www.digital-science.com/wp-content/uploads/2020/11/Figshare-no-padding.png"
                  alt=""
                  class="h-16 mb-3 opacity-50"
                />
                <span class="text-lg mx-5"> Figshare </span>
              </div>
            </div>
          </template>
        </el-popover>
        <el-popover placement="bottom" trigger="hover" content="Coming soon...">
          <template #reference>
            <div>
              <div
                class="flex flex-col justify-between items-center bg-gray-100 p-4 shadow-md rounded-lg hover:bg-gray-300 hover:shadow-lg transition-all cursor-pointer h-[150px] w-[200px] pointer-events-none text-stone-400"
                :class="{ 'selected-repo': repoID === 'softwareheritage' }"
                @click="selectRepo($event, 'softwareheritage')"
              >
                <img
                  src="https://www.softwareheritage.org/wp-content/uploads/2015/08/swh-logo.png"
                  alt=""
                  class="h-16 mb-3 opacity-50"
                />
                <span class="text-lg mx-5 w-full text-center">
                  Software Heritage
                </span>
              </div>
            </div>
          </template>
        </el-popover>
      </div>

      <!-- This will be enabled in the future. -->
      <!-- change to grid-cols-2 -->
      <!-- <div class="grid grid-cols-1 gap-4">
        <div
          v-for="repo of repositories"
          :key="repo.id"
          class="flex flex-col justify-between items-center bg-gray-200 p-4 my-5 shadow-md rounded-lg hover:bg-gray-300 hover:shadow-lg transition-all cursor-pointer h-30 w-30"
          :class="{ 'selected-repo': repoID === repo.id }"
          @click="selectRepo($event, repo.id)"
        >
          <img :src="repo.imgURL" alt="" class="h-16 mb-3" />
          <span class="text-lg mx-5"> {{ repo.name }} </span>
        </div>
      </div> -->

      <div
        class="absolute bottom-0 w-max-content flex flex-row justify-center py-2 space-x-4"
      >
        <router-link
          :to="`/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/createMetadata`"
          class=""
        >
          <el-button type="danger" plain>
            <el-icon><d-arrow-left /></el-icon> Back
          </el-button>
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
    </div>
  </div>
</template>

<script>
import { useDatasetsStore } from "../../store/datasets";

export default {
  name: "SelectRepositoryDestination",
  data() {
    return {
      datasetStore: useDatasetsStore(),
      dataset: {},
      workflowID: this.$route.params.workflowID,
      datasetID: this.$route.params.datasetID,
      workflow: {},
      loading: false,
      repoID: "",
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

      console.log(this.workflow.destination);

      if (this.workflow.destination.name === this.repoID) {
        //do nothing
        this.workflow.destination.name = this.repoID;
      } else {
        // warn the user that they are changing repos (add a sweetalert or something)
        this.workflow.destination.name = this.repoID;
      }

      console.log(this.workflow.destination);

      this.datasetStore.updateCurrentDataset(this.dataset);
      this.datasetStore.syncDatasets();

      const redirectURL = `/datasets/${this.datasetID}/${this.workflowID}/${this.repoID}/metadata`;
      this.$router.push(redirectURL);
    },
  },
  async mounted() {
    this.loading = true;

    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(3);

    if (this.workflow.destination) {
      this.repoID = this.workflow.destination.name;
    }

    console.log(this.workflow.destination);

    this.loading = false;
  },
};
</script>

<style lang="postcss" scoped></style>
