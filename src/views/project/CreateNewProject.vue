<template>
  <div class="flex h-full w-full max-w-screen-lg flex-col items-center justify-center p-3 px-5">
    <div class="flex h-full w-full flex-col">
      <span class="text-lg font-medium"> Start a new data curation project </span>
      <span>
        Fill out some general details about your project here. These fields will be primarily used
        to identify your project.
      </span>

      <line-divider />

      <el-form
        ref="datasetForm"
        :model="datasetForm"
        label-width="150px"
        @submit.prevent
        :rules="rules"
        label-position="top"
      >
        <el-form-item label="Project name" prop="datasetName">
          <el-input v-model="datasetForm.datasetName" size="large"></el-input>
        </el-form-item>

        <el-form-item label="Project description" prop="datasetDescription">
          <el-input
            v-model="datasetForm.datasetDescription"
            type="textarea"
            :autosize="{ minRows: 3, maxRows: 5 }"
          ></el-input>

          <span class="mt-1 text-left text-xs text-slate-500">
            Use a description that is easily identifiable. This will be shown in the dataset
            selection screen and is not part of your submitted metadata.
          </span>
        </el-form-item>

        <el-form-item label="Data type" prop="dataType" class="createNewProjectFormItemContainer">
          <el-checkbox-group v-model="datasetForm.dataType" class="checkbox-group">
            <div class="flex gap-8 transition-all">
              <el-popover placement="bottom" title="" :width="400" :hide-after="0" trigger="hover">
                <template #reference>
                  <el-checkbox
                    border
                    name="type"
                    class="single-check-box transition-all"
                    label="Research software"
                  >
                    <div class="flex flex-col items-center">
                      <Icon icon="bx:bx-code-block" class="my-2 h-12 w-12" />
                      <span class="text-sm">Research</span>
                      <span class="text-sm">software</span>
                    </div>
                  </el-checkbox>
                </template>

                <span class="break-normal text-left text-sm">
                  Computational code, scripts, models, notebooks, code libraries, etc.
                </span>
              </el-popover>

              <el-popover placement="bottom" :width="400" :hide-after="0" trigger="hover">
                <template #reference>
                  <el-checkbox border name="type" class="single-check-box" label="Immunology">
                    <div class="flex flex-col items-center">
                      <Icon icon="mdi:virus-outline" class="my-2 h-12 w-12" />
                      <span class="text-sm">Immunology</span>
                    </div>
                  </el-checkbox>
                </template>

                <span class="break-normal text-left text-sm">
                  Immunology-related research, assay methods, etc.
                </span>
              </el-popover>

              <el-popover
                placement="bottom"
                :hide-after="0"
                trigger="hover"
                content="Coming soon..."
              >
                <template #reference>
                  <el-checkbox
                    border
                    name="type"
                    class="single-check-box"
                    label="Epidemiology"
                    disabled
                  >
                    <div class="flex flex-col items-center">
                      <Icon icon="healthicons:virus-patient-outline" class="my-2 h-12 w-12" />
                      <span class="text-sm">Epidemiology</span>
                    </div>
                  </el-checkbox>
                </template>
              </el-popover>
            </div>

            <div class="flex gap-8">
              <el-popover placement="top" :hide-after="0" trigger="hover" content="Coming soon...">
                <template #reference>
                  <el-checkbox
                    border
                    name="type"
                    class="single-check-box"
                    label="NextGenHighThroughputSequencing"
                  >
                    <div class="flex flex-col items-center">
                      <Icon icon="uil:dna" class="my-2 h-12 w-12" />
                      <span class="text-sm">Genomic</span>
                    </div>
                  </el-checkbox>
                </template>
                <!-- <span class="break-normal text-left text-sm">
                  Next generation high-throughput sequencing data, such as Illumina or PacBio.
                </span> -->
              </el-popover>

              <el-popover placement="top" :hide-after="0" trigger="hover" content="Coming soon...">
                <template #reference>
                  <el-checkbox
                    border
                    name="type"
                    class="single-check-box"
                    label="Document"
                    disabled
                  >
                    <div class="flex flex-col items-center">
                      <video-play class="my-2 h-12 w-12"></video-play>
                      <span class="text-sm">Media</span>
                    </div>
                  </el-checkbox>
                </template>
              </el-popover>

              <el-popover placement="top" :hide-after="0" trigger="hover" content="Coming soon...">
                <template #reference>
                  <el-checkbox border name="type" class="single-check-box" label="Other" disabled>
                    <div class="flex flex-col items-center">
                      <document-icon class="my-2 h-12 w-12"></document-icon>
                      <span class="text-sm">Other</span>
                    </div>
                  </el-checkbox>
                </template>
              </el-popover>

              <!-- <el-popover placement="top" :hide-after="0" trigger="hover" :width="400">
                <template #reference>
                  <el-checkbox border name="type" class="single-check-box" label="Other">
                    <div class="flex flex-col items-center">
                      <document-icon class="my-2 h-12 w-12"></document-icon>
                      <span class="text-sm">Other</span>
                    </div>
                  </el-checkbox>
                </template>
                <span class="break-normal text-left text-sm">
                  Any type of data that is not covered by the other categories.
                </span>
              </el-popover> -->
            </div>
          </el-checkbox-group>
        </el-form-item>

        <el-form-item
          label="Immunology Data Type"
          prop="immunologyDataTypes"
          class="createNewProjectFormItemContainer"
          v-show="datasetForm.dataType.includes('Immunology')"
        >
          <el-checkbox-group v-model="datasetForm.immunologyDataTypes" class="checkbox-group">
            <div class="flex gap-8 transition-all">
              <el-popover placement="bottom" title="" :width="400" :hide-after="0" trigger="hover">
                <template #reference>
                  <el-checkbox
                    border
                    name="type"
                    class="single-check-box transition-all"
                    label="FlowCytometry"
                  >
                    <div class="flex flex-col items-center">
                      <Icon icon="entypo:lab-flask" class="my-2 h-12 w-12" />
                      <span class="text-sm">Flow</span>
                      <span class="text-sm">Cytometry</span>
                    </div>
                  </el-checkbox>
                </template>

                <span class="break-normal text-left text-sm">
                  Flow cytometry data, such as FCS files.
                </span>
              </el-popover>

              <el-popover placement="bottom" title="" :width="400" :hide-after="0" trigger="hover">
                <template #reference>
                  <el-checkbox
                    border
                    name="type"
                    class="single-check-box transition-all"
                    label="RNASequencing"
                  >
                    <div class="flex flex-col items-center">
                      <Icon icon="fluent-emoji-high-contrast:worm" class="my-2 h-12 w-12" />
                      <span class="text-sm">RNA</span>
                      <span class="text-sm">Sequencing</span>
                    </div>
                  </el-checkbox>
                </template>

                <span class="break-normal text-left text-sm">
                  RNA sequencing data, such as FASTQ files.
                </span>
              </el-popover>

              <el-popover placement="bottom" title="" :width="400" :hide-after="0" trigger="hover">
                <template #reference>
                  <el-checkbox
                    border
                    name="type"
                    class="single-check-box transition-all"
                    label="ELISA"
                  >
                    <div class="flex flex-col items-center">
                      <Icon icon="raphael:lab" class="my-2 h-12 w-12" />
                      <span class="text-sm">ELISA</span>
                    </div>
                  </el-checkbox>
                </template>

                <span class="break-normal text-left text-sm">
                  ELISA data, such as raw data files.
                </span>
              </el-popover>

              <el-popover placement="bottom" title="" :width="400" :hide-after="0" trigger="hover">
                <template #reference>
                  <el-checkbox
                    border
                    name="type"
                    class="single-check-box transition-all"
                    label="CyTOF"
                  >
                    <div class="flex flex-col items-center">
                      <Icon icon="codicon:graph-scatter" class="my-2 h-12 w-12" />
                      <span class="text-sm">CyTOF</span>
                    </div>
                  </el-checkbox>
                </template>

                <span class="break-normal text-left text-sm">
                  CyTOF data, such as raw data files.
                </span>
              </el-popover>
            </div>
          </el-checkbox-group>
        </el-form-item>

        <div class="flex flex-row justify-center space-x-4 py-4">
          <button class="danger-plain-button" @click="cancelNewDataset">
            <el-icon><circle-close-filled /></el-icon> Cancel
          </button>

          <button class="primary-button" @click="submitForm('datasetForm')">
            Create new project <el-icon><d-arrow-right /></el-icon>
          </button>
        </div>
      </el-form>
    </div>
    <app-docs-link url="curate-and-share/projects/create-new-project" position="bottom-4" />
  </div>
