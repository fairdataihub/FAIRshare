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
    <div class="w-full p-3 h-full flex flex-row items-center">
      <div class="h-full w-full">
        <div class="w-full flex flex-col h-full pr-5">
          <workflow-progress-bar :currentStep="4" />

          <span class="text-lg font-medium text-left"> Zenodo Metadata </span>
          <span class="text-left"> Lets upload your data to Zenodo. </span>

          <line-divider></line-divider>

          <div class="my-2">
            <el-descriptions
              class="margin-top"
              title="Basic Information"
              size="small"
              border
            >
              <template #extra>
                <el-button
                  type="primary"
                  @click="editInformation(['basicInformation', 'license'])"
                  class="ml-2"
                >
                  Edit basic information
                </el-button>
              </template>
              <el-descriptions-item>
                <template #label> Publication Date </template>
                {{ displayPublicationDate }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Title </template>
                {{ zenodoMetadata.title }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Authors </template>

                <div>
                  <ul class="list-disc list-inside">
                    <li
                      v-for="author in zenodoMetadata.authors"
                      :key="author.id"
                    >
                      Name: {{ author.name }}
                      <ul class="ml-6">
                        <li>Affiliation: {{ author.affiliation }}</li>
                        <li>ORCID: {{ author.orcid }}</li>
                      </ul>
                    </li>
                  </ul>
                </div>
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Keywords </template>
                <div>
                  <el-tag
                    size="medium"
                    v-for="element in zenodoMetadata.keywords"
                    :key="element.id"
                    class="mx-1"
                  >
                    {{ element.keyword }}</el-tag
                  >
                </div>
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Description </template>
                {{ zenodoMetadata.description }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Language </template>
                {{ displayLanguage }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Access right </template>
                {{ zenodoMetadata.license.accessRight }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> License </template>
                {{ zenodoMetadata.license.licenseName }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Version </template>
                {{ zenodoMetadata.version }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Additional notes </template>
                {{ zenodoMetadata.additionalNotes }}
              </el-descriptions-item>
            </el-descriptions>
          </div>

          <div class="my-2" v-if="showRelatedAlternateIdentifiers">
            <el-descriptions
              class="margin-top"
              title="Related/alternate identifiers"
              direction="vertical"
              size="small"
              border
            >
              <template #extra>
                <el-button
                  type="primary"
                  @click="editInformation(['relatedIdentifiers'])"
                  class="ml-2"
                >
                  Edit related/alternate identifiers
                </el-button>
              </template>
              <el-descriptions-item>
                <template #label> Related/alternate identifiers </template>

                <div>
                  <ul class="list-disc list-inside">
                    <li
                      v-for="element in zenodoMetadata.relatedIdentifiers"
                      :key="element.id"
                    >
                      Identifier: {{ element.identifier }}
                      <ul class="ml-6">
                        <li>Relationship: {{ element.relationship }}</li>
                        <li>Type: {{ element.resourceType }}</li>
                      </ul>
                    </li>
                  </ul>
                </div>
              </el-descriptions-item>
            </el-descriptions>
          </div>

          <div class="my-2" v-if="showContributors">
            <el-descriptions
              class="margin-top"
              title="Contributors"
              direction="vertical"
              size="small"
              border
            >
              <template #extra>
                <el-button
                  type="primary"
                  @click="editInformation(['contributors'])"
                  class="ml-2"
                >
                  Edit contributors
                </el-button>
              </template>
              <el-descriptions-item>
                <template #label> Contributors </template>

                <div>
                  <ul class="list-disc list-inside">
                    <li
                      v-for="contributor in zenodoMetadata.contributors"
                      :key="contributor.id"
                    >
                      Name: {{ contributor.name }}
                      <ul class="ml-6">
                        <li>Affiliation: {{ contributor.affiliation }}</li>
                        <li>ORCID: {{ contributor.orcid }}</li>
                        <li>Type: {{ contributor.contributorType }}</li>
                      </ul>
                    </li>
                  </ul>
                </div>
              </el-descriptions-item>
            </el-descriptions>
          </div>

          <div class="my-2" v-if="showReferences">
            <el-descriptions
              class="margin-top"
              title="References"
              direction="vertical"
              size="small"
              border
            >
              <template #extra>
                <el-button
                  type="primary"
                  @click="editInformation(['references'])"
                  class="ml-2"
                >
                  Edit references
                </el-button>
              </template>
              <el-descriptions-item>
                <template #label> References </template>
                <div class="flex flex-col">
                  <span
                    v-for="reference in zenodoMetadata.references"
                    :key="reference.id"
                    class="mb-2"
                  >
                    {{ reference.reference }}
                  </span>
                </div>
              </el-descriptions-item>
            </el-descriptions>
          </div>

          <div class="my-2" v-if="showJournal">
            <el-descriptions
              class="margin-top"
              title="Journal"
              size="small"
              border
            >
              <template #extra>
                <el-button
                  type="primary"
                  @click="editInformation(['journal'])"
                  class="ml-2"
                >
                  Edit journal information
                </el-button>
              </template>
              <el-descriptions-item>
                <template #label> Title </template>
                {{ zenodoMetadata.journal.title }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Volume </template>
                {{ zenodoMetadata.journal.volume }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Issue </template>
                {{ zenodoMetadata.journal.issue }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Pages </template>
                {{ zenodoMetadata.journal.pages }}
              </el-descriptions-item>
            </el-descriptions>
          </div>

          <div class="my-2" v-if="showConference">
            <el-descriptions
              class="margin-top"
              title="Conference"
              size="small"
              border
            >
              <template #extra>
                <el-button
                  type="primary"
                  @click="editInformation(['conference'])"
                  class="ml-2"
                >
                  Edit conference information
                </el-button>
              </template>
              <el-descriptions-item>
                <template #label> Title </template>
                {{ zenodoMetadata.conference.title }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Acronym </template>
                {{ zenodoMetadata.conference.acronym }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Dates </template>
                {{ displayConferenceDate }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Place </template>
                {{ zenodoMetadata.conference.place }}
              </el-descriptions-item>

              <el-descriptions-item>
                <template #label> Session </template>
                {{ zenodoMetadata.conference.session }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Part </template>
                {{ zenodoMetadata.conference.part }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Website </template>
                {{ zenodoMetadata.conference.website }}
              </el-descriptions-item>
            </el-descriptions>
          </div>

          <div class="my-2" v-if="showBookReportChapter">
            <el-descriptions
              class="margin-top"
              title="Book/report/chapter"
              size="small"
              border
            >
              <template #extra>
                <el-button
                  type="primary"
                  @click="editInformation(['bookReportChapter'])"
                  class="ml-2"
                >
                  Edit book/report/chapter information
                </el-button>
              </template>
              <el-descriptions-item>
                <template #label> Title </template>
                {{ zenodoMetadata.bookReportChapter.title }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Publisher </template>
                {{ zenodoMetadata.bookReportChapter.publisher }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> ISBN </template>
                {{ zenodoMetadata.bookReportChapter.isbn }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Pages </template>
                {{ zenodoMetadata.bookReportChapter.pages }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Place </template>
                {{ zenodoMetadata.bookReportChapter.place }}
              </el-descriptions-item>
            </el-descriptions>
          </div>

          <div class="my-2" v-if="showThesis">
            <el-descriptions
              class="margin-top"
              title="Thesis"
              size="small"
              border
            >
              <template #extra>
                <el-button
                  type="primary"
                  @click="editInformation(['thesis'])"
                  class="ml-2"
                >
                  Edit thesis information
                </el-button>
              </template>
              <el-descriptions-item>
                <template #label> Awarding University </template>
                {{ zenodoMetadata.thesis.awardingUniversity }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Supervisors </template>

                <div>
                  <ul class="list-disc list-inside">
                    <li
                      v-for="supervisor in zenodoMetadata.thesis.supervisors"
                      :key="supervisor.id"
                    >
                      Name: {{ supervisor.name }}
                      <ul class="ml-6">
                        <li>Affiliation: {{ supervisor.affiliation }}</li>
                        <li>ORCID: {{ supervisor.orcid }}</li>
                      </ul>
                    </li>
                  </ul>
                </div>
              </el-descriptions-item>
            </el-descriptions>
          </div>

          <div class="my-2 mb-6" v-if="showSubjects">
            <el-descriptions
              class="margin-top"
              title="Subjects"
              direction="vertical"
              size="small"
              border
            >
              <template #extra>
                <el-button
                  type="primary"
                  @click="editInformation(['subjects'])"
                  class="ml-2"
                >
                  Edit subjects
                </el-button>
              </template>
              <el-descriptions-item>
                <template #label> Subjects </template>
                <div class="flex flex-col">
                  <span
                    v-for="subject in zenodoMetadata.subjects"
                    :key="subject.id"
                    class="mb-2"
                  >
                    {{ subject.term }} - {{ subject.identifier }}
                  </span>
                </div>
              </el-descriptions-item>
            </el-descriptions>
          </div>

          <div class="w-full flex flex-row justify-center py-2">
            <router-link
              :to="`/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/zenodo/metadata`"
              class="mx-6"
            >
              <el-button type="danger" plain> Back </el-button>
            </router-link>

            <el-button
              type="primary"
              class="flex flex-row items-center"
              @click="checkZenodoAccessToken"
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
import { ArrowRightBold } from "@element-plus/icons";
import { ElLoading } from "element-plus";
import dayjs from "dayjs";

import { useDatasetsStore } from "../../store/datasets";
import languagesJson from "../../assets/supplementalFiles/zenodoLanguages.json";

export default {
  name: "ZenodoMetadataReview",
  components: {
    ArrowRightBold,
  },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      dataset: {},
      workflowID: this.$route.params.workflowID,
      datasetID: this.$route.params.datasetID,
      workflow: {},
      loading: "",
      zenodoMetadata: {
        license: {},
        journal: {},
        conference: {},
        bookReportChapter: {},
        thesis: {},
      },
      languageOptions: languagesJson.languages,
    };
  },
  computed: {
    displayLanguage() {
      const that = this;

      function getLanguage(language) {
        return that.languageOptions.find((lang) => lang.alpha3 === language);
      }

      if (
        "language" in this.zenodoMetadata &&
        this.zenodoMetadata.language != ""
      ) {
        const lang = this.zenodoMetadata.language;
        const returnVal = getLanguage(lang);
        return `${returnVal.name} (${returnVal.alpha3})`;
      } else {
        return "";
      }
    },
    displayPublicationDate() {
      if (
        "publicationDate" in this.zenodoMetadata &&
        this.zenodoMetadata.publicationDate != ""
      ) {
        const date = this.zenodoMetadata.publicationDate;
        return dayjs(date).format("MMMM D, YYYY");
      } else {
        return "";
      }
    },
    displayConferenceDate() {
      if (
        "conference" in this.zenodoMetadata &&
        "dates" in this.zenodoMetadata.conference &&
        this.zenodoMetadata.conference.dates.length == 2
      ) {
        return (
          dayjs(this.zenodoMetadata.conference.dates[0]).format(
            "MMMM D, YYYY"
          ) +
          " - " +
          dayjs(this.zenodoMetadata.conference.dates[1]).format("MMMM D, YYYY")
        );
      } else {
        return "";
      }
    },
    showRelatedAlternateIdentifiers() {
      if (
        "relatedAlternateIdentifiers" in this.zenodoMetadata &&
        this.zenodoMetadata.relatedAlternateIdentifiers.length > 0
      ) {
        return true;
      } else {
        return false;
      }
    },
    showContributors() {
      if (
        "contributors" in this.zenodoMetadata &&
        this.zenodoMetadata.contributors.length > 0
      ) {
        return true;
      } else {
        return false;
      }
    },
    showReferences() {
      if (
        "references" in this.zenodoMetadata &&
        this.zenodoMetadata.references.length > 0
      ) {
        return true;
      } else {
        return false;
      }
    },
    showJournal() {
      if (
        "journal" in this.zenodoMetadata &&
        (this.zenodoMetadata.journal.title != "" ||
          this.zenodoMetadata.journal.volume != "" ||
          this.zenodoMetadata.journal.issue != "" ||
          this.zenodoMetadata.journal.pages != "")
      ) {
        return true;
      } else {
        return false;
      }
    },
    showConference() {
      if (
        "conference" in this.zenodoMetadata &&
        "dates" in this.zenodoMetadata.conference &&
        (this.zenodoMetadata.conference.title != "" ||
          this.zenodoMetadata.conference.acronym != "" ||
          this.zenodoMetadata.conference.dates.length == 2 ||
          this.zenodoMetadata.conference.place != "" ||
          this.zenodoMetadata.conference.website != "" ||
          this.zenodoMetadata.conference.session != "")
      ) {
        return true;
      } else {
        // console.log(this.zenodoMetadata.conference);
        return false;
      }
    },

    showBookReportChapter() {
      if (
        "bookReportChapter" in this.zenodoMetadata &&
        (this.zenodoMetadata.bookReportChapter.publisher != "" ||
          this.zenodoMetadata.bookReportChapter.place != "" ||
          this.zenodoMetadata.bookReportChapter.isbn != "" ||
          this.zenodoMetadata.bookReportChapter.title != "" ||
          this.zenodoMetadata.bookReportChapter.pages != "")
      ) {
        return true;
      } else {
        return false;
      }
    },
    showThesis() {
      if (
        "thesis" in this.zenodoMetadata &&
        (this.zenodoMetadata.thesis.awardingUniversity != "" ||
          this.zenodoMetadata.thesis.supervisors.length > 0)
      ) {
        return true;
      } else {
        return false;
      }
    },
    showSubjects() {
      if (
        "subjects" in this.zenodoMetadata &&
        this.zenodoMetadata.subjects.length > 0
      ) {
        return true;
      } else {
        return false;
      }
    },
  },
  methods: {
    editInformation(expandOptions) {
      this.workflow.expandOptions = [...expandOptions];

      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/zenodo/metadata`;
      this.$router.push({ path: routerPath });
    },
    checkZenodoAccessToken() {
      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/zenodo/accessToken`;
      this.$router.push({ path: routerPath });
    },
  },
  async mounted() {
    this.loading = ElLoading.service({
      lock: true,
      text: "Loading data from stores...",
      background: "rgba(255, 255, 255, 0.95)",
    });

    this.dataset = await this.datasetStore.getCurrentDataset();

    this.workflow = this.dataset.workflows[this.workflowID];
    this.zenodoMetadata = this.workflow.destination.zenodo.questions;

    this.loading.close();
  },
};
// Add computed to hide properties
</script>

<style lang="postcss">
.handle {
  cursor: move;
}

.el-select-group > .el-select-dropdown__item {
  margin-left: 5px;
}
</style>
