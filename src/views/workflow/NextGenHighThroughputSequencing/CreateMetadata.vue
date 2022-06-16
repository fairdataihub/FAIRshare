<template>
  <div
    class="relative flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 px-5"
  >
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium">
        Provide information about your high-throughput data
      </span>

      <div class="hidden">
        <line-divider></line-divider>
        <div class="flex flex-col">
          <span class="mb-2">
            Would you like FAIRshare to create the mandatory metadata files metadata.json?
          </span>

          <div class="py-1">
            <el-radio
              v-model="generateNextGenHighThroughputSequencingMetadata"
              label="Yes"
              size="large"
            >
              Yes
            </el-radio>
            <el-radio
              v-model="generateNextGenHighThroughputSequencingMetadata"
              label="No"
              size="large"
            >
              No
            </el-radio>
            <el-radio
              v-model="generateNextGenHighThroughputSequencingMetadata"
              label="None"
              size="large"
              border
              class="!hidden"
            >
              None
            </el-radio>
          </div>
        </div>
      </div>

      <div v-if="generateNextGenHighThroughputSequencingMetadata !== 'None'">
        <transition name="fade" mode="out-in" appear>
          <div v-if="generateNextGenHighThroughputSequencingMetadata === 'Yes'">
            <line-divider></line-divider>

            <span class="mb-2">
              Provide information about your dataset below. We will use this information to
              automatically generate and include in your dataset the standard metadata files
              required to make your dataset FAIR.
            </span>

            <div>
              <div class="py-3">
                <pill-progress-bar
                  :totalSteps="totalSteps"
                  :currentStep="currentStep"
                  @updateCurrentStep="setCurrentStep"
                  :titles="pillTitles"
                />
              </div>
              <div class="py-2">
                <div v-if="currentStep == 1">
                  <div
                    class="form-card-content mb-4 rounded-lg border-2 border-slate-100 shadow-md"
                  >
                    <div class="w-full bg-gray-100 px-4 py-2">
                      <span class="pointer-events-none text-lg font-semibold text-primary-600">
                        Study
                      </span>
                    </div>
                    <div class="p-4">
                      <el-form
                        :model="step1Form"
                        :rules="step1FormRules"
                        label-width="160px"
                        label-position="top"
                        size="large"
                        ref="s1Form"
                        @submit.prevent
                        class="metadata-form py-4"
                      >
                        <el-form-item label="Study" prop="study">
                          <div class="flex w-full flex-row items-center">
                            <el-input v-model="step1Form.study" placeholder="GSE131369"></el-input>
                          </div>
                        </el-form-item>

                        <el-form-item label="Title" prop="title">
                          <div class="flex w-full flex-row items-center">
                            <el-input
                              v-model="step1Form.title"
                              placeholder="Decoding the Protein Composition of Whole Nucleosomes with Nuc-MS"
                            ></el-input>
                          </div>
                        </el-form-item>

                        <el-form-item label="Summary(abstract)" prop="summary">
                          <div class="flex w-full flex-row items-center">
                            <el-input
                              v-model="step1Form.summary"
                              type="textarea"
                              placeholder="Goblet cells are considered as a homogeneous population in the intestinal epithelium. We used single cell RNA sequencing (scRNA-seq) to analyze the diversity of GCs in the intestine."
                            ></el-input>
                          </div>
                        </el-form-item>

                        <el-form-item label="Experimental design" prop="title">
                          <div class="flex w-full flex-row items-center">
                            <el-input
                              v-model="step1Form.experimentalDesign"
                              type="textarea"
                              placeholder="Intestinal GCs of the RedMUC298trTg mice were isolated by Fluorescence-activated cell sorting (FACS) according to the presence or absence of mCherry signal and analyzed using scRNAseq."
                            ></el-input>
                          </div>
                        </el-form-item>

                        <el-form-item label="Contributors">
                          <draggable
                            tag="div"
                            :list="step1Form.contributors"
                            item-key="id"
                            handle=".handle"
                            :animation="200"
                            class="w-full"
                          >
                            <template #item="{ element }">
                              <div class="mb-2 flex w-full flex-row justify-between transition-all">
                                <div class="flex w-11/12 flex-row justify-between">
                                  <el-input
                                    v-model="element.contributor"
                                    type="text"
                                    placeholder="First name, Initials, Last name"
                                    v-on:keyup.enter="addContributor"
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
                                  <div
                                    class="flex cursor-pointer items-center justify-center text-gray-500 transition-all hover:text-gray-800"
                                  >
                                    <el-popconfirm
                                      title="Are you sure you want to remove this?"
                                      icon-color="red"
                                      confirm-button-text="Yes"
                                      cancel-button-text="No"
                                      @confirm="deleteContributor(element.id)"
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
                        </el-form-item>

                        <div
                          class="flex w-max cursor-pointer items-center pb-3 text-sm text-gray-500 hover:text-black"
                          @click="addContributor(null, '')"
                        >
                          <Icon icon="carbon:add" />
                          <span> Add a Contributor </span>
                        </div>
                      </el-form>
                    </div>
                  </div>
                  <div class="flex w-full justify-center space-x-4 px-5 py-4">
                    <button @click="prevFormStep" class="primary-plain-button" size="medium">
                      <el-icon><back-icon /></el-icon>
                      Back
                    </button>
                    <!-- :plain="!lastStep" -->
                    <button class="primary-button" @click="navigateToStep2FromStep1">
                      Next
                      <el-icon><right-icon /></el-icon>
                    </button>
                  </div>
                </div>

                <div v-if="currentStep == 2">
                  <div
                    class="form-card-content mb-4 rounded-lg border-2 border-slate-100 shadow-md"
                  >
                    <div class="w-full bg-gray-100 px-4 py-2">
                      <span class="pointer-events-none text-lg font-semibold text-primary-600">
                        Protocols
                      </span>
                    </div>
                    <div class="p-4">
                      <el-form
                        :model="step2Form"
                        :rules="step2FormRules"
                        label-width="160px"
                        label-position="top"
                        size="large"
                        ref="s2Form"
                        @submit.prevent
                        class="metadata-form py-4"
                      >
                        <el-form-item label="Growth protocol">
                          <div class="flex w-full flex-row items-center">
                            <el-input
                              v-model="step2Form.growthProtocol"
                              type="textarea"
                              placeholder="C3H 10T1/2 mesenchymal cells were maintained in DMEM supplemented with 10% fetal bovine serum (FBS) and antibiotics in humidified atmosphere with 5% CO2 at 37C"
                            />
                          </div>
                        </el-form-item>

                        <el-form-item label="Treatment protocol">
                          <div class="flex w-full flex-row items-center">
                            <el-input
                              v-model="step2Form.treatmentProtocol"
                              type="textarea"
                              placeholder="Adipogenic differentiation was induced by treatment of 2-day post confluent cells (designated day 0, D0) with 10ug/ml insulin (Sigma), 1uM dexamethasone (Sigma), and 0.5mM isobutylmethylxanthine (Sigma) in the presence of 10% FBS until day 2. Cells were then fed with DMEM supplemented with 10% FBS and 10ug/ml insulin for 2 days, after which they were fed every other day with DMEM containing 10% FBS"
                            />
                          </div>
                        </el-form-item>

                        <el-form-item label="Extract protocol">
                          <div class="flex w-full flex-row items-center">
                            <el-input
                              v-model="step2Form.extractProtocol"
                              type="textarea"
                              placeholder="RNA was harvested using Rneasy mini plus kit (Qiagen). 1.3 ug of total RNA was used for the construction of sequencing libraries."
                            />
                          </div>
                        </el-form-item>

                        <el-form-item label="Library construction protocol">
                          <div class="flex w-full flex-row items-center">
                            <el-input
                              v-model="step2Form.libraryConstructionProtocol"
                              type="textarea"
                              placeholder="RNA libraries for RNA-seq were prepared using SMARTER mRNA-Seq Library Prep Kit following manufacturer's protocols."
                            />
                          </div>
                        </el-form-item>

                        <el-form-item label="Library strategy">
                          <div class="flex w-full flex-row items-center">
                            <el-input
                              v-model="step2Form.libraryStrategy"
                              type="textarea"
                              placeholder="RNA-seq"
                            />
                          </div>
                        </el-form-item>

                        <el-form-item label="Data processing steps">
                          <div class="flex w-full flex-row items-center">
                            <el-input
                              v-model="step2Form.dataProcessingSteps"
                              type="textarea"
                              placeholder="CLC Genomics Workbench v 11.0.1"
                            />
                          </div>
                        </el-form-item>

                        <el-form-item label="Genome build/assembly">
                          <div class="flex w-full flex-row items-center">
                            <el-input
                              v-model="step2Form.genomeBuild"
                              type="textarea"
                              placeholder="mm10"
                            />
                          </div>
                        </el-form-item>

                        <el-form-item label="Processed data files format and content">
                          <div class="flex w-full flex-row items-center">
                            <el-input
                              v-model="step2Form.processedDataFilesFormat"
                              type="textarea"
                              placeholder="tab-delimited text files include RPKM values for each Sample"
                            />
                          </div>
                        </el-form-item>
                      </el-form>
                    </div>
                  </div>
                  <div class="flex w-full justify-center space-x-4 px-5 py-4">
                    <button
                      @click="prevFormStep"
                      class="secondary-plain-button"
                      size="medium"
                      :disabled="checkInvalidStatus"
                    >
                      <el-icon><back-icon /></el-icon>
                      Previous
                    </button>
                    <!-- :plain="!lastStep" -->
                    <button
                      class="primary-button"
                      @click="navigateToStep3FromStep2"
                      :disabled="checkInvalidStatus"
                    >
                      Next
                      <el-icon><right-icon /></el-icon>
                    </button>
                  </div>
                </div>

                <div v-if="currentStep == 3">
                  <div
                    class="form-card-content mb-4 rounded-lg border-2 border-slate-100 shadow-md"
                  >
                    <div class="w-full bg-gray-50 px-4 py-2">
                      <span class="pointer-events-none text-lg font-semibold text-primary-600">
                        Samples
                      </span>
                    </div>
                    <div class="p-4">
                      <el-form
                        :model="step3Form"
                        :rules="step3FormRules"
                        label-width="160px"
                        label-position="top"
                        size="large"
                        ref="s3Form"
                        @submit.prevent
                        class="metadata-form py-4"
                      >
                        <draggable
                          tag="div"
                          :list="step3Form"
                          item-key="id"
                          handle=".handle"
                          :animation="200"
                          @start="minimizeAllSamples"
                        >
                          <template #item="{ element }">
                            <div class="flex flex-col px-2">
                              <div class="flex flex-row items-center justify-between">
                                <div class="flex w-full flex-row justify-start">
                                  <div
                                    class="mr-2 rounded-md p-1 hover:cursor-pointer hover:bg-slate-200"
                                    @click="element.isExpanded = !element.isExpanded"
                                  >
                                    <Icon
                                      icon="dashicons:arrow-right-alt2"
                                      width="20"
                                      height="20"
                                      class="transition-all"
                                      :class="{
                                        'rotate-90': element.isExpanded,
                                        'rotate-0': !element.isExpanded,
                                      }"
                                    />
                                  </div>

                                  <span class="">{{ element.libraryName }}</span>

                                  <div
                                    class="ml-2 flex cursor-pointer items-center justify-center rounded-md p-2 text-gray-500 transition-all hover:bg-slate-200 hover:text-gray-800"
                                  >
                                    <el-icon><edit-pen /></el-icon>
                                  </div>
                                </div>

                                <div class="flex w-1/12 flex-row justify-evenly">
                                  <div
                                    class="handle mr-1 flex items-center justify-center rounded-md p-2 text-gray-500 transition-all hover:bg-slate-200 hover:text-gray-800"
                                  >
                                    <Icon icon="ic:outline-drag-indicator" />
                                  </div>
                                  <div
                                    class="ml-1 flex cursor-pointer items-center justify-center rounded-md p-2 text-gray-500 transition-all hover:bg-slate-200 hover:text-gray-800"
                                  >
                                    <el-icon><delete-filled /></el-icon>
                                  </div>
                                </div>
                              </div>

                              <el-collapse-transition>
                                <div class="mt-4 flex flex-col px-4" v-show="element.isExpanded">
                                  <el-input
                                    v-model="element.title"
                                    type="text"
                                    placeholder="Title"
                                    class="mb-2"
                                  ></el-input>

                                  <el-input
                                    v-model="element.description"
                                    type="textarea"
                                    placeholder="Description"
                                    class="mb-2"
                                  ></el-input>

                                  <div
                                    class="mb-2 flex w-full flex-row justify-between transition-all"
                                  >
                                    <div class="mr-2 w-4/12">
                                      <el-select
                                        v-model="element.organism"
                                        filterable
                                        remote
                                        reserve-keyword
                                        placeholder="Organism"
                                        :remote-method="loadTaxonomy"
                                        :loading="loading"
                                      >
                                        <el-option
                                          v-for="item in organismOptions"
                                          :key="item.value"
                                          :label="item.label"
                                          :value="item.value"
                                        />
                                      </el-select>
                                    </div>

                                    <div class="mx-2 w-3/12">
                                      <el-input
                                        v-model="element.molecule"
                                        type="text"
                                        placeholder="Molecule"
                                      ></el-input>
                                    </div>

                                    <div class="mx-2 w-3/12 xl:w-2/12">
                                      <el-select
                                        v-model="element.singleOrPairedEnd"
                                        filterable
                                        placeholder="Single or paired end"
                                      >
                                        <el-option label="single" value="single"> </el-option>
                                        <el-option label="paired-end" value="paired-end">
                                        </el-option>
                                      </el-select>
                                    </div>

                                    <div class="mx-2 w-3/12 xl:w-auto">
                                      <el-select
                                        v-model="element.instrumentModel"
                                        filterable
                                        placeholder="Instrument Model"
                                      >
                                        <el-option
                                          v-for="item in instrumentModelOptions"
                                          :key="item"
                                          :label="item"
                                          :value="item"
                                        >
                                        </el-option>
                                      </el-select>
                                    </div>
                                  </div>

                                  <line-divider class="my-2" type="dashed" />

                                  <p class="">Sample Characteristics</p>
                                  <span class="mb-4 text-xs">
                                    One of 'tissue', 'cell line' or 'cell type' fields is required.
                                  </span>

                                  <div
                                    class="flex w-full flex-col justify-between pb-4"
                                    v-for="(_item, key, index) in element.characteristics"
                                    :key="index"
                                  >
                                    <label class="w-[160px] pb-1 text-sm font-medium text-gray-700">
                                      {{ key }}
                                    </label>

                                    <div class="flex items-center justify-between">
                                      <el-input
                                        v-model="element.characteristics[key]"
                                        type="text"
                                      />
                                      <div
                                        class="ml-2 flex cursor-pointer items-center justify-center rounded-md p-2 text-gray-500 transition-all hover:bg-slate-200 hover:text-gray-800"
                                        @click="deleteCustomField(key)"
                                      >
                                        <el-icon><delete-filled /></el-icon>
                                      </div>
                                    </div>
                                  </div>

                                  <div class="flex w-full flex-row justify-start">
                                    <button
                                      class="primary-plain-button"
                                      @click="openAddFieldPrompt(id)"
                                    >
                                      Add a field
                                      <el-icon><circle-plus /></el-icon>
                                    </button>
                                  </div>

                                  <line-divider class="my-4" type="dashed" />

                                  <div class="flex flex-col">
                                    <p class="my-2">Add your raw files</p>

                                    <el-tree-select
                                      v-model="element.rawFiles"
                                      :data="element.filteredRawFilesFolderContents"
                                      @visible-change="
                                        getFilteredRawFilesFolderContents(element.id)
                                      "
                                      multiple
                                      show-checkbox
                                    />
                                  </div>

                                  <div class="flex flex-col">
                                    <p class="my-2">Add your processed files</p>

                                    <el-tree-select
                                      v-model="element.processedDataFiles"
                                      :data="element.filteredProcessedDataFilesFolderContents"
                                      @visible-change="
                                        getFilteredProcessedDataFilesFolderContents(element.id)
                                      "
                                      multiple
                                      show-checkbox
                                    />
                                  </div>
                                </div>
                              </el-collapse-transition>

                              <line-divider></line-divider>
                            </div>
                          </template>
                        </draggable>
                        <add-prompt
                          ref="addCharacteristicPrompt"
                          title="Add a sample characteristic"
                          confirmButtonText="Add this field"
                          :confirmDisabled="disableCustomCharacteristic"
                          @messageConfirmed="addCustomCharacteristic"
                        >
                          <div w-full>
                            <p class="mb-3 text-sm">
                              Please select or enter the name of the field you would like to add.
                              This field will be added to all samples.
                            </p>

                            <el-autocomplete
                              v-model="customFieldName"
                              :fetch-suggestions="customFieldNameSearch"
                              clearable
                              class="w-full"
                              placeholder="Enter a field name"
                            />
                          </div>
                        </add-prompt>
                      </el-form>
                      <div class="m-2 flex w-full justify-center">
                        <button class="primary-plain-button">Add a Sample</button>
                      </div>
                    </div>
                  </div>
                  <div class="flex w-full justify-center space-x-4 px-5 py-4">
                    <button
                      @click="prevFormStep"
                      class="secondary-plain-button"
                      size="medium"
                      :disabled="checkInvalidStatus"
                    >
                      <el-icon><back-icon /></el-icon>
                      Previous
                    </button>
                    <!-- :plain="!lastStep" -->
                    <button
                      class="primary-button"
                      @click="navigateToStep4FromStep3"
                      :disabled="checkInvalidStatus"
                    >
                      Next
                      <el-icon><right-icon /></el-icon>
                    </button>
                  </div>
                </div>

                <div v-if="currentStep == 4">
                  <div
                    class="form-card-content mb-4 rounded-lg border-2 border-slate-100 shadow-md"
                  >
                    <div class="w-full bg-gray-100 px-4 py-2">
                      <span class="pointer-events-none text-lg font-semibold text-primary-600">
                        Additional information
                      </span>
                    </div>
                    <div class="p-4">
                      <el-form
                        :model="step4Form"
                        label-width="160px"
                        label-position="top"
                        size="large"
                        ref="s7Form"
                        @submit.prevent
                        class="py-4"
                      >
                        <el-form-item label="Reference publication">
                          <div class="flex w-full flex-row items-center">
                            <el-input
                              v-model="step4Form.referencePublication"
                              type="text"
                              placeholder="https://doi.org/10.100/xyz123"
                            ></el-input>
                            <form-help-content
                              popoverContent="Link to the scholarly publication that describes the software"
                            ></form-help-content>
                          </div>
                        </el-form-item>

                        <el-form-item label="Development status">
                          <div class="flex w-full flex-row items-center">
                            <form-help-content
                              popoverContent="The current development status of this software. Select one to see the definition. See <a class='text-url' onclick='window.ipcRenderer.send(`open-link-in-browser`, `http://www.repostatus.org`)'> http://www.repostatus.org/ </a> for more details."
                            ></form-help-content>
                          </div>

                          <p class="pt-2 text-xs text-gray-500"></p>
                        </el-form-item>

                        <el-form-item label="Is part of" :error="isPartOfErrorMessage">
                          <div class="flex w-full flex-row items-center">
                            <el-input
                              v-model="step4Form.isPartOf"
                              type="url"
                              placeholder="https://thebiggerframework.org"
                            ></el-input>
                            <form-help-content
                              popoverContent="Link to the project this software is part of"
                            ></form-help-content>
                          </div>
                        </el-form-item>
                      </el-form>
                    </div>
                  </div>
                  <div class="flex w-full justify-center space-x-4 px-5 py-4">
                    <button
                      @click="prevFormStep"
                      class="secondary-plain-button"
                      size="medium"
                      :disabled="checkInvalidStatus"
                    >
                      <el-icon><back-icon /></el-icon>
                      Previous
                    </button>
                    <!-- :plain="!lastStep" -->
                    <button
                      class="primary-button"
                      @click="nextFormStep"
                      :disabled="checkInvalidStatus"
                    >
                      Continue
                      <el-icon><d-arrow-right /></el-icon>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-else>
            <div class="flex w-full justify-center space-x-4 px-5 py-4">
              <button class="primary-plain-button" size="medium" @click="saveSkip">
                <el-icon><back-icon /></el-icon>
                Back
              </button>

              <button
                class="primary-button"
                :disabled="checkInvalidStatus"
                @click="showSkipMetadataCreationWarning"
              >
                Continue
                <el-icon><d-arrow-right /></el-icon>
              </button>
            </div>
            <warning-confirm
              ref="warningConfirm"
              title="Warning"
              @messageConfirmed="navigateToSelectDestination"
              confirmButtonText="Yes, I want to skip"
            >
              <p class="text-center text-base text-gray-500">
                The codemeta.json and CITATION.cff files are highly recommended to make your
                research software FAIR. Are you sure you want to skip this step?
              </p>
            </warning-confirm>
          </div>
        </transition>
      </div>
    </div>

    <fade-transition>
      <div class="fixed bottom-2 right-20" v-if="showSaving">
        <Vue3Lottie
          :animationData="SaveLottieJSON"
          :width="75"
          :height="75"
          :loop="1"
          @onComplete="hideSavingIcon"
        />
      </div>
    </fade-transition>

    <fade-transition>
      <div class="fixed bottom-2 right-20" v-show="showSpinner">
        <Vue3Lottie :animationData="$helix_spinner" :width="80" :height="80" />
      </div>
    </fade-transition>

    <app-docs-link url="curate-and-share/add-codemeta" position="bottom-4" />
  </div>
