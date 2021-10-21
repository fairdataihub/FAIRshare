<template>
  <div class="h-screen w-full flex flex-row lg:justify-center items-center">
    <div class="p-3 h-full flex flex-row items-center">
      <div class="h-full w-full">
        <div class="flex flex-col h-full overflow-y-auto pr-5">
          <span class="font-inter text-lg font-medium text-left">
            General information regarding your data
          </span>
          <span class="font-inter text-base text-left">
            Questions required for creating metadata.json file?
          </span>

          <el-divider class="my-4"> </el-divider>

          <span class="font-inter text-base mb-2">
            We need to know some general details about you and your dataset.
            Please fill this out to the best of your ability.
          </span>

          <el-form
            ref="datasetForm"
            :model="datasetForm"
            label-width="150px"
            label-position="top"
            @submit.prevent
          >
            <el-form-item label="Dataset name" class="font-inter">
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
          </el-form>

          <div class="w-full flex flex-row justify-center py-2">
            <router-link to="/datasets" class="mx-6">
              <el-button type="danger" plain> Cancel </el-button>
            </router-link>

            <el-button type="primary" class="flex flex-row items-center">
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
  name: "DatasetsCurateCreateMetadata",
  components: { ArrowRightBold },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      dataset: {},
      datasetForm: {
        datasetName: "",
        datasetDescription: "",
      },
      workflowID: this.$route.params.workflowID,
      workflow: {},
    };
  },

  methods: {},
  mounted() {
    this.dataset = this.datasetStore.currentDataset;
    this.workflow = this.dataset.workflows[this.workflowID];
  },
};
</script>
