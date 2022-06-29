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

            <div>
              <div class="py-3">
                <pill-progress-bar
                  :totalSteps="totalSteps"
                  :currentStep="currentStep"
                  @updateCurrentStep="setCurrentStep"
                  :titles="pillTitles"
                />
              </div>

              <div class="mt-3 mb-1">
                <span v-if="currentStep === 3">
                  Add some information about your samples below. We will use this information to
                  automatically generate the required metadata files needed for your dataset.
                </span>
                <span v-else>
                  Provide information about your dataset below. We will use this information to
                  automatically generate and include in your dataset the standard metadata files
                  required to make your dataset FAIR.
                </span>
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
                          <div class="flex w-full flex-col items-start">
                            <el-input
                              v-model="step1Form.title"
                              placeholder="Decoding the Protein Composition of Whole Nucleosomes with Nuc-MS"
                            ></el-input>
                            <span class="mt-2 px-1 text-xs text-slate-600">
                              A unique title that describes the whole study
                            </span>
                          </div>
                        </el-form-item>

                        <el-form-item label="Summary(abstract)" prop="summary">
                          <div class="flex w-full flex-col items-start">
                            <el-input
                              v-model="step1Form.summary"
                              type="textarea"
                              placeholder="Goblet cells are considered as a homogeneous population in the intestinal epithelium. We used single cell RNA sequencing (scRNA-seq) to analyze the diversity of GCs in the intestine."
                            ></el-input>
                            <span class="mt-2 px-1 text-xs text-slate-600">
                              Thorough description of the goals and objectives of this study. A
                              working abstract from the associated manuscript may be suitable.
                              Include as much text as necessary.
                            </span>
                          </div>
                        </el-form-item>

                        <el-form-item label="Experimental design" prop="title">
                          <div class="flex w-full flex-col items-start">
                            <el-input
                              v-model="step1Form.experimentalDesign"
                              type="textarea"
                              placeholder="Intestinal GCs of the RedMUC298trTg mice were isolated by Fluorescence-activated cell sorting (FACS) according to the presence or absence of mCherry signal and analyzed using scRNAseq."
                            ></el-input>
                            <span class="mt-2 px-1 text-xs text-slate-600">
                              Describe the SAMPLES. Include what types of Samples are analyzed, if
                              replicates are included, are there control and/or reference Samples,
                              etc.
                            </span>
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

                        <el-form-item label="Supplementary files" prop="supplementaryFiles">
                          <div class="flex flex-col">
                            <el-tree-select
                              v-model="step1Form.supplementaryFiles"
                              :data="step1Form.filteredSupplementaryFilesFolderContents"
                              @visible-change="getSupplementaryFilesFolderContents"
                              multiple
                              clearable
                              class="w-full"
                            />
                            <span class="mt-2 px-1 text-xs text-slate-600">
                              Optional. If you submit a processed data file corresponding to
                              *multiple* Samples, include the processed file here. For example:
                              FPKMs_allsamples.txt The file should have unique column names that
                              match unique descriptors in metadata SAMPLES (for example, "library
                              name" descriptors). An exception would be single-cell submissions.
                            </span>
                          </div>
                        </el-form-item>
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
                          <div class="flex w-full flex-col items-start">
                            <el-input
                              v-model="step2Form.growthProtocol"
                              type="textarea"
                              placeholder="C3H 10T1/2 mesenchymal cells were maintained in DMEM supplemented with 10% fetal bovine serum (FBS) and antibiotics in humidified atmosphere with 5% CO2 at 37C"
                            />
                            <span class="mt-1 px-1 text-xs text-slate-600">
                              Optional. Describe the conditions used to grow or maintain organisms
                              or cells prior to extract preparation
                            </span>
                          </div>
                        </el-form-item>

                        <el-form-item label="Treatment protocol">
                          <div class="flex w-full flex-col items-start">
                            <el-input
                              v-model="step2Form.treatmentProtocol"
                              type="textarea"
                              placeholder="Adipogenic differentiation was induced by treatment of 2-day post confluent cells (designated day 0, D0) with 10ug/ml insulin (Sigma), 1uM dexamethasone (Sigma), and 0.5mM isobutylmethylxanthine (Sigma) in the presence of 10% FBS until day 2. Cells were then fed with DMEM supplemented with 10% FBS and 10ug/ml insulin for 2 days, after which they were fed every other day with DMEM containing 10% FBS"
                            />
                            <span class="mt-1 px-1 text-xs text-slate-600">
                              Optional. Describe the treatments applied to the biological material
                              prior to extract preparation.
                            </span>
                          </div>
                        </el-form-item>

                        <el-form-item label="Extract protocol">
                          <div class="flex w-full flex-col items-start">
                            <el-input
                              v-model="step2Form.extractProtocol"
                              type="textarea"
                              placeholder="RNA was harvested using Rneasy mini plus kit (Qiagen). 1.3 ug of total RNA was used for the construction of sequencing libraries."
                            />
                            <span class="mt-1 px-1 text-xs text-slate-600">
                              Describe the protocols used to extract and prepare the material to be
                              sequenced.
                            </span>
                          </div>
                        </el-form-item>

                        <el-form-item label="Library construction protocol">
                          <div class="flex w-full flex-col items-start">
                            <el-input
                              v-model="step2Form.libraryConstructionProtocol"
                              type="textarea"
                              placeholder="RNA libraries for RNA-seq were prepared using SMARTER mRNA-Seq Library Prep Kit following manufacturer's protocols."
                            />
                            <span class="mt-1 px-1 text-xs text-slate-600">
                              Describe the library construction protocol.
                            </span>
                          </div>
                        </el-form-item>

                        <el-form-item label="Library strategy">
                          <div class="flex w-full flex-col items-start">
                            <el-select
                              v-model="step2Form.libraryStrategy"
                              filterable
                              class="w-full"
                              placeholder="Molecule"
                            >
                              <el-option
                                v-for="item in libraryStrategyOptions"
                                :key="item"
                                :label="item"
                                :value="item"
                              >
                              </el-option>
                            </el-select>

                            <fade-transition>
                              <el-input
                                v-if="step2Form.libraryStrategy == 'OTHER:'"
                                class="mt-2"
                                v-model="step2Form.otherLibraryStrategy"
                                placeholder="specify"
                              />
                            </fade-transition>

                            <span class="mt-1 px-1 text-xs text-slate-600">
                              A Sequence Read Archive-specific field that describes the sequencing
                              technique for each library.
                            </span>
                          </div>
                        </el-form-item>

                        <el-form-item label="Data processing steps">
                          <draggable
                            tag="div"
                            :list="step2Form.dataProcessingSteps"
                            item-key="id"
                            handle=".handle"
                            :animation="200"
                            class="w-full"
                          >
                            <template #item="{ element }">
                              <div class="mb-2 flex w-full flex-row justify-between transition-all">
                                <div class="flex w-11/12 flex-row justify-between">
                                  <el-input
                                    v-model="element.step"
                                    type="text"
                                    placeholder="First name, Initials, Last name"
                                    v-on:keyup.enter="addDataProcessingStep"
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
                                      @confirm="deleteDataProcessingStep(element.id)"
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

                          <span class="mt-1 px-1 text-xs text-slate-600">
                            Provide details of how processed data files were generated. <br />
                            Steps may include: Base-calling software, version, parameters; Data
                            filtering steps; Read alignment software, version, parameters;
                            Additional processing software (e.g., peak-calling, abundance
                            measurement), version, parameters; etc.
                          </span>
                        </el-form-item>

                        <div
                          class="flex w-max cursor-pointer items-center pb-3 text-sm text-gray-500 hover:text-black"
                          @click="addDataProcessingStep(null, '')"
                        >
                          <Icon icon="carbon:add" />
                          <span> Add a data processing step </span>
                        </div>

                        <el-form-item label="Genome build/assembly">
                          <div class="flex w-full flex-col items-start">
                            <el-input
                              v-model="step2Form.genomeBuild"
                              type="textarea"
                              placeholder="mm10"
                            />
                            <span class="mt-1 px-1 text-xs text-slate-600">
                              UCSC or NCBI genome build number (e.g., hg18, mm9, human NCBI genome
                              build 36, etc...), or reference sequence used for read alignment.
                            </span>
                          </div>
                        </el-form-item>

                        <el-form-item label="Processed data files format and content">
                          <div class="flex w-full flex-col items-start">
                            <el-input
                              v-model="step2Form.processedDataFilesFormat"
                              type="textarea"
                              placeholder="tab-delimited text files include RPKM values for each Sample"
                            />
                            <span class="mt-1 px-1 text-xs text-slate-600">
                              For each processed data file type, provide a description of the format
                              and content.
                            </span>
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
                  <div class="px-4 pb-4 pt-2">
                    <el-form
                      :model="step3Form"
                      :rules="step3FormRules"
                      label-width="160px"
                      label-position="top"
                      size="large"
                      ref="s3Form"
                      @submit.prevent
                      class="metadata-form pb-4"
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
                          <div
                            class="form-card-content mb-4 flex flex-col rounded-lg border-2 border-slate-100 shadow-md"
                          >
                            <div
                              class="flex w-full flex-row items-center justify-between bg-gray-50 px-4 py-2"
                              @click="element.isExpanded = !element.isExpanded"
                            >
                              <div class="flex w-full flex-row justify-start">
                                <div
                                  class="mr-2 flex items-center justify-center rounded-md p-1 hover:cursor-pointer hover:bg-slate-200"
                                  @click.stop="element.isExpanded = !element.isExpanded"
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

                                <span class="flex items-center"> {{ element.libraryName }} </span>

                                <div
                                  class="ml-2 flex cursor-pointer items-center justify-center rounded-md p-2 text-gray-500 transition-all hover:bg-slate-200 hover:text-gray-800"
                                  @click.stop="editLibraryName(element.id)"
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
                                  @click.stop="showRemoveSampleConfirm(element.id)"
                                >
                                  <el-icon><delete-filled /></el-icon>
                                </div>
                              </div>
                            </div>

                            <el-collapse-transition>
                              <div class="mt-4 flex flex-col px-4" v-show="element.isExpanded">
                                <div class="mb-4 flex flex-col">
                                  <label class="w-[160px] pb-1 text-sm font-medium text-gray-700">
                                    Title
                                  </label>

                                  <el-input
                                    v-model="element.title"
                                    type="text"
                                    placeholder="Title"
                                  />
                                  <span class="mt-1 px-1 text-xs text-slate-600">
                                    Unique title that describes the Sample. We suggest the
                                    convention: [biomaterial] [condition(s)] [replicate number]
                                  </span>
                                </div>

                                <div class="mb-4 flex flex-col">
                                  <label class="w-[160px] pb-1 text-sm font-medium text-gray-700">
                                    Description
                                  </label>
                                  <el-input
                                    v-model="element.description"
                                    type="textarea"
                                    placeholder="Description"
                                    class="mb-2"
                                  />
                                  <span class="mt-1 px-1 text-xs text-slate-600">
                                    Optional. Additional information not provided in the other
                                    fields, or broad descriptions that cannot be easily dissected
                                    into other fields. <br />
                                    OR <br />
                                    If you submit a matrix containing processed data for multiple
                                    Samples (e.g., counts.txt for all RNA-Seq samples), list the
                                    matrix column names here.
                                  </span>
                                </div>

                                <div
                                  class="mb-2 flex w-full flex-row justify-between transition-all"
                                >
                                  <div class="mr-2 w-4/12 xl:w-3/12">
                                    <div class="mb-4 flex flex-col">
                                      <label
                                        class="w-[160px] pb-1 text-sm font-medium text-gray-700"
                                      >
                                        Organism
                                      </label>
                                      <el-select
                                        v-model="element.organism"
                                        filterable
                                        remote
                                        reserve-keyword
                                        placeholder="Organism"
                                        class="w-full"
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
                                      <span class="mt-1 px-1 text-xs text-slate-600">
                                        Organisms from which the sequences was derived.
                                      </span>
                                    </div>
                                  </div>

                                  <div class="mx-2 w-3/12">
                                    <div class="mb-4 flex flex-col">
                                      <label
                                        class="w-[160px] pb-1 text-sm font-medium text-gray-700"
                                      >
                                        Molecule
                                      </label>
                                      <el-select
                                        v-model="element.molecule"
                                        filterable
                                        class="w-full"
                                        placeholder="Molecule"
                                      >
                                        <el-option
                                          v-for="item in moleculeOptions"
                                          :key="item"
                                          :label="item"
                                          :value="item"
                                        >
                                        </el-option>
                                      </el-select>
                                      <span class="mt-1 px-1 text-xs text-slate-600">
                                        Type of molecule that was extracted from the biological
                                        material.
                                      </span>
                                    </div>
                                  </div>

                                  <div class="mx-2 w-3/12">
                                    <div class="mb-4 flex flex-col">
                                      <label
                                        class="w-[160px] pb-1 text-sm font-medium text-gray-700"
                                      >
                                        Single or paired end
                                      </label>
                                      <el-select
                                        v-model="element.singleOrPairedEnd"
                                        filterable
                                        class="w-full"
                                        placeholder="Single or paired end"
                                      >
                                        <el-option label="single" value="single"> </el-option>
                                        <el-option label="paired-end" value="paired-end">
                                        </el-option>
                                      </el-select>
                                    </div>
                                  </div>

                                  <div class="mx-2 w-2/12 xl:w-3/12">
                                    <div class="mb-4 flex flex-col">
                                      <label
                                        class="w-[160px] pb-1 text-sm font-medium text-gray-700"
                                      >
                                        Instrument Model
                                      </label>
                                      <el-select
                                        v-model="element.instrumentModel"
                                        filterable
                                        class="w-full"
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
                                    <el-autocomplete
                                      v-model="element.characteristics[key]"
                                      :fetch-suggestions="customFieldValueSuggestions"
                                      @focus="setCustomFieldNameForFilter(key)"
                                      clearable
                                      class="w-full"
                                      placeholder="Enter a field name"
                                    />
                                    <div
                                      class="ml-2 flex cursor-pointer items-center justify-center rounded-md p-2 text-gray-500 transition-all hover:bg-slate-200 hover:text-gray-800"
                                      @click="showCustomFieldDeleteConfirm(key)"
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
                                    @visible-change="getFilteredRawFilesFolderContents(element.id)"
                                    multiple
                                    clearable
                                    show-checkbox
                                  />
                                  <span class="mt-1 px-1 text-xs text-slate-600">
                                    Files containing the raw data.
                                  </span>
                                </div>

                                <div class="mb-4 flex flex-col">
                                  <p class="my-2">Add your processed files</p>

                                  <el-tree-select
                                    v-model="element.processedDataFiles"
                                    :data="element.filteredProcessedDataFilesFolderContents"
                                    @visible-change="
                                      getFilteredProcessedDataFilesFolderContents(element.id)
                                    "
                                    multiple
                                    clearable
                                    show-checkbox
                                  />
                                  <span class="mt-1 px-1 text-xs text-slate-600">
                                    Files containing the processed data. The same processed file may
                                    be listed for multiple Samples.
                                  </span>
                                </div>
                              </div>
                            </el-collapse-transition>
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
                            Please select or enter the name of the field you would like to add. This
                            field will be added to all samples.
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

                      <edit-prompt
                        ref="editLibraryNamePrompt"
                        title="Edit library name"
                        confirmButtonText="Save"
                        :confirmDisabled="disableEditLibraryNameSaveButton"
                        @messageConfirmed="saveUpdatedLibraryName"
                      >
                        <div w-full>
                          <p class="mb-3 text-sm">
                            Please enter the new library name for this sample.
                          </p>

                          <el-input
                            v-model="sampleName"
                            clearable
                            class="w-full"
                            placeholder="Enter a field name"
                          />
                        </div>
                      </edit-prompt>

                      <warning-confirm
                        ref="removeSampleConfirm"
                        title="Warning"
                        @messageConfirmed="confirmedRemoveSample"
                      >
                        <p class="text-center text-base text-gray-500">
                          Are you sure you want to remove this sample? This action cannot be undone.
                        </p>
                      </warning-confirm>

                      <warning-confirm
                        ref="removeCustomFieldConfirm"
                        title="Warning"
                        @messageConfirmed="confirmedRemoveCustomField"
                      >
                        <p class="text-center text-base text-gray-500">
                          Are you sure you want to remove this field from all samples? This action
                          cannot be undone.
                        </p>
                      </warning-confirm>
                    </el-form>
                    <div class="m-2 flex w-full justify-center">
                      <button class="primary-plain-button" @click="showAddSamplePrompt">
                        Add a Sample
                      </button>

                      <add-prompt
                        ref="addSamplePrompt"
                        title="Add a sample"
                        confirmButtonText="Add this sample"
                        :confirmDisabled="disableEditLibraryNameSaveButton"
                        @messageConfirmed="addSampleConfirmed"
                      >
                        <div w-full>
                          <p class="mb-3 text-sm">
                            Please select or enter the name of the sample you would like to add.
                          </p>

                          <el-input
                            v-model="sampleName"
                            clearable
                            class="w-full"
                            placeholder="Enter a library name for your sample"
                          />
                        </div>
                      </add-prompt>
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
// import validator from "validator";
import axios from "axios";

import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

import PillProgressBar from "@/components/ui/PillProgressBar.vue";

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
      instrumentModelOptions: nextGenSequencingJSON.instrumentModelOptions,
      customFieldOptions: nextGenSequencingJSON.customFieldOptions,
      moleculeOptions: nextGenSequencingJSON.moleculeOptions,
      libraryStrategyOptions: nextGenSequencingJSON.libraryStrategyOptions,
      generateNextGenHighThroughputSequencingMetadata: "Yes",
      step1Form: {
        study: "",
        title: "",
        summary: "",
        experimentalDesign: "",
        contributors: [],
        supplementaryFiles: [],
        filteredSupplementaryFilesFolderContents: [],
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
        otherLibraryStrategy: "",
        dataProcessingSteps: [],
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
      customFieldNameForFilter: "",
      invalidStatus: {},
      originalObject: {},
      showSaving: false,
      showSpinner: false,
      sampleID: "",
      sampleName: "",
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
  watch: {},
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
    disableEditLibraryNameSaveButton() {
      if (this.sampleName.trim() === "") {
        return true;
      }

      for (const sample of this.step3Form) {
        if (sample.libraryName === this.sampleName.trim()) {
          return true;
        }
      }

      return false;
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

    addDataProcessingStep(_event, step = "") {
      const id = uuidv4();
      this.step2Form.dataProcessingSteps.push({
        step,
        id,
      });
      this.focusOnElementRef(id);
    },
    deleteDataProcessingStep(id) {
      this.step2Form.dataProcessingSteps = this.step2Form.dataProcessingSteps.filter(
        (processingStep) => {
          return processingStep.id !== id;
        }
      );
      this.$refs["s2Form"].validate();
    },

    filterArrayOfObjects(array, key) {
      return array.filter((element) => {
        return element[key] !== "";
      });
    },

    showAddSamplePrompt() {
      this.sampleName = "";
      this.$refs.addSamplePrompt.show();
    },

    addSampleConfirmed() {
      let newSampleObject = {
        id: uuidv4(),
        libraryName: this.sampleName,
        title: "",
        organism: "",
        molecule: "",
        singleOrPairedEnd: "",
        instrumentModel: "",
        description: "",
        characteristics: {},
        processedDataFiles: [],
        rawFiles: [],
        filteredRawFilesFolderContents: [],
        filteredProcessedDataFilesFolderContents: [],
        isExpanded: true,
      };

      if (this.step3Form.length > 0) {
        for (const key in this.step3Form[0].characteristics) {
          newSampleObject.characteristics[key] = "";
        }
      }

      this.step3Form.push(newSampleObject);
    },

    openAddFieldPrompt() {
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

    setCustomFieldNameForFilter(key) {
      this.customFieldNameForFilter = key;
    },

    customFieldValueSuggestions(query, cb) {
      let results = [];
      let fieldOptions = [];
      let customFieldOptions = [];

      for (const sample of this.step3Form) {
        if (sample.characteristics[this.customFieldNameForFilter] !== "") {
          fieldOptions.push(sample.characteristics[this.customFieldNameForFilter]);
        }
      }

      fieldOptions = [...new Set(fieldOptions)];

      for (const value of fieldOptions) {
        customFieldOptions.push({
          value,
        });
      }

      if (query) {
        results = customFieldOptions.filter((element) => {
          return element.value.toLowerCase().indexOf(query.toLowerCase()) === 0;
        });
      } else {
        results = customFieldOptions;
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
    showCustomFieldDeleteConfirm(key) {
      this.customFieldName = key;
      this.$refs.removeCustomFieldConfirm.show();
    },
    confirmedRemoveCustomField() {
      const key = this.customFieldName;
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
    getSupplementaryFilesFolderContents() {
      let alreadyAddedFiles = [];

      const newFolderContents = JSON.parse(JSON.stringify(this.folderContents));

      for (let i = 0; i < this.step3Form.length; i++) {
        alreadyAddedFiles.push(...this.step3Form[i].rawFiles);
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

      this.step1Form.filteredSupplementaryFilesFolderContents = newFolderContents;

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

    editLibraryName(id) {
      let sample = this.step3Form.find((element) => {
        return element.id === id;
      });

      this.sampleID = id;
      this.sampleName = sample.libraryName;
      this.$refs.editLibraryNamePrompt.show();
    },

    saveUpdatedLibraryName() {
      let sample = this.step3Form.find((element) => {
        return element.id === this.sampleID;
      });

      sample.libraryName = this.sampleName;
    },

    showRemoveSampleConfirm(id) {
      this.sampleID = id;
      this.$refs.removeSampleConfirm.show();
    },
    confirmedRemoveSample() {
      const id = this.sampleID;

      this.step3Form = this.step3Form.filter((sample) => {
        return sample.id !== id;
      });
    },

    async saveCurrentEntries() {
      this.showSavingIcon();

      this.dataset.data.general.questions.name = this.step1Form.title;
      this.dataset.data.general.questions.description = this.step1Form.summary;

      this.step1Form.contributors = this.filterArrayOfObjects(
        this.step1Form.contributors,
        "contributor"
      );

      this.dataset.data.general.questions.authors = this.step1Form.contributors;

      let nghtsForm = {};

      nghtsForm.study = this.step1Form.study;
      nghtsForm.title = this.step1Form.title;
      nghtsForm.summary = this.step1Form.summary;
      nghtsForm.experimentalDesign = this.step1Form.experimentalDesign;
      nghtsForm.contributors = this.step1Form.contributors;
      nghtsForm.supplementaryFiles = this.step1Form.supplementaryFiles;

      nghtsForm.growthProtocol = this.step2Form.growthProtocol;
      nghtsForm.treatmentProtocol = this.step2Form.treatmentProtocol;
      nghtsForm.extractProtocol = this.step2Form.extractProtocol;
      nghtsForm.libraryConstructionProtocol = this.step2Form.libraryConstructionProtocol;
      nghtsForm.libraryStrategy = this.step2Form.libraryStrategy;
      nghtsForm.otherLibraryStrategy = this.step2Form.otherLibraryStrategy;
      nghtsForm.dataProcessingSteps = this.step2Form.dataProcessingSteps;
      nghtsForm.genomeBuild = this.step2Form.genomeBuild;
      nghtsForm.processedDataFilesFormat = this.step2Form.processedDataFilesFormat;

      nghtsForm.samples = this.step3Form;

      this.dataset.data.NextGenHighThroughputSequencing.questions = nghtsForm;

      this.workflow.generateNextGenHighThroughputSequencingMetadata = true;

      // if (this.generateNextGenHighThroughputSequencingMetadata === "Yes") {
      //   this.workflow.generateNextGenHighThroughputSequencingMetadata = true;
      // } else {
      //   this.workflow.generateNextGenHighThroughputSequencingMetadata = false;
      // }

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

      const routerPath = `/datasets/${this.$route.params.datasetID}/${this.workflowID}/selectDestination`;

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

        this.step1Form.study = nghtsForm.study;
        this.step1Form.title = nghtsForm.title;
        this.step1Form.summary = nghtsForm.summary;
        this.step1Form.experimentalDesign = nghtsForm.experimentalDesign;
        this.step1Form.contributors = nghtsForm.contributors;
        this.step1Form.supplementaryFiles = nghtsForm.supplementaryFiles;

        this.step2Form.growthProtocol = nghtsForm.growthProtocol;
        this.step2Form.treatmentProtocol = nghtsForm.treatmentProtocol;
        this.step2Form.extractProtocol = nghtsForm.extractProtocol;
        this.step2Form.libraryConstructionProtocol = nghtsForm.libraryConstructionProtocol;
        this.step2Form.libraryStrategy = nghtsForm.libraryStrategy;
        this.step2Form.otherLibraryStrategy = nghtsForm.otherLibraryStrategy;
        this.step2Form.dataProcessingSteps = nghtsForm.dataProcessingSteps;
        this.step2Form.genomeBuild = nghtsForm.genomeBuild;
        this.step2Form.processedDataFilesFormat = nghtsForm.processedDataFilesFormat;

        this.step3Form = nghtsForm.samples;

        this.addIds(this.step1Form.contributors);
        this.addIds(this.step2Form.dataProcessingSteps);
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
