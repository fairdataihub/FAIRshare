<template>
  <div class="flex h-screen w-full max-w-screen-xl flex-row items-center justify-center">
    <div class="flex h-full w-full flex-row items-center p-3">
      <div class="flex h-full w-full flex-col overflow-y-auto">
        <span class="text-left text-lg font-medium"> Start the curation process </span>

        <span class="">
          When you are ready, click on the curation buttons below to start the curation process.
        </span>

        <el-divider> </el-divider>

        <!-- <div class="flex flex-col p-2" v-for="(workflow, key) in dataset.workflows" :key="key">
          <div class="bg-gray-300 px-4 py-2">
            <span class="text-lg">
              {{ combineDataTypes(workflow.type) }}
            </span>
          </div>
          <div class="flex items-center justify-start bg-gray-200 px-4 py-2">
            <button
              class="primary-plain-button"
              @click="navigateToCurate(`${key}`)"
              ref="continueButton"
            >
              Curate {{ combineDataTypes(workflow.type) }}
              <el-icon><arrow-right-bold /></el-icon>
            </button>
            <br />
          </div>
        </div> -->

        <div class="flex w-full flex-col p-2">
          <div
            class="relative my-4 mx-3 flex flex-col rounded-lg border border-zinc-200 px-6 py-4 shadow-md transition-all"
            v-if="codeObject.show"
          >
            <div
              class="absolute top-4 right-5 rounded-xl border-zinc-200 bg-zinc-100 p-2 shadow-sm transition-all hover:shadow-lg"
              @click="codeObject.minimize = !codeObject.minimize"
            >
              <Icon icon="bi:arrows-expand" height="20" />
            </div>

            <div class="flex flex-row items-center pb-2">
              <Icon icon="ant-design:code-filled" height="55" />
              <div class="ml-2 flex w-full flex-col">
                <span class="text-base">
                  {{ codeObject.title }}
                </span>

                <span class="text-sm" v-show="codeObject.name != ''">
                  {{ codeObject.name }}
                </span>
              </div>
            </div>

            <div class="flex justify-start">
              <span class="text-md font-medium text-zinc-600">Summary of progress</span>
            </div>

            <line-divider></line-divider>

            <div
              class="flex flex-col transition-all"
              :class="{ 'max-h-0': codeObject.minimize, 'max-h-screen': !codeObject.minimize }"
            >
              <el-table :data="codeObject.data" stripe style="width: 100%">
                <el-table-column prop="task" label="Task" />
                <el-table-column label="Status">
                  <template #default="scope">
                    <Icon
                      icon="bi:check-circle"
                      class="text-green-500"
                      v-if="
                        scope.row.status !== 'invalid' &&
                        scope.row.status !== '' &&
                        scope.row.status !== false
                      "
                    />
                    <Icon
                      icon="carbon:warning-alt"
                      class="text-yellow-500"
                      v-if="scope.row.status == 'invalid'"
                    />
                    <Icon
                      icon="charm:circle-cross"
                      class="text-orange-500"
                      v-if="scope.row.status == '' || scope.row.status == false"
                    />
                  </template>
                </el-table-column>
                <el-table-column label="Details">
                  <template #default="scope">
                    <span v-if="scope.row.type !== 'doi'">
                      {{ scope.row.detail }}
                    </span>
                    <a
                      v-else
                      :href="`https://doi.org/${scope.row.detail}`"
                      target="_blank"
                      class="text-url"
                      rel="noopener noreferrer"
                    >
                      {{ scope.row.detail }}
                    </a>
                  </template>
                </el-table-column>
              </el-table>
            </div>

            <div class="mt-4 flex items-center justify-end px-2 py-2">
              <button
                class="primary-button"
                @click="navigateToCurate(codeObject.workflowID)"
                ref="continueButton"
              >
                Curate {{ codeObject.title }}
                <el-icon><arrow-right-bold /></el-icon>
              </button>
              <br />
            </div>
          </div>

          <div
            class="relative my-4 mx-3 flex flex-col rounded-lg border border-zinc-200 px-6 py-4 shadow-md transition-all"
            v-if="otherObject.show"
          >
            <div
              class="absolute top-4 right-5 rounded-xl border-zinc-200 bg-zinc-100 p-2 shadow-sm transition-all hover:shadow-lg"
              @click="otherObject.minimize = !otherObject.minimize"
            >
              <Icon icon="bi:arrows-expand" height="20" />
            </div>

            <div class="flex flex-row items-center pb-2">
              <Icon icon="carbon:data-share" height="55" />
              <div class="ml-2 flex w-full flex-col">
                <span class="text-base">
                  {{ otherObject.title }}
                </span>

                <span class="text-sm" v-show="otherObject.name != ''">
                  {{ otherObject.name }}
                </span>
              </div>
            </div>

            <line-divider></line-divider>

            <div
              class="flex flex-col transition-all"
              :class="{ 'max-h-0': otherObject.minimize, 'max-h-screen': !otherObject.minimize }"
            >
              <el-table :data="otherObject.data" stripe style="width: 100%">
                <el-table-column prop="task" label="Task" />
                <el-table-column label="Status">
                  <template #default="scope">
                    <Icon
                      icon="bi:check-circle"
                      class="text-green-500"
                      v-if="
                        scope.row.status !== 'invalid' &&
                        scope.row.status !== '' &&
                        scope.row.status !== false
                      "
                    />
                    <Icon
                      icon="carbon:warning-alt"
                      class="text-yellow-500"
                      v-if="scope.row.status == 'invalid'"
                    />
                    <Icon
                      icon="charm:circle-cross"
                      class="text-orange-500"
                      v-if="scope.row.status == '' || scope.row.status == false"
                    />
                  </template>
                </el-table-column>
                <el-table-column label="Details">
                  <template #default="scope">
                    <span v-if="scope.row.type !== 'doi'">
                      {{ scope.row.detail }}
                    </span>
                    <a
                      v-else
                      :href="`https://doi.org/${scope.row.detail}`"
                      target="_blank"
                      class="text-url"
                      rel="noopener noreferrer"
                    >
                      {{ scope.row.detail }}
                    </a>
                  </template>
                </el-table-column>
              </el-table>
            </div>

            <div class="mt-4 flex items-center justify-end px-2 py-2">
              <button
                class="primary-button"
                @click="navigateToCurate(otherObject.workflowID)"
                ref="continueButton"
              >
                Curate {{ otherObject.title }}
                <el-icon><arrow-right-bold /></el-icon>
              </button>
            </div>
          </div>
        </div>

        <info-confirm
          ref="infoConfirmWorkflowPublished"
          title="Dataset is already published"
          @messageConfirmed="navigateToSelectFolder"
          confirmButtonText="I want to publish a new version"
        >
          <p class="text-center text-base text-gray-500">
            It looks like you've already published this dataset. Would you like to go through this
            workflow again to publish a new version?
          </p>
        </info-confirm>
        <info-confirm
          ref="infoConfirmLocalZenodoUploadNoPublish"
          title="You haven't published this dataset yet"
          @messageConfirmed="localZenodoUploadNoPublishResponse('ok')"
          @messageCancel="localZenodoUploadNoPublishResponse('cancel')"
          confirmButtonText="I want to publish"
          cancelButtonText="I want to upload my data again"
        >
          <p class="text-center text-base text-gray-500">
            It looks like you have already uploaded this dataset to Zenodo but you haven't published
            it yet. Would you like to publish this now or create a new upload for this specific
            workflow?
          </p>
        </info-confirm>
        <info-confirm
          ref="infoConfirmGithubUploadNoPublish"
          title="You haven't published this dataset yet"
          @messageConfirmed="localGithubUploadNoPublishResponse('ok')"
          @messageCancel="localGithubUploadNoPublishResponse('cancel')"
          confirmButtonText="I want to publish"
          cancelButtonText="I want to upload my data again"
        >
          <p class="text-center text-base text-gray-500">
            It looks like you have already uploaded this dataset to GitHub but you haven't published
            it yet. Would you like to publish this now or create a new upload for this specific
            workflow?
          </p>
        </info-confirm>
        <info-confirm
          ref="infoConfirmContinueCuration"
          title="Continue where you left off"
          @messageConfirmed="continueCuration('ok')"
          @messageCancel="continueCuration('cancel')"
          confirmButtonText="Yes, continue"
          cancelButtonText="No, start from the beginning"
        >
          <p class="text-center text-base text-gray-500">
            It looks like you were working on this workflow before. Would you like to continue where
            you left off?
          </p>
        </info-confirm>
      </div>
    </div>
    <app-docs-link url="curate-and-share/your-workflows" position="bottom-4" />
  </div>
