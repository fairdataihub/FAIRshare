<template>
  <div
    class="relative flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 px-5"
  >
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium">
        Provide information about your research sofware
      </span>

      <line-divider></line-divider>

      <transition name="fade" mode="out-in" appear>
        <div>
          <span class="mb-2">
            Provide information about your software below. We will use this information to create an
            entry on the bio.tools registry for your software.
          </span>

          <div>
            <div class="py-3">
              <pill-progress-bar
                :totalSteps="totalSteps"
                :currentStep="currentStep"
                @updateCurrentStep="setCurrentStep"
                :titles="pillTitles"
              />
            </div>
            <div class="py-2">
              <div v-if="currentStep == 1">
                <div class="form-card-content mb-4 rounded-lg border-2 border-slate-100 shadow-md">
                  <div class="w-full bg-gray-100 px-4 py-2">
                    <span class="pointer-events-none text-lg font-semibold text-primary-600">
                      Basic Information
                    </span>
                  </div>
                  <div class="p-4">
                    <el-form
                      :model="step1Form"
                      :rules="step1FormRules"
                      label-width="160px"
                      label-position="top"
                      size="large"
                      ref="s1Form"
                      @submit.prevent
                      class="py-4"
                    >
                      <el-form-item label="Tool name" prop="name">
                        <div class="flex w-full flex-row items-center">
                          <el-input v-model="step1Form.name" placeholder="Needle"></el-input>
                          <form-help-content
                            popoverContent="Canonical software name assigned by the software developer or service provider"
                          ></form-help-content>
                        </div>
                      </el-form-item>

                      <el-form-item label="Persistent biotoolsID" prop="biotoolsID">
                        <div class="flex w-full flex-row items-center">
                          <el-input
                            v-model="step1Form.biotoolsID"
                            type="text"
                            placeholder="needle"
                            :disabled="greyOutIdentifierInput"
                          ></el-input>

                          <form-help-content
                            popoverContent="An identifier for this dataset if applicable. "
                          ></form-help-content>
                        </div>
                        <div class="flex pt-2">
                          <p class="pr-1 text-sm text-gray-500">
                            {{
                              greyOutIdentifierInput
                                ? "This identifier will be assigned when registering your software on the bio.tools platform."
                                : "This identifier will be assigned when registering your software on the bio.tools platform."
                            }}
                          </p>
                          <p class="text-url cursor-pointer !text-sm" @click="editBioToolsID">
                            {{
                              greyOutIdentifierInput
                                ? "Click here to edit the ID."
                                : "Generate ID from tool name"
                            }}
                          </p>
                        </div>
                      </el-form-item>

                      <el-form-item label="Description" prop="description">
                        <div class="flex w-full flex-row items-center">
                          <el-input
                            v-model="step1Form.description"
                            type="textarea"
                            placeholder="Needle reads two input sequences and uses the Needleman-Wunsch alignment algorithm  to ensure the alignment is optimum, by exploring all possible alignments and choosing the best."
                          ></el-input>
                          <form-help-content
                            popoverContent="Textual description of the software"
                          ></form-help-content>
                        </div>
                      </el-form-item>

                      <el-form-item label="Homepage URL" prop="homepage">
                        <div class="flex w-full flex-row items-center">
                          <el-input
                            v-model="step1Form.homepage"
                            placeholder="http://emboss.open-bio.org/rel/rel6/apps/needle.html"
                          ></el-input>
                          <form-help-content
                            popoverContent="Homepage of the software, or some URL that best serves this purpose"
                          ></form-help-content>
                        </div>
                      </el-form-item>

                      <el-form-item label="Versions">
                        <draggable
                          tag="div"
                          :list="step1Form.versions"
                          item-key="id"
                          handle=".handle"
                          class="w-full"
                        >
                          <template #item="{ element }">
                            <div class="mb-2 flex w-full flex-row justify-between transition-all">
                              <div class="flex w-11/12 flex-row justify-between">
                                <el-input
                                  v-model="element.version"
                                  type="text"
                                  placeholder="v2.0.0-alpha, v2.1.0"
                                  v-on:keyup.enter="addVersion"
                                  :ref="element.id"
                                ></el-input>
                                <div class="mx-2"></div>
                              </div>
                              <div class="flex w-1/12 flex-row justify-evenly">
                                <div
                                  class="handle flex items-center justify-center text-gray-400 hover:text-gray-700"
                                >
                                  <Icon icon="ic:outline-drag-indicator" />
                                </div>
                                <div
                                  class="flex cursor-pointer items-center justify-center text-gray-500 transition-all hover:text-gray-800"
                                >
                                  <el-popconfirm
                                    title="Are you sure you want to remove this?"
                                    icon-color="red"
                                    confirm-button-text="Yes"
                                    cancel-button-text="No"
                                    @confirm="deleteVersion(element.id)"
                                  >
                                    <template #reference>
                                      <el-icon><delete-filled /></el-icon>
                                    </template>
                                  </el-popconfirm>
                                </div>
                              </div>
                            </div>
                          </template>
                        </draggable>
                      </el-form-item>

                      <div
                        class="flex w-max cursor-pointer items-center pb-3 text-sm text-gray-500 hover:text-black"
                        @click="addVersion(null, '')"
                      >
                        <Icon icon="carbon:add" />
                        <span> Add a version </span>
                        <form-help-content
                          popoverContent="Version information (typically a version number) of the software applicable to this bio.tools entry"
                        ></form-help-content>
                      </div>
                    </el-form>
                  </div>
                </div>
                <div class="flex w-full justify-center space-x-4 px-5 py-4">
                  <button @click="prevFormStep" class="primary-plain-button" size="medium">
                    <el-icon><back-icon /></el-icon>
                    Back
                  </button>
                  <!-- :plain="!lastStep" -->
                  <button class="primary-button" @click="navigateToStep2FromStep1">
                    Register on bio.tools
                    <el-icon>
                      <d-arrow-right />
                    </el-icon>
                  </button>
                  <warning-confirm
                    ref="publishWarningConfirm"
                    title="Confirm publish"
                    @messageConfirmed="navigateToRegister"
                  >
                    <p class="text-center text-base text-gray-500">
                      Once your software has been registered on bio.tools, you will not be able to
                      remove it without the approval of the bio.tools team. Are you sure you want to
                      continue?
                    </p>
                  </warning-confirm>
                </div>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </div>

    <fade-transition>
      <div class="fixed bottom-2 right-20" v-if="showSaving">
        <Vue3Lottie
          :animationData="SaveLottieJSON"
          :width="75"
          :height="75"
          :loop="1"
          @onComplete="hideSavingIcon"
        />
      </div>
    </fade-transition>

    <fade-transition>
      <div class="fixed bottom-2 right-20" v-show="showSpinner">
        <Vue3Lottie :animationData="$helix_spinner" :width="80" :height="80" />
      </div>
    </fade-transition>

    <app-docs-link url="curate-and-share/add-codemeta" position="bottom-4" />
  </div>
