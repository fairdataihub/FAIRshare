<template>
  <div class="h-screen w-full flex flex-row lg:justify-center items-center">
    <div class="p-3 h-full flex flex-row items-center">
      <div class="h-full w-full">
        <div class="flex flex-col h-full overflow-y-auto pr-5">
          <span class="text-lg font-medium text-left">
            Zenodo Metadata
          </span>
          <span class="text-left">
            Questions required for creating metadata.json file?
          </span>

          <line-divider></line-divider>

          <span class="mb-2">
            We need to know some general details about you and your dataset.
            Please fill this out to the best of your ability.
          </span>

          <el-form
            :model="generalQuestionsForm"
            label-width="auto"
            label-position="top"
            size="medium"
            @submit.prevent
          >
            <el-form-item label="Dataset name">
              <el-input v-model="generalQuestionsForm.datasetName"></el-input>
            </el-form-item>

            <el-form-item label="Dataset description">
              <el-popover
                ref="popover"
                placement="bottom"
                :width="300"
                trigger="manual"
              >
                <template #reference>
                  <el-input
                    v-model="generalQuestionsForm.datasetDescription"
                    type="textarea"
                  ></el-input>
                </template>

                <span class="break-normal text-left text-sm">
                  Use a description that is easily identifiable. This will be
                  shown in the dataset selection screen and is not part of your
                  submitted metadata.
                </span>
              </el-popover>
            </el-form-item>
          </el-form>

          <div class="w-full flex flex-row justify-center py-2">
            <router-link to="/datasets" class="mx-6">
              <el-button type="danger" plain> Cancel </el-button>
            </router-link>

            <el-button
              type="primary"
              class="flex flex-row items-center"
              @click="navigateToSelectDestination"
            >
              Continue
              <el-icon>
                <ArrowRightBold />
              </el-icon>
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import { Icon } from "@iconify/vue";
import { ArrowRightBold } from "@element-plus/icons";

import { useDatasetsStore } from "../store/datasets";

export default {
  name: "DatasetsCurateZenodoMetadata",
  components: { ArrowRightBold },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      dataset: {},
      generalQuestionsForm: {
        datasetName: "",
        datasetDescription: "",
      },

      basicInformationForm: {
        publicationDate: "",
        title: "",
        authors: [],
        description: "",
        version: "",
        language: "",
        keywords: [],
        additionalNotes: "",
      },
      basicInformationRules: {
        publicationDate: [
          {
            required: true,
            message: "Please provide a date for your publication.",
            trigger: "blur",
          },
        ],
        title: [
          {
            required: true,
            message: "Please provide a date for your publication.",
            trigger: "blur",
          },
        ],
      },
      licenseForm: {
        accessRights: "",
        license: "",
      },
      licenseRules: {
        license: [
          {
            required: true,
            message: "Please select a license.",
            trigger: "change",
          },
        ],
      },
      fundingQuestionsForm: {
        grants: [],
      },
      relatedIdentifiersForm: {
        relatedIdentifiers: [],
      },
      contributorsForm: {
        contributors: [],
      },
      referencesForm: {
        references: [],
      },
      journalForm: {
        title: "",
        volume: "",
        issue: "",
        pages: "",
      },
      conferenceForm: {
        title: "",
        acronym: "",
        dates: "",
        place: "",
        website: "",
        session: "",
        part: "",
      },
      bookReportForm: {
        title: "",
        publisher: "",
        place: "",
        isbn: "",
        pages: "",
      },
      thesisForm: {
        awardingUniversity: "",
        supervisors: [],
      },
      subjectsForm: {
        subjects: [],
      },
      workflowID: this.$route.params.workflowID,
      workflow: {},
    };
  },
  computed: {},
  methods: {
    navigateToSelectDestination() {
      this.datasetStore.updateCurrentDataset(this.dataset);

      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/selectDestination`;
      this.$router.push({ path: routerPath });
    },
  },
  mounted() {
    this.dataset = this.datasetStore.currentDataset;
    this.workflow = this.dataset.workflows[this.workflowID];

    // Add the functions here to check the pre saved values for on mounted.
    // decide if the intermdiate data is saved in workflow or data.
  },
};
</script>