</template>

<script>
import { useDatasetsStore } from "@/store/datasets";

import codeLicensesJSON from "@/assets/supplementalFiles/licenses.json";
import otherLicensesJSON from "@/assets/supplementalFiles/otherDataLicenses.json";

import { Icon } from "@iconify/vue";

export default {
  name: "ShowAllWorkflows",
  components: {
    Icon,
  },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      dataset: {},
      currentOptions: {},
      datasetID: this.$route.params.datasetID,
      workflowID: "",
      codeObject: { data: [] },
      otherObject: { data: [] },
      codeLicensesOptions: codeLicensesJSON.licenses,
      otherLicensesOptions: otherLicensesJSON.licenses,
    };
  },
  methods: {
    repoFullName(repoID) {
      switch (repoID) {
        case "figshare":
          return "Figshare";
        case "zenodo":
          return "Zenodo";
        default:
          return repoID;
      }
    },
    getSource(workflowID) {
      const workflow = this.dataset.workflows[workflowID];

      if (workflow.sourceSelected) {
        const source = workflow.source.type;

        if (source === "local") {
          return this.dataset.data[workflow.type[0]].folderPath;
        } else if (source === "github") {
          return `@${workflow.github.repo}`;
        } else {
          return "";
        }
      } else {
        return "";
      }
    },
    getLicenseName(license, type) {
      if (type === "Code") {
        return this.codeLicensesOptions.find((option) => option.licenseId === license).name;
      } else if (type === "Other") {
        return this.otherLicensesOptions.find((option) => option.id === license).title;
      } else {
        return license;
      }
    },
    combineDataTypes(dataTypes) {
      if (dataTypes.length === 1) {
        switch (dataTypes[0]) {
          case "Code":
            return "Research Software";
          case "Other":
            return "Other Data";
          default:
            return dataTypes[0];
        }
      } else if (dataTypes.length === 2) {
        return `${dataTypes[0]} and ${dataTypes[1]}`;
      } else if (dataTypes.length > 2) {
        let returnString = "";
        dataTypes.forEach((type, index) => {
          if (index === dataTypes.length - 1) {
            returnString += `and ${type}`;
          } else {
            returnString += `${type}, `;
          }
        });
        return returnString;
      }
    },
    selectDataPath() {
      // We are assuming one data type per workflow
      const dataType = this.dataset.workflows[this.workflowID].type[0];

      switch (dataType) {
        case "Code":
          return `/datasets/${this.datasetID}/${this.workflowID}/Code/landing`;
        case "Other":
          return `/datasets/${this.datasetID}/${this.workflowID}/Other/selectFolder`;
        default:
          return dataType;
      }
    },
    async navigateToSelectFolder() {
      this.dataset.workflows[this.workflowID].datasetUploaded = false;
      this.dataset.workflows[this.workflowID].datasetPublished = false;

      this.datasetStore.updateCurrentDataset(this.dataset);
      this.datasetStore.syncDatasets();

      const routerPath = this.selectDataPath();
      this.$router.push({ path: routerPath });
    },
    async localZenodoUploadNoPublishResponse(response) {
      let routerPath = "";
      if (response === "ok") {
        routerPath = `/datasets/${this.datasetID}/${this.workflowID}/zenodo/publish`;
        this.$router.push({ path: routerPath });
      } else if (response === "cancel") {
        this.dataset.workflows[this.workflowID].datasetUploaded = false;
        this.dataset.workflows[this.workflowID].datasetPublished = false;

        await this.datasetStore.updateCurrentDataset(this.dataset);
        await this.datasetStore.syncDatasets();

        routerPath = this.selectDataPath();
        this.$router.push({ path: routerPath });
      }
    },
    localGithubUploadNoPublishResponse(response) {
      let routerPath = "";
      if (response === "ok") {
        routerPath = `/datasets/${this.datasetID}/${this.workflowID}/github/publish`;
        this.$router.push({ path: routerPath });
      } else if (response === "cancel") {
        routerPath = this.selectDataPath();
        this.$router.push({ path: routerPath });
      }
    },
    continueCuration(response) {
      let routerPath = "";
      if (response === "ok") {
        routerPath = this.dataset.workflows[this.workflowID].currentRoute;
        this.$router.push({ path: routerPath });
      } else if (response === "cancel") {
        routerPath = this.selectDataPath();
        this.$router.push({ path: routerPath });
      }
    },
    navigateToCurate(workflowID) {
      let routerPath = "";
      this.workflowID = workflowID;

      // Function to reset on data types. Will have to see if this needs to be moved into a utility function
      if (this.dataset.workflows[workflowID].type[0] !== "Other") {
        this.dataset.workflows[workflowID].generateOtherMetadata = false;
      }
      if (this.dataset.workflows[workflowID].type[0] !== "Code") {
        this.dataset.workflows[workflowID].generateCodeMeta = false;
      }

      if (
        "datasetPublished" in this.dataset.workflows[workflowID] &&
        this.dataset.workflows[workflowID].datasetPublished &&
        "source" in this.dataset.workflows[workflowID] &&
        (this.dataset.workflows[workflowID].source.type === "local" ||
          this.dataset.workflows[workflowID].source.type === "github")
      ) {
        this.$refs.infoConfirmWorkflowPublished.show();
        return;
      }

      if (
        "datasetUploaded" in this.dataset.workflows[workflowID] &&
        this.dataset.workflows[workflowID].datasetUploaded &&
        "source" in this.dataset.workflows[workflowID] &&
        this.dataset.workflows[workflowID].source.type === "local"
      ) {
        this.$refs.infoConfirmLocalZenodoUploadNoPublish.show();
        return;
      }

      if (
        "datasetUploaded" in this.dataset.workflows[workflowID] &&
        this.dataset.workflows[workflowID].datasetUploaded &&
        "source" in this.dataset.workflows[workflowID] &&
        this.dataset.workflows[workflowID].source.type === "github"
      ) {
        this.$refs.infoConfirmGithubUploadNoPublish.show();
        return;
      }

      if ("currentRoute" in this.dataset.workflows[workflowID]) {
        if (
          this.dataset.workflows[workflowID].currentRoute != "" &&
          this.dataset.workflows[workflowID].currentRoute != this.selectDataPath()
        ) {
          this.$refs.infoConfirmContinueCuration.show();
        } else {
          routerPath = this.selectDataPath();
          this.$router.push({ path: routerPath });
        }
      } else {
        routerPath = this.selectDataPath();
        this.$router.push({ path: routerPath });
      }
    },
    generateCodeObject() {
      this.codeObject.show = false;
      this.codeObject.minimize = false;

      const allWorkflows = Object.keys(this.dataset.workflows);

      const codeWorkflowPresent = allWorkflows.some(
        (workflow) => this.dataset.workflows[workflow].type[0] === "Code"
      );

      if (!codeWorkflowPresent) {
        return;
      }

      const workflowID = allWorkflows.find(
        (workflow) => this.dataset.workflows[workflow].type[0] === "Code"
      );

      this.codeObject.workflowID = workflowID;

      const workflow = this.dataset.workflows[workflowID];

      let codeMetadata = {};

      if ("Code" in this.dataset.data) {
        codeMetadata = this.dataset.data.Code;
      }

      this.codeObject.data = [];

      this.codeObject.show = true;
      this.codeObject.title = "Research Software";
      if ("name" in this.dataset.data.Code.questions) {
        this.codeObject.name = this.dataset.data.Code.questions.name;
      }

      this.codeObject.data.push({
        status: this.getSource(workflowID),
        task: "Select data files",
        detail: this.getSource(workflowID),
        type: "",
      });

      if ("standards" in codeMetadata) {
        let invalid = false;
        for (let question of Object.keys(codeMetadata.standards)) {
          if (codeMetadata.standards[question] !== "Yes") {
            invalid = true;
          }
        }
        if (invalid) {
          this.codeObject.data.push({
            status: "invalid",
            task: "Review standards",
            detail: "Not all standards have been met",
            type: "standards",
          });
        } else {
          this.codeObject.data.push({
            status: true,
            task: "Review standards",
            detail: "All standards met",
            type: "standards",
          });
        }
      } else {
        this.codeObject.data.push({
          status: false,
          task: "Review standards",
          detail: "None provided",
          type: "standards",
        });
      }

      let generateStatus = "";

      if (workflow.generateCodeMeta) {
        generateStatus = true;
      } else {
        generateStatus = false;
      }
      this.codeObject.data.push({
        status: generateStatus,
        task: "Provide metadata",
        detail: "codemeta.json | CITATION.cff",
        type: "",
      });

      let license = "";

      if ("license" in this.dataset.data.Code.questions) {
        license = this.getLicenseName(this.dataset.data.Code.questions.license, "Code");
      } else {
        license = "";
      }
      this.codeObject.data.push({
        status: license,
        task: "Select a license",
        detail: license,
        type: "",
      });

      let destination = "";
      if (
        "uploadToRepo" in workflow &&
        "destination" in workflow &&
        "name" in workflow.destination
      ) {
        destination = this.repoFullName(workflow.destination.name);
      } else {
        destination = "";
      }
      this.codeObject.data.push({
        status: destination,
        task: "Select repository",
        detail: destination,
        type: "",
      });

      if (workflow.datasetUploaded) {
        generateStatus = true;
      } else {
        generateStatus = false;
      }
      this.codeObject.data.push({
        status: generateStatus,
        task: "Upload dataset",
        detail: "",
        type: "",
      });

      if (workflow.datasetPublished) {
        generateStatus = true;
      } else {
        generateStatus = false;
      }
      this.codeObject.data.push({
        status: generateStatus,
        task: "Publish dataset",
        detail: "",
        type: "",
      });

      let doi = "";
      if (
        "destination" in workflow &&
        "name" in workflow.destination &&
        workflow.destination[workflow.destination.name] != null &&
        workflow.destination[workflow.destination.name] != undefined &&
        "doi" in workflow.destination[workflow.destination.name]
      ) {
        doi = workflow.destination[workflow.destination.name].doi;
      } else {
        doi = "";
      }
      this.codeObject.data.push({
        status: doi,
        task: "Last generated DOI",
        detail: doi,
        type: "doi",
      });
    },
    generateOtherObject() {
      this.otherObject.show = false;
      this.otherObject.minimize = false;

      const allWorkflows = Object.keys(this.dataset.workflows);

      const otherWorkflowPresent = allWorkflows.some(
        (workflow) => this.dataset.workflows[workflow].type[0] === "Other"
      );

      if (!otherWorkflowPresent) {
        return;
      }

      const workflowID = allWorkflows.find(
        (workflow) => this.dataset.workflows[workflow].type[0] === "Other"
      );

      this.otherObject.workflowID = workflowID;

      const workflow = this.dataset.workflows[workflowID];

      let otherMetadata = {};

      if ("Other" in this.dataset.data) {
        otherMetadata = this.dataset.data.Other;
      }

      this.otherObject.data = [];

      this.otherObject.show = true;
      this.otherObject.title = "Other Data";
      if ("name" in this.dataset.data.Other.questions) {
        this.otherObject.name = this.dataset.data.Other.questions.name;
      }

      this.otherObject.data.push({
        status: this.getSource(workflowID),
        task: "Source",
        detail: this.getSource(workflowID),
        type: "",
      });

      if ("standards" in otherMetadata) {
        let invalid = false;
        for (let question of Object.keys(otherMetadata.standards)) {
          if (otherMetadata.standards[question] !== "Yes") {
            invalid = true;
          }
        }
        if (invalid) {
          this.otherObject.data.push({
            status: "invalid",
            task: "Review standards",
            detail: "Not all standards have been met",
            type: "standards",
          });
        } else {
          this.otherObject.data.push({
            status: true,
            task: "Review standards",
            detail: "All standards met",
            type: "standards",
          });
        }
      } else {
        this.otherObject.data.push({
          status: false,
          task: "Review standards",
          detail: "None provided",
          type: "standards",
        });
      }

      let generateStatus = "";

      if (workflow.generateOtherMetadata) {
        generateStatus = true;
      } else {
        generateStatus = false;
      }
      this.otherObject.data.push({
        status: generateStatus,
        task: "Metadata",
        detail: "metadata.json",
        type: "",
      });

      let license = "";

      if ("license" in this.dataset.data.Other.questions) {
        license = this.getLicenseName(this.dataset.data.Other.questions.license, "Other");
      } else {
        license = "";
      }
      this.otherObject.data.push({
        status: license,
        task: "License",
        detail: license,
        type: "",
      });

      let destination = "";
      if (
        "uploadToRepo" in workflow &&
        "destination" in workflow &&
        "name" in workflow.destination
      ) {
        destination = this.repoFullName(workflow.destination.name);
      } else {
        destination = "";
      }
      this.otherObject.data.push({
        status: destination,
        task: "Destination",
        detail: destination,
        type: "",
      });

      if (workflow.datasetUploaded) {
        generateStatus = true;
      } else {
        generateStatus = false;
      }
      this.otherObject.data.push({
        status: generateStatus,
        task: "Uploaded",
        detail: "",
        type: "",
      });

      if (workflow.datasetPublished) {
        generateStatus = true;
      } else {
        generateStatus = false;
      }
      this.otherObject.data.push({
        status: generateStatus,
        task: "Published",
        detail: "",
        type: "",
      });

      let doi = "";
      if (
        "destination" in workflow &&
        "name" in workflow.destination &&
        workflow.destination[workflow.destination.name] != null &&
        workflow.destination[workflow.destination.name] != undefined &&
        "doi" in workflow.destination[workflow.destination.name]
      ) {
        doi = workflow.destination[workflow.destination.name].doi;
      } else {
        doi = "";
      }
      this.otherObject.data.push({
        status: doi,
        task: "Last generated DOI",
        detail: doi,
        type: "doi",
      });
    },
    generateStatusObjects() {
      this.generateCodeObject();
      this.generateOtherObject();
    },
  },

  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();

    this.datasetStore.hideProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(1);

    this.generateStatusObjects();

    if (!this.dataset.workflowConfirmed) {
      this.$router.push({ path: `/datasets/new/${this.dataset.id}/confirm` });
    }

    // this.navigateToCurate("workflow1");
  },
};
</script>
