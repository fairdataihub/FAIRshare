<template>
  <div
    class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 pr-5"
  >
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium">
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
                <span class="px-1 text-red-500"> * </span>
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
              @change="licenseChange"
            >
              <el-option
                v-for="item in licenseOptions"
                :key="item.licenseId"
                :label="item.name"
                :value="item.licenseId"
              >
              </el-option>
            </el-select>

            <div
              class="hover-underline-animation text-primary-600 my-3 flex w-max cursor-pointer flex-row items-center"
              v-if="licenseForm.license != ''"
              @click="openLicenseDetails"
            >
              <span class="text-base font-medium"> Show license details </span>
              <Icon icon="grommet-icons:form-next-link" class="ml-2 h-5 w-5" />
            </div>

            <el-drawer
              v-model="showLicenseDetails"
              :title="licenseTitle"
              direction="rtl"
            >
              <div
                v-loading="loading"
                :class="loading ? 'h-full w-full' : 'h-[0px] w-[0px]'"
              ></div>
              <iframe
                sandbox
                :src="licenseHtmlUrl"
                class="h-full w-full"
                @load="finishLoading"
              ></iframe>
            </el-drawer>
          </el-form-item>

          <div v-if="licenseChanged">
            <p class="text-base">
              Do you want to create and add a license terms file into your
              dataset?
            </p>

            <div class="pb-3">
              <el-radio-group v-model="saveLicense" @change="showLicenseEditor">
                <el-radio label="Yes" size="large"> Yes </el-radio>
                <el-radio label="No" size="large"> No </el-radio>
              </el-radio-group>
            </div>
          </div>

          <div v-if="displayLicenseEditor">
            <p class="py-2">Edit if required and continue</p>

            <QuillEditor
              theme="snow"
              :content="draftLicense"
              toolbar="essential"
              contentType="text"
            />
          </div>
        </el-form>
      </div>

      <div class="flex w-full flex-row justify-center space-x-4 py-2">
        <router-link
          :to="`/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/Code/createMetadata`"
          class=""
        >
          <button class="primary-plain-button">
            <el-icon><d-arrow-left /></el-icon> Back
          </button>
        </router-link>

        <button
          v-if="displayLicenseEditor"
          class="primary-button"
          @click="generateContinue"
        >
          Generate license and Continue
          <el-icon> <d-arrow-right /> </el-icon>
        </button>

        <button
          v-else
          class="primary-button"
          @click="startCuration"
          id="continue"
          :disabled="licenseDisabled"
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
import { useTokenStore } from "@/store/access.js";

import licensesJSON from "@/assets/supplementalFiles/licenses.json";

import { Icon } from "@iconify/vue";
import { ElLoading } from "element-plus";
import axios from "axios";

import { QuillEditor } from "@vueup/vue-quill";
import "@vueup/vue-quill/dist/vue-quill.snow.css";

export default {
  name: "CodePickLicense",
  components: {
    Icon,
    QuillEditor,
  },
  data() {
    return {
      loading: true,
      datasetStore: useDatasetsStore(),
      tokens: useTokenStore(),
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
      licenseChanged: false,
      originalLicense: "",
      saveLicense: "",
      displayLicenseEditor: false,
      draftLicense: "",
    };
  },
  computed: {
    licenseDisabled() {
      let disabled = false;

      if (this.licenseForm.license === "") {
        return true;
      }

      if (this.licenseChanged) {
        disabled = true;
      }

      if (disabled && this.saveLicense === "") {
        return true;
      } else if (disabled && this.saveLicense === "No") {
        return false;
      }

      return disabled;
    },
  },
  methods: {
    finishLoading() {
      this.loadingLicenseDetails = false;
      this.loading = false;
    },
    async openLicenseDetails() {
      this.spinnerGlobal = await this.createLoading("loading...");

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
    createLoading(loadingText) {
      const loading = ElLoading.service({
        lock: true,
        text: loadingText,
      });
      return loading;
    },
    licenseChange(val) {
      if (this.originalLicense !== val) {
        this.licenseChanged = true;
        this.displayLicenseEditor = false;
        this.saveLicense = "";
        this.draftLicense = "";
      } else {
        this.licenseChanged = false;
      }
    },
    async showLicenseEditor() {
      if (this.saveLicense === "Yes") {
        const licenseId = this.licenseForm.license;

        // get license object
        const licenseObject = this.licenseOptions.find(
          (license) => license.licenseId === licenseId
        );

        const licensejson = licenseObject.detailsUrl;

        const response = await axios
          .post(`${this.$server_url}/utilities/requestjson`, {
            url: licensejson,
          })
          .then((response) => {
            return response.data;
          })
          .catch((error) => {
            console.error(error);
            return "ERROR";
          });

        console.log(response);
        this.draftLicense = response.licenseText;

        this.displayLicenseEditor = true;
      } else {
        this.displayLicenseEditor = false;
      }
    },
    generateContinue() {
      this.dataset.data.Code.questions.license = this.licenseForm.license;
      this.dataset.data.general.questions.license = this.licenseForm.license;

      // turn this to false after license is generated at the end of the workflow
      this.workflow.generateLicense = true;
      this.workflow.licenseText = this.draftLicense;

      this.datasetStore.updateCurrentDataset(this.dataset);
      this.datasetStore.syncDatasets();

      this.$router.push(
        `/datasets/${this.datasetID}/${this.workflowID}/selectDestination`
      );
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
    async prefillGithubLicense() {
      console.info("Prefilling other items from github repo");

      let loadingState = await this.createLoading();

      // get a list of contributors for the repo
      const tokenObject = await this.tokens.getToken("github");
      const GithubAccessToken = tokenObject.token;

      const selectedRepo = this.workflow.github.repo;

      let response = "";

      response = await axios
        .get(`${process.env.VUE_APP_GITHUB_SERVER_URL}/repos/${selectedRepo}`, {
          params: {
            accept: "application/vnd.github.v3+json",
          },
          headers: {
            Authorization: `Bearer  ${GithubAccessToken}`,
          },
        })
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });

      if (response !== "ERROR") {
        if ("license" in response && response.license != null) {
          if (
            "spdx_id" in response.license &&
            (response.license.spdx_id != null || response.license.spdx_id != "")
          ) {
            this.originalLicense =
              this.licenseForm.license =
              this.dataset.data.Code.questions.license =
                response.license.spdx_id;
            // this.licenseForm.license = this.dataset.data.Code.questions.license;
            // this.originalLicense = this.licenseForm.license;
          }
        }
      }

      loadingState.close();
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();

    this.workflow = this.dataset.workflows[this.workflowID];

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(4);

    this.workflow.currentRoute = this.$route.path;

    console.log(this.dataset.data.general.questions);

    if (
      "general" in this.dataset.data &&
      "questions" in this.dataset.data.general &&
      "license" in this.dataset.data.general.questions
    ) {
      console.log(this.dataset.data.general.questions.license);
      this.licenseForm.license = this.dataset.data.general.questions.license;
      this.originalLicense = this.licenseForm.license;
    } else {
      if ("source" in this.workflow) {
        if (this.workflow.source.type === "github") {
          await this.prefillGithubLicense();
        }
        if (this.workflow.source.type === "local") {
          this.licenseForm.license = "";
          this.originalLicense = "";
        }
      } else {
        this.licenseForm.license = "";
        this.originalLicense = "";
      }
    }
  },
};
</script>

<style></style>
