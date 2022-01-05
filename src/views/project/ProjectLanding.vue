<template>
  <div
    class="h-full w-full flex flex-col justify-center items-center p-3 px-5 max-w-screen-xl"
  >
    <div class="flex flex-col h-full w-full">
      <span class="font-medium text-left"> FAIRifying </span>

      <span> Let's make your research software FAIR. </span>

      <!-- <p class="py-1">
        In order to do this, SODA will automatically try to group up similar
        data into their own datasets.
      </p> -->

      <line-divider> </line-divider>

      <p class="py-2 pb-4">
        FAIRShare will help you make you research software by guiding you
        step-by-step through the following process:
      </p>

      <el-timeline>
        <el-timeline-item id="step1" timestamp="Step 1" placement="top">
          <el-card class="dynamic-card">
            <h4 class="font-bold text-base">
              Select data files to be included
            </h4>
            <p>
              You will be asked to select the location of the files (source
              code, executable, etc.) you want to include
            </p>
          </el-card>
        </el-timeline-item>
        <el-timeline-item id="step2" timestamp="Step 2" placement="top">
          <el-card class="dynamic-card">
            <h4 class="font-bold text-base">
              Ensure standard development practices are followed
            </h4>
            <p>
              You will be asked a series a question to ensure standard practices
              have been followed when developing your software
            </p>
          </el-card>
        </el-timeline-item>
        <el-timeline-item id="step3" timestamp="Step 3" placement="top">
          <el-card class="dynamic-card">
            <h4 class="font-bold text-base">Provide metadata</h4>
            <p>
              Information about your software will be requested and will be used
              to include the standard codemeta.json file in your dataset
            </p>
          </el-card>
        </el-timeline-item>
        <el-timeline-item id="step4" timestamp="Step 4" placement="top">
          <el-card class="dynamic-card">
            <h4 class="font-bold text-base">Select a suitable repository</h4>
            <p>
              You will be prompted to select one of the suitable repositories
              for research software currently supported by FAIRShare
            </p>
          </el-card>
        </el-timeline-item>
        <el-timeline-item id="step5" timestamp="Step 5" placement="top">
          <el-card class="dynamic-card">
            <h4 class="font-bold text-base">Upload dataset</h4>
            <p>
              The standard codemeta.json and citation.json metadata files will
              be automatically included amongst your data files before uploading
              everything on the repository
            </p>
          </el-card>
        </el-timeline-item>
        <el-timeline-item id="step6" timestamp="Step 6" placement="top">
          <el-card class="dynamic-card">
            <h4 class="font-bold text-base">Publish dataset</h4>
            <p>
              You will be requested to make the dataset visible on the
              repository to complete the process
            </p>
          </el-card>
        </el-timeline-item>
      </el-timeline>

      <div class="w-full flex flex-row justify-center py-6" id="button-area">
        <router-link to="/datasets" class="hidden">
          <el-button type="danger" plain> Cancel </el-button>
        </router-link>

        <button
          class="primary-button"
          @click="navigateToWorkflows"
          ref="continueButton"
        >
          Let's go
          <el-icon> <d-arrow-right /> </el-icon>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { useDatasetsStore } from "@/store/datasets";
import gsap from "gsap";

export default {
  name: "ProjectLanding",
  data() {
    return {
      datasetStore: useDatasetsStore(),
      dataset: {},
      datasetID: this.$route.params.datasetID,
    };
  },
  methods: {
    navigateToWorkflows() {
      this.$router.push({ path: `/datasets/${this.datasetID}` });
    },
  },
  async mounted() {
    this.datasetStore.hideProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(1);

    gsap.fromTo(
      ".el-timeline-item",
      {
        opacity: 0,
        y: -60,
      },
      {
        opacity: 1,
        y: 0,
        duration: 0.1,
        stagger: 0.1,
      }
    );
  },
};
</script>

<style scoped></style>
