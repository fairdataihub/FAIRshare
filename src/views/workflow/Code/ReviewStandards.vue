<template>
  <div
    class="h-full w-full flex flex-col justify-center items-center pr-5 p-3 max-w-screen-xl"
  >
    <div class="flex flex-col h-full w-full">
      <span class="text-lg font-medium text-left">
        Are standard development practices being followed?
      </span>

      <el-divider class="my-4"> </el-divider>

      <div class="divide-y-2 divide-gray-100">
        <div
          v-for="question in questions"
          :key="question"
          class="flex flex-col py-3"
        >
          <span>
            {{ question }}
          </span>
          <div class="pb-3 pt-2">
            <el-radio label="1" size="large"> Yes </el-radio>
            <el-radio label="2" size="large"> No </el-radio>
          </div>
        </div>
      </div>

      <div class="w-full flex flex-row justify-center py-2 space-x-4">
        <router-link
          :to="`/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/Code/selectFolder`"
          class=""
        >
          <button class="danger-button">
            <el-icon><d-arrow-left /></el-icon> Back
          </button>
        </router-link>

        <button
          class="primary-plain-button"
          @click="startCuration"
          id="continue"
        >
          Continue
          <el-icon> <d-arrow-right /> </el-icon>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CodeReviewStandards",
  data() {
    return {
      datasetID: this.$route.params.datasetID,
      workflowID: this.$route.params.workflowID,
      questions: [
        "Is the data being curated in accordance with the standards?",
        "Is the data being curated in accordance with the standards?",
      ],
    };
  },
  methods: {
    startCuration() {
      this.$router.push(
        `/datasets/${this.datasetID}/${this.workflowID}/Code/createMetadata`
      );
    },
  },
};
</script>

<style></style>
