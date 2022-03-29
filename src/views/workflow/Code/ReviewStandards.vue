<template>
  <div class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium">
        Verify if you have followed standard/best research software development practices required
        to make your software FAIR
      </span>

      <el-divider class="my-4"> </el-divider>

      <div class="flex flex-col space-y-4">
        <!-- template start -->
        <div class="rounded-lg border-2 border-slate-100 p-4">
          <p class="pb-2">
            Have you followed applicable high-level standards and best practices for scientific
            research software?
          </p>

          <el-collapse v-model="activeNames" class="border-none">
            <el-collapse-item class="test-header code-collapse-item">
              <template #title>
                <span class="pr-2"> Learn more </span>
              </template>
              <div class="px-3 py-2">
                We refer to the following relevant literature on high-level best practices:
                <span
                  class="text-url"
                  @click="openWebsite('https://doi.org/10.1371/journal.pcbi.1005510')"
                >
                  Good enough practices in scientific computing</span
                >.
              </div>
            </el-collapse-item>
          </el-collapse>

          <div class="pb-3">
            <el-radio v-model="questions.question1" label="Yes" size="large"> Yes </el-radio>
            <el-radio v-model="questions.question1" label="No" size="large"> No </el-radio>
          </div>
        </div>
        <div class="rounded-lg border-2 border-slate-100 p-4">
          <p class="pb-2">
            Have you followed applicable language-specific standards and best practices for your
            code?
          </p>

          <el-collapse v-model="activeNames" class="border-none">
            <el-collapse-item class="test-header code-collapse-item">
              <template #title>
                <span class="pr-2"> Learn more </span>
              </template>

              <div class="px-3 py-2">
                These standards depend on the language used in your software. For instance, we refer
                to the
                <span class="text-url" @click="openWebsite('https://www.python.org/dev/')">
                  Python Developer's Guide
                </span>
                for Python or
                <span
                  class="text-url"
                  @click="openWebsite('https://google.github.io/styleguide/Rguide.html')"
                >
                  Google’s R Style Guide</span
                >
                for R programs.
              </div>
            </el-collapse-item>
          </el-collapse>

          <div class="pb-3">
            <el-radio v-model="questions.question2" label="Yes" size="large"> Yes </el-radio>
            <el-radio v-model="questions.question2" label="No" size="large"> No </el-radio>
          </div>
        </div>
        <div class="rounded-lg border-2 border-slate-100 p-4">
          <p class="pb-2">
            Have you followed applicable domain-specific standards and best practices for biomedical
            research software?
          </p>

          <el-collapse v-model="activeNames" class="border-none">
            <el-collapse-item class="test-header code-collapse-item">
              <template #title>
                <span class="pr-2"> Learn more </span>
              </template>

              <div class="px-3 py-2">
                We refer to the following relevant literature on best practices for biomedical
                research software:
                <span
                  class="text-url"
                  @click="openWebsite('https://dx.doi.org/10.12688%2Ff1000research.10750.2')"
                >
                  General guidelines for biomedical software development</span
                >.
              </div>
            </el-collapse-item>
          </el-collapse>

          <div class="pb-3">
            <el-radio v-model="questions.question3" label="Yes" size="large"> Yes </el-radio>
            <el-radio v-model="questions.question3" label="No" size="large"> No </el-radio>
          </div>
        </div>
        <div class="rounded-lg border-2 border-slate-100 p-4">
          <p class="pb-2">
            Is your software documentation following applicable standards and best practices?
          </p>

          <el-collapse v-model="activeNames" class="border-none">
            <el-collapse-item class="test-header code-collapse-item">
              <template #title>
                <span class="pr-2"> Learn more </span>
              </template>

              <div class="px-3 py-2">
                Ensure that the following aspects are documented: inputs and outputs of the
                software, parameters and data required to run the software, the standards applied,
                and how to contribute to the software. We refer to the following literature for
                additional information on documenting your software:
                <span
                  class="text-url"
                  @click="openWebsite('https://dx.doi.org/10.1371%2Fjournal.pcbi.1006561')"
                >
                  Ten simple rules for documenting scientific software</span
                >.
              </div>
            </el-collapse-item>
          </el-collapse>

          <div class="pb-3">
            <el-radio v-model="questions.question4" label="Yes" size="large"> Yes </el-radio>
            <el-radio v-model="questions.question4" label="No" size="large"> No </el-radio>
          </div>
        </div>
        <div class="rounded-lg border-2 border-slate-100 p-4">
          <p class="pb-2">
            Have you ensured that your code and data files do not include any information violating
            HIPAA?
          </p>

          <el-collapse v-model="activeNames" class="border-none">
            <el-collapse-item class="test-header code-collapse-item">
              <template #title>
                <span class="pr-2"> Learn more </span>
              </template>

              <div class="px-3 py-2">
                We refer to the guidelines of the
                <span
                  class="text-url"
                  @click="
                    openWebsite(
                      'https://www.hhs.gov/hipaa/for-professionals/privacy/laws-regulations/index.html'
                    )
                  "
                >
                  Department of Health and Human Services</span
                >
                for information on the Health Insurance Portability and Accountability Act (HIPAA)
                Privacy Rules.
              </div>
            </el-collapse-item>
          </el-collapse>

          <div class="pb-3">
            <el-radio v-model="questions.question5" label="Yes" size="large"> Yes </el-radio>
            <el-radio v-model="questions.question5" label="No" size="large"> No </el-radio>
          </div>
        </div>
        <!-- template end -->
      </div>

      <div class="flex w-full flex-row justify-center space-x-4 py-6">
        <button class="primary-plain-button" @click="goBack">
          <el-icon><d-arrow-left /></el-icon> Back
        </button>

        <button
          class="primary-button"
          @click="checkStandards"
          :disabled="disableContinue"
          id="continue"
        >
          Continue
          <el-icon> <d-arrow-right /> </el-icon>
        </button>
        <warning-confirm
          ref="warningConfirm"
          title="Warning"
          @messageConfirmed="startCuration"
          confirmButtonText="Continue anyway"
          cancelButtonText="I want to go back and review"
        >
          <p class="text-center text-base text-gray-500">
            For your research software to be completely FAIR, we expect you to answer 'Yes' to all
            the questions. We suggest reviewing where you selected 'No' and modifying your data
            files if necessary before continuing.
          </p>
        </warning-confirm>
      </div>
    </div>
    <app-docs-link url="curate-and-share/verify-best-practices" position="bottom-4" />
  </div>
