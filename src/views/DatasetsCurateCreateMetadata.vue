<template>
  <div class="h-screen w-full flex flex-row lg:justify-center items-center">
    <div class="w-full h-full flex flex-row items-center">
      <div class="h-full w-full">
        <div class="flex flex-col h-full overflow-y-auto px-5">
          <span class="text-lg font-medium text-left">
            Lets make your data FAIR
          </span>

          <line-divider></line-divider>

          <span class="mb-2">
            We need to know some general details your dataset. Please fill all
            the fields in this section and we'll take care of the rest.
          </span>

          <el-collapse v-model="activeNames">
            <el-collapse-item
              class="text-lg"
              title="Basic Information"
              name="general"
            >
              <el-form
                :model="generalForm"
                label-width="160px"
                label-position="right"
                size="small"
                @submit.prevent
              >
                <el-form-item label="Dataset name">
                  <el-input v-model="generalForm.name"></el-input>
                </el-form-item>

                <el-form-item label="Dataset description">
                  <el-input
                    v-model="generalForm.description"
                    type="textarea"
                  ></el-input>
                </el-form-item>

                <el-form-item label="Keywords">
                  <draggable
                    tag="div"
                    :list="generalForm.keywords"
                    item-key="id"
                    handle=".handle"
                  >
                    <template #item="{ element }">
                      <div
                        class="
                          flex flex-row
                          mb-2
                          justify-between
                          transition-all
                        "
                      >
                        <div class="flex flex-row justify-between w-11/12">
                          <el-input
                            v-model="element.keyword"
                            type="text"
                            placeholder=""
                          ></el-input>
                          <div class="mx-2"></div>
                        </div>
                        <div class="flex flex-row justify-evenly w-1/12">
                          <div
                            class="
                              flex
                              justify-center
                              items-center
                              handle
                              text-gray-400
                              hover:text-gray-700
                            "
                          >
                            <Icon icon="ic:outline-drag-indicator" />
                          </div>
                          <div
                            class="
                              flex
                              justify-center
                              items-center
                              text-gray-600
                              hover:text-gray-800
                              cursor-pointer
                            "
                          >
                            <el-popconfirm
                              title="Are you sure you want to remove this?"
                              icon-color="red"
                              confirm-button-text="Yes"
                              cancel-button-text="No"
                              @confirm="deleteKeyword(element.id)"
                            >
                              <template #reference>
                                <Icon icon="bx:bx-x" />
                              </template>
                            </el-popconfirm>
                          </div>
                        </div>
                      </div>
                    </template>
                  </draggable>

                  <div
                    class="
                      flex
                      items-center
                      cursor-pointer
                      text-gray-500
                      hover:text-black
                      w-max
                    "
                    @click="addKeyword()"
                  >
                    <Icon icon="carbon:add" />
                    <span> Add a keyword </span>
                  </div>
                </el-form-item>

                <el-form-item label="Funding code">
                  <el-input
                    v-model="generalForm.funding.code"
                    type="text"
                  ></el-input>
                </el-form-item>

                <el-form-item label="Funding organization">
                  <el-input
                    v-model="generalForm.funding.organization"
                    type="text"
                  ></el-input>
                </el-form-item>

                <el-form-item label="Reference publication">
                  <el-input
                    v-model="generalForm.referencePublication"
                    type="text"
                  ></el-input>
                </el-form-item>

                <el-form-item label="Authors">
                  <draggable
                    tag="div"
                    :list="generalForm.authors"
                    item-key="id"
                    handle=".handle"
                  >
                    <template #item="{ element }">
                      <div
                        class="
                          flex flex-row
                          mb-2
                          justify-between
                          transition-all
                        "
                      >
                        <div class="flex flex-row justify-between w-11/12">
                          <el-input
                            v-model="element.givenName"
                            type="text"
                            placeholder="Given name"
                          ></el-input>
                          <div class="mx-2"></div>
                          <el-input
                            v-model="element.familyName"
                            type="text"
                            placeholder="Family name"
                          ></el-input>
                          <div class="mx-2"></div>
                          <el-input
                            v-model="element.affiliation"
                            type="text"
                            placeholder="Affiliation"
                          ></el-input>
                          <div class="mx-2"></div>
                          <el-input
                            v-model="element.email"
                            type="text"
                            placeholder="E-mail address"
                          ></el-input>
                          <div class="mx-2"></div>
                          <el-input
                            v-model="element.orcid"
                            type="text"
                            placeholder="ORCID (e.g.: 0000-0002-1825-0097)"
                          ></el-input>
                          <div class="mx-2"></div>
                        </div>
                        <div class="flex flex-row justify-evenly w-1/12">
                          <div
                            class="
                              flex
                              justify-center
                              items-center
                              handle
                              text-gray-400
                              hover:text-gray-700
                            "
                          >
                            <Icon icon="ic:outline-drag-indicator" />
                          </div>
                          <div
                            class="
                              flex
                              justify-center
                              items-center
                              text-gray-600
                              hover:text-gray-800
                              cursor-pointer
                            "
                          >
                            <el-popconfirm
                              title="Are you sure you want to remove this?"
                              icon-color="red"
                              confirm-button-text="Yes"
                              cancel-button-text="No"
                              @confirm="deleteAuthor(element.id)"
                            >
                              <template #reference>
                                <Icon icon="bx:bx-x" />
                              </template>
                            </el-popconfirm>
                          </div>
                        </div>
                      </div>
                    </template>
                  </draggable>

                  <div
                    class="
                      flex
                      items-center
                      cursor-pointer
                      text-gray-500
                      hover:text-black
                      w-max
                    "
                    @click="addAuthor()"
                  >
                    <Icon icon="carbon:add" />
                    <span> Add an author </span>
                  </div>
                </el-form-item>

                <el-form-item label="Contributors">
                  <draggable
                    tag="div"
                    :list="generalForm.contributors"
                    item-key="id"
                    handle=".handle"
                  >
                    <template #item="{ element }">
                      <div
                        class="
                          flex flex-row
                          mb-2
                          justify-between
                          transition-all
                        "
                      >
                        <div class="flex flex-row justify-between w-11/12">
                          <div class="mr-2 w-1/5">
                            <el-input
                              v-model="element.givenName"
                              type="text"
                              placeholder="Given name"
                            ></el-input>
                          </div>
                          <div class="mx-2 w-1/5">
                            <el-input
                              v-model="element.familyName"
                              type="text"
                              placeholder="Family name"
                            ></el-input>
                          </div>
                          <div class="mx-2 w-1/5">
                            <el-input
                              v-model="element.affiliation"
                              type="text"
                              placeholder="Affiliation"
                            ></el-input>
                          </div>
                          <div class="mx-2 w-1/5">
                            <el-input
                              v-model="element.email"
                              type="text"
                              placeholder="E-mail address"
                            ></el-input>
                          </div>
                          <div class="mx-2 w-1/5">
                            <el-input
                              v-model="element.orcid"
                              type="text"
                              placeholder="ORCID (e.g. 0000-0002-1825-0097)"
                            ></el-input>
                          </div>
                          <div class="mx-2 md:w-2/12 lg:w-1/5 xl:w-max">
                            <el-select
                              v-model="element.contributorType"
                              filterable
                              placeholder="Select a contributor type"
                            >
                              <el-option
                                v-for="item in contributorTypes"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                              >
                              </el-option>
                            </el-select>
                          </div>
                        </div>
                        <div class="flex flex-row justify-evenly w-1/12">
                          <div
                            class="
                              flex
                              justify-center
                              items-center
                              handle
                              text-gray-400
                              hover:text-gray-700
                            "
                          >
                            <Icon icon="ic:outline-drag-indicator" />
                          </div>
                          <div
                            class="
                              flex
                              justify-center
                              items-center
                              text-gray-600
                              hover:text-gray-800
                              cursor-pointer
                            "
                          >
                            <el-popconfirm
                              title="Are you sure you want to remove this?"
                              icon-color="red"
                              confirm-button-text="Yes"
                              cancel-button-text="No"
                              @confirm="deleteContributor(element.id)"
                            >
                              <template #reference>
                                <Icon icon="bx:bx-x" />
                              </template>
                            </el-popconfirm>
                          </div>
                        </div>
                      </div>
                    </template>
                  </draggable>

                  <div
                    class="
                      flex
                      items-center
                      cursor-pointer
                      text-gray-500
                      hover:text-black
                      w-max
                    "
                    @click="addContributor()"
                  >
                    <Icon icon="carbon:add" />
                    <span> Add a contributor </span>
                  </div>
                </el-form-item>
              </el-form>
            </el-collapse-item>

            <el-collapse-item title="Code" name="code" v-if="codePresent">
              <p class="mb-2">
                Lets make your code FAIR. Please fill the following fields.
              </p>

              <el-form
                :model="codeForm"
                label-width="214px"
                label-position="right"
                size="small"
                @submit.prevent
              >
                <el-form-item label="Creation date">
                  <el-date-picker
                    v-model="codeForm.creationDate"
                    type="date"
                    placeholder="Pick a day"
                    value-format="YYYY-MM-DD"
                  >
                  </el-date-picker>
                </el-form-item>

                <el-form-item label="First release date">
                  <el-date-picker
                    v-model="codeForm.firstReleaseDate"
                    type="date"
                    placeholder="Pick a day"
                    value-format="YYYY-MM-DD"
                  >
                  </el-date-picker>
                </el-form-item>

                <el-form-item label="License">
                  <el-select
                    v-model="codeForm.license"
                    filterable
                    placeholder="Select a license"
                  >
                    <el-option
                      v-for="item in licenseOptions"
                      :key="item.licenseId"
                      :label="item.name"
                      :value="item.licenseId"
                    >
                    </el-option>
                  </el-select>
                  <p class="text-xs pt-2 text-gray-500">Required.</p>
                </el-form-item>

                <el-form-item label="Application category">
                  <el-input v-model="codeForm.applicationCategory"></el-input>
                </el-form-item>

                <el-form-item label="Code repository">
                  <el-input v-model="codeForm.codeRepository"></el-input>
                </el-form-item>

                <el-form-item label="Continuous integration">
                  <el-input v-model="codeForm.continuousIntegration"></el-input>
                </el-form-item>

                <el-form-item label="Issue Tracker">
                  <el-input v-model="codeForm.issueTracker"></el-input>
                </el-form-item>

                <el-form-item label="Related links">
                  <draggable
                    tag="div"
                    :list="codeForm.relatedLinks"
                    item-key="id"
                    handle=".handle"
                  >
                    <template #item="{ element }">
                      <div
                        class="
                          flex flex-row
                          mb-2
                          justify-between
                          transition-all
                        "
                      >
                        <div class="flex flex-row justify-between w-11/12">
                          <el-input
                            v-model="element.link"
                            type="text"
                            placeholder=""
                          ></el-input>
                          <div class="mx-2"></div>
                        </div>
                        <div class="flex flex-row justify-evenly w-1/12">
                          <div
                            class="
                              flex
                              justify-center
                              items-center
                              handle
                              text-gray-400
                              hover:text-gray-700
                            "
                          >
                            <Icon icon="ic:outline-drag-indicator" />
                          </div>
                          <div
                            class="
                              flex
                              justify-center
                              items-center
                              text-gray-600
                              hover:text-gray-800
                              cursor-pointer
                            "
                          >
                            <el-popconfirm
                              title="Are you sure you want to remove this?"
                              icon-color="red"
                              confirm-button-text="Yes"
                              cancel-button-text="No"
                              @confirm="deleteRelatedLink(element.id)"
                            >
                              <template #reference>
                                <Icon icon="bx:bx-x" />
                              </template>
                            </el-popconfirm>
                          </div>
                        </div>
                      </div>
                    </template>
                  </draggable>

                  <div
                    class="
                      flex
                      items-center
                      cursor-pointer
                      text-gray-500
                      hover:text-black
                      w-max
                    "
                    @click="addRelatedLink()"
                  >
                    <Icon icon="carbon:add" />
                    <span> Add a related link </span>
                  </div>
                </el-form-item>

                <el-form-item label="Programming Language">
                  <el-select
                    v-model="codeForm.programmingLanguage"
                    multiple
                    filterable
                    allow-create
                    default-first-option
                    placeholder="C#, Java, Python 3"
                  >
                    <el-option
                      v-for="item in programmingLanguageOptions"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value"
                    >
                    </el-option>
                  </el-select>
                </el-form-item>

                <el-form-item label="Runtime platform">
                  <el-select
                    v-model="codeForm.runtimePlatform"
                    multiple
                    filterable
                    allow-create
                    default-first-option
                    placeholder=".Net, Java"
                  >
                    <el-option
                      v-for="item in runtimePlatformOptions"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value"
                    >
                    </el-option>
                  </el-select>
                </el-form-item>

                <el-form-item label="Operating system">
                  <el-select
                    v-model="codeForm.operatingSystem"
                    multiple
                    filterable
                    allow-create
                    default-first-option
                    placeholder="Linux, Windows"
                  >
                    <el-option
                      v-for="item in operatingSystemOptions"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value"
                    >
                    </el-option>
                  </el-select>
                </el-form-item>

                <el-form-item label="Other software requirements">
                  <draggable
                    tag="div"
                    :list="codeForm.otherSoftwareRequirements"
                    item-key="id"
                    handle=".handle"
                  >
                    <template #item="{ element }">
                      <div
                        class="
                          flex flex-row
                          mb-2
                          justify-between
                          transition-all
                        "
                      >
                        <div class="flex flex-row justify-between w-11/12">
                          <el-input
                            v-model="element.link"
                            type="text"
                            placeholder="Python 3.4 or https://github.com/pst/requests"
                          ></el-input>
                          <div class="mx-2"></div>
                        </div>
                        <div class="flex flex-row justify-evenly w-1/12">
                          <div
                            class="
                              flex
                              justify-center
                              items-center
                              handle
                              text-gray-400
                              hover:text-gray-700
                            "
                          >
                            <Icon icon="ic:outline-drag-indicator" />
                          </div>
                          <div
                            class="
                              flex
                              justify-center
                              items-center
                              text-gray-600
                              hover:text-gray-800
                              cursor-pointer
                            "
                          >
                            <el-popconfirm
                              title="Are you sure you want to remove this?"
                              icon-color="red"
                              confirm-button-text="Yes"
                              cancel-button-text="No"
                              @confirm="
                                deleteOtherSoftwareRequirements(element.id)
                              "
                            >
                              <template #reference>
                                <Icon icon="bx:bx-x" />
                              </template>
                            </el-popconfirm>
                          </div>
                        </div>
                      </div>
                    </template>
                  </draggable>

                  <div
                    class="
                      flex
                      items-center
                      cursor-pointer
                      text-gray-500
                      hover:text-black
                      w-max
                    "
                    @click="addOtherSoftwareRequirements()"
                  >
                    <Icon icon="carbon:add" />
                    <span> Add an additional software requirement </span>
                  </div>
                </el-form-item>

                <el-form-item label="Current version">
                  <el-input
                    v-model="codeForm.currentVersion"
                    placeholder="1.5.6"
                  ></el-input>
                </el-form-item>

                <el-form-item label="Current version release date">
                  <el-date-picker
                    v-model="codeForm.currentVersionReleaseDate"
                    type="date"
                    placeholder="Pick a day"
                    value-format="YYYY-MM-DD"
                  >
                  </el-date-picker>
                </el-form-item>

                <el-form-item label="Current version download URL">
                  <el-input
                    v-model="codeForm.currentVersionDownloadLink"
                    type="url"
                    placeholder="https://www.python.org/downloads/release/python-3100/"
                  ></el-input>
                </el-form-item>

                <el-form-item label="Current version release notes">
                  <el-input
                    v-model="codeForm.currentVersionReleaseNotes"
                    type="textarea"
                    placeholder="Change log: Added this new feature &#10;Bugfixes: Squashed some bugs"
                  ></el-input>
                </el-form-item>

                <el-form-item label="Development status">
                  <el-select
                    v-model="codeForm.developmentStatus"
                    filterable
                    placeholder=""
                  >
                    <el-option
                      v-for="item in repoStatusOptions"
                      :key="item.value"
                      :label="item.display_name"
                      :value="item.value"
                    >
                    </el-option>
                  </el-select>
                  <p class="text-xs pt-2 text-gray-500">
                    {{ developmentStatus }}
                  </p>
                </el-form-item>

                <el-form-item label="Is part of">
                  <el-input
                    v-model="codeForm.isPartOf"
                    type="url"
                    placeholder="https://thebiggerframework.org"
                  ></el-input>
                </el-form-item>
              </el-form>
            </el-collapse-item>
          </el-collapse>

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
import { Icon } from "@iconify/vue";
import { ArrowRightBold } from "@element-plus/icons";
import draggable from "vuedraggable";
import { v4 as uuidv4 } from "uuid";

