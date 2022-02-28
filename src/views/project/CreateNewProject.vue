<template>
  <div
    class="flex h-full w-full max-w-screen-lg flex-col items-center justify-center p-3 px-5"
  >
    <div class="flex h-full w-full flex-col">
      <span class="font-medium"> Start a new data curation project </span>
      <span> Fill out some general details about your dataset here. </span>

      <el-divider> </el-divider>

      <el-form
        ref="datasetForm"
        :model="datasetForm"
        label-width="150px"
        @submit.prevent
        :rules="rules"
        label-position="top"
      >
        <el-form-item label="Project name" prop="datasetName">
          <el-input v-model="datasetForm.datasetName"></el-input>
        </el-form-item>

        <el-form-item label="Project description">
          <el-popover
            ref="popover"
            placement="bottom"
            :width="300"
            trigger="manual"
          >
            <template #reference>
              <el-input
                v-model="datasetForm.datasetDescription"
                type="textarea"
              ></el-input>
            </template>

            <span class="break-normal text-left text-sm">
              Use a description that is easily identifiable. This will be shown
              in the dataset selection screen and is not part of your submitted
              metadata.
            </span>
          </el-popover>
        </el-form-item>

        <el-form-item
          label="Data type"
          prop="dataType"
          class="createNewProjectFormItemContainer"
        >
          <el-checkbox-group
            v-model="datasetForm.dataType"
            class="checkbox-group"
          >
            <div class="flex gap-8">
              <el-popover
                placement="bottom"
                title=""
                :width="400"
                :hide-after="0"
                trigger="hover"
              >
                <template #reference>
                  <el-checkbox
                    border
                    name="type1"
                    class="single-check-box"
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
                  Computational code, scripts, models, notebooks, code
                  libraries, etc.
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
                    label="Immunology"
                    disabled
                  >
                    <div class="flex flex-col items-center">
                      <Icon icon="mdi:virus-outline" class="my-2 h-12 w-12" />
                      <span class="text-sm">Immunology</span>
                    </div>
                  </el-checkbox>
                </template>
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
                      <Icon
                        icon="healthicons:virus-patient-outline"
                        class="my-2 h-12 w-12"
                      />
                      <span class="text-sm">Epidemiology</span>
                    </div>
                  </el-checkbox>
                </template>
              </el-popover>
            </div>

            <div class="flex gap-8">
              <el-popover
                placement="top"
                :hide-after="0"
                trigger="hover"
                content="Coming soon..."
              >
                <template #reference>
                  <el-checkbox
                    border
                    name="type"
                    class="single-check-box"
                    label="Genomic"
                    disabled
                  >
                    <div class="flex flex-col items-center">
                      <Icon icon="uil:dna" class="my-2 h-12 w-12" />
                      <span class="text-sm">Genomic</span>
                    </div>
                  </el-checkbox>
                </template>
              </el-popover>

              <el-popover
                placement="top"
                :hide-after="0"
                trigger="hover"
                content="Coming soon..."
              >
                <template #reference>
                  <el-checkbox
                    border
                    name="type"
                    class="single-check-box"
                    label="Document"
                    disabled
                  >
                    <div class="flex flex-col items-center">
                      <document-icon class="my-2 h-12 w-12" />
                      <span class="text-sm">Document</span>
                    </div>
                  </el-checkbox>
                </template>
              </el-popover>

              <el-popover
                placement="top"
                :hide-after="0"
                trigger="hover"
                content="Coming soon..."
              >
                <template #reference>
                  <el-checkbox
                    border
                    name="type"
                    class="single-check-box"
                    label="Media"
                    disabled
                  >
                    <div class="flex flex-col items-center">
                      <video-play class="my-2 h-12 w-12"></video-play>
                      <span class="text-sm">Media</span>
                    </div>
                  </el-checkbox>
                </template>
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
      },
      rules: {
        datasetName: [
          {
            required: true,
            message: "Please provide a project name",
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

          console.log("dataset: ", dataset);

          dataset.data.general = {
            questions: {},
          };

          for (const type of dataset.dataType) {
            let tempType = type;
            console.log(type);
            if (tempType == "Research software") {
              tempType = "Code";
            }
            dataset.data[tempType] = {
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

          this.$router.push({ path: `/datasets/new/${datasetID}/confirm` });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    cancelNewDataset() {
      this.$router.push({ name: "ShowAllProjects" });
    },
  },
  mounted() {
    document
      .querySelectorAll(
        ".createNewProjectFormItemContainer .el-checkbox__label"
      )
      .forEach((el) => {
        el.style.paddingLeft = "0px";
      });

    document
      .querySelectorAll(".createNewProjectFormItemContainer .el-checkbox")
      .forEach((el) => {
        el.style.display = "flex";
        el.style.flexDirection = "column-reverse";
        el.style.gap = "2px";
      });
    document
      .querySelectorAll(
        ".createNewProjectFormItemContainer .el-checkbox__input"
      )
      .forEach((el) => {
        el.style.display = "none";
      });

    document
      .querySelectorAll(
        ".createNewProjectFormItemContainer .el-checkbox.is-bordered"
      )
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

    document
      .querySelectorAll(".createNewProjectFormItemContainer .el-checkbox")
      .forEach((el) => {
        el.style.marginRight = "0px";
        el.style.setProperty("--el-checkbox-checked-text-color", "#f97316");
      });

    document
      .querySelectorAll(
        ".createNewProjectFormItemContainer .el-form-item__content"
      )
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
  @apply box-border flex flex-col items-center justify-center gap-8 pt-4;
}
.single-check-box {
  @apply flex h-40 w-40 items-center justify-center shadow-md transition-all;
}

.createNewProjectFormItemContainer .el-checkbox.is-bordered.is-checked {
  @apply border-secondary-500 shadow-md shadow-secondary-500/50;
}

.single-check-box:not(.is-disabled):hover {
  @apply border-secondary-500 shadow-lg shadow-secondary-500/50;
}
</style>
