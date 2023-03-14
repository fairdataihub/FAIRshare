<template>
  <div
    class="relative flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 px-5"
  >
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium" ref="topOfPageElement">
        Provide information about your Immunology data
      </span>

      <div>
        <line-divider></line-divider>
        <div class="flex flex-col">
          <span class="mb-2">
            Would you like FAIRshare to create the mandatory metadata files required for registering
            on ImmPort?
          </span>

          <div class="py-1">
            <el-radio v-model="generateImmunologyMetadata" label="Yes" size="large"> Yes </el-radio>
            <el-radio v-model="generateImmunologyMetadata" label="No" size="large"> No </el-radio>
            <el-radio
              v-model="generateImmunologyMetadata"
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

      <div v-if="generateImmunologyMetadata !== 'None'">
        <transition name="fade" mode="out-in" appear>
          <div v-if="generateImmunologyMetadata === 'Yes'">
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
                        class="py-4"
                      >
                        <el-form-item label="Study ID" prop="studyID">
                          <div class="flex w-full flex-col items-start">
                            <el-input
                              v-model="step1Form.studyID"
                              placeholder="study_198423"
                              maxlength="150"
                              show-word-limit
                            ></el-input>
                            <span class="mt-2 text-xs text-slate-600">
                              This identifier should be unique to the ImmPort workspace to which the
                              data will be uploaded.
                            </span>
                          </div>
                        </el-form-item>

                        <el-form-item label="Brief Title" prop="briefTitle">
                          <div class="flex w-full flex-col items-start">
                            <el-input
                              v-model="step1Form.briefTitle"
                              placeholder="Decoding the Protein Composition of Whole Nucleosomes with Nuc-MS"
                              maxlength="250"
                              show-word-limit
                            ></el-input>
                            <span class="mt-2 text-xs text-slate-600">
                              Serves as the working title for the study.
                            </span>
                          </div>
                        </el-form-item>

                        <el-form-item label="Official Study Title" prop="officialTitle">
                          <div class="flex w-full flex-col items-start">
                            <el-input
                              v-model="step1Form.officialTitle"
                              placeholder="Decoding the Protein Composition of Whole Nucleosomes with Nuc-MS"
                              maxlength="500"
                              show-word-limit
                            ></el-input>
                            <span class="mt-2 text-xs text-slate-600">
                              Serves as the working title for the study.
                            </span>
                          </div>
                        </el-form-item>

                        <el-form-item label="Brief Description" prop="briefDescription">
                          <div class="flex w-full flex-col items-start">
                            <el-input
                              v-model="step1Form.briefDescription"
                              type="textarea"
                              rows="3"
                              maxlength="4000"
                              show-word-limit
                              placeholder="Goblet cells are considered as a homogeneous population in the intestinal epithelium. We used single cell RNA sequencing (scRNA-seq) to analyze the diversity of GCs in the intestine."
                            ></el-input>
                            <span class="mt-2 text-xs text-slate-600">
                              Thorough description of the goals and objectives of this study. A
                              working abstract from the associated manuscript may be suitable.
                              Include as much text as necessary.
                            </span>
                          </div>
                        </el-form-item>

                        <el-form-item label="Full Description" prop="description">
                          <div class="flex w-full flex-col items-start">
                            <el-input
                              v-model="step1Form.description"
                              type="textarea"
                              rows="5"
                              placeholder="Goblet cells are considered as a homogeneous population in the intestinal epithelium. We used single cell RNA sequencing (scRNA-seq) to analyze the diversity of GCs in the intestine."
                            ></el-input>
                            <span class="mt-2 text-xs text-slate-600">
                              Thorough description of the goals and objectives of this study. A
                              working abstract from the associated manuscript may be suitable.
                              Include as much text as necessary.
                            </span>
                          </div>
                        </el-form-item>

                        <el-form-item label="Sponsoring Organization" prop="sponsoringOrganization">
                          <div class="flex w-full flex-col items-start">
                            <el-input
                              v-model="step1Form.sponsoringOrganization"
                              placeholder="Univeristy of California, San Francisco"
                              maxlength="250"
                              show-word-limit
                            ></el-input>
                            <span class="mt-2 text-xs text-slate-600">
                              The organization that provides funding and support for the study.
                            </span>
                          </div>
                        </el-form-item>

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
                            <span class="mt-2 text-xs text-slate-600">
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
                        class="py-4"
                      >
                        <el-form-item label="Intervention Agent" prop="interventionAgent">
                          <div class="flex w-full flex-col items-start">
                            <el-input
                              v-model="step2Form.interventionAgent"
                              type="textarea"
                              maxlength="1000"
                              show-word-limit
                              placeholder="Goblet cells are considered as a homogeneous population in the intestinal epithelium. We used single cell RNA sequencing (scRNA-seq) to analyze the diversity of GCs in the intestine."
                            ></el-input>
                            <span class="mt-2 text-xs text-slate-600">
                              Thorough description of the goals and objectives of this study. A
                              working abstract from the associated manuscript may be suitable.
                              Include as much text as necessary.
                            </span>
                          </div>
                        </el-form-item>

                        <el-form-item
                          label="Endpoints/Output Measurements/Clinical Assesments"
                          prop="endpoints"
                        >
                          <div class="flex w-full flex-col items-start">
                            <el-input
                              v-model="step2Form.endpoints"
                              type="textarea"
                              placeholder="Goblet cells are considered as a homogeneous population in the intestinal epithelium. We used single cell RNA sequencing (scRNA-seq) to analyze the diversity of GCs in the intestine."
                            ></el-input>
                            <span class="mt-2 text-xs text-slate-600">
                              Thorough description of the goals and objectives of this study. A
                              working abstract from the associated manuscript may be suitable.
                              Include as much text as necessary.
                            </span>
                          </div>
                        </el-form-item>

                        <el-form-item label="Age Unit" prop="ageUnit">
                          <div class="flex w-full flex-col items-start">
                            <el-select
                              class="w-full"
                              v-model="step2Form.ageUnit"
                              placeholder="Weeks"
                            >
                              <el-option label="Not Specified" value="Not Specified" />
                              <el-option label="Years" value="Years" />
                              <el-option label="Months" value="Months" />
                              <el-option label="Weeks" value="Weeks" />
                              <el-option label="Days" value="Days" />
                              <el-option label="Hours" value="Hours" />
                              <el-option label="Minutes" value="Minutes" />
                              <el-option label="Seconds" value="Seconds" />
                              <el-option label="d.p.c." value="d.p.c." />
                            </el-select>
                            <span class="mt-2 text-xs text-slate-600">
                              The unit of time used to describe the subjects age in the study.
                            </span>
                          </div>
                        </el-form-item>

                        <el-form-item
                          label="Actual Start Date/Commencement Time point of the Study"
                          prop="actualStartDate"
                        >
                          <div class="flex w-full flex-col items-start">
                            <el-date-picker
                              v-model="step2Form.actualStartDate"
                              type="date"
                              placeholder="Pick a date"
                              style="width: 100%"
                            />
                            <span class="mt-2 text-xs text-slate-600">
                              The unit of time used to describe the subjects age in the study.
                            </span>
                          </div>
                        </el-form-item>

                        <el-form-item label="Hypothesis" prop="hypothesis">
                          <div class="flex w-full flex-col items-start">
                            <el-input
                              v-model="step2Form.hypothesis"
                              type="textarea"
                              rows="3"
                              maxlength="4000"
                              show-word-limit
                              placeholder="Goblet cells are considered as a homogeneous population in the intestinal epithelium. We used single cell RNA sequencing (scRNA-seq) to analyze the diversity of GCs in the intestine."
                            ></el-input>
                            <span class="mt-2 text-xs text-slate-600">
                              The proposition(s) being tested by the research study .
                            </span>
                          </div>
                        </el-form-item>

                        <el-form-item label="Objectives" prop="objectives">
                          <div class="flex w-full flex-col items-start">
                            <el-input
                              v-model="step2Form.objectives"
                              type="textarea"
                              rows="5"
                              placeholder="Goblet cells are considered as a homogeneous population in the intestinal epithelium. We used single cell RNA sequencing (scRNA-seq) to analyze the diversity of GCs in the intestine."
                            ></el-input>
                            <span class="mt-2 text-xs text-slate-600">
                              The goals of the research study.
                            </span>
                          </div>
                        </el-form-item>

                        <el-form-item label="Target Enrollment" prop="targetEnrollment">
                          <div class="flex w-full flex-col items-start">
                            <el-input-number v-model="step2Form.targetEnrollment" :min="1" />
                            <span class="mt-2 text-xs text-slate-600">
                              The number of subjects proposed to be enrolled in the study.
                            </span>
                          </div>
                        </el-form-item>

                        <el-form-item label="Mimimum Age" prop="minimumAge">
                          <div class="flex w-full flex-col items-start">
                            <el-input
                              v-model="step2Form.minimumAge"
                              placeholder="20"
                              maxlength="40"
                              show-word-limit
                            ></el-input>
                            <span class="mt-2 text-xs text-slate-600">
                              The minimum age of the subjects enrolled in the study.
                            </span>
                          </div>
                        </el-form-item>

                        <el-form-item label="Maximum Age" prop="maximumAge">
                          <div class="flex w-full flex-col items-start">
                            <el-input
                              v-model="step2Form.maximumAge"
                              placeholder="20"
                              maxlength="40"
                              show-word-limit
                            ></el-input>
                            <span class="mt-2 text-xs text-slate-600">
                              The maximum age of the subjects enrolled in the study.
                            </span>
                          </div>
                        </el-form-item>

                        <el-form-item label="Research Focus" prop="researchFocus">
                          <div class="flex w-full flex-col items-start">
                            <el-select
                              class="w-full"
                              v-model="step2Form.researchFocus"
                              placeholder="Molecular Biology"
                            >
                              <el-option
                                v-for="option in researchFocusOptions"
                                :key="option"
                                :label="option"
                                :value="option"
                              />
                            </el-select>
                            <span class="mt-2 text-xs text-slate-600">
                              The unit of time used to describe the subjects age in the study.
                            </span>
                          </div>
                        </el-form-item>

                        <el-form-item label="Condition or Disease" prop="condition">
                          <div class="flex w-full flex-col items-start">
                            <el-select
                              v-model="step2Form.condition"
                              class="w-full"
                              multiple
                              filterable
                              allow-create
                              default-first-option
                              :reserve-keyword="false"
                              placeholder="Aging"
                            >
                              <el-option
                                v-for="option in conditionOptions"
                                :key="option"
                                :label="option"
                                :value="option"
                              />
                            </el-select>
                            <span class="mt-2 text-xs text-slate-600">
                              The unit of time used to describe the subjects age in the study.
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
                      label-width="160px"
                      label-position="top"
                      size="large"
                      ref="s3Form"
                      @submit.prevent
                      class="pb-4"
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
                                    Title <span class="text-red-500"> * </span>
                                  </label>

                                  <el-input
                                    v-model="element.title"
                                    type="text"
                                    placeholder="[biomaterial], [condition(s)], [replicate number]"
                                  />
                                  <span class="mt-1 text-xs text-slate-600">
                                    Unique title that describes the Sample. We suggest the
                                    convention: [biomaterial], [condition(s)], [replicate number]
                                  </span>
                                </div>

                                <div class="mb-4 flex flex-col">
                                  <label class="w-[160px] pb-1 text-sm font-medium text-gray-700">
                                    Description <span class="text-red-500"> * </span>
                                  </label>
                                  <el-input
                                    v-model="element.description"
                                    type="textarea"
                                    placeholder="Description"
                                    class="mb-2"
                                  />
                                  <span class="mt-1 text-xs text-slate-600">
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
                                        Organism <span class="text-red-500"> * </span>
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
                                      <span class="mt-1 text-xs text-slate-600">
                                        Organisms from which the sequences was derived. <br />
                                        Start typing for suggestions.
                                      </span>
                                    </div>
                                  </div>

                                  <div class="mx-2 w-3/12">
                                    <div class="mb-4 flex flex-col">
                                      <label
                                        class="w-[160px] pb-1 text-sm font-medium text-gray-700"
                                      >
                                        Molecule <span class="text-red-500"> * </span>
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
                                      <span class="mt-1 text-xs text-slate-600">
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
                                        Single or paired end <span class="text-red-500"> * </span>
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
                                        Instrument Model <span class="text-red-500"> * </span>
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

                                <p class="">
                                  Sample Characteristics <span class="text-red-500"> * </span>
                                </p>
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
                                  <p class="my-2">
                                    Add your raw files <span class="text-red-500"> * </span>
                                  </p>

                                  <el-tree-select
                                    v-model="element.rawFiles"
                                    :data="element.filteredRawFilesFolderContents"
                                    @visible-change="getFilteredRawFilesFolderContents(element.id)"
                                    multiple
                                    clearable
                                    show-checkbox
                                  />
                                  <span class="mt-1 text-xs text-slate-600">
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
                                  <span class="mt-1 text-xs text-slate-600">
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
                            size="large"
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

    <!-- <app-docs-link url="curate-and-share/add-codemeta" position="bottom-4" /> -->
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
import ImmunologyJSON from "@/assets/supplementalFiles/immunology.json";

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
      currentStep: 1,
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
      researchFocusOptions: ImmunologyJSON.researchFocusOptions,
      conditionOptions: ImmunologyJSON.conditionOptions,
      generateImmunologyMetadata: "Yes",
      step1Form: {
        studyID: "",
        briefTitle: "",
        officialTitle: "",
        briefDescription: "",
        description: "",
        sponsoringOrganization: "",
      },
      step1FormRules: {
        studyID: [
          {
            required: true,
            message: "Please enter the name or ID of the study",
            trigger: "blur",
          },
        ],
        briefTitle: [
          {
            required: true,
            message: "Please enter a brief title for the study",
            trigger: "blur",
          },
        ],
        sponsoringOrganization: [
          {
            required: true,
            message: "Please enter the name of the sponsoring organization",
            trigger: "blur",
          },
        ],
        briefDescription: [
          {
            required: true,
            message: "Please enter a brief description of the study",
            trigger: "blur",
          },
        ],
        description: [
          {
            required: true,
            message: "Please enter a description of the study",
            trigger: "blur",
          },
        ],
      },
      step2Form: {
        researchFocus: "",
        condition: "",
        interventionAgent: "",
        endpoints: "",
        hypothesis: "",
        objectives: "",
        ageUnit: "",
        minimumAge: "",
        maximumAge: "",
        actualStartDate: "",
        targetEnrollment: 1,
      },
      step2FormRules: {
        endpoints: [
          {
            required: true,
            message: "Please enter the endpoints of the study",
            trigger: "blur",
          },
        ],
        interventionAgent: [
          {
            required: true,
            message: "Please enter the intervention agent of the study",
            trigger: "blur",
          },
        ],
        ageUnit: [
          {
            required: true,
            message: "Please select the age unit",
            trigger: "blur",
          },
        ],
      },
      step3Form: [],
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
      this.$refs["topOfPageElement"].scrollIntoView({
        behavior: "smooth",
        block: "start",
      });

      if (this.currentStep - 1 > 0) {
        this.currentStep--;
      } else {
        this.navigateBack();
      }
    },
    async nextFormStep() {
      if (this.currentStep + 1 > this.totalSteps) {
        const valid = await this.checkSamplesValidity();

        if (!valid) {
          return;
        }

        if (!this.checkInvalidStatus) {
          this.navigateToSelectDestination();
        }
      } else {
        this.currentStep++;
      }
    },
    async saveSkip() {
      if (this.generateImmunologyMetadata === "Yes") {
        this.workflow.generateImmunologyMetadata = true;
      } else {
        this.workflow.generateImmunologyMetadata = false;
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
          this.$refs["topOfPageElement"].scrollIntoView({
            behavior: "smooth",
            block: "start",
          });
        }
      });
    },
    navigateToStep3FromStep2() {
      this.$refs["s2Form"].validate(async (valid) => {
        if (valid) {
          await this.saveCurrentEntries();
          this.setCurrentStep(3);
          this.$refs["topOfPageElement"].scrollIntoView({
            behavior: "smooth",
            block: "start",
          });
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
    dataProcessingStepsValidator(_rule, value, callback) {
      if (value.length === 0) {
        callback(new Error("Please add at least one data processing step."));
      } else if ((value === "" || value === undefined) && value.length > 0) {
        callback(new Error("Please provide a valid data processing step."));
      } else {
        callback();
      }
    },

    libraryStrategyValidator(_rule, value, callback) {
      if (value === "" || value === undefined) {
        callback(new Error("Please provide a valid library strategy."));
      } else if (value === "OTHER:") {
        if (
          this.step2Form.otherLibraryStrategy === undefined ||
          this.step2Form.otherLibraryStrategy.trim() === ""
        ) {
          callback(new Error("Please provide a valid library strategy."));
        } else {
          callback();
        }
      } else {
        callback();
      }
    },

    filterArrayOfObjects(array, key) {
      return array.filter((element) => {
        return element[key] !== "";
      });
    },

    async checkSamplesValidity() {
      if (this.step3Form.length === 0) {
        this.$message.error("Please add at least one sample.");
        return false;
      }

      for (const sample of this.step3Form) {
        if (sample.libraryName.trim() === "") {
          this.$message.error("Please provide a library name for all samples.");
          return false;
        }

        if (sample.title.trim() === "") {
          this.$message.error(
            `Please provide a title for all samples. Sample ${sample.libraryName} is missing a title.`
          );
          return false;
        }

        if (sample.description.trim() === "") {
          this.$message.error(
            `Please provide a description for all samples. Sample ${sample.libraryName} is missing a description.`
          );
          return false;
        }

        if (sample.organism.trim() === "") {
          this.$message.error(
            `Please provide an organism for all samples. Sample ${sample.libraryName} is missing an organism.`
          );
          return false;
        }

        if (sample.molecule.trim() === "") {
          this.$message.error(
            `Please provide a molecule for all samples. Sample ${sample.libraryName} is missing a molecule.`
          );
          return false;
        }

        if (sample.singleOrPairedEnd.trim() === "") {
          this.$message.error(
            `Some samples are missing a single or paired end value. Sample ${sample.libraryName} is missing this value.`
          );
          return false;
        }

        if (sample.instrumentModel.trim() === "") {
          this.$message.error(
            `Some samples are missing an instrument model. Sample ${sample.libraryName} is missing this value.`
          );
          return false;
        }

        // get number of keys in object
        const keys = Object.keys(sample.characteristics);
        if (keys.length === 0) {
          this.$message.error("No required characteristics provided for samples.");
          return false;
        }

        if (
          !keys.includes("tissue") &&
          !keys.includes("cell line") &&
          !keys.includes("cell type")
        ) {
          this.$message.error(
            "Some required characteristics are missing for samples. Please provide at least one of the following: tissue, cell line or cell type."
          );
          return false;
        }

        for (const characteristic in sample.characteristics) {
          if (sample.characteristics[characteristic].trim() === "") {
            this.$message.error(
              `Please provide a value for all samples' characteristics. Sample ${sample.libraryName} is missing a value for ${characteristic}.`
            );
            return false;
          }
        }

        if (sample.rawFiles.length === 0) {
          this.$message.error(
            `Please provide at least one raw file for all samples. Sample ${sample.libraryName} is missing raw files.`
          );
          return false;
        }
      }

      return true;
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
      this.customFieldName = "";
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

      this.dataset.data.general.questions.name = this.step1Form.briefTitle;
      this.dataset.data.general.questions.description = this.step1Form.briefDescription;

      let immunologyForm = {};

      immunologyForm.studyID = this.step1Form.studyID.trim();
      immunologyForm.briefTitle = this.step1Form.briefTitle.trim();
      immunologyForm.officialTitle = this.step1Form.officialTitle.trim();
      immunologyForm.briefDescription = this.step1Form.briefDescription.trim();
      immunologyForm.description = this.step1Form.description.trim();
      immunologyForm.sponsoringOrganization = this.step1Form.sponsoringOrganization.trim();

      immunologyForm.interventionAgent = this.step2Form.interventionAgent.trim();
      immunologyForm.endpoints = this.step2Form.endpoints;
      immunologyForm.ageUnit = this.step2Form.ageUnit;
      immunologyForm.actualStartDate = this.step2Form.actualStartDate;
      immunologyForm.hypothesis = this.step2Form.hypothesis.trim();
      immunologyForm.objectives = this.step2Form.objectives.trim();
      immunologyForm.targetEnrollment = this.step2Form.targetEnrollment;
      immunologyForm.minimumAge = this.step2Form.minimumAge.trim();
      immunologyForm.maximumAge = this.step2Form.maximumAge.trim();
      immunologyForm.researchFocus = this.step2Form.researchFocus;
      immunologyForm.condition = this.step2Form.condition;

      this.dataset.data.Immunology.questions = immunologyForm;

      this.workflow.generateImmunologyMetadata = true;

      if (this.generateImmunologyMetadata === "Yes") {
        this.workflow.generateImmunologyMetadata = true;
      } else {
        this.workflow.generateImmunologyMetadata = false;
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

      if ("generateImmunologyMetadata" in this.workflow) {
        this.generateImmunologyMetadata = this.workflow.generateImmunologyMetadata ? "Yes" : "No";
      } else {
        this.generateImmunologyMetadata = "None";
      }

      if (
        this.dataset.data.Immunology.questions &&
        Object.keys(this.dataset.data.Immunology.questions).length !== 0
      ) {
        let immunologyForm = this.dataset.data.Immunology.questions;

        this.step1Form.studyID = immunologyForm.studyID;
        this.step1Form.briefTitle = immunologyForm.briefTitle;
        this.step1Form.officialTitle = immunologyForm.officialTitle;
        this.step1Form.briefDescription = immunologyForm.briefDescription;
        this.step1Form.description = immunologyForm.description;
        this.step1Form.sponsoringOrganization = immunologyForm.sponsoringOrganization;

        this.step2Form.interventionAgent = immunologyForm.interventionAgent;
        this.step2Form.endpoints = immunologyForm.endpoints;
        this.step2Form.ageUnit = immunologyForm.ageUnit;
        this.step2Form.actualStartDate = immunologyForm.actualStartDate;
        this.step2Form.hypothesis = immunologyForm.hypothesis;
        this.step2Form.objectives = immunologyForm.objectives;
        this.step2Form.targetEnrollment = immunologyForm.targetEnrollment;
        this.step2Form.minimumAge = immunologyForm.minimumAge;
        this.step2Form.maximumAge = immunologyForm.maximumAge;
        this.step2Form.researchFocus = immunologyForm.researchFocus;
        this.step2Form.condition = immunologyForm.condition;

        this.step3Form = immunologyForm.samples;

        // this.addIds(this.step2Form.dataProcessingSteps);
      } else {
        this.step1Form.briefTitle = this.dataset.name;
        this.step1Form.briefDescription = this.dataset.description;

        if ("source" in this.workflow) {
          if (this.workflow.source.type === "local") {
            /**
             * TODO: Will need to enable this when we figure out how to read in metadata files
             */
            // this.showSpinner = true;
            // const response = await axios
            //   .post(`${this.$server_url}/utilities/fileexistinfolder`, {
            //     folder_path: this.dataset.data.Immunology.folderPath,
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
            folder_path: this.dataset.data.Immunology.folderPath,
          });

          this.folderContents = response.data.children;
        }
      }
    });
  },
};
</script>
