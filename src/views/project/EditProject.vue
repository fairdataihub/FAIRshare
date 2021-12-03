<template>
  <div class="h-full w-full flex flex-col justify-center items-center p-3 px-5">
    <div class="flex flex-col h-full w-full">
      <span class="font-medium"> Edit your project details </span>
      <span>
        If you want to change your project name or description you may edit them
        here.
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
      </el-form>
      <div class="py-2 flex flex-row justify-center">
        <el-button @click="cancelNewDataset"> Cancel </el-button>
        <el-button type="primary" @click="submitForm('datasetForm')">
          Save changes
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
// import { Icon } from "@iconify/vue";

import { useDatasetsStore } from "../../store/datasets";

export default {
  name: "EditProject",
  // components: { Icon },
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
    cancelNewDataset() {
      this.$router.push({ name: "ShowAllProjects" });
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();

    this.datasetStore.hideProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(1);

    this.datasetForm.datasetName = this.dataset.name;
    this.datasetForm.datasetDescription = this.dataset.description;
    // this.datasetForm.dataType = this.dataset.dataType;
  },
};
</script>