</template>

<script>
import { Icon } from "@iconify/vue";
import { v4 as uuidv4 } from "uuid";
// import { ElNotification } from "element-plus";

import draggable from "vuedraggable";
import validator from "validator";
import axios from "axios";
// import _ from "lodash";
// import humanparser from "humanparser";

import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

import PillProgressBar from "@/components/ui/PillProgressBar.vue";

import contributorTypesJSON from "@/assets/supplementalFiles/contributorTypes.json";
import codeMetadataJSON from "@/assets/supplementalFiles/codeMetadata.json";

import SaveLottieJSON from "@/assets/lotties/saveLottie.json";

export default {
  name: "BioToolsMetadata",
  components: {
    draggable,
    Icon,
    PillProgressBar,
  },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      tokens: useTokenStore(),
      currentStep: 1,
      totalSteps: 1,
      pillTitles: [
        "Summary",
        "Authors and Contributors",
        "Discoverability",
        "Development tools",
        "Run-time environment",
        "Current version of the software",
        "Additional Info",
      ],
      SaveLottieJSON,
      dataset: {},
      workflowID: this.$route.params.workflowID,
      workflow: {},
      loading: false,
      interval: null,
      contributorTypes: contributorTypesJSON.contributorTypes,
      programmingLanguageOptions: codeMetadataJSON.programmingLanguageOptions,
      runtimePlatformOptions: codeMetadataJSON.runtimePlatformOptions,
      operatingSystemOptions: codeMetadataJSON.operatingSystemOptions,
      applicationCategoryOptions: codeMetadataJSON.applicationCategoryOptions,

      step1Form: {
        name: "",
        biotoolsID: "",
        description: "",
        homepage: "",
        versions: [],
      },
      step1FormRules: {
        name: [
          {
            required: true,
            message: "Please enter the name of the software",
            trigger: "blur",
          },
        ],
        biotoolsID: [
          {
            required: true,
            validator: this.biotoolsIDValidator,
            trigger: "change",
          },
        ],
        description: [
          {
            required: true,
            validator: this.descriptionValidator,
            trigger: "blur",
          },
        ],
        homepage: [
          {
            required: true,
            validator: this.homepageValidator,
            trigger: "blur",
          },
        ],
      },

      authorsErrorMessage: "",
      contributorsErrorMessage: "",
      isPartOfErrorMessage: "",
      versionErrorMessage: "",
      currentVersionDownloadLinkErrorMessage: "",
      relatedLinksErrorMessage: "",
      issueTrackerErrorMessage: "",
      continuousIntegrationErrorMessage: "",
      codeRepositoryErrorMessage: "",
      greyOutIdentifierInput: true,
      invalidStatus: {},
      originalObject: {},
      showSaving: false,
      showSpinner: false,
    };
  },
  watch: {
    "step1Form.name": {
      handler(val) {
        if (val != "" && val != undefined) {
          if (this.greyOutIdentifierInput) {
            const name = val.replaceAll(" ", "_").toLowerCase();
            this.step1Form.biotoolsID = name;
          }
        } else {
          this.step1Form.biotoolsID = "";
        }
      },
      deep: true,
    },
  },
  computed: {
    //check if code workflow is present
    codePresent() {
      if ("type" in this.workflow) {
        return this.workflow.type.includes("Code");
      }
      return false;
    },

    checkInvalidStatus() {
      for (const key in this.invalidStatus) {
        if (this.invalidStatus[key]) {
          return true;
        }
      }
      return false;
    },
  },
  methods: {
    async sleep(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    },
    setCurrentStep(step) {
      this.currentStep = step;
    },
    showSavingIcon() {
      this.showSaving = false;
      this.showSaving = true;
    },
    hideSavingIcon() {
      this.showSaving = false;
    },
    async prevFormStep() {
      if (this.currentStep - 1 > 0) {
        this.showSavingIcon();
        this.currentStep--;
      } else {
        this.navigateBack();
      }
    },
    // To be used when I add the final step
    async nextFormStep() {
      if (this.currentStep + 1 > this.totalSteps) {
        if (!this.checkInvalidStatus) {
          this.navigateToRegister();
        }
      } else {
        this.currentStep++;
      }
    },

    editBioToolsID() {
      this.greyOutIdentifierInput = !this.greyOutIdentifierInput;

      if (this.greyOutIdentifierInput) {
        const name = this.step1Form.name.replaceAll(" ", "_").toLowerCase();
        this.step1Form.biotoolsID = name;
      }
    },

    biotoolsIDValidator(_rule, value, callback) {
      const idRegex = /^[a-zA-Z0-9-_~.]+$/;

      if (value === "" || value === undefined) {
        if (this.greyOutIdentifierInput) {
          callback();
        } else {
          callback(new Error("Please enter a unique identifier"));
        }
      } else if (!idRegex.test(value.trim())) {
        callback(
          new Error("The biotoolsID can only contain letters, numbers or these characters: . - _ ~")
        );
      } else {
        callback();
      }
    },

    descriptionValidator(_rule, value, callback) {
      if (value === "" || value === undefined) {
        callback(new Error("Please enter a description for your software"));
      } else if (value.length < 10) {
        callback(new Error("Please enter a description that is at least 10 characters long"));
      } else {
        callback();
      }
    },

    homepageValidator(_rule, value, callback) {
      if (value === "" || value === undefined) {
        callback(new Error("Please enter a URL for your sofware"));
      } else if (!validator.isURL(value)) {
        callback(new Error("Please enter a valid URL"));
      } else {
        callback();
      }
    },

    async navigateToStep2FromStep1() {
      this.$refs["s1Form"].validate(async (valid) => {
        if (valid) {
          const tokenObject = await this.tokens.getToken("biotools");
          const token = tokenObject.token;
          const data = JSON.stringify({
            name: this.step1Form.name,
            biotoolsID: this.step1Form.biotoolsID,
            description: this.step1Form.description,
            homepage: this.step1Form.homepage,
            versions: this.filterArrayOfObjects(this.step1Form.versions, "version"),
          });

          const response = await axios
            .post(`${this.$server_url}/biotools/tool/validate`, {
              token,
              data,
            })
            .then((response) => {
              return response.data;
            })
            .catch((error) => {
              console.error(error);
              return "ERROR";
            });

          if (response === "ERROR") {
            this.$message.error(
              "An error occurred while validating the tool. Please try again later."
            );

            this.$track("bio.tools", "Validate tool", "failed");
            return;
          } else {
            if (response.status === "error") {
              if ("biotoolsID" in response.data) {
                this.$message.error(
                  "The tool ID you entered is already registered. bio.tools IDs need to be unique. Please enter a different ID."
                );

                this.$track("bio.tools", "Validate tool", "failed");
                return;
              } else {
                this.$alert(
                  JSON.stringify(response.data),
                  "There were some errors in your submission",
                  { type: "error" }
                );

                this.$track("bio.tools", "Validate tool", "failed");
                return;
              }
            }
            if (response.status === "success") {
              // Comment out the lines below. Will come back to this when we are adding more fields.
              // await this.saveCurrentEntries();
              // this.setCurrentStep(2);
              this.$refs.publishWarningConfirm.show();
            }
          }
        }
      });
    },
    navigateToStep3FromStep2() {
      this.$refs["s2Form"].validate(async (valid) => {
        if (valid) {
          await this.saveCurrentEntries();
          this.setCurrentStep(3);
        }
      });
    },
    navigateToStep4FromStep3() {
      this.$refs["s3Form"].validate(async (valid) => {
        if (valid) {
          await this.saveCurrentEntries();
          this.setCurrentStep(4);
        }
      });
    },
    navigateToStep5FromStep4() {
      this.$refs["s4Form"].validate(async (valid) => {
        if (valid) {
          await this.saveCurrentEntries();
          this.setCurrentStep(5);
        }
      });
    },
    navigateToStep6FromStep5() {
      this.$refs["s5Form"].validate(async (valid) => {
        if (valid) {
          await this.saveCurrentEntries();
          this.setCurrentStep(6);
        }
      });
    },
    navigateToStep7FromStep6() {
      this.$refs["s6Form"].validate(async (valid) => {
        if (valid) {
          await this.saveCurrentEntries();
          this.setCurrentStep(7);
        }
      });
    },
    addIds(array) {
      array.forEach((element) => {
        element.id = uuidv4();
      });
    },
    initializeEmptyObjects(root, obj) {
      if (typeof obj === "undefined") {
        root[obj] = {};
      }
    },
    focusOnElementRef(elementRef) {
      // check if element is available in 100ms intervals
      const interval = setInterval(() => {
        if (this.$refs[elementRef]) {
          this.$refs[elementRef].focus();
          clearInterval(interval);
        }
      }, 50);
    },
    addVersion(_event, version = "") {
      if (this.step1Form.versions.some((el) => el.version === version)) {
        this.$message.warning("Version already exists.");
        return;
      }

      const id = uuidv4();
      this.step1Form.versions.push({
        version,
        id,
      });
      this.focusOnElementRef(id);
    },
    deleteVersion(id) {
      this.step1Form.versions = this.step1Form.versions.filter((version) => {
        return version.id !== id;
      });
    },
    filterArrayOfObjects(array, key) {
      return array.filter((element) => {
        return element[key] !== "";
      });
    },
    async saveCurrentEntries() {
      this.showSavingIcon();

      if (!("biotools" in this.workflow)) {
        this.workflow.biotools = {};
      }

      this.workflow.biotools.name = this.step1Form.name;
      this.workflow.biotools.biotoolsID = this.step1Form.biotoolsID.trim();
      this.workflow.biotools.description = this.step1Form.description;
      this.workflow.biotools.homepage = this.step1Form.homepage;
      this.workflow.biotools.versions = this.filterArrayOfObjects(
        this.step1Form.versions,
        "version"
      );

      await this.datasetStore.updateCurrentDataset(this.dataset);
      await this.datasetStore.syncDatasets();
    },
    generateDataForBiotools() {
      let response = {};

      response.name = this.workflow.biotools.name;
      response.biotoolsID = this.workflow.biotools.biotoolsID;
      response.description = this.workflow.biotools.description;
      response.homepage = this.workflow.biotools.homepage;

      if (this.workflow.biotools.versions.length > 0) {
        response.version = [];
        this.workflow.biotools.versions.forEach((version) => {
          response.version.push(version.version);
        });
      }

      return JSON.stringify(response);
    },
    async registerOnBiotools() {
      const tokenObject = await this.tokens.getToken("biotools");
      const token = tokenObject.token;

      const data = this.generateDataForBiotools();

      const response = await axios
        .post(`${this.$server_url}/biotools/tool/register`, {
          token,
          data,
        })
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });

      return response;
    },
    async navigateToRegister(_evt, shouldNavigateBack = false) {
      await this.saveCurrentEntries();

      if (shouldNavigateBack) {
        this.$router.push({
          path: `/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/selectFolder`,
        });
        return;
      }

      const response = await this.registerOnBiotools();

      if (response === "ERROR") {
        this.$message.error(
          "There was an error while trying to register your tool on bio.tools. Please try again later."
        );

        this.$track("bio.tools", "Register tool", "failed");
        return;
      } else {
        if (response.status === "error") {
          this.$alert(JSON.stringify(response.data), "There were some errors in your submission", {
            type: "error",
          });

          this.$track("bio.tools", "Register tool", "failed");
          return;
        } else {
          this.$track("bio.tools", "Register tool", "success");

          const routerPath = `/datasets/${this.dataset.id}/${this.workflowID}/biotools/review`;

          this.$router.push({ path: routerPath });
        }
      }
    },
    navigateBack() {
      this.$router.push({
        path: `/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/biotools/login`,
      });
    },
  },
  async mounted() {
    this.$nextTick(async function () {
      this.dataset = await this.datasetStore.getCurrentDataset();

      this.workflow = this.dataset.workflows[this.workflowID];

      this.datasetStore.showProgressBar();
      this.datasetStore.setProgressBarType("zenodo");
      this.datasetStore.setCurrentStep(8);

      this.workflow.currentRoute = this.$route.path;

      if (this.codePresent) {
        if (this.workflow.biotools && Object.keys(this.workflow.biotools).length !== 0) {
          const toolsForm = this.workflow.biotools;

          this.step1Form.name = toolsForm.name;
          this.step1Form.biotoolsID = toolsForm.biotoolsID;
          this.step1Form.description = toolsForm.description;
          this.step1Form.homepage = toolsForm.homepage;
          this.step1Form.versions = toolsForm.versions;

          this.addIds(this.step1Form.versions);

          // this.step1Form.name = codeForm.name;
          // this.step1Form.description = codeForm.description;
          // this.step1Form.creationDate = codeForm.creationDate;
          // this.step1Form.firstReleaseDate = codeForm.firstReleaseDate;
          // this.initializeEmptyObjects(this.step3Form, this.step3Form.funding);
          // this.addIds(this.step3Form.keywords);
          // this.addIds(this.step2Form.authors);
          // this.addIds(this.step2Form.contributors);
          // this.addIds(this.step4Form.relatedLinks);
          // this.addIds(this.step5Form.otherSoftwareRequirements);
        } else {
          this.step1Form.name = this.dataset.name;
          this.step1Form.description = this.dataset.description;
        }
      }
    });
  },
};
</script>
