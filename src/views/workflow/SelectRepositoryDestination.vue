<template>
  <div
    class="h-screen w-full flex flex-row justify-center items-center"
    v-loading="loading"
  >
    <div class="p-3 h-full flex flex-row items-center">
      <div class="h-full w-full">
        <workflow-progress-bar :currentStep="3" />
        <div
          class="
            flex flex-col
            h-full
            overflow-y-auto
            pr-5
            justify-center
            items-center
          "
        >
          <span class="text-center">
            Based on your data requirements, we suggest uploading your data to
            one of these repositories.
          </span>
          <span class="text-sm text-center">
            Please click one of the following options:
          </span>

          <div class="grid grid-cols-2 gap-4">
            <div
              v-for="repo of repositories"
              :key="repo.id"
              class="
                flex flex-col
                justify-between
                items-center
                bg-gray-200
                p-4
                my-5
                shadow-md
                rounded-lg
                hover:bg-gray-300 hover:shadow-lg
                transition-all
                cursor-pointer
                h-30
                w-30
              "
              :class="{ selected: repoID === repo.id }"
              @click="selectRepo(repo.id)"
            >
              <img :src="repo.imgURL" alt="" class="h-16 mb-3" />
              <span class="text-lg mx-5"> {{ repo.name }} </span>
            </div>
          </div>

          <div
            class="absolute bottom-0 w-full flex flex-row justify-center py-2"
          >
            <router-link
              :to="`/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/createMetadata/review`"
              class="mx-6"
            >
              <el-button type="danger" plain> Back </el-button>
            </router-link>

            <el-button
              type="primary"
              class="flex flex-row items-center"
              @click="addMetadata"
              :disabled="repoID === ''"
              id="continue"
            >
              Continue
              <el-icon>
                <ArrowRightBold />
              </el-icon>
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import { Icon } from "@iconify/vue";
import { ArrowRightBold } from "@element-plus/icons";

import { useDatasetsStore } from "../../store/datasets";

export default {
  name: "SelectRepositoryDestination",
  components: { ArrowRightBold },
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
    selectRepo(repoID) {
      this.repoID = repoID;
    },
    addMetadata() {
      this.dataset.destinationSelected = true;

      if (!this.workflow.destination) {
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
      } else {
        // warn the user that they are changing repos (add a sweetalert or something)
        this.workflow.destination.name = this.repoID;
      }

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

    if (this.workflow.destination) {
      this.repoID = this.workflow.destination.name;
    }

    this.loading = false;
  },
};
</script>

<style lang="postcss" scoped>
.selected {
  @apply border-2 border-solid border-green-500 bg-green-100;
}
</style>
