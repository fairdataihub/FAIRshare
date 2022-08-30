<template>
  <div class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium"> Figshare Metadata </span>

      <span class="mb-2">
        Before we send this data over, Figshare requires some additional information from you. We
        will use this information to create a Figshare article. Please fill out the following form.
      </span>

      <line-divider class="mb-8"></line-divider>

      <el-form
        :model="figshareMetadataForm"
        :rules="rulesFigshareMetadataForm"
        label-width="130px"
        label-position="right"
        size="large"
        ref="fmForm"
        class="rounded-lg border-2 border-slate-100 p-4"
        @submit.prevent
      >
        <el-form-item label="Item type" prop="uploadType">
          <div class="flex w-full flex-col">
            <el-select v-model="figshareMetadataForm.uploadType" placeholder="Media">
              <el-option
                v-for="item in uploadTypeOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              >
                <div class="flex w-full flex-row items-center justify-start">
                  <Icon :icon="item.icon" />
                  <span class="pl-4">{{ item.label }}</span>
                </div>
              </el-option>
            </el-select>
          </div>
        </el-form-item>

        <el-form-item label="Title" prop="title">
          <el-input v-model="figshareMetadataForm.title" type="text"> </el-input>
        </el-form-item>

        <el-form-item label="Description" prop="description">
          <VuePopper
            :hover="true"
            offsetDistance="0"
            content="Use a description that is easily identifiable. This will
                        be shown in the dataset selection screen and is not part
                        of your submitted metadata."
            class="mx-0 w-full"
          >
            <el-input v-model="figshareMetadataForm.description" type="textarea"></el-input>
          </VuePopper>
        </el-form-item>

        <el-form-item label="Authors" prop="authors">
          <draggable
            tag="div"
            :list="figshareMetadataForm.authors"
            item-key="id"
            handle=".handle"
            class="w-full"
            :animation="200"
          >
            <template #item="{ element }">
              <div class="mb-2 flex w-full flex-row justify-between transition-all">
                <div class="flex w-11/12 flex-row justify-between">
                  <el-input
                    v-model="element.givenName"
                    type="text"
                    placeholder="Given name"
                    class="h-[40px]"
                  ></el-input>

                  <div class="mx-2"></div>

                  <el-input
                    v-model="element.familyName"
                    type="text"
                    placeholder="Family name"
                    class="h-[40px]"
                  ></el-input>

                  <div class="mx-2"></div>

                  <div class="mx-2 flex w-full flex-col">
                    <el-input
                      v-model="element.email"
                      type="text"
                      placeholder="E-mail address"
                    ></el-input>
                    <span class="mt-1 ml-2 text-xs text-gray-400"> Optional </span>
                  </div>

                  <div class="mx-2 flex w-full flex-col">
                    <el-input
                      v-model="element.orcid"
                      type="text"
                      placeholder="ORCID (e.g.: 0000-0002-1825-0097)"
                    ></el-input>
                    <span class="mt-1 ml-2 text-xs text-gray-400"> Optional </span>
                  </div>
                </div>
                <div class="flex w-1/12 flex-row items-start justify-evenly py-4">
                  <div
                    class="handle flex items-center justify-center text-gray-400 hover:text-gray-700"
                  >
                    <Icon icon="ic:outline-drag-indicator" />
                  </div>
                  <div
                    class="flex cursor-pointer items-center justify-center text-gray-500 transition-all hover:text-gray-800"
                  >
                    <el-popconfirm
                      confirm-button-text="Yes"
                      cancel-button-text="No"
                      icon-color="red"
                      title="Are you sure you want to remove this?"
                      @confirm="deleteAuthor(element.id)"
                    >
                      <template #reference>
                        <el-icon><delete-filled /></el-icon>
                      </template>
                    </el-popconfirm>
                  </div>
                </div>
              </div>
            </template>
          </draggable>

          <div
            class="flex w-max cursor-pointer items-center text-sm text-gray-500 hover:text-black"
            @click="addAuthor"
          >
            <Icon icon="carbon:add" />
            <span class="flex items-center text-primary-600 hover:text-primary-500">
              Add an author
            </span>
            <form-help-content popoverContent="Add a developer of the software"></form-help-content>
          </div>
        </el-form-item>

        <el-form-item label="Categories" prop="categories">
          <el-tree-select
            v-model="figshareMetadataForm.categories"
            :data="categoryOptions"
            multiple
            clearable
            filterable
            :filter-node-method="categoriesFilterMethod"
            class="w-full"
          />
        </el-form-item>

        <el-form-item label="Keywords">
          <draggable
            tag="div"
            :list="figshareMetadataForm.keywords"
            item-key="id"
            handle=".handle"
            :animation="200"
            class="w-full"
          >
            <template #item="{ element }">
              <div class="mb-2 flex flex-row justify-between transition-all">
                <div class="flex w-11/12 flex-row justify-between">
                  <el-input
                    v-model="element.keyword"
                    type="text"
                    placeholder=""
                    v-on:keyup.enter="addKeyword"
                    :ref="element.id"
                  ></el-input>
                  <div class="mx-2"></div>
                </div>
                <div class="flex w-1/12 flex-row justify-evenly">
                  <div
                    class="handle flex items-center justify-center text-gray-400 hover:text-gray-700"
                  >
                    <Icon icon="ic:outline-drag-indicator" />
                  </div>
                  <div class="flex items-center justify-center text-gray-500 transition-all">
                    <el-popconfirm
                      title="Are you sure you want to remove this?"
                      icon-color="red"
                      confirm-button-text="Yes"
                      cancel-button-text="No"
                      @confirm="deleteKeyword(element.id)"
                    >
                      <template #reference>
                        <el-icon class="cursor-pointer hover:text-gray-800">
                          <delete-filled />
                        </el-icon>
                      </template>
                    </el-popconfirm>
                  </div>
                </div>
              </div>
            </template>
          </draggable>

          <div class="flex w-max cursor-pointer items-center text-gray-500 hover:text-black">
            <button
              class="flex items-center text-primary-600 hover:text-primary-500"
              @click="addKeyword(null, '')"
            >
              <Icon icon="carbon:add" /> Add a keyword
            </button>
          </div>
        </el-form-item>

        <el-form-item label="Funding">
          <draggable
            tag="div"
            :list="figshareMetadataForm.funding"
            item-key="id"
            :animation="200"
            handle=".handle"
            class="w-full"
          >
            <template #item="{ element }">
              <div class="mb-2 flex flex-row justify-between transition-all">
                <div class="flex w-11/12 flex-row justify-between">
                  <el-input v-model="element.funding" type="text" placeholder=""></el-input>
                  <div class="mx-2"></div>
                </div>
                <div class="flex w-1/12 flex-row justify-evenly">
                  <div
                    class="handle flex items-center justify-center text-gray-400 hover:text-gray-700"
                  >
                    <Icon icon="ic:outline-drag-indicator" />
                  </div>
                  <div class="flex items-center justify-center text-gray-500 transition-all">
                    <el-popconfirm
                      title="Are you sure you want to remove this?"
                      icon-color="red"
                      confirm-button-text="Yes"
                      cancel-button-text="No"
                      @confirm="deleteFunding(element.id)"
                    >
                      <template #reference>
                        <el-icon class="cursor-pointer hover:text-gray-800">
                          <delete-filled />
                        </el-icon>
                      </template>
                    </el-popconfirm>
                  </div>
                </div>
              </div>
            </template>
          </draggable>

          <div
            class="flex w-max cursor-pointer items-center text-gray-500 hover:text-black"
            @click="addFunding()"
          >
            <Icon icon="carbon:add" />
            <span class="flex items-center text-primary-600 hover:text-primary-500">
              Add {{ figshareMetadataForm.funding.length >= 1 ? "another" : "a" }} grant
            </span>
          </div>
        </el-form-item>

        <!-- filter this for urls and DOIs. -->
        <el-form-item label="References" prop="references">
          <draggable
            tag="div"
            :list="figshareMetadataForm.references"
            item-key="id"
            :animation="200"
            handle=".handle"
            class="w-full"
          >
            <template #item="{ element }">
              <div class="mb-2 flex flex-row justify-between transition-all">
                <div class="flex w-11/12 flex-row justify-between">
                  <el-input
                    v-model="element.reference"
                    type="text"
                    placeholder="http://fairdataihub.org"
                  ></el-input>
                  <div class="mx-2"></div>
                </div>
                <div class="flex w-1/12 flex-row justify-evenly pt-4">
                  <div
                    class="handle flex items-start justify-center text-gray-400 hover:text-gray-700"
                  >
                    <Icon icon="ic:outline-drag-indicator" />
                  </div>
                  <div class="flex items-start justify-center text-gray-500 transition-all">
                    <el-popconfirm
                      title="Are you sure you want to remove this?"
                      icon-color="red"
                      confirm-button-text="Yes"
                      cancel-button-text="No"
                      @confirm="deleteReference(element.id)"
                    >
                      <template #reference>
                        <el-icon class="cursor-pointer hover:text-gray-800">
                          <delete-filled />
                        </el-icon>
                      </template>
                    </el-popconfirm>
                  </div>
                </div>
              </div>
            </template>
          </draggable>

          <div
            class="flex w-max cursor-pointer items-center text-gray-500 hover:text-black"
            @click="addReference()"
          >
            <Icon icon="carbon:add" />
            <span class="flex items-center text-primary-600 hover:text-primary-500">
              Add a reference
            </span>
          </div>
        </el-form-item>

        <el-form-item label="License" prop="license">
          <el-select
            v-model="figshareMetadataForm.license.licenseName"
            filterable
            disabled
            placeholder="Select a license"
            class="w-full"
          >
            <el-option
              v-for="item in licenseOptions"
              :key="item.licenseId"
              :label="item.name"
              :value="item.licenseId"
            >
            </el-option>
          </el-select>
          <p class="pt-2 text-xs text-gray-500">
            Required. Selected license applies to all of your files that will be shared on Figshare.
            <br />
            If you want to upload some of your files under different licenses, please do so in
            separate uploads.
          </p>
        </el-form-item>
      </el-form>

      <div class="flex w-full flex-row justify-center space-x-4 py-6">
        <button class="primary-plain-button" @click="navigateBack">
          <el-icon><d-arrow-left /></el-icon> Back
        </button>

        <button class="primary-button" @click="addFigshareMetadata" :disabled="checkInvalidStatus">
          Continue <el-icon> <d-arrow-right /> </el-icon>
        </button>

        <warning-confirm
          ref="warningConfirm"
          title="Warning"
          @messageConfirmed="confirmNavigateBackSave('ok')"
          @messageCancel="confirmNavigateBackSave('cancel')"
          confirmButtonText="Save and go back"
          cancelButtonText="Don't save and go back"
        >
          <p class="text-center text-base text-gray-500">
            You have some unsaved changes. Do you want to save your edits?
          </p>
        </warning-confirm>
      </div>
    </div>
    <fade-transition>
      <div class="fixed bottom-1 right-2" v-if="savingSpinner">
        <Vue3Lottie
          :animationData="$helix_spinner"
          :width="60"
          :height="60"
          :loop="1"
          @onComplete="savingSpinner = false"
        />
      </div>
      <div v-else>
        <app-docs-link url="curate-and-share/figshare/add-figshare-metadata" position="bottom-4" />
      </div>
    </fade-transition>
  </div>