import { useDatasetsStore } from "../store/datasets";
import licensesJSON from "../assets/supplementalFiles/licenses.json";
import contributorTypesJSON from "../assets/supplementalFiles/contributorTypes.json";
import repoStatusJSON from "../assets/supplementalFiles/repoStatus.json";

export default {
  name: "DatasetsCurateCreateMetadata",
  components: { ArrowRightBold, draggable, Icon },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      dataset: {},
      workflowID: this.$route.params.workflowID,
      workflow: {},
      activeNames: ["general", "code"],
      licenseOptions: licensesJSON.licenses,
      contributorTypes: contributorTypesJSON.contributorTypes,
      programmingLanguageOptions: [
        {
          value: "C#",
          label: "C#",
        },
        {
          value: "Java",
          label: "Java",
        },
        {
          value: "Python 3",
          label: "Python 3",
        },
      ],
      runtimePlatformOptions: [
        {
          value: ".Net",
          label: ".Net",
        },
        {
          value: "Java",
          label: "Java",
        },
      ],
      operatingSystemOptions: [
        {
          value: "Linux",
          label: "Linux",
        },
        {
          value: "Windows",
          label: "Windows",
        },
      ],
      repoStatusOptions: repoStatusJSON.repoStatus,
      generalForm: {
        name: "",
        description: "",
        keywords: [],
        funding: {
          code: "",
          organization: "",
        },
        referencePublication: "",
        authors: [],
        contributors: [],
      },
      codeForm: {
        creationDate: "",
        firstReleaseDate: "",
        license: "",
        uniqueIdentifier: "",
        applicationCategory: "",
        codeRepository: "",
        continuousIntegration: "",
        issueTracker: "",
        relatedLinks: [],
        programmingLanguage: [],
        runtimePlatform: [],
        operatingSystem: [],
        otherSoftwareRequirements: [],
        currentVersion: "",
        currentVersionReleaseDate: "",
        currentVersionDownloadLink: "",
        currentVersionReleaseNotes: "",
        developmentStatus: "",
        isPartOf: "",
      },
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
    developmentStatus() {
      const that = this;

      function getStatus(repoStatus) {
        return that.repoStatusOptions.find(
          (status) => status.value === repoStatus
        );
      }

      if (
        "developmentStatus" in this.codeForm &&
        this.codeForm.developmentStatus != ""
      ) {
        const status = this.codeForm.developmentStatus;
        const returnVal = getStatus(status);

        return returnVal.description;
      } else {
        return "";
      }
    },
  },
  methods: {
    addIds(array) {
      array.forEach((element) => {
        element.id = uuidv4();
      });
    },
    initializeEmptyObjects(root, obj) {
      if (typeof obj === "undefined") {
        root[obj] = {};
      }
    },
    addKeyword() {
      this.generalForm.keywords.push({
        keyword: "",
        id: uuidv4(),
      });
    },
    deleteKeyword(id) {
      this.generalForm.keywords = this.generalForm.keywords.filter(
        (keyword) => {
          return keyword.id !== id;
        }
      );
    },
    addAuthor() {
      this.generalForm.authors.push({
        givenName: "",
        familyName: "",
        affiliation: "",
        email: "",
        orcid: "",
        id: uuidv4(),
      });
    },
    deleteAuthor(id) {
      this.generalForm.authors = this.generalForm.authors.filter((author) => {
        return author.id !== id;
      });
    },
    addContributor() {
      this.generalForm.contributors.push({
        contributorType: "",
        givenName: "",
        familyName: "",
        affiliation: "",
        email: "",
        orcid: "",
        id: uuidv4(),
      });
    },
    deleteContributor(id) {
      this.generalForm.contributors = this.generalForm.contributors.filter(
        (contributor) => {
          return contributor.id !== id;
        }
      );
    },
    addRelatedLink() {
      this.codeForm.relatedLinks.push({
        link: "",
        id: uuidv4(),
      });
    },
    deleteRelatedLink(id) {
      this.codeForm.relatedLinks = this.codeForm.relatedLinks.filter(
        (relatedLink) => {
          return relatedLink.id !== id;
        }
      );
    },
    addOtherSoftwareRequirements() {
      this.codeForm.otherSoftwareRequirements.push({
        link: "",
        id: uuidv4(),
      });
    },
    deleteOtherSoftwareRequirements(id) {
      this.codeForm.otherSoftwareRequirements =
        this.codeForm.otherSoftwareRequirements.filter(
          (otherSoftwareRequirement) => {
            return otherSoftwareRequirement.id !== id;
          }
        );
    },
    navigateToSelectDestination() {
      this.dataset.data.general.questions = this.generalForm;

      if (this.codePresent) {
        this.dataset.data.Code.questions = this.codeForm;
      }

      this.datasetStore.updateCurrentDataset(this.dataset);
      this.datasetStore.syncDatasets();

      this.workflow.expandOptions = [];

      const routerPath = `/datasets/${this.dataset.id}/${this.workflowID}/createMetadata/review`;
      console.log(routerPath);
      this.$router.push({ path: routerPath });
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();

    this.workflow = this.dataset.workflows[this.workflowID];

    if (this.workflow.expandOptions.length === 0) {
      this.activeNames = ["general"];
    } else {
      this.activeNames = this.workflow.expandOptions;
    }

    if (
      this.dataset.data.general.questions &&
      Object.keys(this.dataset.data.general.questions).length !== 0
    ) {
      this.generalForm = this.dataset.data.general.questions;

      this.initializeEmptyObjects(this.generalForm, this.generalForm.funding);

      this.addIds(this.generalForm.keywords);
      this.addIds(this.generalForm.authors);
      this.addIds(this.generalForm.contributors);
    }

    if (this.codePresent) {
      if (
        this.dataset.data.Code.questions &&
        Object.keys(this.dataset.data.Code.questions).length !== 0
      ) {
        this.codeForm = this.dataset.data.Code.questions;

        this.addIds(this.codeForm.relatedLinks);
        this.addIds(this.codeForm.otherSoftwareRequirements);
      }
    }
  },
};

// Right now, going to put all the general questions in the dataset object under a metadata.general key.
// questions regarding the detination will be put under worflow[workflowID].destination.name/questions key.
// might be slightly confusing but it will be easier to manage.
</script>