</template>

<script>
import { useDatasetsStore } from "@/store/datasets";

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
        question1: process.env.NODE_ENV === "development" ? "Yes" : "",
        question2: process.env.NODE_ENV === "development" ? "Yes" : "",
        question3: process.env.NODE_ENV === "development" ? "Yes" : "",
        question4: process.env.NODE_ENV === "development" ? "Yes" : "",
        question5: process.env.NODE_ENV === "development" ? "Yes" : "",
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
    async openWebsite(url) {
      window.ipcRenderer.send("open-link-in-browser", url);
    },
    async goBack() {
      let routerPath = "";

      if ("source" in this.workflow) {
        if (this.workflow.source.type === "local") {
          routerPath = `/datasets/${this.datasetID}/${this.workflowID}/Code/selectFolder`;
        } else if (this.workflow.source.type === "github") {
          routerPath = `/datasets/${this.datasetID}/${this.workflowID}/Code/selectGithubRepo`;
        }
      }

      this.$router.push(routerPath);
    },
    async checkStandards() {
      let showWarning = false;

      for (const question in this.questions) {
        if (this.questions[question] === "No") {
          showWarning = true;
        }
      }

      if (showWarning) {
        this.$refs.warningConfirm.show();
      } else {
        this.startCuration();
      }
    },
    startCuration() {
      this.dataset.data.Code.standards = this.questions;

      this.datasetStore.updateCurrentDataset(this.dataset);
      this.datasetStore.syncDatasets();

      this.$router.push(`/datasets/${this.datasetID}/${this.workflowID}/Code/createMetadata`);
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
