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
                <span>
                  Provide information about your dataset below. We will use this information to
                  automatically generate and include in your dataset the standard metadata files
                  required.
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
                            <div class="flex w-full space-x-4">
                              <el-input
                                v-model="step1Form.studyID"
                                placeholder="study_198423"
                                maxlength="150"
                                show-word-limit
                                class="w-full"
                              />

                              <el-popover
                                placement="top-start"
                                :width="180"
                                trigger="hover"
                                content="Automatically generate a random ID."
                              >
                                <template #reference>
                                  <button
                                    @click="generateRandomID('study')"
                                    class="rounded-md px-3 hover:bg-slate-100"
                                  >
                                    <Icon icon="mdi:magic" />
                                  </button>
                                </template>
                              </el-popover>
                            </div>
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
                            />
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
                            />
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
                            />
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
                            />
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
                            />
                            <span class="mt-2 text-xs text-slate-600">
                              The organization that provides funding and support for the study.
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
                            />
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
                            />
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
                            />
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
                            />
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
                            />
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
                            />
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
                        @start="minimizeAllArmGroups"
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

                                <span class="flex items-center"> {{ element.armID }} </span>

                                <div
                                  class="ml-2 flex cursor-pointer items-center justify-center rounded-md p-2 text-gray-500 transition-all hover:bg-slate-200 hover:text-gray-800"
                                  @click.stop="editArmID(element.id)"
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
                                  @click.stop="showRemoveArmGroupConfirm(element.id)"
                                >
                                  <el-icon><delete-filled /></el-icon>
                                </div>
                              </div>
                            </div>

                            <el-collapse-transition>
                              <div class="mt-4 flex flex-col px-4" v-show="element.isExpanded">
                                <div class="mb-4 flex flex-col">
                                  <label class="w-[160px] pb-1 text-sm font-medium text-gray-700">
                                    Name <span class="text-red-500"> * </span>
                                  </label>

                                  <el-input
                                    v-model="element.name"
                                    type="text"
                                    placeholder="arm-cohort_1056-7"
                                    maxlength="126"
                                    show-word-limit
                                  />
                                  <span class="mt-1 text-xs text-slate-600">
                                    The arm or cohort name is an alternate identifier that is
                                    visible when the study is shared.
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
                                    maxlength="4000"
                                    show-word-limit
                                    rows="4"
                                  />
                                  <span class="mt-1 text-xs text-slate-600">
                                    The arm or cohort description should explain any abbreviations
                                    used in the arm or cohort name.
                                  </span>
                                </div>

                                <div class="mb-4 flex flex-col">
                                  <label class="w-[160px] pb-1 text-sm font-medium text-gray-700">
                                    Type Reported <span class="text-red-500"> * </span>
                                  </label>

                                  <el-select
                                    v-model="element.type"
                                    filterable
                                    allow-create
                                    default-first-option
                                    :reserve-keyword="false"
                                    placeholder="Choose a type for this group"
                                  >
                                    <el-option
                                      v-for="item in armTypeOptions"
                                      :key="item"
                                      :label="item"
                                      :value="item"
                                    />
                                  </el-select>

                                  <span class="mt-1 text-xs text-slate-600">
                                    Arms used in the clinical trial. Terms are derived from the
                                    National Cancer Institute.
                                  </span>
                                </div>
                              </div>
                            </el-collapse-transition>
                          </div>
                        </template>
                      </draggable>

                      <edit-prompt
                        ref="editArmIDPrompt"
                        title="Edit Arm/Cohort/Subject group ID"
                        confirmButtonText="Save"
                        :confirmDisabled="disableEditArmIDSaveButton"
                        @messageConfirmed="saveUpdatedArmID"
                      >
                        <div w-full>
                          <p class="mb-3 text-sm">Please enter a new ID for this group.</p>

                          <div class="flex w-full space-x-2">
                            <el-input
                              v-model="armID"
                              size="large"
                              clearable
                              class="w-full"
                              placeholder="arm_i5nUpTcaZ"
                              maxlength="100"
                              show-word-limit
                            />

                            <el-popover
                              placement="top-start"
                              :width="180"
                              trigger="hover"
                              content="Automatically generate a random ID."
                            >
                              <template #reference>
                                <button
                                  @click="generateRandomID('arm-cohort')"
                                  class="rounded-md px-3 hover:bg-slate-100"
                                >
                                  <Icon icon="mdi:magic" />
                                </button>
                              </template>
                            </el-popover>
                          </div>
                        </div>
                      </edit-prompt>

                      <warning-confirm
                        ref="removeArmGroupConfirm"
                        title="Warning"
                        @messageConfirmed="confirmedRemoveArmGroup"
                      >
                        <p class="text-center text-base text-gray-500">
                          Are you sure you want to remove this group? This action cannot be undone.
                        </p>
                      </warning-confirm>
                    </el-form>
                    <div class="m-2 flex w-full justify-center">
                      <button class="primary-plain-button" @click="showAddArmGroupPrompt">
                        Add an Arm/Cohort/Subject group
                      </button>

                      <add-prompt
                        ref="addArmGroupPrompt"
                        title="Add a Arm/Cohort/Subject group"
                        confirmButtonText="Add this group"
                        :confirmDisabled="disableEditArmIDSaveButton"
                        @messageConfirmed="addArmGroupConfirmed"
                      >
                        <div w-full>
                          <p class="mb-3 text-sm">
                            Please add a unique ID for this Arm/Cohort/Subject group. This ID should
                            be unique within your ImmPort workspace.
                          </p>

                          <div class="flex w-full space-x-2">
                            <el-input
                              v-model="armID"
                              clearable
                              size="large"
                              class="w-full"
                              placeholder="Enter a ID for this Arm/Cohort/Subject group"
                              maxlength="100"
                              show-word-limit
                            />

                            <el-popover
                              placement="top-start"
                              :width="180"
                              trigger="hover"
                              content="Automatically generate a random ID."
                            >
                              <template #reference>
                                <button
                                  @click="generateRandomID('arm-cohort')"
                                  class="rounded-md px-3 hover:bg-slate-100"
                                >
                                  <Icon icon="mdi:magic" />
                                </button>
                              </template>
                            </el-popover>
                          </div>
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
                  <div class="px-4 pb-4 pt-2">
                    <el-form
                      :model="step4Form"
                      label-width="160px"
                      label-position="top"
                      size="large"
                      ref="s3Form"
                      @submit.prevent
                      class="pb-4"
                    >
                      <draggable
                        tag="div"
                        :list="step4Form"
                        item-key="id"
                        handle=".handle"
                        :animation="200"
                        @start="minimizeAllPersonnel"
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

                                <span class="flex items-center"> {{ element.personnelID }} </span>

                                <div
                                  class="ml-2 flex cursor-pointer items-center justify-center rounded-md p-2 text-gray-500 transition-all hover:bg-slate-200 hover:text-gray-800"
                                  @click.stop="editPersonnelID(element.id)"
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
                                  @click.stop="showRemovePersonnelEntryConfirm(element.id)"
                                >
                                  <el-icon><delete-filled /></el-icon>
                                </div>
                              </div>
                            </div>

                            <el-collapse-transition>
                              <div class="mt-4 flex flex-col px-4" v-show="element.isExpanded">
                                <div
                                  class="mb-2 flex w-full flex-row justify-between transition-all"
                                >
                                  <div class="mr-2 w-2/12">
                                    <div class="mb-4 flex flex-col">
                                      <label
                                        class="w-[160px] pb-1 text-sm font-medium text-gray-700"
                                      >
                                        Honorific
                                      </label>
                                      <el-input
                                        v-model="element.honorific"
                                        type="text"
                                        placeholder="Dr."
                                        maxlength="20"
                                        show-word-limit
                                      />
                                    </div>
                                  </div>

                                  <div class="mx-2 w-4/12">
                                    <div class="mb-4 flex flex-col">
                                      <label
                                        class="w-[160px] pb-1 text-sm font-medium text-gray-700"
                                      >
                                        First Name <span class="text-red-500"> * </span>
                                      </label>
                                      <el-input
                                        v-model="element.firstName"
                                        type="text"
                                        placeholder="Steven"
                                        maxlength="40"
                                        show-word-limit
                                      />
                                    </div>
                                  </div>

                                  <div class="mx-2 w-4/12">
                                    <div class="mb-4 flex flex-col">
                                      <label
                                        class="w-[160px] pb-1 text-sm font-medium text-gray-700"
                                      >
                                        Last Name <span class="text-red-500"> * </span>
                                      </label>
                                      <el-input
                                        v-model="element.lastName"
                                        type="text"
                                        placeholder="Strange"
                                        maxlength="40"
                                        show-word-limit
                                      />
                                    </div>
                                  </div>

                                  <div class="mx-2 w-2/12">
                                    <div class="mb-4 flex flex-col">
                                      <label
                                        class="w-[160px] pb-1 text-sm font-medium text-gray-700"
                                      >
                                        Suffix
                                      </label>
                                      <el-input
                                        v-model="element.suffix"
                                        type="text"
                                        placeholder="Jr."
                                        maxlength="40"
                                        show-word-limit
                                      />
                                    </div>
                                  </div>
                                </div>

                                <div class="mb-4 flex flex-col">
                                  <label class="w-[160px] pb-1 text-sm font-medium text-gray-700">
                                    Organization <span class="text-red-500"> * </span>
                                  </label>

                                  <el-input
                                    v-model="element.organization"
                                    type="text"
                                    placeholder="University of California, San Francisco"
                                    maxlength="100"
                                    show-word-limit
                                  />
                                  <span class="mt-1 text-xs text-slate-600">
                                    The organization with whom the study personnel being described
                                    is affiliated.
                                  </span>
                                </div>

                                <div class="mb-4 flex flex-col">
                                  <label class="w-[160px] pb-1 text-sm font-medium text-gray-700">
                                    Site Name <span class="text-red-500"> * </span>
                                  </label>

                                  <el-input
                                    v-model="element.siteName"
                                    type="text"
                                    placeholder="Department of Neurology"
                                    maxlength="125"
                                    show-word-limit
                                  />
                                  <span class="mt-1 text-xs text-slate-600">
                                    Enter the site name if there is a need to further differentiate
                                    the affiliation of the study personnel from the organization.
                                  </span>
                                </div>

                                <div class="mb-4 flex flex-col">
                                  <label class="w-[160px] pb-1 text-sm font-medium text-gray-700">
                                    Email <span class="text-red-500"> * </span>
                                  </label>

                                  <el-input
                                    v-model="element.email"
                                    type="text"
                                    placeholder="stevenstrange@ucsf.edu"
                                    maxlength="100"
                                    show-word-limit
                                  />
                                  <span class="mt-1 text-xs text-slate-600">
                                    The organization with whom the study personnel being described
                                    is affiliated.
                                  </span>
                                </div>

                                <div class="mb-4 flex flex-col">
                                  <label class="w-[160px] pb-1 text-sm font-medium text-gray-700">
                                    ORCID
                                  </label>

                                  <el-input
                                    v-model="element.orcid"
                                    type="text"
                                    placeholder="0000-0003-2829-8032"
                                    maxlength="100"
                                    show-word-limit
                                  />
                                  <span class="mt-1 text-xs text-slate-600">
                                    The organization with whom the study personnel being described
                                    is affiliated.
                                  </span>
                                </div>

                                <div class="mb-4 flex flex-col">
                                  <label class="w-[160px] pb-1 text-sm font-medium text-gray-700">
                                    Title in the Study <span class="text-red-500"> * </span>
                                  </label>

                                  <el-input
                                    v-model="element.titleInStudy"
                                    type="text"
                                    placeholder="Principal Investigator"
                                    maxlength="100"
                                    show-word-limit
                                  />
                                  <span class="mt-1 text-xs text-slate-600">
                                    The role the personnel plays in the study as defined by the
                                    research team.
                                  </span>
                                </div>

                                <div class="mb-4 flex flex-col">
                                  <label class="w-[160px] pb-1 text-sm font-medium text-gray-700">
                                    Role in the Study <span class="text-red-500"> * </span>
                                  </label>

                                  <el-select
                                    v-model="element.roleInStudy"
                                    filterable
                                    default-first-option
                                    :reserve-keyword="false"
                                    placeholder="Choose a type for this group"
                                  >
                                    <el-option
                                      v-for="item in studyRoleOptions"
                                      :key="item"
                                      :label="item"
                                      :value="item"
                                    />
                                  </el-select>

                                  <span class="mt-1 text-xs text-slate-600"> </span>
                                </div>
                              </div>
                            </el-collapse-transition>
                          </div>
                        </template>
                      </draggable>

                      <edit-prompt
                        ref="editpersonnelIDPrompt"
                        title="Edit Arm/Cohort/Subject group ID"
                        confirmButtonText="Save"
                        :confirmDisabled="disableEditPersonnelIDSaveButton"
                        @messageConfirmed="saveUpdatedPersonnelID"
                      >
                        <div w-full>
                          <p class="mb-3 text-sm">Please enter a new ID for this person.</p>

                          <div class="flex w-full space-x-2">
                            <el-input
                              v-model="personnelID"
                              clearable
                              size="large"
                              class="w-full"
                              placeholder="Enter a ID for this person"
                              maxlength="100"
                              show-word-limit
                            />

                            <el-popover
                              placement="top-start"
                              :width="180"
                              trigger="hover"
                              content="Automatically generate a random ID."
                            >
                              <template #reference>
                                <button
                                  @click="generateRandomID('personnel')"
                                  class="rounded-md px-3 hover:bg-slate-100"
                                >
                                  <Icon icon="mdi:magic" />
                                </button>
                              </template>
                            </el-popover>
                          </div>
                        </div>
                      </edit-prompt>

                      <warning-confirm
                        ref="removePersonnelEntryConfirm"
                        title="Warning"
                        @messageConfirmed="confirmedRemovePersonnelEntry"
                      >
                        <p class="text-center text-base text-gray-500">
                          Are you sure you want to remove this person from this study? This action
                          cannot be undone.
                        </p>
                      </warning-confirm>
                    </el-form>
                    <div class="m-2 flex w-full justify-center">
                      <button class="primary-plain-button" @click="showAddPersonnelPrompt">
                        Add a person to the study
                      </button>

                      <add-prompt
                        ref="addPersonnelPrompt"
                        title="Add a person"
                        confirmButtonText="Add this person to the study"
                        :confirmDisabled="disableEditPersonnelIDSaveButton"
                        @messageConfirmed="addPersonnelConfirmed"
                      >
                        <div w-full>
                          <p class="mb-3 text-sm">
                            Please add a unique ID for this person. This ID should be unique within
                            your ImmPort workspace.
                          </p>

                          <div class="flex w-full space-x-2">
                            <el-input
                              v-model="personnelID"
                              clearable
                              size="large"
                              class="w-full"
                              placeholder="personnel_1056_2"
                              maxlength="100"
                              show-word-limit
                            />

                            <el-popover
                              placement="top-start"
                              :width="180"
                              trigger="hover"
                              content="Automatically generate a random ID."
                            >
                              <template #reference>
                                <button
                                  @click="generateRandomID('personnel')"
                                  class="rounded-md px-3 hover:bg-slate-100"
                                >
                                  <Icon icon="mdi:magic" />
                                </button>
                              </template>
                            </el-popover>
                          </div>
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

                    <button
                      class="primary-button"
                      @click="navigateToStep5FromStep4"
                      :disabled="checkInvalidStatus"
                    >
                      Next
                      <el-icon><right-icon /></el-icon>
                    </button>
                  </div>
                </div>

                <div v-if="currentStep == 5">
                  <div class="px-4 pb-4 pt-2">
                    <el-form
                      :model="step5Form"
                      label-width="160px"
                      label-position="top"
                      size="large"
                      ref="s3Form"
                      @submit.prevent
                      class="pb-4"
                    >
                      <draggable
                        tag="div"
                        :list="step5Form"
                        item-key="id"
                        handle=".handle"
                        :animation="200"
                        @start="minimizeAllPlannedVisits"
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

                                <span class="flex items-center"> {{ element.visitID }} </span>

                                <div
                                  class="ml-2 flex cursor-pointer items-center justify-center rounded-md p-2 text-gray-500 transition-all hover:bg-slate-200 hover:text-gray-800"
                                  @click.stop="editPlannedVisitID(element.id)"
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
                                  @click.stop="showRemovePlannedVisitConfirm(element.id)"
                                >
                                  <el-icon><delete-filled /></el-icon>
                                </div>
                              </div>
                            </div>

                            <el-collapse-transition>
                              <div class="mt-4 flex flex-col px-4" v-show="element.isExpanded">
                                <div class="mb-4 flex flex-col">
                                  <label class="w-[160px] pb-1 text-sm font-medium text-gray-700">
                                    Visit Name <span class="text-red-500"> * </span>
                                  </label>

                                  <el-input
                                    v-model="element.name"
                                    type="text"
                                    placeholder="Screening Vaccination, Week 1"
                                    maxlength="125"
                                    show-word-limit
                                  />
                                  <span class="mt-1 text-xs text-slate-600">
                                    This is an alternate identifier that is visible when the study
                                    is shared.
                                  </span>
                                </div>

                                <div class="mb-4 flex flex-col">
                                  <label class="w-[160px] pb-1 text-sm font-medium text-gray-700">
                                    Order Number <span class="text-red-500"> * </span>
                                  </label>
                                  <el-input-number v-model="element.orderNumber" :min="1" />
                                  <span class="mt-1 text-xs text-slate-600">
                                    The order of the visit within the study schedule.
                                  </span>
                                </div>

                                <div
                                  class="mb-2 flex w-full flex-row justify-between transition-all"
                                >
                                  <div class="mr-2 w-6/12">
                                    <div class="mb-4 flex flex-col">
                                      <label
                                        class="w-[160px] pb-1 text-sm font-medium text-gray-700"
                                      >
                                        Min Start Day <span class="text-red-500"> * </span>
                                      </label>
                                      <el-input-number v-model="element.minStartDay" :min="1" />
                                      <span class="mt-1 text-xs text-slate-600">
                                        The minimum start day for a visit as defined in the study
                                        schedule.
                                      </span>
                                    </div>
                                  </div>

                                  <div class="mx-2 w-6/12">
                                    <div class="mb-4 flex flex-col">
                                      <label
                                        class="w-[160px] pb-1 text-sm font-medium text-gray-700"
                                      >
                                        Max Start Day <span class="text-red-500"> * </span>
                                      </label>
                                      <el-input-number v-model="element.maxStartDay" :min="1" />
                                      <span class="mt-1 text-xs text-slate-600">
                                        The maximum start day for a visit as defined in the study
                                        schedule.
                                      </span>
                                    </div>
                                  </div>
                                </div>

                                <div class="mb-4 flex flex-col">
                                  <label class="w-[160px] pb-1 text-sm font-medium text-gray-700">
                                    Start Rule
                                  </label>

                                  <el-input
                                    v-model="element.startRule"
                                    type="text"
                                    placeholder="2 weeks after initial vaccination"
                                    maxlength="256"
                                    show-word-limit
                                  />
                                  <span class="mt-1 text-xs text-slate-600">
                                    Enter a start rule for the visit, if applicable.
                                  </span>
                                </div>

                                <div class="mb-4 flex flex-col">
                                  <label class="w-[160px] pb-1 text-sm font-medium text-gray-700">
                                    End Rule
                                  </label>

                                  <el-input
                                    v-model="element.endRule"
                                    type="text"
                                    placeholder="Subjects experience a severe or fatal adverse event"
                                    maxlength="256"
                                    show-word-limit
                                  />
                                  <span class="mt-1 text-xs text-slate-600">
                                    Enter an end rule for the visit, if applicable.
                                  </span>
                                </div>
                              </div>
                            </el-collapse-transition>
                          </div>
                        </template>
                      </draggable>

                      <edit-prompt
                        ref="editPlannedVisitPrompt"
                        title="Edit Planned Visit ID"
                        confirmButtonText="Save"
                        :confirmDisabled="disableEditPlannedVisitsIDSaveButton"
                        @messageConfirmed="saveUpdatedPlannedVisitID"
                      >
                        <div w-full>
                          <p class="mb-3 text-sm">Please enter a new ID for this visit.</p>

                          <div class="flex w-full space-x-2">
                            <el-input
                              v-model="visitID"
                              clearable
                              size="large"
                              class="w-full"
                              placeholder="plannedvisit_1056_2"
                              maxlength="100"
                              show-word-limit
                            />

                            <el-popover
                              placement="top-start"
                              :width="180"
                              trigger="hover"
                              content="Automatically generate a random ID."
                            >
                              <template #reference>
                                <button
                                  @click="generateRandomID('plannedvisit')"
                                  class="rounded-md px-3 hover:bg-slate-100"
                                >
                                  <Icon icon="mdi:magic" />
                                </button>
                              </template>
                            </el-popover>
                          </div>
                        </div>
                      </edit-prompt>

                      <warning-confirm
                        ref="removePlannedVisitConfirm"
                        title="Warning"
                        @messageConfirmed="confirmedRemovePlannedVisit"
                      >
                        <p class="text-center text-base text-gray-500">
                          Are you sure you want to remove this person from this study? This action
                          cannot be undone.
                        </p>
                      </warning-confirm>
                    </el-form>
                    <div class="m-2 flex w-full justify-center">
                      <button class="primary-plain-button" @click="showAddPlannedVisitPrompt">
                        Add a Planned Visit/Time Series to the study
                      </button>

                      <add-prompt
                        ref="addPlannedVisitPrompt"
                        title="Add a Planned Visit/Time Series to the study"
                        confirmButtonText="Add this planned visit to the study"
                        :confirmDisabled="disableEditPlannedVisitsIDSaveButton"
                        @messageConfirmed="addPlannedVisitConfirmed"
                      >
                        <div w-full>
                          <p class="mb-3 text-sm">
                            Please add a unique ID for this visit. This ID should be unique within
                            your ImmPort workspace.
                          </p>

                          <div class="flex w-full space-x-2">
                            <el-input
                              v-model="visitID"
                              clearable
                              size="large"
                              class="w-full"
                              placeholder="plannedvisit_1056_2"
                              maxlength="100"
                              show-word-limit
                            />

                            <el-popover
                              placement="top-start"
                              :width="180"
                              trigger="hover"
                              content="Automatically generate a random ID."
                            >
                              <template #reference>
                                <button
                                  @click="generateRandomID('plannedvisit')"
                                  class="rounded-md px-3 hover:bg-slate-100"
                                >
                                  <Icon icon="mdi:magic" />
                                </button>
                              </template>
                            </el-popover>
                          </div>
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

                    <button
                      class="primary-button"
                      @click="navigateToStep6FromStep5"
                      :disabled="checkInvalidStatus"
                    >
                      Next
                      <el-icon><right-icon /></el-icon>
                    </button>
                  </div>
                </div>

                <div v-if="currentStep == 6">
                  <div
                    class="form-card-content mb-4 rounded-lg border-2 border-slate-100 shadow-md"
                  >
                    <div class="w-full bg-gray-100 px-4 py-2">
                      <span class="pointer-events-none text-lg font-semibold text-primary-600">
                        Inclusion or Exclusion Criteria
                      </span>
                    </div>
                    <div class="p-4">
                      <el-form
                        :model="step6Form"
                        :rules="step6FormRules"
                        label-width="160px"
                        label-position="top"
                        size="large"
                        ref="s6Form"
                        @submit.prevent
                        class="py-4"
                      >
                        <el-form-item label="Inclusions & Exclusions" prop="inexclusions">
                          <draggable
                            tag="div"
                            :list="step6Form.inexclusions"
                            item-key="id"
                            :animation="200"
                            handle=".handle"
                            class="w-full divide-y-2"
                          >
                            <template #item="{ element }">
                              <div class="mb-2 flex w-full flex-row justify-between py-2">
                                <div class="flex w-11/12 flex-col px-2">
                                  <div class="flex w-full flex-row justify-between">
                                    <el-input
                                      v-model="element.userDefinedID"
                                      type="text"
                                      placeholder="User Defined ID"
                                      class="h-[40px]"
                                      maxlength="100"
                                      show-word-limit
                                    />

                                    <div class="mx-1"></div>

                                    <el-select
                                      v-model="element.criterionCategory"
                                      class=""
                                      placeholder="Criterion Category"
                                      size="large"
                                    >
                                      <el-option label="Inclusion" value="Inclusion" />
                                      <el-option label="Exclusion" value="Exclusion" />
                                    </el-select>
                                  </div>

                                  <div class="my-2"></div>

                                  <div class="flex w-full flex-col">
                                    <el-input
                                      v-model="element.criterion"
                                      type="textarea"
                                      placeholder="Criterion"
                                      maxlength="750"
                                      show-word-limit
                                    />
                                    <span class="mt-1 text-xs text-gray-400">
                                      The criterion describes the parameter used to decide if a
                                      subject may be enrolled in a study.
                                    </span>
                                  </div>
                                </div>
                                <div class="flex w-1/12 flex-row items-center justify-evenly">
                                  <div
                                    class="handle flex items-center justify-center text-gray-400 hover:text-gray-700"
                                  >
                                    <Icon icon="ic:outline-drag-indicator" />
                                  </div>
                                  <div
                                    class="flex cursor-pointer items-center justify-center text-gray-500 transition-all hover:text-gray-800"
                                  >
                                    <el-popconfirm
                                      width="220"
                                      confirm-button-text="Yes"
                                      cancel-button-text="No"
                                      icon-color="red"
                                      title="Are you sure you want to remove this?"
                                      @confirm="deleteInexclusion(element.id)"
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
                          class="mb-6 flex w-max cursor-pointer items-center text-sm text-gray-500 hover:text-black"
                          @click="addInexclusion"
                        >
                          <Icon icon="carbon:add" />
                          <span class="text-primary-600 hover:text-primary-500">
                            Add an inclusion/exclusion
                          </span>
                          <form-help-content
                            popoverContent="Add a new inclusion/exclusion to the list."
                          ></form-help-content>
                        </div>
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

                    <button
                      class="primary-button"
                      @click="navigateToStep7FromStep6"
                      :disabled="checkInvalidStatus"
                    >
                      Next
                      <el-icon><right-icon /></el-icon>
                    </button>
                  </div>
                </div>

                <div v-if="currentStep == 7">
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
                        :model="step7Form"
                        :rules="step7FormRules"
                        label-width="160px"
                        label-position="top"
                        size="large"
                        ref="s7Form"
                        @submit.prevent
                        class="py-4"
                      >
                        <el-form-item label="Protocol" prop="protocols">
                          <draggable
                            tag="div"
                            :list="step7Form.protocols"
                            item-key="id"
                            :animation="200"
                            handle=".handle"
                            class="w-full divide-y-2"
                          >
                            <template #item="{ element }">
                              <div class="flex w-full flex-row justify-between py-4">
                                <div class="flex w-11/12 flex-col px-2">
                                  <div class="flex w-full flex-row justify-between">
                                    <div class="flex w-full flex-col">
                                      <div class="flex w-full space-x-1">
                                        <el-input
                                          v-model="element.userDefinedID"
                                          type="text"
                                          placeholder="User Defined ID"
                                          class="h-[40px]"
                                          maxlength="100"
                                          show-word-limit
                                        />

                                        <el-popover
                                          placement="top-start"
                                          :width="180"
                                          trigger="hover"
                                          content="Automatically generate a random ID."
                                        >
                                          <template #reference>
                                            <button
                                              @click="
                                                () =>
                                                  (element.userDefinedID =
                                                    generateRandomID('protocol'))
                                              "
                                              class="rounded-md px-3 hover:bg-slate-100"
                                            >
                                              <Icon icon="mdi:magic" />
                                            </button>
                                          </template>
                                        </el-popover>
                                      </div>

                                      <span class="mt-1 text-xs text-gray-400">
                                        Should be unique across your ImmPort workspace.
                                      </span>
                                    </div>

                                    <div class="mx-3"></div>

                                    <el-select
                                      v-model="element.type"
                                      class=""
                                      placeholder="Protocol Type"
                                      size="large"
                                    >
                                      <el-option
                                        v-for="type in protocolTypeOptions"
                                        :key="type"
                                        :label="type"
                                        :value="type"
                                      />
                                    </el-select>
                                  </div>

                                  <div class="my-2"></div>

                                  <div class="flex w-full flex-col">
                                    <el-input
                                      v-model="element.name"
                                      type="text"
                                      placeholder="Name"
                                      maxlength="250"
                                      show-word-limit
                                    />
                                    <span class="mt-1 text-xs text-gray-400">
                                      The protocol name is an alternate identifier that is visible
                                      when the protocol is shared.
                                    </span>
                                  </div>

                                  <div class="my-2"></div>

                                  <div class="flex w-full flex-col">
                                    <el-input
                                      v-model="element.description"
                                      type="textarea"
                                      placeholder="Description"
                                      rows="3"
                                      maxlength="4000"
                                      show-word-limit
                                    />
                                    <span class="mt-1 text-xs text-gray-400">
                                      The protocol summary describes the purpose of the protocol.
                                    </span>
                                  </div>

                                  <div class="my-2"></div>

                                  <div class="flex flex-col">
                                    <el-tree-select
                                      v-model="element.filePath"
                                      :data="step7Form.filteredFolderContents"
                                      @visible-change="
                                        getFilteredFolderContentsForProtocols(element.filePath)
                                      "
                                      placeholder="Select a file to associate with this protocol"
                                      clearable
                                      class="w-full"
                                    />
                                    <span class="mt-2 text-xs text-slate-600">
                                      Select the file that is associated with this protocol.
                                    </span>
                                  </div>
                                </div>
                                <div class="flex w-1/12 flex-row items-center justify-evenly">
                                  <div
                                    class="handle flex items-center justify-center text-gray-400 hover:text-gray-700"
                                  >
                                    <Icon icon="ic:outline-drag-indicator" />
                                  </div>
                                  <div
                                    class="flex cursor-pointer items-center justify-center text-gray-500 transition-all hover:text-gray-800"
                                  >
                                    <el-popconfirm
                                      width="220"
                                      confirm-button-text="Yes"
                                      cancel-button-text="No"
                                      icon-color="red"
                                      title="Are you sure you want to remove this?"
                                      @confirm="deleteProtocol(element.id)"
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
                          class="mb-6 flex w-max cursor-pointer items-center text-sm text-gray-500 hover:text-black"
                          @click="addProtocol"
                        >
                          <Icon icon="carbon:add" />
                          <span class="text-primary-600 hover:text-primary-500">
                            Add a new protocol
                          </span>
                          <form-help-content
                            popoverContent="Add a new protocol to the list."
                          ></form-help-content>
                        </div>
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
                      @click="navigateToStep8FromStep7"
                      :disabled="checkInvalidStatus"
                    >
                      Next
                      <el-icon><right-icon /></el-icon>
                    </button>
                  </div>
                </div>

                <div v-if="currentStep == 8">
                  <div
                    class="form-card-content mb-4 rounded-lg border-2 border-slate-100 shadow-md"
                  >
                    <div class="w-full bg-gray-100 px-4 py-2">
                      <span class="pointer-events-none text-lg font-semibold text-primary-600">
                        Study Files and Links
                      </span>
                    </div>
                    <div class="p-4">
                      <el-form
                        :model="step8Form"
                        :rules="step8FormRules"
                        label-width="160px"
                        label-position="top"
                        size="large"
                        ref="s8Form"
                        @submit.prevent
                        class="py-4"
                      >
                        <el-form-item label="Study Files" prop="studyFiles">
                          <draggable
                            tag="div"
                            :list="step8Form.studyFiles"
                            item-key="id"
                            :animation="200"
                            handle=".handle"
                            class="w-full divide-y-2"
                          >
                            <template #item="{ element }">
                              <div class="flex w-full flex-row justify-between py-4">
                                <div class="flex w-11/12 flex-col px-2">
                                  <div class="flex flex-col">
                                    <el-select
                                      v-model="element.type"
                                      class=""
                                      placeholder="Study File Type"
                                      size="large"
                                    >
                                      <el-option
                                        v-for="type in studyFileTypeOptions"
                                        :key="type"
                                        :label="type"
                                        :value="type"
                                      />
                                    </el-select>
                                    <span class="mt-2 text-xs text-slate-600"> text here... </span>
                                  </div>

                                  <div class="my-2"></div>

                                  <div class="flex flex-col">
                                    <el-tree-select
                                      v-model="element.filePaths"
                                      multiple
                                      show-checkbox
                                      clearable
                                      :data="step8Form.filteredFolderContents"
                                      @visible-change="
                                        getFilteredFolderContentsForStudyFiles(element.filePaths)
                                      "
                                      placeholder="Select your data files here"
                                      class="w-full"
                                    />
                                    <span class="mt-2 text-xs text-slate-600">
                                      Select the study file to be associated with the study. This
                                      can be data dictionaries, Case Report Forms, custom-formatted
                                      data files, etc...
                                    </span>
                                  </div>

                                  <div class="my-2"></div>

                                  <div class="flex w-full flex-col">
                                    <el-input
                                      v-model="element.description"
                                      type="textarea"
                                      placeholder="Description"
                                      rows="3"
                                      maxlength="4000"
                                      show-word-limit
                                    />
                                    <span class="mt-1 text-xs text-gray-400">
                                      The protocol summary describes the purpose of the protocol.
                                    </span>
                                  </div>
                                </div>

                                <div class="flex w-1/12 flex-row items-center justify-evenly">
                                  <div
                                    class="handle flex items-center justify-center text-gray-400 hover:text-gray-700"
                                  >
                                    <Icon icon="ic:outline-drag-indicator" />
                                  </div>
                                  <div
                                    class="flex cursor-pointer items-center justify-center text-gray-500 transition-all hover:text-gray-800"
                                  >
                                    <el-popconfirm
                                      width="220"
                                      confirm-button-text="Yes"
                                      cancel-button-text="No"
                                      icon-color="red"
                                      title="Are you sure you want to remove this?"
                                      @confirm="deleteStudyFile(element.id)"
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
                          class="mb-6 flex w-max cursor-pointer items-center text-sm text-gray-500 hover:text-black"
                          @click="addStudyFile"
                        >
                          <Icon icon="carbon:add" />
                          <span class="text-primary-600 hover:text-primary-500">
                            Add a new study file
                          </span>
                          <form-help-content
                            popoverContent="Add a new protocol to the list."
                          ></form-help-content>
                        </div>

                        <el-form-item label="Study Links" prop="studyLinks">
                          <draggable
                            tag="div"
                            :list="step8Form.studyLinks"
                            item-key="id"
                            :animation="200"
                            handle=".handle"
                            class="w-full divide-y-2"
                          >
                            <template #item="{ element }">
                              <div class="flex w-full flex-row justify-between py-4">
                                <div class="flex w-11/12 flex-col px-2">
                                  <div class="flex w-full flex-col">
                                    <el-input
                                      v-model="element.name"
                                      type="text"
                                      placeholder="Clinicaltrials.gov"
                                      maxlength="500"
                                      show-word-limit
                                    />
                                    <span class="mt-1 text-xs text-gray-400">
                                      Provide the name of the website to which the link refers.
                                    </span>
                                  </div>

                                  <div class="my-2"></div>

                                  <div class="flex w-full flex-col">
                                    <el-input
                                      v-model="element.url"
                                      type="textarea"
                                      placeholder="https://clinicaltrials.gov/ct2/show/NCT04505795"
                                      maxlength="2000"
                                      show-word-limit
                                    />
                                    <span class="mt-1 text-xs text-gray-400">
                                      Provide the website URL.
                                    </span>
                                  </div>
                                </div>

                                <div class="flex w-1/12 flex-row items-center justify-evenly">
                                  <div
                                    class="handle flex items-center justify-center text-gray-400 hover:text-gray-700"
                                  >
                                    <Icon icon="ic:outline-drag-indicator" />
                                  </div>
                                  <div
                                    class="flex cursor-pointer items-center justify-center text-gray-500 transition-all hover:text-gray-800"
                                  >
                                    <el-popconfirm
                                      width="220"
                                      confirm-button-text="Yes"
                                      cancel-button-text="No"
                                      icon-color="red"
                                      title="Are you sure you want to remove this?"
                                      @confirm="deleteStudyLink(element.id)"
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
                          class="mb-6 flex w-max cursor-pointer items-center text-sm text-gray-500 hover:text-black"
                          @click="addStudyLink"
                        >
                          <Icon icon="carbon:add" />
                          <span class="text-primary-600 hover:text-primary-500">
                            Add a new study link
                          </span>
                          <form-help-content
                            popoverContent="Add a new study link to the list."
                          ></form-help-content>
                        </div>
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

                    <button
                      class="primary-button"
                      @click="navigateToStep9FromStep8"
                      :disabled="checkInvalidStatus"
                    >
                      Next
                      <el-icon><right-icon /></el-icon>
                    </button>
                  </div>
                </div>

                <div v-if="currentStep == 9">
                  <div class="px-4 pb-4 pt-2">
                    <el-form
                      :model="step9Form"
                      label-width="160px"
                      label-position="top"
                      size="large"
                      ref="s3Form"
                      @submit.prevent
                      class="pb-4"
                    >
                      <draggable
                        tag="div"
                        :list="step9Form"
                        item-key="id"
                        handle=".handle"
                        :animation="200"
                        @start="minimizeAllStudyPublications"
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

                                <span class="flex items-center"> {{ element.publicationID }} </span>

                                <div
                                  class="ml-2 flex cursor-pointer items-center justify-center rounded-md p-2 text-gray-500 transition-all hover:bg-slate-200 hover:text-gray-800"
                                  @click.stop="editPublicationID(element.id)"
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
                                  @click.stop="showRemoveStudyPublicationConfirm(element.id)"
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
                                    type="textarea"
                                    placeholder="36921622"
                                    maxlength="4000"
                                    show-word-limit
                                    rows="2"
                                  />
                                  <span class="mt-1 text-xs text-slate-600">
                                    The title of an article that includes data from this study.
                                  </span>
                                </div>

                                <div class="mb-4 flex flex-col">
                                  <label class="w-[160px] pb-1 text-sm font-medium text-gray-700">
                                    Authors <span class="text-red-500"> * </span>
                                  </label>
                                  <el-input
                                    v-model="element.authors"
                                    type="textarea"
                                    placeholder="Authors"
                                    class="mb-2"
                                    maxlength="4000"
                                    show-word-limit
                                    rows="4"
                                  />
                                  <span class="mt-1 text-xs text-slate-600">
                                    Authors of the article.
                                  </span>
                                </div>

                                <div class="mb-4 flex flex-col">
                                  <label class="w-[160px] pb-1 text-sm font-medium text-gray-700">
                                    Journal <span class="text-red-500"> * </span>
                                  </label>

                                  <el-input
                                    v-model="element.journal"
                                    type="text"
                                    placeholder="Nature Communications"
                                    maxlength="250"
                                    show-word-limit
                                  />
                                </div>

                                <div
                                  class="mb-2 flex w-full flex-row justify-between transition-all"
                                >
                                  <div class="mr-2 w-3/12">
                                    <div class="mb-4 flex w-full flex-col">
                                      <label
                                        class="w-[160px] pb-1 text-sm font-medium text-gray-700"
                                      >
                                        Date
                                      </label>

                                      <el-date-picker
                                        v-model="element.date"
                                        type="month"
                                        placeholder="2023-03"
                                        class="w-full"
                                      />
                                      <span class="mt-1 text-xs text-slate-600">
                                        The article's publication date.
                                      </span>
                                    </div>
                                  </div>

                                  <div class="mx-2 w-4/12">
                                    <div class="mb-4 flex flex-col">
                                      <label
                                        class="w-[160px] pb-1 text-sm font-medium text-gray-700"
                                      >
                                        Issue
                                      </label>
                                      <el-input
                                        v-model="element.issue"
                                        type="text"
                                        placeholder="something here"
                                        maxlength="20"
                                        show-word-limit
                                      />
                                      <span class="mt-1 text-xs text-slate-600">
                                        The Journal's issue number.
                                      </span>
                                    </div>
                                  </div>

                                  <div class="mx-2 w-5/12">
                                    <div class="mb-4 flex flex-col">
                                      <label
                                        class="w-[160px] pb-1 text-sm font-medium text-gray-700"
                                      >
                                        Pages
                                      </label>
                                      <el-input
                                        v-model="element.pages"
                                        type="text"
                                        placeholder="something here"
                                        maxlength="20"
                                        show-word-limit
                                      />
                                      <span class="mt-1 text-xs text-slate-600">
                                        The Journal's page number.
                                      </span>
                                    </div>
                                  </div>
                                </div>

                                <div class="mb-4 flex flex-col">
                                  <label class="w-[160px] pb-1 text-sm font-medium text-gray-700">
                                    DOI <span class="text-red-500"> * </span>
                                  </label>

                                  <el-input
                                    v-model="element.doi"
                                    type="text"
                                    placeholder="36921622"
                                    maxlength="100"
                                    show-word-limit
                                  />
                                </div>
                              </div>
                            </el-collapse-transition>
                          </div>
                        </template>
                      </draggable>

                      <edit-prompt
                        ref="editPublicationIDrompt"
                        title="Edit Study Publication ID"
                        confirmButtonText="Save"
                        :confirmDisabled="disableEditPublicationIDSaveButton"
                        @messageConfirmed="saveUpdatedPublicationID"
                      >
                        <div w-full>
                          <p class="mb-3 text-sm">Please enter a new ID for this publication.</p>

                          <el-input
                            v-model="publicationID"
                            clearable
                            class="w-full"
                            placeholder="Enter a new ID for this publication"
                            maxlength="100"
                            show-word-limit
                          />
                        </div>
                      </edit-prompt>

                      <warning-confirm
                        ref="removeStudyPublicationConfirm"
                        title="Warning"
                        @messageConfirmed="confirmedRemoveStudyPublication"
                      >
                        <p class="text-center text-base text-gray-500">
                          Are you sure you want to remove this group? This action cannot be undone.
                        </p>
                      </warning-confirm>
                    </el-form>
                    <div class="m-2 flex w-full justify-center">
                      <button class="primary-plain-button" @click="showAddStudyPublicationPrompt">
                        Add a Study Publication
                      </button>

                      <add-prompt
                        ref="addStudyPublicationPrompt"
                        title="Add a Study Publication"
                        confirmButtonText="Add this publication"
                        :confirmDisabled="disableEditPublicationIDSaveButton"
                        @messageConfirmed="addStudyPublicationConfirmed"
                      >
                        <div w-full>
                          <p class="mb-3 text-sm">Please add a unique ID for this publication.</p>

                          <el-input
                            v-model="publicationID"
                            clearable
                            size="large"
                            class="w-full"
                            placeholder="Enter a ID for this publication"
                            maxlength="100"
                            show-word-limit
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

              <button class="primary-button" @click="nextFormStep" :disabled="checkInvalidStatus">
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
import { nanoid } from "nanoid";

