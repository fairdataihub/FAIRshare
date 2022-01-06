<template>
  <div
    class="h-full w-full flex flex-col justify-center items-center pr-5 p-3 max-w-screen-xl"
  >
    <div class="flex flex-col h-full w-full">
      <span class="text-lg font-medium text-left">
        Verify if you have followed standard/best research software development practices
      </span>

      <el-divider class="my-4"> </el-divider>

      <div class="flex flex-col space-y-4">
        <!-- template start -->
        <div class="border-2 border-slate-100 p-4 rounded-lg">
          <p>Is the data being curated in accordance with the standards?</p>

          <el-collapse v-model="activeNames" class="border-none">
            <el-collapse-item class="test-header code-collapse-item">
              <template #title>
                <span class="pr-2"> Learn more </span>
              </template>

              <div class="py-2 px-3">Some explanation text here.</div>
            </el-collapse-item>
          </el-collapse>

          <div class="pb-3">
            <el-radio v-model="questions.question1" label="Yes" size="large">
              Yes
            </el-radio>
            <el-radio v-model="questions.question1" label="No" size="large">
              No
            </el-radio>
          </div>
        </div>
        <div class="border-2 border-slate-100 p-4 rounded-lg">
          <p>Is the data being curated in accordance with the standards?</p>

          <el-collapse v-model="activeNames" class="border-none">
            <el-collapse-item class="test-header code-collapse-item">
              <template #title>
                <span class="pr-2"> Learn more </span>
              </template>

              <div class="py-2 px-3">Some explanation text here.</div>
            </el-collapse-item>
          </el-collapse>

          <div class="pb-3">
            <el-radio v-model="questions.question2" label="Yes" size="large">
              Yes
            </el-radio>
            <el-radio v-model="questions.question2" label="No" size="large">
              No
            </el-radio>
          </div>
        </div>
        <!-- template end -->
      </div>

      <div class="w-full flex flex-row justify-center py-2 space-x-4">
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
          @click="startCuration"
          :disabled="disableContinue"
          id="continue"
        >
          Continue
          <el-icon> <d-arrow-right /> </el-icon>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { useDatasetsStore } from "@/store/datasets";

import { ElMessageBox } from "element-plus";

export default {
  name: "CodeReviewStandards",
  data() {
    return {
      datasetStore: useDatasetsStore(),
      datasetID: this.$route.params.datasetID,
      workflowID: this.$route.params.workflowID,
      dataset: {},
      workflow: {},
      activeNames: [],
      questions: {
        question1: "",
        question2: "",
      },
    };
  },
  computed: {
    disableContinue() {
      //disable continue button if no questions answered
      let disabled = false;

      for (const question in this.questions) {
        if (this.questions[question] === "") {
          disabled = true;
        }
      }

      return disabled;
    },
  },
  methods: {
    async startCuration() {
      let showWarning = false;

      for (const question in this.questions) {
        if (this.questions[question] === "No") {
          showWarning = true;
        }
      }

      if (showWarning) {
        ElMessageBox.confirm(
          "For your research software to be fully FAIR, we expect you to answer 'Yes' to all the questions. We suggest to review again where you answered 'No' and modyfying your data files if necessary before contuining.",
          "Warning",
          {
            confirmButtonText: "Continue anyway",
            cancelButtonText: "I want to go back and review",
            type: "warning",
          }
        )
          .then(() => {
            this.dataset.data.Code.standards = this.questions;

            this.datasetStore.updateCurrentDataset(this.dataset);
            this.datasetStore.syncDatasets();

            this.$router.push(
              `/datasets/${this.datasetID}/${this.workflowID}/Code/createMetadata`
            );
          })
          .catch(() => {});
      } else {
        this.dataset.data.Code.standards = this.questions;

        this.datasetStore.updateCurrentDataset(this.dataset);
        this.datasetStore.syncDatasets();

        this.$router.push(
          `/datasets/${this.datasetID}/${this.workflowID}/Code/createMetadata`
        );
      }
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();

    this.workflow = this.dataset.workflows[this.workflowID];

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(2);

    if ("standards" in this.dataset.data.Code) {
      this.questions = this.dataset.data.Code.standards;
    }
  },
};
</script>

<style></style>
