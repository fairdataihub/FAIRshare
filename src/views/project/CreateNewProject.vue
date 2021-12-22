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

        <el-form-item label="Data type" prop="dataType">
          <el-checkbox-group v-model="datasetForm.dataType" class="p-0">
            <div>
              <el-checkbox label="Code" name="type"></el-checkbox>
            </div>

            <el-tooltip
              class="item"
              effect="dark"
              content="Coming soon..."
              placement="right-end"
            >
              <div class="w-max">
                <el-checkbox label="Figure" name="type" disabled></el-checkbox>
                <el-checkbox label="Media" name="type" disabled></el-checkbox>
                <el-checkbox label="Poster" name="type" disabled></el-checkbox>
              </div>
            </el-tooltip>

            <div>
              <el-tooltip
                class="item"
                effect="dark"
                content="Coming soon..."
                placement="right-end"
              >
                <el-checkbox
                  label="Publications"
                  name="type"
                  disabled
                ></el-checkbox>
              </el-tooltip>
            </div>

            <div>
              <el-tooltip
                class="item"
                effect="dark"
                content="Coming soon..."
                placement="right-end"
              >
                <el-checkbox
                  label="Genomic Data"
                  name="type"
                  disabled
                ></el-checkbox>
              </el-tooltip>
            </div>
          </el-checkbox-group>
        </el-form-item>

        <div class="py-2 flex flex-row justify-center space-x-4">
          <el-button @click="cancelNewDataset" type="danger" plain>
            <el-icon><d-arrow-left /></el-icon> Cancel
          </el-button>
          <el-button type="primary" @click="submitForm('datasetForm')">
            Create new project <el-icon><d-arrow-right /></el-icon>
          </el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
import { v4 as uuidv4 } from "uuid";

import { useDatasetsStore } from "../../store/datasets";
import { ElNotification } from "element-plus";

export default {
  name: "CreateNewProject",
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
            message: "Please type a dataset name",
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

          let dataset = {
            id: datasetID,
            image: datasetImage,
            name: this.datasetForm.datasetName,
            description: this.datasetForm.datasetDescription,
            dataType: this.datasetForm.dataType,
            data: {},
            workflowConfirmed: false,
          };

          dataset.data.general = {
            questions: {},
          };

          for (const type of dataset.dataType) {
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
  mounted() {},
};
</script>
