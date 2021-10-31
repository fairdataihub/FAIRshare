<template>
  <div
    class="
      h-screen
      w-full
      flex flex-row
      lg:justify-center
      items-center
      overflow-y-auto
    "
  >
    <div class="p-3 h-full flex flex-row items-center">
      <div class="h-full w-full">
        <div class="flex flex-col h-full pr-5">
          <span class="text-lg font-medium text-left"> Zenodo Metadata </span>
          <span class="text-left"> Lets upload your data to Zenodo. </span>

          <line-divider></line-divider>

          <span class="mb-2">
            Before we send this data over, Zenodo requires some metadata from
            you. We have filled any information we have learned from the data as
            well as your previous metadata.
          </span>

          <el-form
            :model="zenodoMetadataForm"
            label-width="150px"
            label-position="right"
            size="mini"
            @submit.prevent
          >
            <el-collapse v-model="activeNames">
              <el-collapse-item
                class="text-lg"
                title="Basic Information"
                name="basicInformation"
              >
                <div>
                  <el-form-item label="Publication Date">
                    <el-date-picker
                      v-model="zenodoMetadataForm.publicationDate"
                      type="date"
                      placeholder="Pick a day"
                    >
                    </el-date-picker>
                  </el-form-item>

                  <el-form-item label="Title">
                    <el-popover
                      ref="popover"
                      placement="bottom"
                      :width="300"
                      trigger="manual"
                    >
                      <template #reference>
                        <el-input
                          v-model="zenodoMetadataForm.title"
                          type="text"
                        ></el-input>
                      </template>

                      <span class="break-normal text-left text-sm">
                        Use a description that is easily identifiable. This will
                        be shown in the dataset selection screen and is not part
                        of your submitted metadata.
                      </span>
                    </el-popover>
                  </el-form-item>

                  <!-- Add authors table thing -->

                  <el-form-item label="Description">
                    <el-popover
                      ref="popover"
                      placement="bottom"
                      :width="300"
                      trigger="hover"
                      content=""
                    >
                      <template #reference>
                        <el-input
                          v-model="zenodoMetadataForm.description"
                          type="textarea"
                        ></el-input>
                      </template>

                      <span class="break-normal text-left text-sm">
                        Use a description that is easily identifiable. This will
                        be shown in the dataset selection screen and is not part
                        of your submitted metadata.
                      </span>
                    </el-popover>
                  </el-form-item>

                  <el-form-item label="Version">
                    <el-popover
                      ref="popover"
                      placement="bottom"
                      :width="300"
                      trigger="hover"
                      content=""
                    >
                      <template #reference>
                        <el-input
                          v-model="zenodoMetadataForm.version"
                          type="text"
                        ></el-input>
                      </template>

                      <span class="break-normal text-left text-sm">
                        Optional. Mostly relevant for software and dataset
                        uploads. Any string will be accepted, but
                        semantically-versioned tag is recommended. <br />
                        See
                        <a href="https://semver.org/" target="_blank">
                          semver.org
                        </a>
                        for more information on semantic versioning.
                      </span>
                    </el-popover>
                  </el-form-item>

                  <el-form-item label="Language">
                    <el-popover
                      ref="popover"
                      placement="bottom"
                      :width="300"
                      trigger="manual"
                    >
                      <template #reference>
                        <el-input
                          v-model="zenodoMetadataForm.language"
                          type="text"
                          placeholder="e.g.: 'eng', 'fr' or 'Polish'"
                        ></el-input>
                      </template>

                      <span class="break-normal text-left text-sm">
                        Optional. Primary language of the record. Start by
                        typing the language's common name in English, or its ISO
                        639 code (two or three-letter code).
                        <br />
                        See
                        <a href="https://semver.org/" target="_blank">
                          ISO 639 language codes list
                        </a>
                        for more information.
                      </span>
                    </el-popover>
                  </el-form-item>

                  <el-form-item label="Additional Notes">
                    <el-input
                      v-model="zenodoMetadataForm.additionalNotes"
                      type="text"
                    ></el-input>
                  </el-form-item>
                </div>
              </el-collapse-item>
              <el-collapse-item title="License" name="license">
                <div>
                  <el-form-item label="Access right">
                    <div class="flex flex-col">
                      <el-radio-group
                        v-model="zenodoMetadataForm.license.accessRight"
                        class="flex flex-col"
                      >
                        <el-radio label="openAccess">
                          <el-icon>
                            <unlock />
                          </el-icon>
                          Open Access
                        </el-radio>
                        <el-radio label="embargoedAccess" disabled>
                          <el-icon> <remove-filled /> </el-icon> Embargoed
                          Access
                        </el-radio>
                        <el-radio label="restrictedAccess" disabled>
                          <el-icon>
                            <key />
                          </el-icon>
                          Restricted Access
                        </el-radio>
                        <el-radio label="closedAccess" disabled>
                          <el-icon>
                            <lock />
                          </el-icon>
                          Closed Access
                        </el-radio>
                      </el-radio-group>
                      <p class="text-xs pt-2 text-gray-500">
                        Required. Open access uploads have considerably higher
                        visibility on Zenodo.
                      </p>
                    </div>
                  </el-form-item>

                  <el-form-item label="Access right">
                    <div class="flex flex-col">
                      <el-select
                        v-model="zenodoMetadataForm.license.licenseName"
                        filterable
                        placeholder="Select a license"
                      >
                        <el-option
                          v-for="item in licenseOptions"
                          :key="item.value"
                          :label="item.label"
                          :value="item.value"
                        >
                        </el-option>
                      </el-select>
                      <p class="text-xs pt-2 text-gray-500">
                        Required. Selected license applies to all of your files
                        displayed on the top of the form. If you want to upload
                        some of your files under different licenses, please do
                        so in separate uploads. If you cannot find the license
                        you're looking for, include a relevant LICENSE file in
                        your record and choose one of the
                        <span class="italic"> Other </span> licenses available
                        <span class="italic">
                          (Other (Open), Other (Attribution) </span
                        >, etc.). The supported licenses in the list are
                        harvested from
                        <a
                          href="https://opendefinition.org/"
                          target="_blank"
                          class="text-blue-500 hover:underline"
                        >
                          opendefinition.org
                        </a>
                        and
                        <a
                          href="https://spdx.org/"
                          target="_blank"
                          class="text-blue-500 hover:underline"
                        >
                          spdx.org
                        </a>
                        .
                      </p>
                    </div>
                  </el-form-item>
                  <el-form-item label=""> </el-form-item>
                </div>
              </el-collapse-item>
              <el-collapse-item title="Funding" name="funding">
                <span class="text-xs">
                  Zenodo is integrated into reporting lines for research funded
                  by the European Commission via OpenAIRE. Specify grants which
                  have funded your research, and we will let your funding agency
                  know!
                </span>
                <div>
                  <p class="text-xs pt-2 text-gray-500">
                    Optional. OpenAIRE-supported projects only. For other
                    funding acknowledgements, please use the Additional Notes
                    field. Note: a human Zenodo curator will need to validate
                    your upload - you may experience a delay before it is
                    available in OpenAIRE.
                  </p>
                </div>
              </el-collapse-item>
              <el-collapse-item
                title="Related/alternate identifiers"
                name="relatedIdentifiers"
              >
                <span class="text-xs">
                  Specify identifiers of related publications and datasets.
                  Supported identifiers include: DOI, Handle, ARK, PURL, ISSN,
                  ISBN, PubMed ID, PubMed Central ID, ADS Bibliographic Code,
                  arXiv, Life Science Identifiers (LSID), EAN-13, ISTC, URNs and
                  URLs.
                </span>
                <div></div>
              </el-collapse-item>
              <el-collapse-item title="Contributors" name="contributors">
                <div></div>
              </el-collapse-item>
              <el-collapse-item title="References" name="references">
                <div></div>
              </el-collapse-item>
              <el-collapse-item title="Journal" name="journal">
                <div>
                  <el-form-item label="Journal title">
                    <el-input
                      v-model="zenodoMetadataForm.journal.title"
                      type="text"
                    ></el-input>
                  </el-form-item>
                  <el-form-item label="Volume">
                    <el-input
                      v-model="zenodoMetadataForm.journal.volume"
                      type="text"
                    ></el-input>
                  </el-form-item>
                  <el-form-item label="Issue">
                    <el-input
                      v-model="zenodoMetadataForm.journal.issue"
                      type="text"
                    ></el-input>
                  </el-form-item>
                  <el-form-item label="Pages">
                    <el-input
                      v-model="zenodoMetadataForm.journal.pages"
                      type="text"
                    ></el-input>
                  </el-form-item>
                </div>
              </el-collapse-item>
              <el-collapse-item title="Conference" name="conference">
                <div>
                  <el-form-item label="Conference title">
                    <el-input
                      v-model="zenodoMetadataForm.conference.title"
                      type="text"
                    ></el-input>
                  </el-form-item>
                  <el-form-item label="Acronym">
                    <el-input
                      v-model="zenodoMetadataForm.conference.acronym"
                      type="text"
                    ></el-input>
                  </el-form-item>
                  <el-form-item label="Dates">
                    <el-date-picker
                      v-model="zenodoMetadataForm.conference.dates"
                      type="daterange"
                      range-separator="-"
                      start-placeholder="Start date"
                      end-placeholder="End date"
                      size="medium"
                    >
                    </el-date-picker>
                  </el-form-item>
                  <el-form-item label="Place">
                    <el-input
                      v-model="zenodoMetadataForm.conference.place"
                      type="text"
                      placeholder="e.g. city, country"
                    ></el-input>
                  </el-form-item>
                  <el-form-item label="Website">
                    <el-input
                      v-model="zenodoMetadataForm.conference.website"
                      type="text"
                      placeholder="e.g. http://zenodo.org"
                    ></el-input>
                  </el-form-item>
                  <el-form-item label="Session">
                    <div class="flex flex-col">
                      <el-input
                        v-model="zenodoMetadataForm.conference.session"
                        type="text"
                        placeholder="e.g. VI"
                      ></el-input>
                      <p class="text-xs pt-2 text-gray-500">
                        Optional. Number of session within the conference.
                      </p>
                    </div>
                  </el-form-item>
                  <el-form-item label="Part">
                    <div class="flex flex-col">
                      <el-input
                        v-model="zenodoMetadataForm.conference.part"
                        type="text"
                        placeholder="e.g. 1"
                      ></el-input>
                      <p class="text-xs pt-2 text-gray-500">
                        Optional. Number of part within a session.
                      </p>
                    </div>
                  </el-form-item>
                </div>
              </el-collapse-item>
              <el-collapse-item
                title="Book/Report/Chapter"
                name="bookReportChapter"
              >
                <span class="text-xs"> For parts of books and reports. </span>
                <div>
                  <el-form-item label="Publisher">
                    <el-input
                      v-model="zenodoMetadataForm.bookReportChapter.publisher"
                      type="text"
                    ></el-input>
                  </el-form-item>
                  <el-form-item label="Place">
                    <el-input
                      v-model="zenodoMetadataForm.bookReportChapter.place"
                      type="text"
                      placeholder="e.g. city, country"
                    ></el-input>
                  </el-form-item>
                  <el-form-item label="ISBN">
                    <el-input
                      v-model="zenodoMetadataForm.bookReportChapter.isbn"
                      type="text"
                      placeholder="e.g. 0-06-251587-X"
                    ></el-input>
                  </el-form-item>
                  <el-form-item label="Book title">
                    <div class="flex flex-col">
                      <el-input
                        v-model="zenodoMetadataForm.bookReportChapter.bookTitle"
                        type="text"
                      ></el-input>
                      <p class="text-xs pt-2 text-gray-500">
                        Optional. Title of the book or report which this upload
                        is part of.
                      </p>
                    </div>
                  </el-form-item>
                  <el-form-item label="Pages">
                    <el-input
                      v-model="zenodoMetadataForm.bookReportChapter.pages"
                      type="text"
                    ></el-input>
                  </el-form-item>
                </div>
              </el-collapse-item>
              <el-collapse-item title="Thesis" name="thesis">
                <div>
                  <el-form-item label="Awarding university">
                    <el-input
                      v-model="zenodoMetadataForm.thesis.awardingUniversity"
                      type="text"
                    ></el-input>
                  </el-form-item>
                </div>
              </el-collapse-item>
              <el-collapse-item title="Subjects" name="subjects">
                <p class="text-xs mb-4">
                  Specify subjects from a taxonomy or controlled vocabulary.
                  Each term must be uniquely identified (e.g. a URL). For free
                  form text, use the keywords field in basic information
                  section.
                  <br />
                </p>
                <div>
                  <el-form-item label="Awarding university">
                    <draggable
                      v-model="zenodoMetadataForm.subjects"
                      v-bind="dragOptions"
                      tag="transition-group"
                      @start="drag = true"
                      @end="drag = false"
                      item-key="term"
                    >
                      <template #item="{ element }">
                        <div class="flex flex-row mb-2 justify-evenly">
                          <div class="pr-5">
                            <el-input
                              v-model="element.term"
                              type="text"
                            ></el-input>
                          </div>
                          <div class="pl-5">
                            <el-input
                              v-model="element.identifier"
                              type="text"
                            ></el-input>
                          </div>
                        </div>
                      </template>
                    </draggable>
                  </el-form-item>
                </div>
              </el-collapse-item>
            </el-collapse>
          </el-form>

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
// import { Icon } from "@iconify/vue";
import {
  ArrowRightBold,
  Lock,
  Unlock,
  RemoveFilled,
  Key,
} from "@element-plus/icons";
import draggable from "vuedraggable";

