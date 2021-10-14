<template>
  <div class="h-screen w-full flex flex-row items-center overflow-y-auto">
    <div class="p-3 h-full flex flex-row">
      <div class="flex flex-col h-full">
        <span class="font-inter text-base font-medium">
          Create a new dataset
        </span>
        <span class="font-inter text-base">
          Fill out some general details about your dataset here.
        </span>

        <el-divider> </el-divider>

        <el-form
          ref="datasetForm"
          :model="datasetForm"
          label-width="150px"
          @submit.prevent
          :rules="rules"
        >
          <el-form-item label="Dataset name" prop="datasetName" class="font-inter">
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
                ></el-input>
              </template>

              <span class="break-normal text-left text-sm">
                Use a description that is easily identifiable. This will be
                shown in the dataset selection screen and is not part of your
                submitted metadata.
              </span>
            </el-popover>
          </el-form-item>

          <el-form-item label="Data type" prop="dataType">
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
          </el-form-item>

          <el-form-item>
            <div class="py-2">
              <el-button type="primary" @click="submitForm('datasetForm')">
                Create
              </el-button>
              <el-button @click="cancelNewDataset"> Cancel </el-button>
            </div>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
// import { Icon } from "@iconify/vue";
import { v4 as uuidv4 } from "uuid";

import { useDatasetsStore } from "../store/datasets";

export default {
  name: "DatasetsCreateNew",
  // components: { Icon },
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
          };

          this.datasetStore.addDataset(dataset);
          this.datasetStore.writeDatasetsToFile();
          this.$router.push({ name: "DatasetsShowAll" }); //subject to change
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    cancelNewDataset() {
      this.$router.push({ name: "DatasetsShowAll" });
    },
  },
  mounted() {},
};
</script>

<style>
#unpublishedDatasets::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
  background-color: #f5f5f5;
}

#unpublishedDatasets::-webkit-scrollbar {
  width: 6px;
  background-color: #f5f5f5;
}

#unpublishedDatasets::-webkit-scrollbar-thumb {
  background-color: #424242;
}

::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
  background-color: #f5f5f5;
}

::-webkit-scrollbar {
  width: 6px;
  background-color: #f5f5f5;
}

::-webkit-scrollbar-thumb {
  background-color: #424242;
}
</style>
