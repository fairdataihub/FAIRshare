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

                      <el-form-item label="Persistent biotoolsID">
                        <div class="flex w-full flex-row items-center">
                          <el-input
                            v-model="step1Form.bioToolsID"
                            type="text"
                            placeholder="needle"
                            :disabled="greyOutIdentifierInput"
                          ></el-input>

                          <form-help-content
                            popoverContent="An identifier for this dataset if applicable. "
                          ></form-help-content>
                        </div>
                        <div v-if="greyOutIdentifierInput" class="flex pt-2">
                          <p class="pr-1 text-sm text-gray-500">
                            This identifier will be assigned when registering your software on the
                            bio.tools platform.
                          </p>
                          <p
                            class="text-url hidden cursor-pointer !text-sm"
                            @click="editUniqueIdentifier"
                          >
                            Click here to override this.
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
                    Next
                    <el-icon><right-icon /></el-icon>
                  </button>
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
// import { Icon } from "@iconify/vue";
import { v4 as uuidv4 } from "uuid";
// import { ElNotification } from "element-plus";

// import draggable from "vuedraggable";
import validator from "validator";
// import axios from "axios";
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
    // draggable,
    // Icon,
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
        bioToolsID: "",
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
          const name = val.replaceAll(" ", "_").toLowerCase();
          this.step1Form.bioToolsID = name;
        } else {
          this.step1Form.bioToolsID = "";
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
      this.showSavingIcon();

      if (this.currentStep - 1 > 0) {
        this.currentStep--;
      } else {
        this.navigateBack();
      }
    },
    async nextFormStep() {
      if (this.currentStep + 1 > this.totalSteps) {
        if (!this.checkInvalidStatus) {
          this.navigateToSelectDestination();
        }
      } else {
        this.currentStep++;
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

    navigateToStep2FromStep1() {
      this.$refs["s1Form"].validate(async (valid) => {
        if (valid) {
          await this.saveCurrentEntries();
          this.setCurrentStep(2);
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

    filterArrayOfObjects(array, key) {
      return array.filter((element) => {
        return element[key] !== "";
      });
    },
    async saveCurrentEntries() {
      this.showSavingIcon();

      this.dataset.data.general.questions.name = this.step1Form.name;
      this.dataset.data.general.questions.description = this.step1Form.description;

      this.step3Form.keywords = this.filterArrayOfObjects(this.step3Form.keywords, "keyword");

      this.dataset.data.general.questions.keywords = this.step3Form.keywords;
      this.dataset.data.general.questions.authors = this.step2Form.authors;
      this.dataset.data.general.questions.contributors = this.step2Form.contributors;
      this.dataset.data.general.questions.funding = this.step3Form.funding;
      this.dataset.data.general.questions.referencePublication =
        this.step7Form.referencePublication;

      this.step4Form.relatedLinks = this.filterArrayOfObjects(this.step4Form.relatedLinks, "link");

      this.step5Form.otherSoftwareRequirements = this.filterArrayOfObjects(
        this.step5Form.otherSoftwareRequirements,
        "link"
      );

      if (this.codePresent) {
        let codeForm = {};

        codeForm.name = this.step1Form.name;
        codeForm.description = this.step1Form.description;
        codeForm.creationDate = this.step1Form.creationDate;
        codeForm.firstReleaseDate = this.step1Form.firstReleaseDate;

        codeForm.authors = this.step2Form.authors;
        codeForm.contributors = this.step2Form.contributors;

        codeForm.identifier = this.step3Form.identifier;
        codeForm.keywords = this.step3Form.keywords;
        codeForm.funding = this.step3Form.funding;
        codeForm.applicationCategory = this.step3Form.applicationCategory;

        codeForm.codeRepository = this.step4Form.codeRepository;
        codeForm.continuousIntegration = this.step4Form.continuousIntegration;
        codeForm.issueTracker = this.step4Form.issueTracker;
        codeForm.relatedLinks = this.step4Form.relatedLinks;

        codeForm.programmingLanguage = this.step5Form.programmingLanguage;
        codeForm.runtimePlatform = this.step5Form.runtimePlatform;
        codeForm.operatingSystem = this.step5Form.operatingSystem;
        codeForm.otherSoftwareRequirements = this.step5Form.otherSoftwareRequirements;

        codeForm.currentVersion = this.step6Form.currentVersion;
        codeForm.currentVersionReleaseDate = this.step6Form.currentVersionReleaseDate;
        codeForm.currentVersionDownloadLink = this.step6Form.currentVersionDownloadLink;
        codeForm.currentVersionReleaseNotes = this.step6Form.currentVersionReleaseNotes;

        codeForm.referencePublication = this.step7Form.referencePublication;
        codeForm.developmentStatus = this.step7Form.developmentStatus;
        codeForm.isPartOf = this.step7Form.isPartOf;

        this.dataset.data.Code.questions = codeForm;
      }

      await this.datasetStore.updateCurrentDataset(this.dataset);
      await this.datasetStore.syncDatasets();
    },
    async navigateToSelectDestination(_evt, shouldNavigateBack = false) {
      await this.saveCurrentEntries();

      if (shouldNavigateBack) {
        this.$router.push({
          path: `/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/selectFolder`,
        });
        return;
      }

      const routerPath = `/datasets/${this.dataset.id}/${this.workflowID}/Code/pickLicense`;

      this.$router.push({ path: routerPath });
    },
    navigateBack() {
      this.$router.push({
        path: `/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/Code/reviewStandards`,
      });
    },
  },
  async mounted() {
    this.$nextTick(async function () {
      this.dataset = await this.datasetStore.getCurrentDataset();

      this.workflow = this.dataset.workflows[this.workflowID];

      this.datasetStore.showProgressBar();
      this.datasetStore.setProgressBarType("zenodo");
      this.datasetStore.setCurrentStep(3);

      this.workflow.currentRoute = this.$route.path;

      if (this.codePresent) {
        if (
          this.dataset.data.Code.questions &&
          Object.keys(this.dataset.data.Code.questions).length !== 0
        ) {
          // let codeForm = this.dataset.data.Code.questions;
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
