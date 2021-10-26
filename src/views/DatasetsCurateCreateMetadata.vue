<template>
  <div class="h-screen w-full flex flex-row lg:justify-center items-center">
    <div class="p-3 h-full flex flex-row items-center">
      <div class="h-full w-full">
        <div class="flex flex-col h-full overflow-y-auto pr-5">
          <span class="text-lg font-medium text-left">
            General information regarding your data
          </span>
          <span class="text-left">
            Questions required for creating metadata.json file?
          </span>

          <line-divider></line-divider>

          <span class="mb-2">
            We need to know some general details about you and your dataset.
            Please fill this out to the best of your ability.
          </span>

          <el-form
            :model="generalQuestionsForm"
            label-width="auto"
            label-position="top"
            size="medium"
            @submit.prevent
          >
            <el-form-item label="Dataset name">
              <el-input v-model="generalQuestionsForm.datasetName"></el-input>
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
                    v-model="generalQuestionsForm.datasetDescription"
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

          <line-divider></line-divider>
          <div ref="codeQuestions" v-if="codePresent">
            <span class="mb-2">
              Lets make your Code fair. Please fill the following fields.
            </span>

            <el-form
              :model="codeQuestionsForm"
              label-width="auto"
              label-position="top"
              size="medium"
              @submit.prevent
            >
              <el-form-item label="Does your code have a license file already?">
                <el-input v-model="codeQuestionsForm.datasetName"></el-input>
              </el-form-item>
            </el-form>
          </div>

          <div class="w-full flex flex-row justify-center py-2">
            <router-link to="/datasets" class="mx-6">
              <el-button type="danger" plain> Cancel </el-button>
            </router-link>

            <el-button
              type="primary"
              class="flex flex-row items-center"
              @click="navigateToSelectDestination"
            >
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
import { ArrowRightBold } from "@element-plus/icons";

import { useDatasetsStore } from "../store/datasets";

export default {
  name: "DatasetsCurateCreateMetadata",
  components: { ArrowRightBold },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      dataset: {},
      generalQuestionsForm: {
        datasetName: "",
        datasetDescription: "",
      },
      codeQuestionsForm: {
        datasetName: "",
      },
      workflowID: this.$route.params.workflowID,
      workflow: {},
    };
  },
  computed: {
    //check if code workflow is present
    codePresent() {
      if ("type" in this.workflow) {
        return this.workflow.type.includes("Code");
      }
      return false;
    },
  },
  methods: {
    navigateToSelectDestination() {
      this.datasetStore.updateCurrentDataset(this.dataset);

      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/selectDestination`;
      this.$router.push({ path: routerPath });
    },
  },
  mounted() {
    this.dataset = this.datasetStore.currentDataset;
    this.workflow = this.dataset.workflows[this.workflowID];

    // Add the functions here to check the pre saved values for on mounted.
    // decide if the intermediate data is saved in workflow or data.
  },
};

// Right now, going to put all the general questions in the dataset object under a metadata.general key.
// questions regarding the detination will be put under worflow[workflowID].destination.name/questions key.
// might be slightly confusing but it will be easier to manage.
</script>
