<template>
  <div class="flex flex-col items-center justify-center w-full h-full p-3 pr-5">
    <div class="flex flex-col w-full h-full">
      <span class="text-lg font-medium text-left"> File Preview </span>

      <span class="mb-2">
        Here are the files we are going to send to zenodo
      </span>

      <el-collapse v-model="showFiles">
        <el-collapse-item
          class="my-1 border-2 border-gray-100 zenodo-collapse-item"
          name="codemetajson"
        >
          <template #title>
            <div
              class="flex flex-row items-center justify-between w-full font-inter"
            >
              <p class="px-4 text-sm font-semibold text-blue-500">
                codemeta.json
              </p>
            </div>
          </template>
          <div class="p-4">
            <el-table
              :data="tableData"
              style="width: 100%"
              row-key="id"
              border
              default-expand-all
            >
              <el-table-column prop="Name" label="Name" />
              <el-table-column prop="Value" label="Value" />
            </el-table>
          </div>
        </el-collapse-item>

        <el-collapse-item
          class="my-1 border-2 border-gray-100 zenodo-collapse-item"
          name="citationcff"
        >
          <template #title>
            <div
              class="flex flex-row items-center justify-between w-full font-inter"
            >
              <p class="px-4 text-sm font-semibold text-blue-500">
                citation.cff
              </p>
            </div>
          </template>
          <div class="p-4">
            <el-table
              :data="tableData"
              style="width: 100%"
              row-key="id"
              border
              default-expand-all
            >
              <el-table-column prop="Name" label="Name" />
              <el-table-column prop="Value" label="Value" />
            </el-table>
          </div>
        </el-collapse-item>

        <el-collapse-item
          class="my-1 border-2 border-gray-100 zenodo-collapse-item"
          name="LICENSEfile"
        >
          <template #title>
            <div
              class="flex flex-row items-center justify-between w-full font-inter"
            >
              <p class="px-4 text-sm font-semibold text-blue-500">
                LICENSE file
              </p>
            </div>
          </template>
          <div class="p-4">
            <el-table
              :data="lisenceData"
              style="width: 100%"
              row-key="id"
              border
              default-expand-all
            >
              <el-table-column prop="Name" label="Name" />
              <el-table-column prop="Value" label="Value" />
            </el-table>
          </div>
        </el-collapse-item>
      </el-collapse>

      <span class="text-lg font-medium text-left">
        Zenodo connection details
      </span>
      <span class="text-left">
        We will use this to upload and edit your dataset on your Zenodo account.
      </span>

      <el-divider class="my-4"> </el-divider>

      <div v-if="ready">
        <p v-if="validTokenAvailable" class="w-full my-10 text-center">
          Looks like we already have your Zenodo login details. Click on the
          'Start upload' button below.
        </p>
        <!-- show error message if token is not valid -->
        <div v-else class="flex flex-col items-center justify-center py-10">
          <p class="mb-5">
            We couldn't find your Zenodo login details. Please click on the
            button below to connect to your Zenodo account.
          </p>

          <ConnectZenodo :statusChangeFunction="showConnection"></ConnectZenodo>
        </div>
      </div>
      <LoadingFoldingCube v-else></LoadingFoldingCube>

      <div class="flex flex-row justify-center w-full py-2 space-x-4">
        <router-link
          :to="`/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/zenodo/metadata`"
          class=""
        >
          <button class="primary-plain-button">
            <el-icon><d-arrow-left /></el-icon> Back
          </button>
        </router-link>

        <button
          class="primary-button"
          :disabled="disableContinue"
          @click="uploadToZenodo"
          v-if="validTokenAvailable"
        >
          Start upload
          <el-icon> <d-arrow-right /> </el-icon>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
// import axios from "axios";

import LoadingFoldingCube from "@/components/spinners/LoadingFoldingCube";
// import ZenodoTokenConnectionVue from "@/components/serviceIntegration/ZenodoTokenConnection";
import ConnectZenodo from "@/components/serviceIntegration/ConnectZenodo";

import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