import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

import PillProgressBar from "@/components/ui/PillProgressBar.vue";

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
      totalSteps: 9,
      pillTitles: ["Study", "Protocols", "Samples"],
      SaveLottieJSON,
      dataset: {},
      workflowID: this.$route.params.workflowID,
      workflow: {},
      loading: false,
      interval: null,

      researchFocusOptions: ImmunologyJSON.researchFocusOptions,
      conditionOptions: ImmunologyJSON.conditionOptions,
      armTypeOptions: ImmunologyJSON.armTypeOptions,
      studyRoleOptions: ImmunologyJSON.studyRoleOptions,
      protocolTypeOptions: ImmunologyJSON.protocolTypeOptions,
      studyFileTypeOptions: ImmunologyJSON.studyFileTypeOptions,

      filteredFolderContents: [],

      generateImmunologyMetadata: "Yes",
      step1Form: {
        studyID: "study",
        briefTitle: "briefTitle",
        officialTitle: "officialTitle",
        briefDescription: "briefDescription",
        description: "description",
        sponsoringOrganization: "someOrg",
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
        researchFocus: "Development",
        condition: ["alcohol use disorder", "alcohol dependence"],
        interventionAgent: "ia",
        endpoints: "end",
        hypothesis: "hype",
        objectives: "obj",
        ageUnit: "Years",
        minimumAge: "20",
        maximumAge: "30",
        actualStartDate: "2023-03-14T07:00:00.000Z",
        targetEnrollment: 10,
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
      step3Form: [
        {
          id: "f6c67289-949c-498c-8df4-a10da3c6dad9",
          armID: "test",
          name: "ar",
          description: "asddf",
          type: "No Intervention Arm",
          isExpanded: true,
        },
      ],
      step4Form: [
        {
          id: "44b71c40-343e-492f-a943-cbae29b0095c",
          personnelID: "test",
          firstName: "steven",
          lastName: "strange",
          suffix: "",
          honorific: "",
          orcid: "",
          organization: "ucsf",
          email: "asd@amd.vef",
          titleInStudy: "pi",
          roleInStudy: "Investigator",
          siteName: "sn",
          isExpanded: true,
          type: "Investigator",
        },
      ],
      step5Form: [
        {
          id: "64e38224-0cc5-42a1-b0e4-ee13336a90fc",
          visitID: "test",
          orderNumber: 3,
          minStartDay: 5,
          maxStartDay: 7,
          startRule: "sr",
          endRule: "er",
          isExpanded: true,
          name: "tasx",
        },
      ],
      step6Form: {
        inexclusions: [
          {
            userDefinedID: "test",
            criterion: "test description2",
            criterionCategory: "Inclusion",
            id: "362e293d-1c61-4e9c-b64a-d7e897dbe029",
          },
        ],
      },
      step6FormRules: {
        inexclusions: [
          {
            required: true,
            validator: this.inexclusionValidator,
            trigger: "blur",
          },
        ],
      },
      step7Form: {
        protocols: [
          {
            userDefinedID: "test",
            name: "test",
            description: "test",
            type: "Clinical",
            filePath: "C:\\Users\\dev\\Desktop\\temp2\\codemeta.json",
            id: "a799a5ed-a33c-4bff-a04b-a1090809b4b3",
          },
        ],
      },
      step7FormRules: {
        protocols: [
          {
            required: true,
            validator: this.protocolsValidator,
            trigger: "blur",
          },
        ],
      },
      step8Form: {
        studyFiles: [
          {
            description: "test",
            type: "Assesment Results",
            filePaths: [
              "C:\\Users\\dev\\Desktop\\temp2\\01d3328c-582d-41ff-a8d3-cf563ec2b97a.soda",
              "C:\\Users\\dev\\Desktop\\temp2\\CITATION.cff",
            ],
            id: "0cd1a639-0ebb-4c9c-b766-152a2af5925f",
          },
        ],
        studyLinks: [],
      },
      step8FormRules: {
        studyFiles: [
          {
            required: true,
            validator: this.studyFilesValidator,
            trigger: "blur",
          },
        ],
        studyLinks: [
          {
            required: false,
            validator: this.studyLinksValidator,
            trigger: "blur",
          },
        ],
      },
      step9Form: [
        {
          id: "f6c67289-949c-498c-8df4-a10da3c6dad9",
          publicationID: "test",
          doi: "",
          title: "",
          journal: "",
          date: "",
          issue: "",
          pages: "",
          authors: "",
          isExpanded: true,
        },
      ],

      invalidStatus: {},
      showSaving: false,
      showSpinner: false,

      armGroupID: "",
      armID: "",

      personnelEntryID: "",
      personnelID: "",

      plannedVisitID: "",
      visitID: "",

      studyPublicationsID: "",
      publicationID: "",

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
    disableEditArmIDSaveButton() {
      if (this.armID.trim() === "") {
        return true;
      }

      for (const group of this.step3Form) {
        if (group.armID === this.armID.trim()) {
          return true;
        }
      }

      return false;
    },
    disableEditPersonnelIDSaveButton() {
      if (this.personnelID.trim() === "") {
        return true;
      }

      for (const entry of this.step4Form) {
        if (entry.personnelID === this.personnelID.trim()) {
          return true;
        }
      }

      return false;
    },
    disableEditPlannedVisitsIDSaveButton() {
      if (this.visitID.trim() === "") {
        return true;
      }

      for (const entry of this.step5Form) {
        if (entry.visitID === this.visitID.trim()) {
          return true;
        }
      }

      return false;
    },
    disableEditPublicationIDSaveButton() {
      if (this.publicationID.trim() === "") {
        return true;
      }

      for (const entry of this.step9Form) {
        if (entry.publicationID === this.publicationID.trim()) {
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
        const valid = await this.checkStudyPublicationsValidity();

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
    async navigateToStep4FromStep3() {
      const valid = await this.checkArmGroupValidity();

      if (!valid) {
        return;
      }

      await this.saveCurrentEntries();

      this.setCurrentStep(4);
      this.$refs["topOfPageElement"].scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    },
    async navigateToStep5FromStep4() {
      const valid = await this.checkPersonnelEntryValidity();

      if (!valid) {
        return;
      }

      await this.saveCurrentEntries();

      this.setCurrentStep(5);
      this.$refs["topOfPageElement"].scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    },
    async navigateToStep6FromStep5() {
      const valid = await this.checkPlannedVisitsValidity();

      if (!valid) {
        return;
      }

      await this.saveCurrentEntries();

      this.setCurrentStep(6);
      this.$refs["topOfPageElement"].scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    },
    navigateToStep7FromStep6() {
      this.$refs["s6Form"].validate(async (valid) => {
        if (valid) {
          await this.saveCurrentEntries();
          this.setCurrentStep(7);
          this.$refs["topOfPageElement"].scrollIntoView({
            behavior: "smooth",
            block: "start",
          });
        }
      });
    },
    navigateToStep8FromStep7() {
      this.$refs["s7Form"].validate(async (valid) => {
        if (valid) {
          await this.saveCurrentEntries();
          this.setCurrentStep(8);
          this.$refs["topOfPageElement"].scrollIntoView({
            behavior: "smooth",
            block: "start",
          });
        }
      });
    },
    navigateToStep9FromStep8() {
      this.$refs["s8Form"].validate(async (valid) => {
        if (valid) {
          await this.saveCurrentEntries();
          this.setCurrentStep(9);
          this.$refs["topOfPageElement"].scrollIntoView({
            behavior: "smooth",
            block: "start",
          });
        }
      });
    },

    generateRandomID(prefix) {
      const randomID = `${prefix}_${nanoid(5)}`;

      switch (prefix) {
        case "study":
          this.step1Form.studyID = randomID;
          break;
        case "arm-cohort":
          this.armID = randomID;
          break;
        case "personnel":
          this.personnelID = randomID;
          break;
        case "plannedvisit":
          this.visitID = randomID;
          break;
        default:
          break;
      }

      return randomID;
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
    filterArrayOfObjects(array, key) {
      return array.filter((element) => {
        return element[key] !== "";
      });
    },
    getFilteredFolderContentsForProtocols(preselected) {
      const alreadyAddedFiles = [];

      const newFolderContents = JSON.parse(JSON.stringify(this.folderContents));

      for (let i = 0; i < this.step7Form.protocols.length; i++) {
        alreadyAddedFiles.push(this.step7Form.protocols[i].filePath);
      }

      for (let i = 0; i < this.step8Form.studyFiles.length; i++) {
        for (let j = 0; j < this.step8Form.studyFiles[i].filePaths.length; j++) {
          alreadyAddedFiles.push(this.step8Form.studyFiles[i].filePaths[j]);
        }
      }

      //recurse through the folder contents
      function recurse(folderContents) {
        for (let i = 0; i < folderContents.length; i++) {
          if (folderContents[i].isDir) {
            recurse(folderContents[i].children);
          } else {
            if (alreadyAddedFiles.includes(folderContents[i].value)) {
              if (preselected == folderContents[i].value) {
                folderContents[i].disabled = true;
              } else {
                folderContents[i].disabled = false;
              }
            } else {
              folderContents[i].disabled = false;
            }
          }
        }
      }

      recurse(newFolderContents);

      this.step7Form.filteredFolderContents = newFolderContents;

      return;
    },

    getFilteredFolderContentsForStudyFiles(preselected) {
      const alreadyAddedFiles = [];

      const newFolderContents = JSON.parse(JSON.stringify(this.folderContents));

      for (let i = 0; i < this.step7Form.protocols.length; i++) {
        alreadyAddedFiles.push(this.step7Form.protocols[i].filePath);
      }

      for (let i = 0; i < this.step8Form.studyFiles.length; i++) {
        for (let j = 0; j < this.step8Form.studyFiles[i].filePaths.length; j++) {
          alreadyAddedFiles.push(this.step8Form.studyFiles[i].filePaths[j]);
        }
      }

      //recurse through the folder contents
      function recurse(folderContents) {
        for (let i = 0; i < folderContents.length; i++) {
          if (folderContents[i].isDir) {
            recurse(folderContents[i].children);
          } else {
            if (alreadyAddedFiles.includes(folderContents[i].value)) {
              if (typeof preselected !== "undefined")
                if (!preselected.includes(folderContents[i].value)) {
                  folderContents[i].disabled = true;
                } else {
                  folderContents[i].disabled = false;
                }
            } else {
              folderContents[i].disabled = false;
            }
          }
        }
      }

      recurse(newFolderContents);

      this.step8Form.filteredFolderContents = newFolderContents;

      return;
    },

    async checkArmGroupValidity() {
      if (this.step3Form.length === 0) {
        this.$message.error("Please add at least one arm group.");
        return false;
      }

      for (const group of this.step3Form) {
        if (group.armID.trim() === "") {
          this.$message.error("Please provide a Arm ID for all groups.");
          return false;
        }

        if (group.name.trim() === "") {
          this.$message.error("Please provide a name for all groups.");
          return false;
        }
      }

      return true;
    },
    showAddArmGroupPrompt() {
      this.armID = "";
      this.$refs.addArmGroupPrompt.show();
    },
    addArmGroupConfirmed() {
      const entry = {
        id: uuidv4(),
        armID: this.armID,
        name: "",
        description: "",
        type: "",
        isExpanded: true,
      };

      this.step3Form.push(entry);
    },
    minimizeAllArmGroups() {
      this.step3Form.map((group) => {
        group.isExpanded = false;
      });
    },
    editArmID(id) {
      let group = this.step3Form.find((element) => {
        return element.id === id;
      });

      this.armGroupID = id;
      this.armID = group.armID;
      this.$refs.editArmIDPrompt.show();
    },
    saveUpdatedArmID() {
      let group = this.step3Form.find((element) => {
        return element.id === this.armGroupID;
      });

      group.armID = this.armID;
    },
    showRemoveArmGroupConfirm(id) {
      this.armGroupID = id;
      this.$refs.removeArmGroupConfirm.show();
    },
    confirmedRemoveArmGroup() {
      const id = this.armGroupID;

      this.step3Form = this.step3Form.filter((group) => {
        return group.id !== id;
      });
    },

    async checkPersonnelEntryValidity() {
      if (this.step4Form.length === 0) {
        this.$message.error("Please add at least one arm group.");
        return false;
      }

      for (const person of this.step4Form) {
        if (person.personnelID.trim() === "") {
          this.$message.error("Please provide a Personnel ID for all entries.");
          return false;
        }

        if (person.firstName.trim() === "") {
          this.$message.error("Please provide a first name for all entries.");
          return false;
        }

        if (person.lastName.trim() === "") {
          this.$message.error("Please provide a last name for all entries.");
          return false;
        }

        if (person.organization.trim() === "") {
          this.$message.error("Please provide an organization for all entries.");
          return false;
        }

        if (person.email.trim() === "") {
          this.$message.error("Please provide an email for all entries.");
          return false;
        }

        if (person.titleInStudy.trim() === "") {
          this.$message.error("Please provide a title in study for all entries.");
          return false;
        }

        if (person.roleInStudy.trim() === "") {
          this.$message.error("Please provide a role in study for all entries.");
          return false;
        }

        if (person.siteName.trim() === "") {
          this.$message.error("Please provide a site name for all entries.");
          return false;
        }
      }

      return true;
    },
    showAddPersonnelPrompt() {
      this.personnelID = "";
      this.$refs.addPersonnelPrompt.show();
    },
    addPersonnelConfirmed() {
      const entry = {
        id: uuidv4(),
        personnelID: this.personnelID,
        firstName: "",
        lastName: "",
        suffix: "",
        honorific: "",
        orcid: "",
        organization: "",
        email: "",
        titleInStudy: "",
        roleInStudy: "",
        siteName: "",
        isExpanded: true,
      };

      this.step4Form.push(entry);
    },
    minimizeAllPersonnel() {
      this.step4Form.map((entry) => {
        entry.isExpanded = false;
      });
    },
    editPersonnelID(id) {
      let entry = this.step4Form.find((element) => {
        return element.id === id;
      });

      this.personnelEntryID = id;
      this.personnelID = entry.personnelID;
      this.$refs.editpersonnelIDPrompt.show();
    },
    saveUpdatedPersonnelID() {
      let group = this.step4Form.find((element) => {
        return element.id === this.personnelEntryID;
      });

      group.personnelID = this.personnelID;
    },
    showRemovePersonnelEntryConfirm(id) {
      this.personnelEntryID = id;
      this.$refs.removePersonnelEntryConfirm.show();
    },
    confirmedRemovePersonnelEntry() {
      const id = this.personnelEntryID;

      this.step4Form = this.step4Form.filter((entry) => {
        return entry.id !== id;
      });
    },

    async checkPlannedVisitsValidity() {
      for (const visit of this.step5Form) {
        if (visit.visitID.trim() === "") {
          this.$message.error("Please provide an ID for all planned visits.");
          return false;
        }

        if (visit.name.trim() === "") {
          this.$message.error("Please provide a name for all planned visits.");
          return false;
        }
      }

      return true;
    },
    showAddPlannedVisitPrompt() {
      this.visitID = "";
      this.$refs.addPlannedVisitPrompt.show();
    },
    addPlannedVisitConfirmed() {
      const entry = {
        id: uuidv4(),
        visitID: this.visitID,
        orderNumber: 0,
        minStartDay: 0,
        maxStartDay: 0,
        startRule: "",
        endRule: "",
        isExpanded: true,
      };

      this.step5Form.push(entry);
    },
    minimizeAllPlannedVisits() {
      this.step5Form.map((entry) => {
        entry.isExpanded = false;
      });
    },
    editPlannedVisitID(id) {
      let entry = this.step5Form.find((element) => {
        return element.id === id;
      });

      this.plannedVisitID = id;
      this.visitID = entry.visitID;
      this.$refs.editPlannedVisitPrompt.show();
    },
    saveUpdatedPlannedVisitID() {
      let visit = this.step5Form.find((element) => {
        return element.id === this.plannedVisitID;
      });

      visit.visitID = this.visitID;
    },
    showRemovePlannedVisitConfirm(id) {
      this.plannedVisitID = id;
      this.$refs.removePlannedVisitConfirm.show();
    },
    confirmedRemovePlannedVisit() {
      const id = this.plannedVisitID;

      this.step5Form = this.step5Form.filter((entry) => {
        return entry.id !== id;
      });
    },

    inexclusionValidator(_rule, value, callback) {
      if (value.length > 0) {
        for (let item of value) {
          //check if id is not empty
          if (item.userDefinedID.trim() === "") {
            this.invalidStatus.inexclusion = true;
            callback(new Error("Please provide an ID for all entries"));
            return;
          }

          //check if id is unique
          if (value.filter((x) => x.userDefinedID === item.userDefinedID).length > 1) {
            this.invalidStatus.inexclusion = true;
            callback(new Error("Please provide a unique ID for all entries"));
            return;
          }
        }
      } else {
        this.invalidStatus.inexclusion = true;
        callback(new Error("Please provide at least one entry"));
        return;
      }
      this.invalidStatus.inexclusion = false;
      callback();
    },
    addInexclusion() {
      this.step6Form.inexclusions.push({
        userDefinedID: "",
        criterion: "",
        criterionCategory: "",
        id: uuidv4(),
      });
    },
    deleteInexclusion(id) {
      this.step6Form.inexclusions = this.step6Form.inexclusions.filter((inexclusion) => {
        return inexclusion.id !== id;
      });
      this.$refs["s6Form"].validate();
    },

    protocolsValidator(_rule, value, callback) {
      if (value.length > 0) {
        for (let item of value) {
          //check if id is not empty
          if (item.userDefinedID.trim() === "") {
            this.invalidStatus.protocols = true;
            callback(new Error("Please provide an ID for all entries"));
            return;
          }

          //check if id is unique
          if (value.filter((x) => x.userDefinedID === item.userDefinedID).length > 1) {
            this.invalidStatus.protocols = true;
            callback(new Error("Please provide a unique ID for all entries"));
            return;
          }
        }
      } else {
        this.invalidStatus.protocols = true;
        callback(new Error("Please provide at least one entry"));
        return;
      }
      this.invalidStatus.protocols = false;
      callback();
    },
    addProtocol() {
      this.step7Form.protocols.push({
        userDefinedID: "",
        name: "",
        description: "",
        type: "",
        filePath: "",
        id: uuidv4(),
      });
    },
    deleteProtocol(id) {
      this.step7Form.protocols = this.step7Form.protocols.filter((protocol) => {
        return protocol.id !== id;
      });
      this.$refs["s7Form"].validate();
    },

    studyFilesValidator(_rule, value, callback) {
      if (value.length > 0) {
        for (let item of value) {
          // check if description is present
          if (item.description.trim() === "") {
            this.invalidStatus.studyFiles = true;
            callback(new Error("Please provide a description for all entries"));
            return;
          }

          // check if type is present
          if (item.type.trim() === "") {
            this.invalidStatus.studyFiles = true;
            callback(new Error("Please provide a type for all entries"));
            return;
          }
        }
      } else {
        this.invalidStatus.studyFiles = true;
        callback(new Error("Please provide at least one entry"));
        return;
      }
      this.invalidStatus.studyFiles = false;
      callback();
    },
    addStudyFile() {
      this.step8Form.studyFiles.push({
        description: "",
        type: "",
        filePaths: [],
        id: uuidv4(),
      });
    },
    deleteStudyFile(id) {
      this.step8Form.studyFiles = this.step8Form.studyFiles.filter((item) => {
        return item.id !== id;
      });
      this.$refs["s8Form"].validate();
    },

    studyLinksValidator(_rule, value, callback) {
      if (value.length > 0) {
        for (let item of value) {
          // check if description is present
          if (item.name.trim() === "") {
            this.invalidStatus.studyFiles = true;
            callback(new Error("Please provide a name for all entries"));
            return;
          }

          // check if type is present
          if (item.url.trim() === "") {
            this.invalidStatus.url = true;
            callback(new Error("Please provide a URL for all entries"));
            return;
          }
        }
      }
      this.invalidStatus.studyLinks = false;
      callback();
    },
    addStudyLink() {
      this.step8Form.studyLinks.push({
        name: "",
        url: "",
        id: uuidv4(),
      });
    },
    deleteStudyLink(id) {
      this.step8Form.studyLinks = this.step8Form.studyLinks.filter((item) => {
        return item.id !== id;
      });
      this.$refs["s8Form"].validate();
    },

    async checkStudyPublicationsValidity() {
      if (this.step9Form.length === 0) {
        return true;
      }

      for (const group of this.step9Form) {
        if (group.publicationID.trim() === "") {
          this.$message.error("Please provide an ID for all publications.");
          return false;
        }
      }

      return true;
    },
    showAddStudyPublicationPrompt() {
      this.publicationID = "";
      this.$refs.addStudyPublicationPrompt.show();
    },
    addStudyPublicationConfirmed() {
      const entry = {
        id: uuidv4(),
        publicationID: this.publicationID,
        doi: "",
        title: "",
        authors: "",
        journal: "",
        date: "",
        issue: "",
        pages: "",
        isExpanded: true,
      };

      this.step9Form.push(entry);
    },
    minimizeAllStudyPublications() {
      this.step9Form.map((group) => {
        group.isExpanded = false;
      });
    },
    editPublicationID(id) {
      let publication = this.step9Form.find((element) => {
        return element.id === id;
      });

      this.studyPublicationsID = id;
      this.publicationID = publication.publicationID;
      this.$refs.editPublicationIDrompt.show();
    },
    saveUpdatedPublicationID() {
      let publication = this.step9Form.find((element) => {
        return element.id === this.studyPublicationsID;
      });

      publication.publicationID = this.publicationID;
    },
    showRemoveStudyPublicationConfirm(id) {
      this.studyPublicationsID = id;
      this.$refs.removeStudyPublicationConfirm.show();
    },
    confirmedRemoveStudyPublication() {
      const id = this.studyPublicationsID;

      this.step9Form = this.step9Form.filter((publication) => {
        return publication.id !== id;
      });
    },

    async saveCurrentEntries() {
      this.showSavingIcon();

      this.dataset.data.general.questions.name = this.step1Form.briefTitle;
      this.dataset.data.general.questions.description = this.step1Form.briefDescription;

      const authors = this.step4Form.map((person) => {
        return {
          familyName: person.lastName,
          givenName: person.firstName,
          email: person.email,
          affiliation: person.organization,
          orcid: person.orcid,
        };
      });

      this.dataset.data.general.questions.authors = authors;

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

      immunologyForm.arms = this.step3Form;

      immunologyForm.studyPersonnel = this.step4Form;

      immunologyForm.plannedVisits = this.step5Form;

      immunologyForm.inexclusions = this.step6Form.inexclusions;

      immunologyForm.protocols = this.step7Form.protocols;

      immunologyForm.studyFiles = this.step8Form.studyFiles;
      immunologyForm.studyLinks = this.step8Form.studyLinks;

      immunologyForm.studyPublications = this.step9Form;

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
          path: `/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/Immunology/selectFolder`,
        });
        return;
      }

      const routerPath = `/datasets/${this.$route.params.datasetID}/${this.workflowID}/Immunology/pickLicense`;

      this.$router.push({ path: routerPath });
    },
    navigateBack() {
      this.$router.push({
        path: `/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/Immunology/reviewStandards`,
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
      this.datasetStore.setProgressBarType("immport");
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

        this.step3Form = immunologyForm.arms;

        this.step4Form = immunologyForm.studyPersonnel;

        this.step5Form = immunologyForm.plannedVisits;

        this.step6Form.inexclusions = immunologyForm.inexclusions;

        this.step7Form.protocols = immunologyForm.protocols;

        this.step8Form.studyFiles = immunologyForm.studyFiles;
        this.step8Form.studyLinks = immunologyForm.studyLinks;

        this.step9Form = immunologyForm.studyPublications;

        this.addIds(this.step6Form.inexclusions);
        this.addIds(this.step7Form.protocols);
        this.addIds(this.step8Form.studyFiles);
        this.addIds(this.step8Form.studyLinks);
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
