<template>
  <div
    class="h-full w-full flex flex-col justify-center items-center pr-5 p-3 max-w-screen-xl"
  >
    <div class="flex flex-col h-full w-full">
      <span class="text-lg font-medium text-left">
        Select a license that defines the desired conditions for using your
        software
      </span>

      <el-divider> </el-divider>

      <div>
        <el-form
          :model="licenseForm"
          label-position="top"
          size="large"
          ref="licenseForm"
          @submit.prevent
          hide-required-asterisk
        >
          <el-form-item label="License" required prop="license">
            <template #label>
              <div class="flex">
                <span> License </span>
                <span class="text-red-500 px-1"> * </span>
                <form-help-content
                  popoverContent="<p class='text-sm'> Required. Selected license applies to all of your files <br /> If you want to upload some of your files under different licenses, please do so in separate uploads. <br /> If you cannot find the license you're looking for, include a relevant LICENSE file in your record and choose one of the <span class='italic'> Other </span> licenses available <span class='italic'> (Other (Open), Other (Attribution) </span>, etc.). <br /> The supported licenses in the list are harvested from <a onclick='window.ipcRenderer.send(`open-link-in-browser`, `https://opendefinition.org`)' class='text-url'> opendefinition.org </a> and <a onclick='window.ipcRenderer.send(`open-link-in-browser`, `https://spdx.org`)' class='text-url' > spdx.org </a>.</p>"
                ></form-help-content>
              </div>
            </template>
            <el-select
              v-model="licenseForm.license"
              filterable
              placeholder="Select a license"
              class="w-full"
              @change="openLicenseDetails"
            >
              <el-option
                v-for="item in licenseOptions"
                :key="item.licenseId"
                :label="item.name"
                :value="item.licenseId"
              >
              </el-option>
            </el-select>

            <button
              class="secondary-plain-button my-4 px-2 py-1 h-[30px]"
              v-if="licenseForm.license != ''"
              @click="openLicenseDetails"
            >
              Show license details
            </button>

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
import { ElLoading } from "element-plus";
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
      spinnerGlobal: null,
    };
  },
  methods: {
    async openLicenseDetails() {
      this.spinnerGlobal = await this.createLoading();

      this.licenseHtmlUrl = "/";
      const licenseId = this.licenseForm.license;

      //get license object
      const licenseObject = await this.licenseOptions.find(
        (license) => license.licenseId === licenseId
      );

      this.licenseHtmlUrl = licenseObject.reference;
      this.licenseTitle = licenseObject.name;

      this.showLicenseDetails = true;
      this.loadingLicenseDetails = true;
      await this.spinnerGlobal.close();
    },
    createLoading() {
      const loading = ElLoading.service({
        lock: true,
        text: "loading...",
      });
      return loading;
    },
    startCuration() {
      this.$refs.licenseForm.validate((valid) => {
        console.log(valid);
        if (valid) {
          this.dataset.data.Code.questions.license = this.licenseForm.license;
          this.dataset.data.general.questions.license =
            this.licenseForm.license;

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
    this.datasetStore.setCurrentStep(4);

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
