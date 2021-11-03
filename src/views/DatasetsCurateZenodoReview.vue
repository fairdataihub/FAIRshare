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

          <div class="my-2">
            <el-descriptions
              class="margin-top"
              title="Basic Information"
              direction="vertical"
              size="small"
              border
            >
              <template #extra>
                <el-button
                  type="primary"
                  @click="editInformation(['basicInformation', 'license'])"
                >
                  Edit basic information
                </el-button>
              </template>
              <el-descriptions-item>
                <template #label> Publication Date </template>
                {{ zenodoMetadata.publicationDate }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Title </template>
                {{ zenodoMetadata.title }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Authors </template>
                {{ zenodoMetadata.authors }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Keywords </template>
                <el-tag size="small"> {{ zenodoMetadata.keywords }}</el-tag>
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Description </template>
                {{ zenodoMetadata.description }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Version </template>
                {{ zenodoMetadata.version }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Language </template>
                {{ zenodoMetadata.language }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Additional notes </template>
                {{ zenodoMetadata.additionalNotes }}
              </el-descriptions-item>

              <el-descriptions-item>
                <template #label> Access right </template>
                {{ zenodoMetadata.license.accessRight }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> License </template>
                {{ zenodoMetadata.license.licenseName }}
              </el-descriptions-item>
            </el-descriptions>
          </div>

          <div class="my-2">
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
                >
                  Edit related/alternate identifiers
                </el-button>
              </template>
              <el-descriptions-item>
                <template #label> Related/alternate identifiers </template>
                {{ zenodoMetadata.relatedIdentifiers }}
              </el-descriptions-item>
            </el-descriptions>
          </div>

          <div class="my-2">
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
                >
                  Edit contributors
                </el-button>
              </template>
              <el-descriptions-item>
                <template #label> Contributors </template>
                {{ zenodoMetadata.contributors }}
              </el-descriptions-item>
            </el-descriptions>
          </div>

          <div class="my-2">
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
                >
                  Edit references
                </el-button>
              </template>
              <el-descriptions-item>
                <template #label> References </template>
                {{ zenodoMetadata.references }}
              </el-descriptions-item>
            </el-descriptions>
          </div>

          <div class="my-2">
            <el-descriptions
              class="margin-top"
              title="Journal"
              direction="vertical"
              size="small"
              border
            >
              <template #extra>
                <el-button type="primary" @click="editInformation(['journal'])">
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
              <el-descriptions-item>
                <template #label> Year </template>
                {{ zenodoMetadata.journal.year }}
              </el-descriptions-item>
            </el-descriptions>
          </div>

          <div class="my-2">
            <el-descriptions
              class="margin-top"
              title="Conference"
              direction="vertical"
              size="small"
              border
            >
              <template #extra>
                <el-button
                  type="primary"
                  @click="editInformation(['conference'])"
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
                {{ zenodoMetadata.conference.dates }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Place </template>
                {{ zenodoMetadata.conference.place }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Website </template>
                {{ zenodoMetadata.conference.website }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Session </template>
                {{ zenodoMetadata.conference.session }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Part </template>
                {{ zenodoMetadata.conference.part }}
              </el-descriptions-item>
            </el-descriptions>
          </div>

          <div class="my-2">
            <el-descriptions
              class="margin-top"
              title="Book/report/chapter"
              direction="vertical"
              size="small"
              border
            >
              <template #extra>
                <el-button
                  type="primary"
                  @click="editInformation(['bookReportChapter'])"
                >
                  Edit book/report/chapter information
                </el-button>
              </template>
              <el-descriptions-item>
                <template #label> Publisher </template>
                {{ zenodoMetadata.bookReportChapter.publisher }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Place </template>
                {{ zenodoMetadata.bookReportChapter.place }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> ISBN </template>
                {{ zenodoMetadata.bookReportChapter.isbn }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Title </template>
                {{ zenodoMetadata.bookReportChapter.title }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Pages </template>
                {{ zenodoMetadata.bookReportChapter.pages }}
              </el-descriptions-item>
            </el-descriptions>
          </div>

          <div class="my-2">
            <el-descriptions
              class="margin-top"
              title="Thesis"
              direction="vertical"
              size="small"
              border
            >
              <template #extra>
                <el-button type="primary" @click="editInformation(['thesis'])">
                  Edit thesis information
                </el-button>
              </template>
              <el-descriptions-item>
                <template #label> Awarding University </template>
                {{ zenodoMetadata.thesis.awardingUniversity }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Supervisors </template>
                {{ zenodoMetadata.thesis.supervisors }}
              </el-descriptions-item>
            </el-descriptions>
          </div>

          <div class="my-2 mb-6">
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
                >
                  Edit subjects
                </el-button>
              </template>
              <el-descriptions-item>
                <template #label> Subjects </template>
                {{ zenodoMetadata.subjects }}
              </el-descriptions-item>
            </el-descriptions>
          </div>

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
import { ElLoading } from "element-plus";

import { useDatasetsStore } from "../store/datasets";

export default {
  name: "DatasetsCurateZenodoReview",
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
    };
  },
  computed: {},
  methods: {
    editInformation(expandOptions) {
      this.workflow.expandOptions = [...expandOptions];

      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/zenodo/metadata`;
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
