<template>
  <div
    class="h-full w-full flex flex-col justify-center items-center pr-5 p-3 max-w-screen-xl"
  >
    <div class="flex flex-col h-full w-full">
      <span class="text-lg font-medium text-left">
        Let's select an appropriate license for your data
      </span>

      <el-divider> </el-divider>

      <div>
        <el-form
          :model="licenseForm"
          label-width="160px"
          label-position="top"
          size="large"
          ref="licenseForm"
          @submit.prevent
        >
          <el-form-item label="License">
            <el-select
              v-model="licenseForm.license"
              filterable
              placeholder="Select a license"
              class="w-full"
            >
              <el-option
                v-for="item in licenseOptions"
                :key="item.licenseId"
                :label="item.name"
                :value="item.licenseId"
              >
              </el-option>
            </el-select>

            <p
              class="text-sm pt-2 text-gray-500 cursor-pointer hover:text-gray-800"
              v-if="licenseForm.license != ''"
              @click="openLicenseDetails"
            >
              Show license details.
            </p>

            <el-drawer
              v-model="showLicenseDetails"
              :title="licenseTitle"
              direction="rtl"
            >
              <iframe
                sandbox
                :src="licenseHtmlUrl"
                class="w-full h-full"
                :load="(loadingLicenseDetails = false)"
              ></iframe>
            </el-drawer>
          </el-form-item>
        </el-form>
      </div>

      <div class="w-full flex flex-row justify-center py-2 space-x-4">
        <router-link
          :to="`/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/Code/createMetadata`"
          class=""
        >
          <button class="primary-plain-button">
            <el-icon><d-arrow-left /></el-icon> Back
          </button>
        </router-link>

        <button class="primary-button" @click="startCuration" id="continue">
          Continue
          <el-icon> <d-arrow-right /> </el-icon>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { useDatasetsStore } from "@/store/datasets";

import licensesJSON from "@/assets/supplementalFiles/licenses.json";

export default {
  name: "CodePickLicense",
  data() {
    return {
      datasetStore: useDatasetsStore(),
      datasetID: this.$route.params.datasetID,
      workflowID: this.$route.params.workflowID,
      dataset: {},
      workflow: {},
      questions: [
        "Is the data being curated in accordance with the standards?",
        "Is the data being curated in accordance with the standards?",
      ],
      licenseForm: {
        license: "",
      },
      rules: {
        license: [
          {
            type: "string",
            required: true,
            message: "Please select your license",
            trigger: "change",
          },
        ],
      },
      licenseHtmlUrl: "",
      licenseTitle: "",
      showLicenseDetails: false,
      loadingLicenseDetails: false,
      licenseOptions: licensesJSON.licenses,
    };
  },
  methods: {
    async openLicenseDetails() {
      this.licenseHtmlUrl = "/";
      const licenseId = this.licenseForm.license;

      //get license object
      const licenseObject = this.licenseOptions.find(
        (license) => license.licenseId === licenseId
      );

      this.licenseHtmlUrl = licenseObject.reference;
      this.licenseTitle = licenseObject.name;

      this.showLicenseDetails = true;
      this.loadingLicenseDetails = true;
    },
    startCuration() {
      this.$refs.licenseForm.validate((valid) => {
        if (valid) {
          this.dataset.data.Code.questions.license = this.licenseForm.license;

          this.datasetStore.updateCurrentDataset(this.dataset);
          this.datasetStore.syncDatasets();

          this.$router.push(
            `/datasets/${this.datasetID}/${this.workflowID}/selectDestination`
          );
        }
      });
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();

    this.workflow = this.dataset.workflows[this.workflowID];

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(2);

    if (
      "Code" in this.dataset.data &&
      "questions" in this.dataset.data.Code &&
      "license" in this.dataset.data.Code.questions
    ) {
      this.licenseForm.license = this.dataset.data.Code.questions.license;
    } else {
      this.licenseForm.license = "";
    }
  },
};
</script>

<style></style>