</template>

<script>
import { useDatasetsStore } from "@/store/datasets";
import { v4 as uuidv4 } from "uuid";
import { ElNotification } from "element-plus";
import { Icon } from "@iconify/vue";

export default {
  name: "CreateNewProject",
  components: {
    Icon,
  },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      datasetForm: {
        datasetName: "",
        datasetDescription: "",
        dataType: [],
        immunologyDataTypes: [],
      },
      rules: {
        datasetName: [
          {
            required: true,
            message: "Please provide a project name",
            trigger: "blur",
          },
        ],
        datasetDescription: [
          {
            required: true,
            message: "Please provide a project description",
            trigger: "blur",
          },
        ],
        dataType: [
          {
            type: "array",
            required: true,
            message: "Please select at least one data type",
            trigger: "change",
          },
        ],
        immunologyDataTypes: [
          {
            type: "array",
            validator: this.validateImmunoDataTypes,
            trigger: "change",
          },
        ],
      },
    };
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          const datasetID = uuidv4();
          const datasetImage = `https://avatars.dicebear.com/api/jdenticon/${uuidv4()}.svg`;

          const index = this.datasetForm.dataType.indexOf("Research software");

          if (index !== -1) {
            this.datasetForm.dataType[index] = "Code";
          }

          const now = new Date();

          let dataset = {
            id: datasetID,
            image: datasetImage,
            name: this.datasetForm.datasetName.trim(),
            description: this.datasetForm.datasetDescription.trim(),
            dataType: this.datasetForm.dataType,
            immunologyDataTypes: this.datasetForm.immunologyDataTypes,
            data: {},
            workflowConfirmed: false,
            meta: {
              dateCreated: now,
              dateModified: now,
              location: "Unknown",
              locationPath: "Unknown",
              destination: "Unknown",
            },
          };

          dataset.data.general = {
            questions: {},
          };

          for (const type of dataset.dataType) {
            let tempType = type;
            if (tempType == "Research software") {
              tempType = "Code";
            }
            dataset.data[tempType] = {
              uploaded: false,
              questions: {},
            };
          }

          for (const type of dataset.immunologyDataTypes) {
            dataset.data[type] = {
              uploaded: false,
              questions: {},
            };
          }

          this.datasetStore.addDataset(dataset, datasetID);

          ElNotification({
            type: "success",
            message: "Created your new project!",
            position: "bottom-right",
            duration: 3000,
          });

          this.$track("Projects", "Create new project", "success");

          this.$router.push({ path: `/datasets/new/${datasetID}/confirm` });
        } else {
          this.$track("Projects", "Create new project", "failed");

          console.error("Invalid form entries");
          return false;
        }
      });
    },
    validateImmunoDataTypes(_rule, value, callback) {
      if (this.datasetForm.dataType.includes("Immunology")) {
        if (value.length === 0) {
          callback(new Error("Please select at least one immunology data type"));
        } else {
          callback();
        }
      } else {
        callback();
      }
    },
    cancelNewDataset() {
      this.$router.push({ name: "ShowAllProjects" });
    },
  },
  mounted() {
    document
      .querySelectorAll(".createNewProjectFormItemContainer .el-checkbox__label")
      .forEach((el) => {
        el.style.paddingLeft = "0px";
      });

    document.querySelectorAll(".createNewProjectFormItemContainer .el-checkbox").forEach((el) => {
      el.style.display = "flex";
      el.style.flexDirection = "column-reverse";
      el.style.gap = "2px";
    });
    document
      .querySelectorAll(".createNewProjectFormItemContainer .el-checkbox__input")
      .forEach((el) => {
        el.style.display = "none";
      });

    document
      .querySelectorAll(".createNewProjectFormItemContainer .el-checkbox.is-bordered")
      .forEach((el) => {
        el.style.padding = "0px";
      });

    document
      .querySelectorAll(
        ".createNewProjectFormItemContainer .el-checkbox.is-bordered+.el-checkbox.is-bordered"
      )
      .forEach((el) => {
        el.style.marginLeft = "0px";
      });

    document.querySelectorAll(".createNewProjectFormItemContainer .el-checkbox").forEach((el) => {
      el.style.marginRight = "0px";
      el.style.setProperty("--el-checkbox-checked-text-color", "#f97316");
    });

    document
      .querySelectorAll(".createNewProjectFormItemContainer .el-form-item__content")
      .forEach((el) => {
        el.style.marginRight = "0px";
        el.style.setProperty("justify-content", "center");
        el.style.setProperty("align-items", "center");
      });
  },
};
</script>
<style scoped>
.checkbox-group {
  @apply box-border flex flex-col items-center justify-center gap-8 pt-4 transition-all;
}
.single-check-box {
  @apply flex h-40 w-40 items-center justify-center shadow-md transition-all;
}

.createNewProjectFormItemContainer .el-checkbox.is-bordered.is-checked {
  @apply border-secondary-500 shadow-md shadow-secondary-500/50 transition-all;
}

.single-check-box:not(.is-disabled):hover {
  @apply border-secondary-500 shadow-lg shadow-secondary-500/50 transition-all;
}
</style>