export default {
  name: "ZenodoAccessToken",
  components: { LoadingFoldingCube, ConnectZenodo },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      tokens: useTokenStore(),
      dataset: {},
      folderPath: "",
      workflowID: this.$route.params.workflowID,
      workflow: {},
      validTokenAvailable: false,
      errorMessage: "",
      zenodoAccessToken: "",
      ready: false,
      showFiles: "1",
      lisenceData: [{ Name: "Lisence", Value: "", id: 0 }],
      tableData: [],
    };
  },
  computed: {
    disableContinue() {
      if (this.validTokenAvailable) {
        return false;
      }
      if (!this.validTokenAvailable && this.zenodoAccessToken !== "") {
        return false;
      }
      return true;
    },
  },
  methods: {
    // async getDepositions(token) {
    //   return await axios
    //     .get(`${process.env.VUE_APP_ZENODO_SERVER_URL}deposit/depositions`, {
    //       params: {
    //         access_token: token,
    //       },
    //     })
    //     .then((response) => {
    //       return { data: response.data, status: response.status };
    //     })
    //     .catch((error) => {
    //       return { data: error.response.data, status: error.response.status };
    //     });
    // },
    jsonToTableDataRecursive(jsonObject, parentId, parentName) {
      // console.log("obj: ", jsonObject)
      if (
        jsonObject &&
        typeof jsonObject === "object" &&
        Object.keys(jsonObject).length != 0 &&
        !Array.isArray(jsonObject)
      ) {
        // object child
        let result = [];
        let count = 1;
        for (let property in jsonObject) {
          //console.log(property, jsonObject);
          let newObj = { Name: "", Value: "" };
          let newId = parentId + String(count);
          let value = this.jsonToTableDataRecursive(
            jsonObject[property],
            newId,
            property
          );
          // console.log(property, value)
          if (Array.isArray(value)) {
            newObj.id = newId;
            newObj.Name = property;
            newObj.Value = "";
            newObj.children = value;
          } else {
            newObj.id = newId;
            newObj.Name = property;
            newObj.Value = value;
          }
          result.push(newObj);
          count += 1;
        }
        return result;
      } else if (
        jsonObject &&
        Array.isArray(jsonObject) &&
        jsonObject.length != 0
      ) {
        // array
        let result = [];
        for (let i = 0; i < jsonObject.length; i++) {
          let newObj = { Name: "", Value: "" };
          let newId = parentId + String(i);
          let newName = "";
          if (i == 0) {
            newName = String(i + 1) + "st" + " in " + parentName;
          } else if (i == 1) {
            newName = String(i + 1) + "nd" + " in " + parentName;
          } else if (i == 2) {
            newName = String(i + 1) + "rd" + " in " + parentName;
          } else {
            newName = String(i + 1) + "th" + " in " + parentName;
          }
          let value = this.jsonToTableDataRecursive(
            jsonObject[i],
            newId,
            newName
          );
          if (Array.isArray(value)) {
            newObj.id = newId;
            newObj.Name = newName;
            newObj.Value = "";
            newObj.children = value;
          } else {
            newObj.id = newId;
            newObj.Name = newName;
            newObj.Value = value;
            newObj.children = [];
          }
          result.push(newObj);
        }
        return result;
      } else {
        // string, empty obj, empty arr
        return jsonObject;
      }
    },

    async checkToken(token) {
      console.log(token);
      const response = await this.tokens.getDepositions(token);

      if (response.status === 200) {
        this.validTokenAvailable = true;
        this.tokens.saveToken("zenodo", token);
        return true;
      } else if (response.status === 401) {
        this.errorMessage =
          "Invalid Zenodo access token. Please enter a valid Zenodo access token.";
        this.validTokenAvailable = false;
        return false;
      } else {
        this.errorMessage = "Something went wrong. Please try again.";
        this.validTokenAvailable = false;
        return false;
      }
    },
    async uploadToZenodo() {
      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/zenodo/upload`;
      if (this.validTokenAvailable) {
        this.$router.push({ path: routerPath });
      } else {
        const zenodoToken = this.zenodoAccessToken;
        const res = await this.checkToken(zenodoToken);

        if (res) {
          this.$router.push({ path: routerPath });
        }
      }
    },
    async showConnection(status) {
      console.log(status);
      if (status === "connected") {
        this.validTokenAvailable = true;
      }
      // this.uploadToZenodo(); console.log(this.workflow.licenseText)
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];
    this.lisenceData["Value"] = this.workflow.licenseText;
    this.tableData = this.jsonToTableDataRecursive(
      this.dataset.data,
      1,
      "ROOT"
    );
    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(6);

    const validZenodoConnection = await this.tokens.verifyZenodoConnection();

    if (validZenodoConnection) {
      this.validTokenAvailable = true;
      this.ready = true;
    } else {
      this.validTokenAvailable = false;
      this.ready = true;
    }
  },
};
</script>

<style lang="postcss" scoped></style>