import { useDatasetsStore } from "../store/datasets";

// const message = [
//   "vue.draggable",
//   "draggable",
//   "component",
//   "for",
//   "vue.js 2.0",
//   "based",
//   "on",
//   "Sortablejs",
// ];

export default {
  name: "DatasetsCurateZenodoMetadata",
  components: { ArrowRightBold, Lock, Unlock, RemoveFilled, Key, draggable },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      dataset: {},
      workflowID: this.$route.params.workflowID,
      workflow: {},
      activeNames: ["basicInformation", "license", "subjects"],
      drag: false,
      licenseOptions: [
        {
          value: "CC0-1.0",
          label: "CC0 1.0 Universal (CC0 1.0) - Attribution",
        },
        {
          value: "CC-BY-4.0",
          label: "CC BY 4.0 Attribution (CC BY 4.0)",
        },
      ],
      zenodoMetadataForm: {
        publicationDate: "",
        title: "",
        authors: [],
        description: "",
        version: "",
        language: "",
        keywords: [],
        additionalNotes: "",
        license: {
          accessRight: "openAccess",
          licenseName: "",
          embargoDate: "",
          conditions: "",
        },
        grants: [
          {
            grantInstitution: "",
            grantName: "",
          },
        ],
        relatedIdentifier: [
          {
            identifier: "",
            relatedIdentifierType: "",
            resourceType: "",
          },
        ],
        contributors: [
          {
            contributorType: "",
            name: "",
            affiliation: "",
            orcid: "",
          },
        ],
        references: [],
        journal: {
          title: "",
          volume: "",
          issue: "",
          pages: "",
          year: "",
        },
        conference: {
          title: "",
          acronym: "",
          dates: "",
          place: "",
          website: "",
          session: "",
          part: "",
        },
        bookReportChapter: {
          publisher: "",
          place: "",
          isbn: "",
          bookTitle: "",
          pages: "",
        },
        thesis: {
          awardingUniversity: "",
          supervisors: [{ name: "", affiliation: "", orcid: "" }],
        },
        subjects: [
          {
            term: "term1",
            identifier: "identifier2",
          },
          {
            term: "term2",
            identifier: "identifier2",
          },
          {
            term: "term3",
            identifier: "identifier3",
          },
        ],
      },
    };
  },
  computed: {
    dragOptions() {
      return {
        animation: 200,
        group: "description",
        disabled: false,
      };
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
    // decide if the intermdiate data is saved in workflow or data.
  },
};
// CHANGE TO ONE FORM SINCE THAT iS BETTER
</script>

<style lang="postcss"></style>
