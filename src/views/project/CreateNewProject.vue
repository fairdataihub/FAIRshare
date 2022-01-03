<template>
  <div
    class="h-full w-full flex flex-col justify-center items-center p-3 px-5 max-w-screen-lg"
  >
    <div class="flex flex-col h-full w-full">
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
                hide-after="0"
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
                      <monitor class="h-12 w-12"></monitor>
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
                hide-after="0"
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
                      <Icon icon="mdi:virus-outline" class="h-12 w-12" />
                      <span class="text-sm">Immunology</span>
                    </div>
                  </el-checkbox>
                </template>
              </el-popover>

              <el-popover
                placement="bottom"
                hide-after="0"
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
                        class="h-12 w-12"
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
                hide-after="0"
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
                      <Icon icon="uil:dna" class="h-12 w-12" />
                      <span class="text-sm">Genomic</span>
                    </div>
                  </el-checkbox>
                </template>
              </el-popover>

              <el-popover
                placement="top"
                hide-after="0"
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
                      <document class="h-12 w-12"></document>
                      <span class="text-sm">Document</span>
                    </div>
                  </el-checkbox>
                </template>
              </el-popover>

              <el-popover
                placement="top"
                hide-after="0"
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
                      <video-play class="h-12 w-12"></video-play>
                      <span class="text-sm">Media</span>
                    </div>
                  </el-checkbox>
                </template>
              </el-popover>
            </div>
          </el-checkbox-group>
        </el-form-item>

        <div class="py-2 flex flex-row justify-center space-x-4">
          <button class="danger-plain-button" @click="cancelNewDataset">
            <el-icon><d-arrow-left /></el-icon> Cancel
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
      hovering: [false, false, false, false, false, false],
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

          let dataset = {
            id: datasetID,
            image: datasetImage,
            name: this.datasetForm.datasetName,
            description: this.datasetForm.datasetDescription,
            dataType: this.datasetForm.dataType,
            data: {},
            workflowConfirmed: false,
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
  @apply gap-8 pt-4 flex flex-col box-border items-center justify-center;
}
.single-check-box {
  @apply transition-all flex justify-center items-center w-40 h-40;
}

.createNewProjectFormItemContainer .el-checkbox.is-bordered.is-checked {
  @apply border-secondary-500 shadow-md shadow-secondary-500/50;
}

.single-check-box:not(.is-disabled):hover {
  @apply border-secondary-500 shadow-lg shadow-secondary-500/50;
}

.createNewProjectFormItemContainer .el-form-item__error {
  @apply w-full flex justify-center;
}
</style>
