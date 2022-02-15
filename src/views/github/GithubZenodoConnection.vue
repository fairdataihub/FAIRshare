<template>
  <div
    class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 pr-5"
  >
    <div class="flex h-full w-full flex-col">
      <h1 class="pb-1 text-left text-lg font-medium">
        Connect your GitHub account to Zenodo
      </h1>
      <h2 class="text-left">
        Let's see if you GitHub account is already connected to Zenodo.
      </h2>

      <el-divider class="my-4"> </el-divider>

      <div>
        <div v-if="validZenodoHookTokenFound" class="my-10">
          <div class="flex items-center justify-center">
            <p class="my-3 mx-2 font-medium text-emerald-400">
              We found a Zenodo webhook on your GitHub repository.
            </p>
            <Vue3Lottie
              animationLink="https://assets2.lottiefiles.com/packages/lf20_xvusaxau.json"
              :width="30"
              :height="30"
              :loop="1"
            />
          </div>
          <p class="my-3 w-full text-center">
            Your account has been setup for Zenodo integration. Let's move on to
            the next step.
          </p>
        </div>
        <!-- show how to connect to zenodo if no hook is found -->
        <div v-else class="flex w-full flex-col">
          <div class="mb-5 flex items-center justify-center">
            <h3 class="mx-2 font-normal text-secondary-600">
              We are not seeing any Zenodo connections already setup with
              GitHub.
            </h3>
            <Vue3Lottie
              animationLink="https://assets1.lottiefiles.com/private_files/lf30_lkauxe8i.json"
              :width="45"
              :height="45"
            />
          </div>

          <div>
            <p class="mb-2">
              To connect your GitHub account with Zenodo there are a few steps
              you need to do from your side.
            </p>
            <ul class="ml-2 list-inside list-disc">
              <li>
                Login to Zenodo and go to the Github connections in your profile
                settings. Alternatively, you can also click the button below to
                take you to the appropriate page.
              </li>

              <div class="my-2 flex w-full items-center justify-center">
                <button
                  class="secondary-plain-button my-1"
                  @click="openWebsite"
                >
                  Connect Github to Zenodo
                </button>
              </div>

              <li>
                Authenticate with Github and wait for your list of repositories
                to show up.
              </li>

              <li>
                Toggle the switch for the
                <span class="font-bold">
                  {{ selectedRepo }}
                </span>
                repository to the 'ON' position.
              </li>

              <li>Wait for FairShare to notice the change.</li>
            </ul>
            <p class="mt-2">
              You will only need to do this once. For any future GitHub
              repositories, Fair Share will automatically add the relevant
              connections for you.
            </p>
          </div>
        </div>
      </div>

      <div class="flex w-full flex-row justify-center space-x-4 py-2">
        <router-link
          :to="`/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/zenodo/metadata`"
          class=""
        >
          <button class="primary-plain-button">
            <el-icon><d-arrow-left /></el-icon> Back
          </button>
        </router-link>

        <button
          class="secondary-plain-button"
          @click="showFilePreview"
          v-if="validZenodoHookTokenFound"
        >
          <el-icon><checked-icon /></el-icon>
          View files ready for upload
        </button>

        <button
          class="primary-button"
          @click="uploadToZenodo"
          v-if="validZenodoHookTokenFound"
        >
          Start upload
          <el-icon> <d-arrow-right /> </el-icon>
        </button>
      </div>
      <transition appear mode="out-in" name="fade">
        <div v-if="showFilePreviewSection" class="py-5">
          <line-divider />
          <p class="text=lg my-5">
            We will be adding some files to your GitHub repository. A preview of
            what it will look like after is shown below.
          </p>
          <div
            v-loading="loadingTree"
            :class="loadingTree ? 'h-full w-full' : 'h-[0px] w-[0px]'"
          ></div>
          <el-tree
            :data="fileData"
            :props="defaultProps"
            @node-click="handleNodeClick"
          >
            <template #default="{ node }">
              <el-icon v-if="!node.isLeaf"><folder-icon /></el-icon>
              <el-icon v-if="node.isLeaf"><document-icon /></el-icon>
              <span
                :class="
                  node.label == 'codemeta.json' ||
                  node.label == 'citation.cff' ||
                  (node.label == 'LICENSE' && workflow.generateLicense)
                    ? 'text-secondary-500'
                    : ''
                "
                >{{ node.label }}</span
              >
            </template>
          </el-tree>

          <el-drawer
            v-if="anyfilePreview"
            v-model="drawerModel"
            :title="fileTitle"
            direction="rtl"
            size="60%"
            :before-close="handleCloseDrawer"
            :lock-scroll="false"
          >
            <el-scrollbar style="height: calc(100vh - 45px)">
              <div v-if="PreviewNewlyCreatedMetadataFile" class="pb-20">
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

              <div v-if="PreviewNewlyCreatedCitationFile" class="pb-20">
                <el-table
                  :data="citationData"
                  style="width: 100%"
                  row-key="id"
                  border
                  default-expand-all
                >
                  <el-table-column prop="Name" label="Name" />
                  <el-table-column
                    prop="Value"
                    label="Value"
                    class="break-normal"
                  />
                </el-table>
              </div>

              <div v-if="PreviewNewlyCreatedLicenseFile" class="">
                <!-- <el-table
                  :data="licenseData"
                  style="width: 100%"
                  row-key="id"
                  border
                  default-expand-all
                >
                  <el-table-column prop="Name" label="Name" />
                  <el-table-column prop="Value" label="Value" />
                </el-table> -->
                <div class="whitespace-pre-line pb-20 text-sm">
                  {{ licenseData }}
                </div>
              </div>
            </el-scrollbar>
          </el-drawer>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

