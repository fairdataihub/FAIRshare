<template>
  <div
    class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 pr-5"
  >
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium">
        Verify if you have followed standard/best research software development
        practices
      </span>

      <el-divider class="my-4"> </el-divider>

      <div class="flex flex-col space-y-4">
        <!-- template start -->
        <div class="rounded-lg border-2 border-slate-100 p-4">
          <p class="pb-2">
            Have you followed applicable high-level best practices for research
            software?
          </p>

          <el-collapse v-model="activeNames" class="border-none">
            <el-collapse-item class="test-header code-collapse-item">
              <template #title>
                <span class="pr-2"> Learn more </span>
              </template>

              <div class="px-3 py-2">Some explanation text here.</div>
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
        <div class="rounded-lg border-2 border-slate-100 p-4">
          <p class="pb-2">
            Have you followed applicable language-specific standards and best
            practices?
          </p>

          <el-collapse v-model="activeNames" class="border-none">
            <el-collapse-item class="test-header code-collapse-item">
              <template #title>
                <span class="pr-2"> Learn more </span>
              </template>

              <div class="px-3 py-2">Some explanation text here.</div>
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
        <div class="rounded-lg border-2 border-slate-100 p-4">
          <p class="pb-2">
            Have you followed applicable domain-specific standards and best
            practices?
          </p>

          <el-collapse v-model="activeNames" class="border-none">
            <el-collapse-item class="test-header code-collapse-item">
              <template #title>
                <span class="pr-2"> Learn more </span>
              </template>

              <div class="px-3 py-2">Some explanation text here.</div>
            </el-collapse-item>
          </el-collapse>

          <div class="pb-3">
            <el-radio v-model="questions.question3" label="Yes" size="large">
              Yes
            </el-radio>
            <el-radio v-model="questions.question3" label="No" size="large">
              No
            </el-radio>
          </div>
        </div>
        <div class="rounded-lg border-2 border-slate-100 p-4">
          <p class="pb-2">
            Is your software documentation following applicable standards and
            best practices?
          </p>

          <el-collapse v-model="activeNames" class="border-none">
            <el-collapse-item class="test-header code-collapse-item">
              <template #title>
                <span class="pr-2"> Learn more </span>
              </template>

              <div class="px-3 py-2">Some explanation text here.</div>
            </el-collapse-item>
          </el-collapse>

          <div class="pb-3">
            <el-radio v-model="questions.question4" label="Yes" size="large">
              Yes
            </el-radio>
            <el-radio v-model="questions.question4" label="No" size="large">
              No
            </el-radio>
          </div>
        </div>
        <div class="rounded-lg border-2 border-slate-100 p-4">
          <p class="pb-2">
            Have you ensured that your code does not include any information
            violating HIPAA?
          </p>

          <el-collapse v-model="activeNames" class="border-none">
            <el-collapse-item class="test-header code-collapse-item">
              <template #title>
                <span class="pr-2"> Learn more </span>
              </template>

              <div class="px-3 py-2">Some explanation text here.</div>
            </el-collapse-item>
          </el-collapse>

          <div class="pb-3">
            <el-radio v-model="questions.question5" label="Yes" size="large">
              Yes
            </el-radio>
            <el-radio v-model="questions.question5" label="No" size="large">
              No
            </el-radio>
          </div>
        </div>
        <!-- template end -->
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
        question3: "",
        question4: "",
        question5: "",
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

    this.workflow.currentRoute = this.$route.path;

    if ("standards" in this.dataset.data.Code) {
      this.questions = this.dataset.data.Code.standards;
    }
  },
};
</script>

<style></style>
