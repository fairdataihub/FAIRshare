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
              size="small"
              direction="vertical"
              border
            >
              <template #extra>
                <el-button
                  type="primary"
                  @click="editInformation(['general'])"
                >
                  Edit basic information
                </el-button>
              </template>
              <el-descriptions-item>
                <template #label> Dataset name </template>
                {{ generalMetadata.name }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Dataset description </template>
                {{ generalMetadata.description }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Authors </template>

                <div>
                  <ul class="list-disc list-inside">
                    <li
                      v-for="author in generalMetadata.authors"
                      :key="author.id"
                    >
                      Name: {{ author.familyName }}, {{ author.givenName }}
                      <ul class="ml-6">
                        <li>Affiliation: {{ author.affiliation }}</li>
                        <li>ORCID: {{ author.orcid }}</li>
                        <li>E-mail: {{ author.email }}</li>
                      </ul>
                    </li>
                  </ul>
                </div>
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Keywords </template>
                <div class="flex justify-start">
                  <el-tag
                    size="medium"
                    v-for="element in generalMetadata.keywords"
                    :key="element.id"
                    class="mx-1"
                  >
                    {{ element.keyword }}</el-tag
                  >
                </div>
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Contributors </template>
                <div>
                  <ul class="list-disc list-inside">
                    <li
                      v-for="contributor in generalMetadata.contributors"
                      :key="contributor.id"
                    >
                      Name: {{ contributor.familyName }},
                      {{ contributor.givenName }}
                      <ul class="ml-6">
                        <li>Affiliation: {{ contributor.affiliation }}</li>
                        <li>ORCID: {{ contributor.orcid }}</li>
                        <li>E-mail: {{ contributor.email }}</li>
                      </ul>
                    </li>
                  </ul>
                </div>
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Funding code </template>
                {{ generalMetadata.funding.code }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Funding organization </template>
                {{ generalMetadata.funding.organization }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Reference publication </template>
                {{ generalMetadata.referencePublication }}
              </el-descriptions-item>
            </el-descriptions>
          </div>

          <div class="my-2" v-if="codePresent">
            <el-descriptions
              class="margin-top"
              title="Code"
              direction="vertical"
              size="small"
              border
            >
              <template #extra>
                <el-button type="primary" @click="editInformation(['code'])">
                  Edit code metadata
                </el-button>
              </template>

              <el-descriptions-item>
                <template #label> Creation date </template>
                {{ codeMetadata.creationDate }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> First release date </template>
                {{ codeMetadata.firstReleaseDate }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> License </template>
                {{ codeMetadata.license }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Application category </template>
                {{ codeMetadata.applicationCategory }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Repository </template>
                {{ codeMetadata.codeRepository }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Continuous integration </template>
                {{ codeMetadata.continuousIntegration }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Issue tracker </template>
                {{ codeMetadata.issueTracker }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> References </template>
                <ul class="list-disc list-inside">
                  <li v-for="link in codeMetadata.relatedLinks" :key="link.id">
                    {{ link.link }}
                  </li>
                </ul>
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Programming language </template>
                <div class="flex justify-start">
                  <el-tag
                    size="medium"
                    v-for="element in codeMetadata.programmingLanguage"
                    :key="element"
                    class="mx-1"
                  >
                    {{ element }}
                  </el-tag>
                </div>
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Runtime platform </template>
                <div class="flex justify-start">
                  <el-tag
                    size="medium"
                    v-for="element in codeMetadata.runtimePlatform"
                    :key="element"
                    class="mx-1"
                  >
                    {{ element }}
                  </el-tag>
                </div>
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Operating system </template>
                <div class="flex justify-start">
                  <el-tag
                    size="medium"
                    v-for="element in codeMetadata.operatingSystem"
                    :key="element"
                    class="mx-1"
                  >
                    {{ element }}
                  </el-tag>
                </div>
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Other software requirements </template>
                <ul class="list-disc list-inside">
                  <li
                    v-for="link in codeMetadata.otherSoftwareRequirements"
                    :key="link.id"
                  >
                    {{ link.link }}
                  </li>
                </ul>
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Current version </template>
                {{ codeMetadata.currentVersion }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Current version release date </template>
                {{ codeMetadata.currentVersionReleaseDate }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Current version download URL </template>
                {{ codeMetadata.currentVersionDownloadLink }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Current version release notes </template>
                {{ codeMetadata.currentVersionReleaseNotes }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Development status </template>
                {{ codeMetadata.issueTracker }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label> Is part of </template>
                {{ codeMetadata.isPartOf }}
              </el-descriptions-item>
            </el-descriptions>
          </div>

          <div class="w-full flex flex-row justify-center py-2">
            <router-link to="/datasets" class="mx-6">
              <el-button type="danger" plain> Cancel </el-button>
            </router-link>

            <el-button
              type="primary"
              class="flex flex-row items-center"
              @click="selectDestination"
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

import { useDatasetsStore } from "../store/datasets";
import repoStatusJSON from "../assets/supplementalFiles/repoStatus.json";

export default {
  name: "DatasetsCurateMetadataReview",
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
      generalMetadata: {
        funding: {},
      },
      codeMetadata: {},
      repoStatusOptions: repoStatusJSON.repoStatus,
    };
  },
  computed: {
    displayDevelopmentStatus() {
      const that = this;

      function getStatus(status) {
        return that.repoStatusOptions.find((item) => item.value === status);
      }

      if (
        "developmentStatus" in this.codeMetadata &&
        this.codeMetadata.developmentStatus != ""
      ) {
        const status = this.codeMetadata.developmentStatus;
        const returnVal = getStatus(status);
        return returnVal.description;
      } else {
        return "";
      }
    },
    codePresent() {
      if ("type" in this.workflow) {
        return this.workflow.type.includes("Code");
      }
      return false;
    },
  },
  methods: {
    editInformation(expandOptions) {
      this.workflow.expandOptions = [...expandOptions];

      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/createMetadata`;
      this.$router.push({ path: routerPath });
    },
    selectDestination() {
      const routerPath = `/datasets/${this.dataset.id}/${this.workflowID}/selectDestination`;
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

    this.generalMetadata = this.dataset.data.general.questions;

    if (this.codePresent) {
      this.codeMetadata = this.dataset.data.Code.questions;
    }

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