import axios from "axios";
import Vue3Lottie from "vue3-lottie";
import { ElLoading, ElNotification } from "element-plus";

import rippleLottieJSON from "@/assets/lotties/rippleLottie.json";

export default {
  name: "GithubZenodoConnection",
  components: {
    Vue3Lottie,
  },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      tokens: useTokenStore(),
      dataset: {},
      folderPath: "",
      workflowID: this.$route.params.workflowID,
      workflow: {},
      validZenodoHookTokenFound: false,
      errorMessage: "",
      showFilePreviewSection: "",
      zenodoAccessToken: "",
      selectedRepo: "",
      rippleLottieJSON,
      defaultProps: {
        children: "children",
        label: "label",
      },
      fileData: [],
      tree: [],
      fileTitle: "",
      PreviewNewlyCreatedLicenseFile: false,
      PreviewNewlyCreatedMetadataFile: false,
      PreviewNewlyCreatedCitationFile: false,
      licenseData: "",
      tableData: [],
      citationData: [],
      fullNameDictionary: {},
      ownerDictionary: {},
      nameDictionary: {},
      branchDictionary: {},
      drawerModel: true,
      loadingTree: false,
    };
  },
  computed: {
    currentBranch() {
      if (
        this.selectedRepo !== "" &&
        this.branchDictionary[this.selectedRepo]
      ) {
        return this.branchDictionary[this.selectedRepo].name;
      }
      return null;
    },
    anyfilePreview() {
      if (
        this.PreviewNewlyCreatedMetadataFile ||
        this.PreviewNewlyCreatedLicenseFile ||
        this.PreviewNewlyCreatedCitationFile
      ) {
        return true;
      } else {
        return false;
      }
    },
  },
  methods: {
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

          let customName = "";

          switch (parentName) {
            case "keywords":
              customName = "keyword";
              break;
            default:
              customName = parentName;
              break;
          }

          const readableIndex = i + 1;

          if (readableIndex % 10 == 1 && readableIndex % 100 != 11) {
            newName = String(i + 1) + "st " + customName;
          } else if (readableIndex % 10 == 2 && readableIndex % 100 != 12) {
            newName = String(i + 1) + "nd " + customName;
          } else if (readableIndex % 10 == 3 && readableIndex % 100 != 13) {
            newName = String(i + 1) + "rd " + customName;
          } else {
            newName = String(i + 1) + "th " + customName;
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
    async createCodeMetadataFile() {
      const response = await axios
        .post(`${this.$server_url}/metadata/create`, {
          data_types: JSON.stringify(this.workflow.type),
          data_object: JSON.stringify(this.dataset.data),
          virtual_file: true,
        })
        .then((response) => {
          return JSON.parse(response.data);
        })
        .catch((error) => {
          console.log(error);
          return "ERROR";
        });
      return response;
    },
    async createCitationFile() {
      const response = await axios
        .post(`${this.$server_url}/metadata/citation/create`, {
          data_types: JSON.stringify(this.workflow.type),
          data_object: JSON.stringify(this.dataset.data),
          virtual_file: true,
        })
        .then((response) => {
          return JSON.parse(response.data);
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });
      return response;
    },
    openGithubWebsite(url) {
      window.ipcRenderer.send("open-link-in-browser", url);
    },
    async handleNodeClick(data) {
      if (
        data.label == "LICENSE" ||
        data.label == "codemeta.json" ||
        data.label == "citation.cff"
      ) {
        if (data.label == "LICENSE") {
          this.PreviewNewlyCreatedLicenseFile = true;
        } else if (data.label == "codemeta.json") {
          this.PreviewNewlyCreatedMetadataFile = true;
        } else if (data.label == "citation.cff") {
          this.PreviewNewlyCreatedCitationFile = true;
        }
        let title = data.label;
        this.handleOpenDrawer(title);
      } else {
        this.openGithubWebsite(
          "https://github.com/" +
            this.selectedRepo +
            "/tree/" +
            this.currentBranch +
            "/" +
            this.fullNameDictionary[data.label]
        );
      }
    },
    async handleOpenDrawer(title) {
      this.fileTitle = title;
    },
    handleCloseDrawer() {
      this.fileTitle = "";
      this.PreviewNewlyCreatedLicenseFile = false;
      this.PreviewNewlyCreatedMetadataFile = false;
      this.PreviewNewlyCreatedCitationFile = false;
    },
    async buildDictionary() {
      const tokenObject = await this.tokens.getToken("github");
      const GithubAccessToken = tokenObject.token;
      const response = await axios
        .get(`${process.env.VUE_APP_GITHUB_SERVER_URL}/user/repos`, {
          params: {
            accept: "application/vnd.github.v3+json",
            per_page: 100,
          },
          headers: {
            Authorization: `Bearer ${GithubAccessToken}`,
          },
        })
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          console.log(error);
          return "ERROR";
        });
      if (response != "ERROR") {
        response.forEach((repo) => {
          this.ownerDictionary[repo.full_name] = repo.owner.login;
          this.nameDictionary[repo.full_name] = repo.name;
        });
      }
    },
    async read_sodaForCovid19Repo() {
      let selected = this.selectedRepo;
      const tokenObject = await this.tokens.getToken("github");
      const GithubAccessToken = tokenObject.token;
      let branches = await this.tokens.githubAPI_listCurrentRepoBranches(
        GithubAccessToken,
        this.nameDictionary[selected],
        this.ownerDictionary[selected]
      );
      this.branchDictionary[selected] = branches[0];
      let tree = await this.tokens.githubAPI_getTreeFromRepo(
        GithubAccessToken,
        this.nameDictionary[selected],
        this.ownerDictionary[selected],
        branches[0].name
      );
      for (let i = 0; i < tree.tree.length; i++) {
        this.tree.push(tree.tree[i]["path"]);
      }
      this.fileData = await this.parseTree();
    },
    async parseTree() {
      let paths = this.tree;
      let result = [];
      let level = { result };
      paths.forEach((path) => {
        this.fullNameDictionary[path.split("/").pop()] = path;
      });
      paths.forEach((path) => {
        path.split("/").reduce((r, label) => {
          if (!r[label]) {
            r[label] = { result: [] };
            r.result.push({ label, children: r[label].result });
          }
          return r[label];
        }, level);
      });
      return result;
    },
    createLoading() {
      const loading = ElLoading.service({
        lock: true,
        text: "Reading Github repository...",
      });
      return loading;
    },

    async uploadToZenodo() {
      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/github/upload`;

      this.$router.push({ path: routerPath });
    },

    openWebsite() {
      const url = `${process.env.VUE_APP_ZENODO_URL}/account/settings/github`;
      window.ipcRenderer.send("open-link-in-browser", url);
    },

    async showFilePreview() {
      this.showFilePreviewSection = !this.showFilePreviewSection;
      this.loadingTree = true;
      await this.buildDictionary();
      await this.read_sodaForCovid19Repo();
      this.finishLoading();
    },
    finishLoading() {
      this.loadingTree = false;
    },
    async checkIfZenodoHookIsPresent() {
      const tokenObject = await this.tokens.getToken("github");
      const GithubAccessToken = tokenObject.token;
      // console.log(GithubAccessToken);

      let response = "";

      response = await axios
        .get(
          `${process.env.VUE_APP_GITHUB_SERVER_URL}/repos/${this.selectedRepo}/hooks`,
          {
            params: {
              per_page: 100,
            },
            headers: {
              Accept: "application/vnd.github.v3+json",
              Authorization: `Bearer ${GithubAccessToken}`,
            },
          }
        )
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });

      if (response !== "ERROR" && response.length > 0) {
        for (const webhook of response) {
          if (
            "config" in webhook &&
            "events" in webhook &&
            webhook.events.includes("release") &&
            "url" in webhook.config &&
            webhook.config.url.includes(
              `${process.env.VUE_APP_ZENODO_SERVER_URL}/hooks/receivers/github/events/?access_token=`
            )
          ) {
            return response;
          } else {
            return false;
          }
        }
      } else {
        return false;
      }
    },

    async createGithubZenodoWebhook(GithubZenodoConnectionToken) {
      const tokenObject = await this.tokens.getToken("github");
      const GithubAccessToken = tokenObject.token;

      let response = "";

      const data = JSON.stringify({
        name: "web",
        config: {
          url: `https://sandbox.zenodo.org/api/hooks/receivers/github/events/?access_token=${GithubZenodoConnectionToken}`,
          content_type: "json",
          secret: "secret",
          insecure_ssl: 0,
        },
        events: ["release"],
        active: true,
      });

      const config = {
        method: "post",
        url: `${process.env.VUE_APP_GITHUB_SERVER_URL}/repos/${this.selectedRepo}/hooks`,
        headers: {
          Accept: "application/vnd.github.v3+json",
          Authorization: `Bearer ${GithubAccessToken}`,
          "Content-Type": "application/json",
        },
        data: data,
      };

      response = await axios(config)
        .then((response) => {
          console.log(response);
          if (response.status === 200 || response.status === 201) {
            return true;
          } else {
            return false;
          }
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });

      if (response !== "ERROR") {
        return response;
      } else {
        return false;
      }
    },
  },

  async mounted() {
    let spinner = this.createLoading();
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    this.selectedRepo = this.workflow.github.repo;

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(6);

    const tokenObject = await this.tokens.getToken("github");
    const GithubZenodoConnectionToken = tokenObject.zenodoHookToken;
    // const GithubZenodoConnectionToken = false;

    if (GithubZenodoConnectionToken) {
      const response = await this.checkIfZenodoHookIsPresent();
      spinner.close();

      if (response) {
        this.validZenodoHookTokenFound = true;
      } else {
        ElNotification({
          title: "Info",
          message: "Creating a Zenodo webhook for this repository.",
          type: "info",
        });

        const tokenCreated = await this.createGithubZenodoWebhook(
          GithubZenodoConnectionToken
        );

        if (tokenCreated) {
          ElNotification({
            title: "Success",
            message: "Created a zenodo webhook for this repo successfully.",
            type: "success",
          });

          setTimeout(() => {
            this.validZenodoHookTokenFound = true;
          }, 1000);
        } else {
          ElNotification({
            title: "Error",
            message:
              "Could not create the Zenodo webhook automatically. Please connect your Zenodo account to the GitHub repository manually.",
            type: "error",
            duration: 10000,
          });
        }
      }
    } else {
      let interval = setInterval(async () => {
        const response = await this.checkIfZenodoHookIsPresent();
        console.log(response);

        spinner.close();

        if (response) {
          if (response.length > 0) {
            for (const webhook of response) {
              if (
                "config" in webhook &&
                "events" in webhook &&
                webhook.events.includes("release") &&
                "url" in webhook.config &&
                webhook.config.url.includes(
                  `${process.env.VUE_APP_ZENODO_SERVER_URL}/hooks/receivers/github/events/?access_token=`
                )
              ) {
                const webhookConfigURL = webhook.config.url;
                const webhookConfigURLArray =
                  webhookConfigURL.split("access_token=");
                const webhookConfigURLToken = webhookConfigURLArray[1];
                console.log(webhookConfigURLToken);

                if (webhookConfigURLToken) {
                  const newTokenObject = JSON.parse(
                    JSON.stringify(await this.tokens.getToken("github"))
                  );
                  newTokenObject.zenodoHookToken = webhookConfigURLToken;

                  await this.tokens.saveToken("github", newTokenObject);
                }
              }
            }
          }

          this.validZenodoHookTokenFound = true;

          clearInterval(interval);
        }
      }, 5000);
    }
    let spinner2 = this.createLoading();
    this.tableData = await this.createCodeMetadataFile();
    this.citationData = await this.createCitationFile();
    this.tableData = this.jsonToTableDataRecursive(this.tableData, 1, "ROOT");
    this.citationData = this.jsonToTableDataRecursive(
      this.citationData,
      1,
      "ROOT"
    );
    if (this.workflow.generateLicense) {
      // await this.createLicenseFile();
      this.licenseData = this.workflow.licenseText;
    }
    spinner2.close();
    this.workflow.currentRoute = this.$route.path;
  },
};
</script>
