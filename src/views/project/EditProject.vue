<template>
  <div class="h-full w-full flex flex-col justify-center items-center p-3 px-5">
    <div class="flex flex-col h-full w-full">
      <el-page-header @back="goBack" class="text-lg">
        <template #content>
          <p>
            Project settings -
            <span class="text-sm">
              Update your project name, description and other settings
            </span>
          </p>
        </template>
      </el-page-header>

      <span class="hidden">
        Update your project name, description and other settings.
      </span>

      <el-divider> </el-divider>

      <el-form
        ref="datasetForm"
        :model="datasetForm"
        label-width="150px"
        @submit.prevent
        :rules="rules"
      >
        <el-form-item label="Dataset name" prop="datasetName">
          <el-input v-model="datasetForm.datasetName"></el-input>
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
                v-model="datasetForm.datasetDescription"
                type="textarea"
                autosize
              ></el-input>
            </template>

            <span class="break-normal text-left text-sm">
              Use a description that is easily identifiable. This will be shown
              in the dataset selection screen and is not part of your submitted
              metadata.
            </span>
          </el-popover>
        </el-form-item>

        <!-- <el-form-item label="Data type" prop="dataType" >
            <el-checkbox-group v-model="datasetForm.dataType" class="p-0">
              <el-checkbox label="Code" name="type"></el-checkbox>

              <el-tooltip
                class="item"
                effect="dark"
                content="Coming soon..."
                placement="top-end"
              >
                <el-checkbox
                  label="Publications"
                  name="type"
                  disabled
                ></el-checkbox>
              </el-tooltip>

              <el-tooltip
                class="item"
                effect="dark"
                content="Coming soon..."
                placement="top-end"
              >
                <el-checkbox label="Images" name="type" disabled></el-checkbox>
              </el-tooltip>

              <el-tooltip
                class="item"
                effect="dark"
                content="Coming soon..."
                placement="top-end"
              >
                <el-checkbox
                  label="Genomic Data"
                  name="type"
                  disabled
                ></el-checkbox>
              </el-tooltip>
            </el-checkbox-group>
          </el-form-item> -->

        <el-form-item label="Delete project">
          <span>
            Once you delete a project, there is no going back. Please be
            certain.
          </span>

          <br />

          <button class="danger-button py-0" @click="deleteDataset">
            <el-icon><delete /></el-icon> Delete project
          </button>
        </el-form-item>
      </el-form>
      <div class="py-2 flex flex-row justify-center space-x-4">
        <button class="danger-plain-button" @click="goBack">
          <el-icon><circle-close-filled /></el-icon> Cancel
        </button>
        <button class="primary-button" @click="submitForm('datasetForm')">
          Save changes <el-icon><circle-check-filled /></el-icon>
        </button>
      </div>
      <div class="py-2 flex flex-row justify-center space-x-4 hidden">
        <button class="primary-plain-button">
          Test button <el-icon><circle-check-filled /></el-icon>
        </button>
        <button class="secondary-plain-button">
          Test button <el-icon><circle-check-filled /></el-icon>
        </button>
        <button class="danger-plain-button">
          Test button <el-icon><circle-check-filled /></el-icon>
        </button>
        <button class="primary-button">
          Test button <el-icon><circle-check-filled /></el-icon>
        </button>
        <button class="danger-button">
          Test button <el-icon><circle-check-filled /></el-icon>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ElMessageBox, ElMessage } from "element-plus";

import { useDatasetsStore } from "../../store/datasets";

export default {
  name: "EditProject",

  data() {
    return {
      datasetStore: useDatasetsStore(),
      datasetID: this.$route.params.datasetID,
      dataset: {},
      datasetForm: {
        datasetName: "",
        datasetDescription: "",
        // dataType: [],
      },
      originalName: "",
      deleteDisabled: false,
      rules: {
        datasetName: [
          {
            required: true,
            message: "Please type a dataset name",
            trigger: "blur",
          },
        ],
        // dataType: [
        //   {
        //     type: "array",
        //     required: true,
        //     message: "Please select at least one data type",
        //     trigger: "change",
        //   },
        // ],
      },
    };
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.dataset.name = this.datasetForm.datasetName;
          this.originalName = this.datasetForm.datasetName;
          this.dataset.description = this.datasetForm.datasetDescription;

          this.datasetStore.updateCurrentDataset(this.dataset);
          this.datasetStore.syncDatasets();

          //   dataset.data.general = {
          //     questions: {},
          //   };

          //   for (const type of dataset.dataType) {
          //     dataset.data[type] = {
          //       uploaded: false,
          //       questions: {},
          //     };
          //   }

          //   this.datasetStore.addDataset(dataset, datasetID);

          this.$router.push({ name: "ShowAllProjects" });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    goBack() {
      this.$router.push({ name: "ShowAllProjects" });
    },
    deleteDataset() {
      ElMessageBox.prompt(
        `This action cannot be undone. This will permanently delete the project.
        <br />
        Please type <strong> ${this.originalName} </strong> to confirm.`,
        "Are you absolutely sure?",
        {
          showCancelButton: false,
          type: "warning",
          confirmButtonText:
            "I understand the consequences, delete this project",
          confirmButtonClass:
            "danger-plain-button plain danger border-red-500 --el-button-hover-border-color='#fff'",
          dangerouslyUseHTMLString: true,
          inputValidator: (value) => {
            if (value === this.originalName) {
              return true;
            }
            return "Please type the project name correctly";
          },
        }
      )
        .then(async ({ value }) => {
          console.log(value);

          await this.datasetStore.deleteDataset(this.datasetID);

          ElMessage({
            type: "success",
            message: `Project ${value} deleted.`,
          });

          this.goBack();
        })
        .catch(() => {});
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();

    this.datasetStore.hideProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(1);

    this.datasetForm.datasetName = this.dataset.name;
    this.originalName = this.dataset.name;
    this.datasetForm.datasetDescription = this.dataset.description;
    // this.datasetForm.dataType = this.dataset.dataType;
  },
};
</script>