</template>

<script>
import { Icon } from "@iconify/vue";
import { v4 as uuidv4 } from "uuid";
// import { ElNotification } from "element-plus";

import draggable from "vuedraggable";
import validator from "validator";
import axios from "axios";

import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

import PillProgressBar from "@/components/ui/PillProgressBar.vue";

import contributorTypesJSON from "@/assets/supplementalFiles/contributorTypes.json";
import repoStatusJSON from "@/assets/supplementalFiles/repoStatus.json";
import codeMetadataJSON from "@/assets/supplementalFiles/codeMetadata.json";
import nextGenSequencingJSON from "@/assets/supplementalFiles/nextGenSequencing.json";

import SaveLottieJSON from "@/assets/lotties/saveLottie.json";

export default {
  name: "NextGenHighThroughputSequencingCreateMetadata",
  components: {
    draggable,
    Icon,
    PillProgressBar,
  },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      tokens: useTokenStore(),
      currentStep: 3,
      totalSteps: 3,
      pillTitles: ["Study", "Protocols", "Samples"],
      SaveLottieJSON,
      dataset: {},
      workflowID: this.$route.params.workflowID,
      workflow: {},
      loading: false,
      interval: null,
      contributorTypes: contributorTypesJSON.contributorTypes,
      programmingLanguageOptions: codeMetadataJSON.programmingLanguageOptions,
      runtimePlatformOptions: codeMetadataJSON.runtimePlatformOptions,
      operatingSystemOptions: codeMetadataJSON.operatingSystemOptions,
      repoStatusOptions: repoStatusJSON.repoStatus,
      instrumentModelOptions: nextGenSequencingJSON.instrumentModelOptions,
      customFieldOptions: nextGenSequencingJSON.customFieldOptions,
      generateNextGenHighThroughputSequencingMetadata: "Yes",
      step1Form: {
        study: "",
        title: "",
        summary: "",
        experimentalDesign: "",
        contributors: [],
        supplementaryFile: "",
      },
      step1FormRules: {
        study: [
          {
            required: true,
            message: "Please enter the name or ID of the study",
            trigger: "blur",
          },
        ],
        title: [
          {
            required: true,
            message: "Please enter a unique title for the study",
            trigger: "blur",
          },
        ],
        summary: [
          {
            required: true,
            message: "Please enter a summary of the study",
            trigger: "blur",
          },
        ],
      },
      step2Form: {
        growthProtocol: "",
        treatmentProtocol: "",
        extractProtocol: "",
        libraryConstructionProtocol: "",
        libraryStrategy: "",
        dataProcessingSteps: "",
        genomeBuild: "",
        processedDataFilesFormat: "",
      },
      step2FormRules: {},

      step3Form: [
        {
          id: uuidv4(),
          libraryName: "name 1",
          title: "",
          organism: "",
          molecule: "",
          singleOrPairedEnd: "",
          instrumentModel: "",
          description: "",
          processedDataFiles: [],
          rawFiles: [],
          characteristics: {
            tissue: "",
            "developmental stage": "",
          },
          filteredRawFilesFolderContents: [],
          filteredProcessedDataFilesFolderContents: [],
          isExpanded: true,
        },
        {
          id: uuidv4(),
          libraryName: "name 2",
          title: "",
          organism: "",
          molecule: "",
          singleOrPairedEnd: "",
          instrumentModel: "",
          description: "",
          processedDataFiles: [],
          rawFiles: [],
          characteristics: {
            tissue: "",
            "developmental stage": "",
          },
          filteredRawFilesFolderContents: [],
          filteredProcessedDataFilesFolderContents: [],
          isExpanded: true,
        },
      ],

      step3FormRules: {},
      step4Form: {
        referencePublication: "",

        isPartOf: "",
      },
      isPartOfErrorMessage: "",

      invalidStatus: {},
      originalObject: {},
      showSaving: false,
      showSpinner: false,
      sampleID: "",
      customFieldName: "",
      folderContents: [
        {
          value: "1",
          label: "Level one 1",
          isDir: true,
          children: [
            {
              value: "1-1",
              label: "Level two 1-1",
              isDir: false,
            },
          ],
        },
      ],
      organismOptions: [],
    };
  },
  watch: {
    "step4Form.isPartOf": {
      handler(val) {
        if (val != "" && val != undefined) {
          const validIdentifier = validator.isURL(val);

          if (!validIdentifier) {
            this.isPartOfErrorMessage = "Please provide a valid URL";
            this.$refs.s7Form.validate();
            this.invalidStatus.isPartOf = true;
            return;
          } else {
            this.isPartOfErrorMessage = "";
            this.invalidStatus.isPartOf = false;
          }
        } else {
          this.isPartOfErrorMessage = "";
          this.invalidStatus.isPartOf = false;
        }
      },
      deep: true,
    },
  },
  computed: {
    checkInvalidStatus() {
      for (const key in this.invalidStatus) {
        if (this.invalidStatus[key]) {
          return true;
        }
      }
      return false;
    },
    disableCustomCharacteristic() {
      return this.customFieldName.trim() === "";
    },
  },
  methods: {
    async sleep(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    },
    setCurrentStep(step) {
      this.currentStep = step;
    },
    showSavingIcon() {
      this.showSaving = false;
      this.showSaving = true;
    },
    hideSavingIcon() {
      this.showSaving = false;
    },
    async prevFormStep() {
      this.showSavingIcon();

      if (this.currentStep - 1 > 0) {
        this.currentStep--;
      } else {
        this.navigateBack();
      }
    },
    async nextFormStep() {
      if (this.currentStep + 1 > this.totalSteps) {
        if (!this.checkInvalidStatus) {
          this.navigateToSelectDestination();
        }
      } else {
        this.currentStep++;
      }
    },
    async saveSkip() {
      if (this.generateNextGenHighThroughputSequencingMetadata === "Yes") {
        this.workflow.generateNextGenHighThroughputSequencingMetadata = true;
      } else {
        this.workflow.generateNextGenHighThroughputSequencingMetadata = false;
      }

      await this.datasetStore.updateCurrentDataset(this.dataset);
      await this.datasetStore.syncDatasets();

      this.navigateBack();
    },
    showSkipMetadataCreationWarning() {
      this.$refs.warningConfirm.show();
    },
    navigateToStep2FromStep1() {
      this.$refs["s1Form"].validate(async (valid) => {
        if (valid) {
          await this.saveCurrentEntries();
          this.setCurrentStep(2);
        }
      });
    },
    navigateToStep3FromStep2() {
      this.$refs["s2Form"].validate(async (valid) => {
        if (valid) {
          await this.saveCurrentEntries();
          this.setCurrentStep(3);
        }
      });
    },
    navigateToStep4FromStep3() {
      if (this.step3Form.keywords.length <= 0) {
        this.$message({
          message: "Please add at least one keyword.",
          type: "error",
        });
        return;
      }

      this.$refs["s3Form"].validate(async (valid) => {
        if (valid) {
          await this.saveCurrentEntries();
          this.setCurrentStep(4);
        }
      });
    },
    addIds(array) {
      array.forEach((element) => {
        element.id = uuidv4();
      });
    },
    initializeEmptyObjects(root, obj) {
      if (obj === undefined) {
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

    addContributor(_event, contributor = "") {
      if (this.step1Form.contributors.some((el) => el.contributor === contributor)) {
        this.$message.warning("This contributor already exists.");
        return;
      }

      const id = uuidv4();
      this.step1Form.contributors.push({
        contributor,
        id,
      });
      this.focusOnElementRef(id);
    },
    deleteContributor(id) {
      this.step1Form.contributors = this.step1Form.contributors.filter((contributor) => {
        return contributor.id !== id;
      });
      this.$refs["s1Form"].validate();
    },

    filterArrayOfObjects(array, key) {
      return array.filter((element) => {
        return element[key] !== "";
      });
    },

    openAddFieldPrompt(id) {
      this.sampleID = id;
      this.$refs.addCharacteristicPrompt.show();
    },
    customFieldNameSearch(query, cb) {
      let results;

      if (query) {
        results = this.customFieldOptions.filter((element) => {
          return element.value.toLowerCase().indexOf(query.toLowerCase()) === 0;
        });
      } else {
        results = this.customFieldOptions;
      }

      cb(results);
    },
    addCustomCharacteristic() {
      const customFieldName = this.customFieldName.trim();

      if (customFieldName.toLocaleLowerCase() in this.step3Form[0].characteristics) {
        this.$message.error("This field already exists.");
        return;
      }

      for (let sample of this.step3Form) {
        sample.characteristics[customFieldName] = "";
      }

      this.customFieldName = "";
    },
    deleteCustomField(key) {
      /**
       * TODO: Add a confirmation dialog
       */

      if (key in this.step3Form[0].characteristics) {
        for (let sample of this.step3Form) {
          delete sample.characteristics[key];
        }
      }
    },

    getFilteredRawFilesFolderContents(id) {
      let alreadyAddedFiles = [];

      const newFolderContents = JSON.parse(JSON.stringify(this.folderContents));

      for (let i = 0; i < this.step3Form.length; i++) {
        alreadyAddedFiles.push(...this.step3Form[i].processedDataFiles);
        if (this.step3Form[i].id !== id) {
          alreadyAddedFiles.push(...this.step3Form[i].rawFiles);
        }
      }

      //recurse through the folder contents
      function recurse(folderContents) {
        for (let i = 0; i < folderContents.length; i++) {
          if (folderContents[i].isDir) {
            recurse(folderContents[i].children);
          } else {
            if (alreadyAddedFiles.includes(folderContents[i].value)) {
              folderContents[i].disabled = true;
            } else {
              folderContents[i].disabled = false;
            }
          }
        }
      }

      recurse(newFolderContents);

      let sample = this.step3Form.find((element) => {
        return element.id === id;
      });

      console.log(sample, id);

      sample.filteredRawFilesFolderContents = newFolderContents;

      return;
    },
    getFilteredProcessedDataFilesFolderContents(id) {
      let alreadyAddedFiles = [];

      const newFolderContents = JSON.parse(JSON.stringify(this.folderContents));

      for (let i = 0; i < this.step3Form.length; i++) {
        alreadyAddedFiles.push(...this.step3Form[i].rawFiles);
        if (this.step3Form[i].id !== id) {
          alreadyAddedFiles.push(...this.step3Form[i].processedDataFiles);
        }
      }

      //recurse through the folder contents
      function recurse(folderContents) {
        for (let i = 0; i < folderContents.length; i++) {
          if (folderContents[i].isDir) {
            recurse(folderContents[i].children);
          } else {
            if (alreadyAddedFiles.includes(folderContents[i].value)) {
              folderContents[i].disabled = true;
            } else {
              folderContents[i].disabled = false;
            }
          }
        }
      }

      recurse(newFolderContents);

      let sample = this.step3Form.find((element) => {
        return element.id === id;
      });

      sample.filteredProcessedDataFilesFolderContents = newFolderContents;

      return;
    },

    async loadTaxonomy(query) {
      if (query) {
        this.loading = true;
        this.organismOptions = [];

        try {
          const response = await axios.get(
            `https://rest.ensembl.org/taxonomy/id/${query}?simple=0`,
            {
              headers: {
                "Content-Type": "application/json",
              },
            }
          );

          if (response.status === 200) {
            const res = response.data;

            if ("children" in res) {
              this.organismOptions = res.children.map((child) => {
                return {
                  value: child.scientific_name,
                  label: child.scientific_name,
                };
              });
            }

            if (res.scientific_name) {
              this.organismOptions = [
                {
                  value: res.scientific_name,
                  label: res.scientific_name,
                },
                ...this.organismOptions,
              ];
            }

            this.loading = false;
          }
        } catch (error) {
          this.organismOptions = [];
          this.loading = false;
          return;
        }
      } else {
        this.organismOptions = [];
      }
    },

    minimizeAllSamples() {
      this.step3Form.map((sample) => {
        sample.isExpanded = false;
      });
    },

    async saveCurrentEntries() {
      this.showSavingIcon();

      this.dataset.data.general.questions.name = this.step1Form.name;
      this.dataset.data.general.questions.description = this.step1Form.description;

      this.step3Form.keywords = this.filterArrayOfObjects(this.step3Form.keywords, "keyword");

      this.dataset.data.general.questions.keywords = this.step3Form.keywords;
      this.dataset.data.general.questions.authors = this.step2Form.authors;
      this.dataset.data.general.questions.contributors = this.step2Form.contributors;
      this.dataset.data.general.questions.fundingCode = this.step3Form.fundingCode;
      this.dataset.data.general.questions.fundingOrganization = this.step3Form.fundingOrganization;
      this.dataset.data.general.questions.referencePublication =
        this.step4Form.referencePublication;

      let nghtsForm = {};

      nghtsForm.name = this.step1Form.name;
      nghtsForm.description = this.step1Form.description;
      nghtsForm.creationDate = this.step1Form.creationDate;
      nghtsForm.firstReleaseDate = this.step1Form.firstReleaseDate;

      nghtsForm.authors = this.step2Form.authors;
      nghtsForm.contributors = this.step2Form.contributors;

      nghtsForm.identifier = this.step3Form.identifier;
      nghtsForm.keywords = this.step3Form.keywords;
      nghtsForm.fundingCode = this.step3Form.fundingCode;
      nghtsForm.fundingOrganization = this.step3Form.fundingOrganization;

      nghtsForm.referencePublication = this.step4Form.referencePublication;

      nghtsForm.isPartOf = this.step4Form.isPartOf;

      this.dataset.data.NextGenHighThroughputSequencing.questions = nghtsForm;

      this.workflow.generateCodeMeta = false;

      if (this.generateNextGenHighThroughputSequencingMetadata === "Yes") {
        this.workflow.generateNextGenHighThroughputSequencingMetadata = true;
      } else {
        this.workflow.generateNextGenHighThroughputSequencingMetadata = false;
      }

      await this.datasetStore.updateCurrentDataset(this.dataset);
      await this.datasetStore.syncDatasets();
    },
    async navigateToSelectDestination(_evt, shouldNavigateBack = false) {
      await this.saveCurrentEntries();

      if (shouldNavigateBack) {
        this.$router.push({
          path: `/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/NextGenHighThroughputSequencing/selectFolder`,
        });
        return;
      }

      const routerPath = `/datasets/${this.dataset.id}/${this.workflowID}/NextGenHighThroughputSequencing/pickLicense`;

      this.$router.push({ path: routerPath });
    },
    navigateBack() {
      this.$router.push({
        path: `/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/NextGenHighThroughputSequencing/reviewStandards`,
      });
    },

    prefillFormFromMetadataObject(nghtsMetadata) {
      this.step1Form.name = nghtsMetadata.name;
      this.step1Form.description = nghtsMetadata.description;
      this.step1Form.creationDate = nghtsMetadata.dateCreated;
      this.step1Form.firstReleaseDate = nghtsMetadata.datePublished;

      this.step2Form.authors = [];
      nghtsMetadata.author.forEach(
        ({ givenName = "", familyName = "", email = "", affiliation = "", orcid = "" }) => {
          this.step2Form.authors.push({
            givenName,
            familyName,
            affiliation: affiliation.name,
            email,
            orcid,
            id: uuidv4(),
          });
        }
      );

      this.step2Form.contributors = [];
      if ("contributor" in nghtsMetadata) {
        nghtsMetadata.contributor.forEach(
          ({ givenName = "", familyName = "", email = "", affiliation = "", orcid = "" }) => {
            this.step2Form.contributors.push({
              givenName,
              familyName,
              affiliation: affiliation.name,
              email,
              orcid,
              id: uuidv4(),
            });
          }
        );
      }

      this.step3Form.identifier = nghtsMetadata.identifier;
      if ("keywords" in nghtsMetadata) {
        nghtsMetadata.keywords.forEach((keyword) => {
          this.step3Form.keywords.push({ keyword, id: uuidv4() });
        });
      }
      if ("fundingCode" in nghtsMetadata) {
        this.step3Form.fundingCode = nghtsMetadata.fundingCode;
      }
      if ("fundingOrganization" in nghtsMetadata) {
        this.step3Form.fundingOrganization = nghtsMetadata.fundingOrganization;
      }

      this.step4Form.referencePublication = nghtsMetadata.referencePublication;

      this.step4Form.isPartOf = nghtsMetadata.isPartOf;
    },
  },
  async mounted() {
    this.$nextTick(async function () {
      this.dataset = await this.datasetStore.getCurrentDataset();

      this.workflow = this.dataset.workflows[this.workflowID];

      this.datasetStore.showProgressBar();
      this.datasetStore.setProgressBarType("geo");
      this.datasetStore.setCurrentStep(3);

      this.workflow.currentRoute = this.$route.path;

      /**
       * TODO: Will need to enable this when we figure out how to read in metadata files
       * */
      // if ("generateNextGenHighThroughputSequencingMetadata" in this.workflow) {
      //   this.generateNextGenHighThroughputSequencingMetadata = this.workflow
      //     .generateNextGenHighThroughputSequencingMetadata
      //     ? "Yes"
      //     : "No";
      // } else {
      //   this.generateNextGenHighThroughputSequencingMetadata = "None";
      // }

      if (
        this.dataset.data.NextGenHighThroughputSequencing.questions &&
        Object.keys(this.dataset.data.NextGenHighThroughputSequencing.questions).length !== 0
      ) {
        let nghtsForm = this.dataset.data.NextGenHighThroughputSequencing.questions;

        this.step1Form.name = nghtsForm.name;
        this.step1Form.description = nghtsForm.description;
        this.step1Form.creationDate = nghtsForm.creationDate;
        this.step1Form.firstReleaseDate = nghtsForm.firstReleaseDate;

        this.step2Form.authors = nghtsForm.authors;
        this.step2Form.contributors = nghtsForm.contributors;

        this.step3Form.identifier = nghtsForm.identifier;
        this.step3Form.keywords = nghtsForm.keywords;
        this.step3Form.fundingCode = nghtsForm.fundingCode;
        this.step3Form.fundingOrganization = nghtsForm.fundingOrganization;

        this.step4Form.referencePublication = nghtsForm.referencePublication;

        this.step4Form.isPartOf = nghtsForm.isPartOf;

        this.addIds(this.step3Form.keywords);
        this.addIds(this.step2Form.authors);
        this.addIds(this.step2Form.contributors);
      } else {
        this.step1Form.title = this.dataset.name;
        this.step1Form.summary = this.dataset.description;

        if ("source" in this.workflow) {
          if (this.workflow.source.type === "local") {
            /**
             * TODO: Will need to enable this when we figure out how to read in metadata files
             */
            // this.showSpinner = true;
            // const response = await axios
            //   .post(`${this.$server_url}/utilities/fileexistinfolder`, {
            //     folder_path: this.dataset.data.NextGenHighThroughputSequencing.folderPath,
            //     file_name: "metadata.json",
            //   })
            //   .then((response) => {
            //     return response.data;
            //   })
            //   .catch((error) => {
            //     console.log(error);
            //     return "ERROR";
            //   });
            // if (response !== "ERROR" && response !== "Not Found") {
            //   ElNotification({
            //     title: "Info",
            //     message: "Found a previous metadata.json file. Loading it...",
            //     position: "top-right",
            //     type: "info",
            //   });
            //   await this.prefillFormFromMetadataObject(response);
            //   ElNotification({
            //     title: "Success",
            //     message: "Successfully loaded metadata.json file.",
            //     position: "top-right",
            //     type: "success",
            //   });
            // }
            // this.showSpinner = false;
          }
        }
      }
      if ("source" in this.workflow) {
        if (this.workflow.source.type === "local") {
          const response = await axios.post(`${this.$server_url}/utilities/readfoldercontents`, {
            folder_path: this.dataset.data.NextGenHighThroughputSequencing.folderPath,
          });

          this.folderContents = response.data.children;
        }
      }
    });
  },
};
</script>