</template>

<script>
import { Icon } from "@iconify/vue";
import draggable from "vuedraggable";
import { v4 as uuidv4 } from "uuid";
import { ElMessage } from "element-plus";

import _ from "lodash";
import validator from "validator";

import { useDatasetsStore } from "@/store/datasets";
import figshareMetadataOptions from "@/assets/supplementalFiles/figshareMetadataOptions.json";

export default {
  name: "FigshareMetadata",
  components: {
    draggable,
    Icon,
  },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      dataset: {},
      workflowID: this.$route.params.workflowID,
      workflow: {},
      loading: true,
      savingSpinner: true,
      drag: true,
      licenseOptions: figshareMetadataOptions.licenseOptions,
      relatedIdentifierRelationships: figshareMetadataOptions.relatedIdentifierRelationships,
      relatedIdentifierTypes: figshareMetadataOptions.relatedIdentifierTypes,
      figshareMetadataForm: figshareMetadataOptions.defaultForm,
      categoryOptions: figshareMetadataOptions.categoryOptions,
      uploadTypeOptions: figshareMetadataOptions.uploadType,
      invalidStatus: {},
      rulesFigshareMetadataForm: {
        title: [
          {
            required: true,
            message: "Required.",
            trigger: "blur",
          },
        ],
        authors: [
          {
            required: true,
            validator: this.authorValidator,
            trigger: "blur",
          },
        ],
        description: [
          {
            required: true,
            message: "Required.",
            trigger: "blur",
          },
        ],
        license: [
          {
            required: true,
            message: "Required. Selected license applies to all of your files in the dataset.",
            trigger: "change",
          },
        ],
        references: [
          {
            required: false,
            validator: this.referencesValidator,
            trigger: "blur",
          },
        ],
        categories: [
          {
            required: true,
            message: "Required. Select at least one category.",
            trigger: "change",
          },
        ],
      },
      originalObject: {},
    };
  },
  computed: {
    dragOptions() {
      return {
        animation: 200,
        disabled: false,
      };
    },
    checkInvalidStatus() {
      if (this.$refs.fmForm) {
        this.$refs.fmForm.validate();
      }

      if (this.invalidStatus == {}) {
        return true;
      }

      for (const key in this.invalidStatus) {
        if (this.invalidStatus[key]) {
          return true;
        }
      }

      return false;
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
    focusOnElementRef(elementRef) {
      // check if element is available in 100ms intervals
      const interval = setInterval(() => {
        if (this.$refs[elementRef]) {
          this.$refs[elementRef].focus();
          clearInterval(interval);
        }
      }, 50);
    },
    filterArrayOfObjects(array, key) {
      return array.filter((element) => {
        return element[key] !== "";
      });
    },

    categoriesFilterMethod(value, data) {
      return data.label.toLowerCase().includes(value.toLowerCase());
    },

    authorValidator(_rule, value, callback) {
      if (value.length > 0) {
        for (let author of value) {
          if (
            author.givenName === undefined ||
            author.givenName.trim() === "" ||
            author.familyName === undefined ||
            author.familyName.trim() === ""
          ) {
            callback(new Error("First name and last name for each author is mandatory"));
            return;
          }

          // validate orcid
          if (author.orcid !== "") {
            const orcid = author.orcid;
            let total = 0;
            for (let i = 0; i < orcid.length - 1; i++) {
              const digit = parseInt(orcid.substr(i, 1));
              if (isNaN(digit)) {
                continue;
              }
              total = (total + digit) * 2;
            }

            const remainder = total % 11;
            const result = (12 - remainder) % 11;
            const checkDigit = result === 10 ? "X" : String(result);

            if (checkDigit !== orcid.substr(-1)) {
              callback(new Error("ORCID is not valid"));
            }
          }
        }
      } else {
        callback(new Error("Please provide at least one author"));
        return;
      }
      callback();
    },
    addAuthor(_event) {
      this.figshareMetadataForm.authors.push({
        name: "",
        affiliation: "",
        orcid: "",
        id: uuidv4(),
      });
    },
    deleteAuthor(id) {
      this.figshareMetadataForm.authors = this.figshareMetadataForm.authors.filter((author) => {
        return author.id !== id;
      });
    },

    addKeyword(_event, keyword = "") {
      if (this.figshareMetadataForm.keywords.some((el) => el.keyword === keyword)) {
        this.$message.warning("Keyword already exists.");
        return;
      }

      const id = uuidv4();
      this.figshareMetadataForm.keywords.push({
        keyword,
        id,
      });
      this.focusOnElementRef(id);
    },
    deleteKeyword(id) {
      this.figshareMetadataForm.keywords = this.figshareMetadataForm.keywords.filter((keyword) => {
        return keyword.id !== id;
      });
    },

    addFunding() {
      this.figshareMetadataForm.funding.push({
        funding: "",
        id: uuidv4(),
      });
    },
    deleteFunding(id) {
      this.figshareMetadataForm.funding = this.figshareMetadataForm.funding.filter((funding) => {
        return funding.id !== id;
      });
    },

    referencesValidator(_rule, value, callback) {
      if (value.length > 0) {
        for (let reference of value) {
          // validate reference
          if (reference.reference !== "") {
            const validIdentifier = validator.isURL(reference.reference);

            if (!validIdentifier) {
              this.invalidStatus.references = true;
              callback(new Error("Only URLs are allowed for references"));
              return;
            }
          }
        }
        this.invalidStatus.references = false;
        callback();
        return;
      } else {
        this.invalidStatus.references = false;
        callback();
        return;
      }
    },
    addReference() {
      this.figshareMetadataForm.references.push({
        reference: "",
        id: uuidv4(),
      });
    },
    deleteReference(id) {
      this.figshareMetadataForm.references = this.figshareMetadataForm.references.filter(
        (reference) => {
          return reference.id !== id;
        }
      );
    },

    addFigshareMetadata(_evt, shouldNavigateBack = false) {
      if (this.figshareMetadataForm.authors.length == 0) {
        ElMessage.error("Please add at least one author.");
      }

      if (this.figshareMetadataForm.license.licenseName === "") {
        ElMessage.error("Please select a license.");
        return;
      }

      this.$refs["fmForm"].validate(async (valid) => {
        if (valid) {
          this.workflow = this.dataset.workflows[this.workflowID];

          this.workflow.expandOptions = [];

          this.figshareMetadataForm.keywords = this.filterArrayOfObjects(
            this.figshareMetadataForm.keywords,
            "keyword"
          );
          this.figshareMetadataForm.funding = this.filterArrayOfObjects(
            this.figshareMetadataForm.funding,
            "funding"
          );
          this.figshareMetadataForm.references = this.filterArrayOfObjects(
            this.figshareMetadataForm.references,
            "reference"
          );

          this.workflow.destination.figshare.questions = this.figshareMetadataForm;
          this.datasetStore.updateCurrentDataset(this.dataset);
          this.datasetStore.syncDatasets();

          if (shouldNavigateBack) {
            this.$router.push(
              `/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/selectDestination`
            );
            return;
          }

          let routerPath = "";

          if ("source" in this.workflow) {
            if (this.workflow.source.type === "github") {
              routerPath = `/datasets/${this.datasetID}/${this.workflowID}/github/chooseUpload`;
            }
            if (this.workflow.source.type === "local") {
              routerPath = `/datasets/${this.datasetID}/${this.workflowID}/figshare/accessToken`;
            }
          } else {
            routerPath = `/datasets/${this.datasetID}/${this.workflowID}/figshare/accessToken`;
          }

          // const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/figshare/accessToken`;
          this.$router.push({ path: routerPath });
        } else {
          ElMessage.error("Please verify all fields are valid and try again.");
        }
      });

      //validate first
    },
    prefillFigshareQuestions() {
      if (
        "questions" in this.dataset.data.general &&
        Object.keys(this.dataset.data.general.questions).length !== 0
      ) {
        const generalForm = this.dataset.data.general.questions;

        if ("name" in generalForm) {
          this.figshareMetadataForm.title = generalForm.name;
        }

        if ("description" in generalForm) {
          this.figshareMetadataForm.description = generalForm.description;
        }

        if ("keywords" in generalForm) {
          this.figshareMetadataForm.keywords = [];
          generalForm.keywords.forEach((element) => {
            this.figshareMetadataForm.keywords.push({
              keyword: element.keyword,
              id: uuidv4(),
            });
          });
        }

        if ("license" in generalForm) {
          this.figshareMetadataForm.license.licenseName = generalForm.license;
        }

        if ("authors" in generalForm) {
          let authors = generalForm.authors;
          let newAuthors = [];
          authors.forEach((author) => {
            let newAuthor = {
              givenName: author.givenName,
              familyName: author.familyName,
              email: author.email,
              orcid: author.orcid,
              id: uuidv4(),
            };
            newAuthors.push(newAuthor);
          });
          this.figshareMetadataForm.authors = newAuthors;
        }

        // Will need to come back and this when we figure out how to add a new version to a figshare dataset
        // if (
        //   "newVersion" in this.workflow.destination.figshare &&
        //   this.workflow.destination.figshare.newVersion
        // ) {
        //   if (this.figshareMetadataForm.keywords.length == 0) {
        //     if ("keywords" in this.workflow.destination.figshare.selectedDeposition.metadata) {
        //       this.workflow.destination.figshare.selectedDeposition.metadata.keywords.forEach(
        //         (keyword) => {
        //           this.figshareMetadataForm.keywords.push({
        //             keyword,
        //             id: uuidv4(),
        //           });
        //         }
        //       );
        //     }
        //   }

        //   if (this.figshareMetadataForm.authors.length == 0) {
        //     if ("creators" in this.workflow.destination.figshare.selectedDeposition.metadata) {
        //       this.workflow.destination.figshare.selectedDeposition.metadata.creators.forEach(
        //         ({ name, affiliation, orcid }) => {
        //           this.figshareMetadataForm.authors.push({
        //             name,
        //             affiliation,
        //             orcid,
        //             id: uuidv4(),
        //           });
        //         }
        //       );
        //     }
        //   }

        //   if (this.figshareMetadataForm.contributors.length == 0) {
        //     if ("contributors" in this.workflow.destination.figshare.selectedDeposition.metadata) {
        //       this.workflow.destination.figshare.selectedDeposition.metadata.contributors.forEach(
        //         ({ name, type, affiliation, orcid }) => {
        //           this.figshareMetadataForm.contributors.push({
        //             name,
        //             contributorType: type,
        //             affiliation,
        //             orcid,
        //             id: uuidv4(),
        //           });
        //         }
        //       );
        //     }
        //   }

        //   if ("notes" in this.workflow.destination.figshare.selectedDeposition.metadata) {
        //     this.figshareMetadataForm.additionalNotes =
        //       this.workflow.destination.figshare.selectedDeposition.metadata.notes;
        //   }

        //   if (
        //     "related_identifiers" in this.workflow.destination.figshare.selectedDeposition.metadata
        //   ) {
        //     this.figshareMetadataForm.relatedIdentifiers = [];
        //     this.workflow.destination.figshare.selectedDeposition.metadata.related_identifiers.forEach(
        //       ({ identifier, relation, resource_type }) => {
        //         this.figshareMetadataForm.relatedIdentifiers.push({
        //           identifier,
        //           relationship: relation,
        //           resourceType: resource_type,
        //           id: uuidv4(),
        //         });
        //       }
        //     );
        //   }

        //   if ("references" in this.workflow.destination.figshare.selectedDeposition.metadata) {
        //     this.figshareMetadataForm.references = [];
        //     this.workflow.destination.figshare.selectedDeposition.metadata.references.forEach(
        //       (reference) => {
        //         this.figshareMetadataForm.references.push({
        //           reference,
        //           id: uuidv4(),
        //         });
        //       }
        //     );
        //   }

        //   if ("version" in this.workflow.destination.figshare.selectedDeposition.metadata) {
        //     this.figshareMetadataForm.version =
        //       this.workflow.destination.figshare.selectedDeposition.metadata.version;
        //   }
        //   if ("language" in this.workflow.destination.figshare.selectedDeposition.metadata) {
        //     this.figshareMetadataForm.language =
        //       this.workflow.destination.figshare.selectedDeposition.metadata.language;
        //   }

        //   if ("journal_title" in this.workflow.destination.figshare.selectedDeposition.metadata) {
        //     this.figshareMetadataForm.journal.title =
        //       this.workflow.destination.figshare.selectedDeposition.metadata.journal_title;
        //   }
        //   if ("journal_volume" in this.workflow.destination.figshare.selectedDeposition.metadata) {
        //     this.figshareMetadataForm.journal.volume =
        //       this.workflow.destination.figshare.selectedDeposition.metadata.journal_volume;
        //   }
        //   if ("journal_issue" in this.workflow.destination.figshare.selectedDeposition.metadata) {
        //     this.figshareMetadataForm.journal.issue =
        //       this.workflow.destination.figshare.selectedDeposition.metadata.journal_issue;
        //   }
        //   if ("journal_pages" in this.workflow.destination.figshare.selectedDeposition.metadata) {
        //     this.figshareMetadataForm.journal.pages =
        //       this.workflow.destination.figshare.selectedDeposition.metadata.journal_pages;
        //   }

        //   if ("conference_title" in this.workflow.destination.figshare.selectedDeposition.metadata) {
        //     this.figshareMetadataForm.conference.title =
        //       this.workflow.destination.figshare.selectedDeposition.metadata.conference_title;
        //   }
        //   if (
        //     "conference_acronym" in this.workflow.destination.figshare.selectedDeposition.metadata
        //   ) {
        //     this.figshareMetadataForm.conference.acronym =
        //       this.workflow.destination.figshare.selectedDeposition.metadata.conference_acronym;
        //   }
        //   // Will have to comeback to this one
        //   // if (
        //   //   "conference_dates" in
        //   //   this.workflow.destination.figshare.selectedDeposition.metadata
        //   // ) {
        //   //   this.figshareMetadataForm.conference.dates =
        //   //     this.workflow.destination.figshare.selectedDeposition.metadata.conference_dates;
        //   // }
        //   if ("conference_place" in this.workflow.destination.figshare.selectedDeposition.metadata) {
        //     this.figshareMetadataForm.conference.place =
        //       this.workflow.destination.figshare.selectedDeposition.metadata.conference_place;
        //   }
        //   if ("conference_url" in this.workflow.destination.figshare.selectedDeposition.metadata) {
        //     this.figshareMetadataForm.conference.website =
        //       this.workflow.destination.figshare.selectedDeposition.metadata.conference_url;
        //   }
        //   if (
        //     "conference_session" in this.workflow.destination.figshare.selectedDeposition.metadata
        //   ) {
        //     this.figshareMetadataForm.conference.session =
        //       this.workflow.destination.figshare.selectedDeposition.metadata.conference_session;
        //   }
        //   if (
        //     "conference_session_part" in
        //     this.workflow.destination.figshare.selectedDeposition.metadata
        //   ) {
        //     this.figshareMetadataForm.conference.part =
        //       this.workflow.destination.figshare.selectedDeposition.metadata.conference_session_part;
        //   }

        //   if ("imprint_publisher" in this.workflow.destination.figshare.selectedDeposition.metadata) {
        //     this.figshareMetadataForm.bookReportChapter.publisher =
        //       this.workflow.destination.figshare.selectedDeposition.metadata.imprint_publisher;
        //   }
        //   if ("imprint_isbn" in this.workflow.destination.figshare.selectedDeposition.metadata) {
        //     this.figshareMetadataForm.bookReportChapter.isbn =
        //       this.workflow.destination.figshare.selectedDeposition.metadata.imprint_isbn;
        //   }
        //   if ("imprint_place" in this.workflow.destination.figshare.selectedDeposition.metadata) {
        //     this.figshareMetadataForm.bookReportChapter.place =
        //       this.workflow.destination.figshare.selectedDeposition.metadata.imprint_place;
        //   }
        //   if ("partof_title" in this.workflow.destination.figshare.selectedDeposition.metadata) {
        //     this.figshareMetadataForm.bookReportChapter.title =
        //       this.workflow.destination.figshare.selectedDeposition.metadata.partof_title;
        //   }
        //   if ("partof_pages" in this.workflow.destination.figshare.selectedDeposition.metadata) {
        //     this.figshareMetadataForm.bookReportChapter.pages =
        //       this.workflow.destination.figshare.selectedDeposition.metadata.partof_pages;
        //   }

        //   if ("thesis_university" in this.workflow.destination.figshare.selectedDeposition.metadata) {
        //     this.figshareMetadataForm.thesis.awardingUniversity =
        //       this.workflow.destination.figshare.selectedDeposition.metadata.thesis_university;
        //   }
        //   if (
        //     "thesis_supervisors" in this.workflow.destination.figshare.selectedDeposition.metadata
        //   ) {
        //     this.figshareMetadataForm.thesis.supervisors = [];
        //     this.workflow.destination.figshare.selectedDeposition.metadata.thesis_supervisors.forEach(
        //       ({ name, affiliation, orcid }) => {
        //         this.figshareMetadataForm.thesis.supervisors.push({
        //           name,
        //           affiliation,
        //           orcid,
        //           id: uuidv4(),
        //         });
        //       }
        //     );
        //   }

        //   if ("subjects" in this.workflow.destination.figshare.selectedDeposition.metadata) {
        //     this.figshareMetadataForm.subjects = [];
        //     this.workflow.destination.figshare.selectedDeposition.metadata.subjects.forEach(
        //       ({ term, identifier }) => {
        //         this.figshareMetadataForm.subjects.push({
        //           term,
        //           identifier,
        //           id: uuidv4(),
        //         });
        //       }
        //     );
        //   }
        // }
      }
    },
    confirmNavigateBackSave(response) {
      if (response == "ok") {
        // save changes
        this.addFigshareMetadata(true, true);
      } else if (response == "cancel") {
        // don't save changes
        this.$router.push({
          path: `/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/selectDestination`,
        });
      }
    },
    navigateBack() {
      let newChanges = false;

      if (!_.isEqual(this.originalObject, this.figshareMetadataForm)) {
        newChanges = true;
      }

      if (newChanges) {
        this.$refs.warningConfirm.show();
      } else {
        this.$router.push({
          path: `/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/selectDestination`,
        });
      }
    },
  },
  watch: {},
  async mounted() {
    this.loading = this.$loading({
      lock: true,
      text: "Loading",
      fullscreen: true,
      background: "rgba(0, 0, 0, 0.7)",
    });

    this.figshareMetadataForm = figshareMetadataOptions.defaultForm;

    this.dataset = JSON.parse(JSON.stringify(await this.datasetStore.getCurrentDataset()));

    this.workflow = this.dataset.workflows[this.workflowID];

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(5);

    this.workflow.currentRoute = this.$route.path;

    if (
      this.workflow.destination.figshare.questions &&
      Object.keys(this.workflow.destination.figshare.questions).length !== 0
    ) {
      this.figshareMetadataForm = this.workflow.destination.figshare.questions;

      this.initializeEmptyObjects(this.figshareMetadataForm, this.figshareMetadataForm.license);

      const generalForm = this.dataset.data.general.questions;
      this.figshareMetadataForm.license.licenseName = generalForm.license;

      this.addIds(this.figshareMetadataForm.authors);
      this.addIds(this.figshareMetadataForm.keywords);
      this.addIds(this.figshareMetadataForm.references);
      this.addIds(this.figshareMetadataForm.funding);

      this.loading.close();

      this.originalObject = JSON.parse(JSON.stringify(this.figshareMetadataForm));
    } else {
      this.prefillFigshareQuestions();

      this.originalObject = JSON.parse(JSON.stringify(this.figshareMetadataForm));

      this.loading.close();
    }

    // Add the functions here to check the pre saved values for on mounted.
    // decide if the intermdiate data is saved in workflow or data.
  },
};
// CHANGE TO ONE FORM SINCE THAT iS BETTER
</script>

<style lang="postcss" scoped>
.handle {
  cursor: move;
}

.el-select-group > .el-select-dropdown__item {
  margin-left: 5px;
}
</style>
