<template>
  <div
    class="flex h-screen w-full max-w-screen-xl flex-col items-center justify-center p-3 px-5"
  >
    <div class="flex h-full w-full flex-col py-5">
      <el-page-header @back="goBack" class="hidden text-lg">
        <template #content>
          <p>
            Project settings -
            <span class="text-sm">
              Update your project name, description and other settings
            </span>
          </p>
        </template>
      </el-page-header>

      <!-- <span class="font-medium text-left"> Project settings </span>

      <span class="pt-1">
        Update your project name, description and other settings.
      </span> -->

      <el-divider> </el-divider>

      <el-form
        ref="datasetForm"
        :model="datasetForm"
        label-width="150px"
        @submit.prevent
        class="rounded-lg border-2 border-slate-100 p-4"
        :rules="rules"
        size="large"
      >
        <el-form-item label="Project ID">
          <span class="cursor-not-allowed text-zinc-500">
            {{ dataset.id }}
          </span>
        </el-form-item>

        <el-form-item label="Dataset name" prop="datasetName">
          <el-input v-model="datasetForm.datasetName" size="large"></el-input>
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
                size="large"
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
          <div class="flex w-full flex-col">
            <p>
              Once you delete a project, there is no going back. Please be
              certain.
            </p>
            <div>
              <button class="danger-button py-0" @click="openDialog">
                <el-icon><delete-icon /></el-icon> Delete project
              </button>

              <warning-prompt
                ref="warningPrompt"
                title="Delete project"
                confirmButtonText="I understand. Delete this project"
                :confirmDisabled="disableConfirm"
                @messageConfirmed="deleteProject"
              >
                <div w-full>
                  <p class="mb-3 w-full text-left text-base text-gray-500">
                    This action cannot be undone. This will permanently delete
                    the
                    <span class="font-bold">{{ originalName }}</span>
                    project.
                  </p>
                  <p class="mb-2 text-left text-base text-gray-500">
                    Please type
                    <span class="font-bold">{{ originalName }}</span> to
                    confirm.
                  </p>

                  <el-input
                    v-model="deleteInput"
                    :placeholder="originalName"
                    clearable
                    size="large"
                    class="w-full"
                  />
                </div>
              </warning-prompt>
            </div>
          </div>
        </el-form-item>
      </el-form>
      <div class="flex flex-row justify-center space-x-4 py-4">
        <button class="danger-plain-button" @click="goBack">
          <el-icon><circle-close-filled /></el-icon> Cancel
        </button>
        <button class="primary-button" @click="submitForm('datasetForm')">
          Save changes <el-icon><circle-check-filled /></el-icon>
        </button>
      </div>
      <div class="flex hidden flex-row justify-center space-x-4 py-2">
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
import { ElMessage } from "element-plus";

import { useDatasetsStore } from "@/store/datasets";

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
      deleteInput: "",
      deleteDisabled: false,
      rules: {
        datasetName: [
          {
            required: true,
            message: "Please provide a project name",
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
  computed: {
    disableConfirm() {
      return this.deleteInput.trim() !== this.originalName.trim();
    },
  },
  methods: {
    openDialog() {
      this.deleteInput = "";
      this.$refs.warningPrompt.show();
    },
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
    async deleteProject() {
      await this.datasetStore.deleteDataset(this.datasetID);

      ElMessage({
        type: "success",
        message: `Your project was deleted.`,
      });

      this.goBack();
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
