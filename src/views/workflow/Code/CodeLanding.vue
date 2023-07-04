<template>
  <div class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 px-5">
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium"> FAIRifying </span>

      <span> Let's make your research software FAIR </span>

      <line-divider> </line-divider>

      <p class="pt-2">
        Currently, FAIRshare supports making research software FAIR according to the FAIR Biomedical
        Research Software (FAIR-BioRS) guidelines v1.0. To our knowledge, these are the only
        actionable FAIR guidelines available for biomedical research software irrespective of the
        field of research, funding source, etc. Read our
        <span
          class="text-url"
          @click="
            openWebsite(
              'https://docs.fairshareapp.io/docs/how-to-fair/how-to-make-research-software-fair'
            )
          "
        >
          dedicated documentation page
        </span>
        to find out more about them.
      </p>
      <p class="pb-4 pt-1">
        <br />
        To implement these guidelines, FAIRshare will guide you step-by-step through the following
        process:
      </p>

      <el-timeline>
        <el-timeline-item id="step1" timestamp="Step 1" placement="top">
          <el-card class="dynamic-card">
            <h4 class="text-base font-bold">Select data files</h4>
            <p>
              You will be asked to select the location of the files (source code, executable, etc.)
              you want to include in your dataset
            </p>
          </el-card>
        </el-timeline-item>
        <el-timeline-item id="step2" timestamp="Step 2" placement="top">
          <el-card class="dynamic-card">
            <h4 class="text-base font-bold">Review standard development practices</h4>
            <p>
              You will be asked a series a question to ensure standard practices have been followed
              when developing your research software
            </p>
          </el-card>
        </el-timeline-item>
        <el-timeline-item id="step3" timestamp="Step 3" placement="top">
          <el-card class="dynamic-card">
            <h4 class="text-base font-bold">Provide metadata</h4>
            <p>
              Information about your software will be requested and will be used to include the
              standard codemeta.json and CITATION.cff metadata files in your dataset
            </p>
          </el-card>
        </el-timeline-item>
        <el-timeline-item id="step3" timestamp="Step 4" placement="top">
          <el-card class="dynamic-card">
            <h4 class="text-base font-bold">Select a license</h4>
            <p>Select the license under which you want to share your research software</p>
          </el-card>
        </el-timeline-item>
        <el-timeline-item id="step4" timestamp="Step 5" placement="top">
          <el-card class="dynamic-card">
            <h4 class="text-base font-bold">Select a suitable repository</h4>
            <p>
              You will be prompted to select one of the suitable repositories for research software
              currently supported and requested to provide repository-specific metadata
            </p>
          </el-card>
        </el-timeline-item>
        <el-timeline-item id="step5" timestamp="Step 6" placement="top">
          <el-card class="dynamic-card">
            <h4 class="text-base font-bold">Upload dataset</h4>
            <p>
              The standard codemeta.json and CITATION.cff metadata files will be automatically
              included amongst your data files before uploading everything on the repository
            </p>
          </el-card>
        </el-timeline-item>
        <el-timeline-item id="step6" timestamp="Step 7" placement="top">
          <el-card class="dynamic-card">
            <h4 class="text-base font-bold">Publish dataset</h4>
            <p>
              You will be prompted to publish the dataset for making it openly accesible on the
              repository to complete the process
            </p>
          </el-card>
        </el-timeline-item>
      </el-timeline>

      <div class="flex w-full flex-row justify-center py-6" id="button-area">
        <router-link to="/datasets" class="hidden">
          <el-button type="danger" plain> Cancel </el-button>
        </router-link>

        <button class="primary-button" @click="navigateToSelectFolder" ref="continueButton">
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
  name: "CodeLanding",
  data() {
    return {
      datasetStore: useDatasetsStore(),
      dataset: {},
      datasetID: this.$route.params.datasetID,
      workflowID: this.$route.params.workflowID,
    };
  },
  methods: {
    navigateToSelectFolder() {
      this.$router.push({
        path: `/datasets/${this.datasetID}/${this.workflowID}/Code/selectFolder`,
      });
    },
    openWebsite(url) {
      window.ipcRenderer.send("open-link-in-browser", url);
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();

    this.workflow = this.dataset.workflows[this.workflowID];

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(1);

    this.workflow.fairListShown = true;

    this.datasetStore.updateCurrentDataset(this.dataset);
    this.datasetStore.syncDatasets();

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
