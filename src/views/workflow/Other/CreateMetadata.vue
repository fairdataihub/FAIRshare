<template>
  <div
    class="relative flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 px-5"
  >
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium"> Provide information about your data </span>

      <line-divider></line-divider>

      <div class="flex flex-col">
        <span class="mb-2">
          Would you like FAIRshare to create the mandatory metadata files metadata.json?
        </span>

        <div class="py-1">
          <el-radio v-model="generateOtherMetadata" label="Yes" size="large"> Yes </el-radio>
          <el-radio v-model="generateOtherMetadata" label="No" size="large"> No </el-radio>
          <el-radio
            v-model="generateOtherMetadata"
            label="None"
            size="large"
            border
            class="!hidden"
          >
            None
          </el-radio>
        </div>
      </div>

      <div v-if="generateOtherMetadata !== 'None'">
        <transition name="fade" mode="out-in" appear>
          <div v-if="generateOtherMetadata === 'Yes'">
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
                        Basic Information
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
                        <el-form-item label="Name" prop="name">
                          <div class="flex w-full flex-row items-center">
                            <el-input v-model="step1Form.name" placeholder="My Software"></el-input>
                            <form-help-content
                              popoverContent="The name of the software"
                            ></form-help-content>
                          </div>
                        </el-form-item>

                        <el-form-item label="Description/abstract" prop="description">
                          <div class="flex w-full flex-row items-center">
                            <el-input
                              v-model="step1Form.description"
                              type="textarea"
                              placeholder="My Software computes orbit propogation. It has been used in the NASA Spacecraft Orbit Propogation Center."
                            ></el-input>
                            <form-help-content
                              popoverContent="A brief description of the software"
                            ></form-help-content>
                          </div>
                        </el-form-item>

                        <el-form-item label="Creation date">
                          <div class="flex w-full flex-row items-center">
                            <el-date-picker
                              v-model="step1Form.creationDate"
                              type="date"
                              placeholder="Pick a day"
                              value-format="YYYY-MM-DD"
                            >
                            </el-date-picker>
                            <form-help-content
                              popoverContent="The date on which the software was first created"
                            ></form-help-content>
                          </div>
                        </el-form-item>

                        <el-form-item label="First release date">
                          <div class="flex w-full flex-row items-center">
                            <el-date-picker
                              v-model="step1Form.firstReleaseDate"
                              type="date"
                              placeholder="Pick a day"
                              value-format="YYYY-MM-DD"
                            >
                            </el-date-picker>
                            <form-help-content
                              popoverContent="The date on which the software was first released"
                            ></form-help-content>
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
                        Authors and Contributors
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
                        <el-form-item label="Authors" prop="authors">
                          <draggable
                            tag="div"
                            :list="step2Form.authors"
                            item-key="id"
                            handle=".handle"
                          >
                            <template #item="{ element }">
                              <div class="mb-2 flex flex-row justify-between transition-all">
                                <div class="flex w-11/12 flex-row justify-between">
                                  <el-input
                                    v-model="element.givenName"
                                    type="text"
                                    placeholder="Given name"
                                    class="h-[40px]"
                                  ></el-input>

                                  <div class="mx-1"></div>

                                  <el-input
                                    v-model="element.familyName"
                                    type="text"
                                    placeholder="Family name"
                                    class="h-[40px]"
                                  ></el-input>

                                  <div class="mx-2"></div>

                                  <el-input
                                    v-model="element.affiliation"
                                    type="text"
                                    placeholder="Affiliation"
                                    class="h-[40px]"
                                  ></el-input>

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
                        </el-form-item>

                        <div
                          class="mb-6 flex w-max cursor-pointer items-center text-sm text-gray-500 hover:text-black"
                          @click="addAuthor"
                        >
                          <Icon icon="carbon:add" />
                          <span class="text-primary-600 hover:text-primary-500">
                            Add an author
                          </span>
                          <form-help-content
                            popoverContent="Add a developer of the software"
                          ></form-help-content>
                        </div>

                        <el-form-item label="Contributors" prop="contributors">
                          <draggable
                            tag="div"
                            :list="step2Form.contributors"
                            item-key="id"
                            handle=".handle"
                          >
                            <template #item="{ element }">
                              <div class="mb-2 flex flex-row justify-between transition-all">
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

                                <div class="flex w-11/12 flex-row justify-between">
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

                                  <div class="mx-2 flex w-1/5 flex-col">
                                    <el-input
                                      v-model="element.email"
                                      type="text"
                                      placeholder="E-mail address"
                                    ></el-input>
                                    <span class="mt-1 ml-2 text-xs text-gray-400"> Optional </span>
                                  </div>

                                  <div class="mx-2 flex w-1/5 flex-col">
                                    <el-input
                                      v-model="element.orcid"
                                      type="text"
                                      placeholder="ORCID (e.g. 0000-0002-1825-0097)"
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
                          class="flex w-max cursor-pointer items-center text-sm text-gray-500 hover:text-black"
                          @click="addContributor"
                        >
                          <Icon icon="carbon:add" />
                          <span class="text-primary-600 hover:text-primary-500">
                            Add a contributor
                          </span>
                          <form-help-content
                            popoverContent="Add a person who contributed to the software.  This can range from project managers, editors, sponsors, data curators, and other contributors."
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
                    <div class="w-full bg-gray-100 px-4 py-2">
                      <span class="pointer-events-none text-lg font-semibold text-primary-600">
                        Discoverability
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
                        class="py-4"
                      >
                        <el-form-item label="Unique identifier">
                          <div class="flex w-full flex-row items-center">
                            <el-input
                              v-model="step3Form.identifier"
                              type="text"
                              :placeholder="
                                greyOutIdentifierInput
                                  ? 'Auto assigned during upload'
                                  : '10.151.xxxxx'
                              "
                              :disabled="greyOutIdentifierInput"
                            ></el-input>

                            <form-help-content
                              popoverContent="An identifier for this dataset if applicable. "
                            ></form-help-content>
                          </div>
                          <div v-if="greyOutIdentifierInput" class="flex pt-2">
                            <p class="pr-1 text-sm text-gray-500">
                              An identifier will be automatically assigned to this dataset when
                              files are uploaded from your system.
                            </p>
                            <p
                              class="text-url cursor-pointer !text-sm"
                              @click="editUniqueIdentifier"
                            >
                              Click here to override this.
                            </p>
                          </div>
                        </el-form-item>

                        <el-form-item label="Keywords" prop="keywords">
                          <draggable
                            tag="div"
                            :list="step3Form.keywords"
                            item-key="id"
                            handle=".handle"
                            class="w-full"
                          >
                            <template #item="{ element }">
                              <div class="mb-2 flex w-full flex-row justify-between transition-all">
                                <div class="flex w-11/12 flex-row justify-between">
                                  <el-input
                                    v-model="element.keyword"
                                    type="text"
                                    placeholder="orbit"
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
                                  <div
                                    class="flex cursor-pointer items-center justify-center text-gray-500 transition-all hover:text-gray-800"
                                  >
                                    <el-popconfirm
                                      title="Are you sure you want to remove this?"
                                      icon-color="red"
                                      confirm-button-text="Yes"
                                      cancel-button-text="No"
                                      @confirm="deleteKeyword(element.id)"
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
                          <div class="flex w-full flex-row items-center">
                            <span class="mx-2 text-sm italic text-zinc-600"> Suggestions: </span>
                            <div class="flex-row">
                              <el-tag
                                class="mx-1 cursor-copy transition-all hover:shadow-md"
                                size="small"
                                @click="addKeyword(null, 'COVID-19')"
                                :type="
                                  step3Form.keywords.some((el) => el.keyword === 'COVID-19')
                                    ? ''
                                    : 'info'
                                "
                              >
                                COVID-19
                              </el-tag>
                              <el-tag
                                class="mx-1 cursor-copy transition-all hover:shadow-md"
                                size="small"
                                @click="addKeyword(null, 'Machine Learning')"
                                :type="
                                  step3Form.keywords.some((el) => el.keyword === 'Machine Learning')
                                    ? ''
                                    : 'info'
                                "
                              >
                                Machine Learning
                              </el-tag>
                              <el-tag
                                class="mx-1 cursor-copy transition-all hover:shadow-md"
                                size="small"
                                @click="addKeyword(null, 'Artificial Intelligence')"
                                :type="
                                  step3Form.keywords.some(
                                    (el) => el.keyword === 'Artificial Intelligence'
                                  )
                                    ? ''
                                    : 'info'
                                "
                              >
                                Artificial Intelligence
                              </el-tag>
                              <el-tag
                                class="mx-1 cursor-copy transition-all hover:shadow-md"
                                size="small"
                                @click="addKeyword(null, 'Infection rate')"
                                :type="
                                  step3Form.keywords.some((el) => el.keyword === 'Infection rate')
                                    ? ''
                                    : 'info'
                                "
                              >
                                Infection rate
                              </el-tag>
                              <el-tag
                                class="mx-1 cursor-copy transition-all hover:shadow-md"
                                size="small"
                                @click="addKeyword(null, 'Mortality prediction')"
                                :type="
                                  step3Form.keywords.some(
                                    (el) => el.keyword === 'Mortality prediction'
                                  )
                                    ? ''
                                    : 'info'
                                "
                              >
                                Mortality prediction
                              </el-tag>
                            </div>
                          </div>
                        </el-form-item>

                        <div
                          class="flex w-max cursor-pointer items-center pb-3 text-sm text-gray-500 hover:text-black"
                          @click="addKeyword(null, '')"
                        >
                          <Icon icon="carbon:add" />
                          <span> Add a keyword </span>
                          <form-help-content
                            popoverContent="Keywords relevant to your software"
                          ></form-help-content>
                        </div>

                        <el-form-item label="Funding code">
                          <div class="flex w-full flex-row items-center">
                            <el-input
                              v-model="step3Form.fundingCode"
                              type="text"
                              placeholder="PRA_2018_73"
                            ></el-input>
                            <form-help-content
                              popoverContent="Code of the grant funding this software (comma separate if multiple)"
                            ></form-help-content>
                          </div>
                        </el-form-item>

                        <el-form-item label="Funding organization">
                          <div class="flex w-full flex-row items-center">
                            <el-input
                              v-model="step3Form.fundingOrganization"
                              type="text"
                              placeholder="University of California, San Francisco"
                            ></el-input>
                            <form-help-content
                              popoverContent="The organization funding this software (comma separate if multiple)"
                            ></form-help-content>
                          </div>
                          <div class="flex w-full flex-row items-center">
                            <span class="mx-1 text-sm italic text-zinc-600"> Suggestions: </span>
                            <div class="flex-row">
                              <el-tag
                                class="mx-2 cursor-copy transition-all hover:shadow-md"
                                size="small"
                                @click="
                                  step3Form.fundingOrganization =
                                    'National Institutes of Health (NIH)'
                                "
                                :type="
                                  step3Form.fundingOrganization ===
                                  'National Institutes of Health (NIH)'
                                    ? ''
                                    : 'info'
                                "
                              >
                                National Institutes of Health (NIH)
                              </el-tag>
                              <el-tag
                                class="mx-1 cursor-copy transition-all hover:shadow-md"
                                size="small"
                                @click="
                                  step3Form.fundingOrganization =
                                    'National Science Foundation (NSF)'
                                "
                                :type="
                                  step3Form.fundingOrganization ===
                                  'National Science Foundation (NSF)'
                                    ? ''
                                    : 'info'
                                "
                              >
                                National Science Foundation (NSF)
                              </el-tag>
                            </div>
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
                            <el-select
                              v-model="step4Form.developmentStatus"
                              filterable
                              placeholder=""
                              class="w-full"
                            >
                              <el-option
                                v-for="item in repoStatusOptions"
                                :key="item.value"
                                :label="item.display_name"
                                :value="item.value"
                              >
                              </el-option>
                            </el-select>
                            <form-help-content
                              popoverContent="The current development status of this software. Select one to see the definition. See <a class='text-url' onclick='window.ipcRenderer.send(`open-link-in-browser`, `http://www.repostatus.org`)'> http://www.repostatus.org/ </a> for more details."
                            ></form-help-content>
                          </div>

                          <p class="pt-2 text-xs text-gray-500">
                            {{ developmentStatus }}
                          </p>
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
import { ElNotification } from "element-plus";

import draggable from "vuedraggable";
import validator from "validator";
import axios from "axios";
import _ from "lodash";
import humanparser from "humanparser";

import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

import PillProgressBar from "@/components/ui/PillProgressBar.vue";

import contributorTypesJSON from "@/assets/supplementalFiles/contributorTypes.json";
import repoStatusJSON from "@/assets/supplementalFiles/repoStatus.json";
import codeMetadataJSON from "@/assets/supplementalFiles/codeMetadata.json";

import SaveLottieJSON from "@/assets/lotties/saveLottie.json";

export default {
  name: "CodeCreateMetadata",
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
      totalSteps: 4,
      pillTitles: [
        "Basic info",
        "Authors and Contributors",
        "Discoverability",
        "Development tools",
        "Run-time environment",
        "Current version of the software",
        "Additional Info",
      ],
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
      generateOtherMetadata: "None",
      step1Form: {
        name: "",
        description: "",
        creationDate: "",
        firstReleaseDate: "",
      },
      step1FormRules: {
        name: [
          {
            required: true,
            message: "Please enter the name of the software",
            trigger: "blur",
          },
        ],
        description: [
          {
            required: true,
            message: "Please enter a description",
            trigger: "blur",
          },
        ],
      },
      step2Form: {
        authors: [],
        contributors: [],
      },
      step2FormRules: {
        authors: [
          {
            required: true,
            validator: this.authorValidator,
            trigger: "blur",
          },
        ],
        contributors: [
          {
            required: false,
            validator: this.contributorValidator,
            trigger: "blur",
          },
        ],
      },
      step3Form: {
        identifier: "",
        keywords: [],
        fundingCode: "",
        fundingOrganization: "",
      },
      step3FormRules: {
        keywords: [
          {
            required: true,
            validator: this.keywordValidator,
            trigger: "blur",
          },
        ],
      },
      step4Form: {
        referencePublication: "",
        developmentStatus: "",
        isPartOf: "",
      },
      isPartOfErrorMessage: "",
      greyOutIdentifierInput: false,
      invalidStatus: {},
      originalObject: {},
      showSaving: false,
      showSpinner: false,
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
    developmentStatus() {
      const that = this;

      function getStatus(repoStatus) {
        return that.repoStatusOptions.find((status) => status.value === repoStatus);
      }

      if ("developmentStatus" in this.step4Form && this.step4Form.developmentStatus != "") {
        const status = this.step4Form.developmentStatus;
        const returnVal = getStatus(status);

        return returnVal.description;
      } else {
        return "";
      }
    },
    checkInvalidStatus() {
      for (const key in this.invalidStatus) {
        if (this.invalidStatus[key]) {
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
      if (this.generateOtherMetadata === "Yes") {
        this.workflow.generateOtherMetadata = true;
      } else {
        this.workflow.generateOtherMetadata = false;
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
      if (this.step2Form.authors.length <= 0) {
        this.$message({
          message: "Please add at least one author.",
          type: "error",
        });
        return;
      }

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

    keywordValidator(_rule, array, callback) {
      if ((array === "" || array === undefined) && array.length > 0) {
        this.invalidStatus.keywords = true;
        callback(new Error("Please provide a valid keyword"));
      } else {
        for (let item of array) {
          if (item.keyword.trim() === "") {
            this.invalidStatus.keywords = true;
            callback(new Error("Please provide a valid keyword"));
            return;
          }
        }

        this.invalidStatus.keywords = false;
        callback();
      }
    },
    addKeyword(_event, keyword = "") {
      if (this.step3Form.keywords.some((el) => el.keyword === keyword)) {
        this.$message.warning("Keyword already exists.");
        return;
      }

      const id = uuidv4();
      this.step3Form.keywords.push({
        keyword,
        id,
      });
      this.focusOnElementRef(id);
    },
    deleteKeyword(id) {
      this.step3Form.keywords = this.step3Form.keywords.filter((keyword) => {
        return keyword.id !== id;
      });
      this.$refs["s3Form"].validate();
    },

    authorValidator(_rule, value, callback) {
      if (value.length > 0) {
        for (let author of value) {
          if (
            author.givenName === "" ||
            author.affiliation === "" ||
            author.affiliation === undefined
          ) {
            this.invalidStatus.authors = true;
            callback(new Error("First name and Affiliation for each author is mandatory"));
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
              this.invalidStatus.authors = true;
              callback(new Error("ORCID is not valid"));
            }
          }

          // validate email
          if (author.email !== "") {
            const validIdentifier = validator.isEmail(author.email);

            if (!validIdentifier) {
              this.invalidStatus.authors = true;
              callback(new Error("Email is not valid"));
              return;
            }
          }
        }
      } else {
        this.invalidStatus.authors = true;
        callback(new Error("Please provide at least one author"));
        return;
      }
      this.invalidStatus.authors = false;
      callback();
    },
    addAuthor() {
      this.step2Form.authors.push({
        givenName: "",
        familyName: "",
        affiliation: "",
        email: "",
        orcid: "",
        id: uuidv4(),
      });
    },
    deleteAuthor(id) {
      this.step2Form.authors = this.step2Form.authors.filter((author) => {
        return author.id !== id;
      });
      this.$refs["s2Form"].validate();
    },

    contributorValidator(_rule, value, callback) {
      if (value.length > 0) {
        for (let contributor of value) {
          if (
            contributor.givenName === undefined ||
            contributor.givenName.trim() === "" ||
            contributor.affiliation === undefined ||
            contributor.affiliation.trim() === ""
          ) {
            callback(new Error("First name and Affiliation for each contributor is mandatory"));
            return;
          }

          // validate orcid
          if (contributor.orcid !== "") {
            const orcid = contributor.orcid;
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
              return;
            }
          }

          // validate email
          if (contributor.email !== "") {
            const validIdentifier = validator.isEmail(contributor.email);

            if (!validIdentifier) {
              callback(new Error("Email is not valid"));
              return;
            }
          }

          if (
            contributor.contributorType === undefined ||
            contributor.contributorType.trim() === ""
          ) {
            callback(new Error("Contributor type is mandatory"));
            return;
          }
        }
      }
      callback();
    },
    addContributor() {
      this.step2Form.contributors.push({
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
      this.step2Form.contributors = this.step2Form.contributors.filter((contributor) => {
        return contributor.id !== id;
      });
      this.$refs["s2Form"].validate();
    },

    filterArrayOfObjects(array, key) {
      return array.filter((element) => {
        return element[key] !== "";
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

      let otherForm = {};

      otherForm.name = this.step1Form.name;
      otherForm.description = this.step1Form.description;
      otherForm.creationDate = this.step1Form.creationDate;
      otherForm.firstReleaseDate = this.step1Form.firstReleaseDate;

      otherForm.authors = this.step2Form.authors;
      otherForm.contributors = this.step2Form.contributors;

      otherForm.identifier = this.step3Form.identifier;
      otherForm.keywords = this.step3Form.keywords;
      otherForm.fundingCode = this.step3Form.fundingCode;
      otherForm.fundingOrganization = this.step3Form.fundingOrganization;

      otherForm.referencePublication = this.step4Form.referencePublication;
      otherForm.developmentStatus = this.step4Form.developmentStatus;
      otherForm.isPartOf = this.step4Form.isPartOf;

      this.dataset.data.Other.questions = otherForm;

      this.workflow.generateCodeMeta = false;

      if (this.generateOtherMetadata === "Yes") {
        this.workflow.generateOtherMetadata = true;
      } else {
        this.workflow.generateOtherMetadata = false;
      }

      await this.datasetStore.updateCurrentDataset(this.dataset);
      await this.datasetStore.syncDatasets();
    },
    async navigateToSelectDestination(_evt, shouldNavigateBack = false) {
      await this.saveCurrentEntries();

      if (shouldNavigateBack) {
        this.$router.push({
          path: `/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/Other/selectFolder`,
        });
        return;
      }

      const routerPath = `/datasets/${this.dataset.id}/${this.workflowID}/Other/pickLicense`;

      this.$router.push({ path: routerPath });
    },
    navigateBack() {
      this.$router.push({
        path: `/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/Other/reviewStandards`,
      });
    },
    async prefillGithubAuthors() {
      ElNotification({
        title: "Info",
        message: "Requesting authors",
        position: "top-right",
        type: "info",
      });

      // get a list of contributors for the repo
      const tokenObject = await this.tokens.getToken("github");
      const GithubAccessToken = tokenObject.token;

      const selectedRepo = this.workflow.github.repo;

      let response = "";

      response = await axios
        .get(`${this.$server_url}/github/repo/contributors`, {
          params: {
            access_token: GithubAccessToken,
            owner: selectedRepo.split("/")[0],
            repo: selectedRepo.split("/")[1],
          },
        })
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });

      let contributors = [];

      if (response != "ERROR") {
        response.forEach((contributor) => {
          contributors.push(contributor.login);
        });
      }

      let authors = [];

      for (const contributor of contributors) {
        response = await axios
          .get(`${process.env.VUE_APP_GITHUB_SERVER_URL}/users/${contributor}`, {
            params: {
              accept: "application/vnd.github.v3+json",
            },
            headers: {
              Authorization: `Bearer  ${GithubAccessToken}`,
            },
          })
          .then((response) => {
            const authorObject = {};

            if (response.data.name != null) {
              const parsedNames = humanparser.parseName(response.data.name);
              if ("lastName" in parsedNames) {
                authorObject.familyName = parsedNames.lastName;
              } else {
                authorObject.familyName = "";
              }
              if ("firstName" in parsedNames) {
                authorObject.givenName = parsedNames.firstName;
              } else {
                authorObject.givenName = response.data.name;
              }
            }

            if (response.data.email != null) {
              authorObject.email = response.data.email;
            }

            if (response.data.company != null) {
              authorObject.company = response.data.company;
            }

            if (!_.isEmpty(authorObject)) {
              authors.push(authorObject);
            }
          })
          .catch((error) => {
            console.error(error);
          });
      }

      authors.forEach((author) => {
        const authorObject = {
          givenName: author.givenName,
          familyName: author.familyName,
          affiliation: author.company,
          email: author.email,
          orcid: "",
          id: uuidv4(),
        };

        this.step2Form.authors.push(authorObject);
      });

      ElNotification({
        title: "Success",
        message: "Retrieved authors",
        position: "top-right",
        type: "success",
      });
    },
    async prefillGithubMisc() {
      ElNotification({
        title: "Info",
        message: "Requesting repository info",
        position: "top-right",
        type: "info",
      });

      // get a list of contributors for the repo
      const tokenObject = await this.tokens.getToken("github");
      const GithubAccessToken = tokenObject.token;

      const selectedRepo = this.workflow.github.repo;

      let response = "";

      response = await axios
        .get(`${process.env.VUE_APP_GITHUB_SERVER_URL}/repos/${selectedRepo}`, {
          params: {
            accept: "application/vnd.github.v3+json",
          },
          headers: {
            Authorization: `Bearer  ${GithubAccessToken}`,
          },
        })
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });

      if (response != "ERROR") {
        if (response.html_url != null) {
          this.step4Form.codeRepository = response.html_url;
          this.step4Form.issueTracker = `${response.html_url}/issues`;
        }

        if (response.homepage != null) {
          this.step4Form.relatedLinks.push({
            link: response.homepage,
            id: uuidv4(),
          });
        }

        if (response.topics != null && response.topics.length > 0) {
          response.topics.forEach((topic) => {
            this.step3Form.keywords.push({
              keyword: topic,
              id: uuidv4(),
            });
          });
        }

        if ("created_at" in response) {
          this.step1Form.creationDate = response.created_at;
        }

        this.step5Form.currentVersionReleaseDate = new Date().toISOString();

        if (response.description != null) {
          this.step1Form.description = response.description;
        }

        const splitRepoNameOwner = selectedRepo.split("/");

        const releaseList = await axios
          .get(`${this.$server_url}/github/repo/releases`, {
            params: {
              access_token: GithubAccessToken,
              owner: splitRepoNameOwner[0],
              repo: splitRepoNameOwner[1],
            },
          })
          .then((response) => {
            return response.data;
          })
          .catch((error) => {
            console.error(error);
            return "ERROR";
          });

        if (releaseList !== "ERROR") {
          if (releaseList.length > 0) {
            const release = releaseList.slice(-1).pop();

            if ("created_at" in release) {
              this.step1Form.firstReleaseDate = release.created_at;
            }
          }
        }

        const lanuagesResponse = await axios
          .get(`${process.env.VUE_APP_GITHUB_SERVER_URL}/repos/${selectedRepo}/languages`, {
            params: {
              accept: "application/vnd.github.v3+json",
            },
            headers: {
              Authorization: `Bearer  ${GithubAccessToken}`,
            },
          })
          .then((response) => {
            return response.data;
          })
          .catch((error) => {
            console.error(error);
            return "ERROR";
          });

        if (lanuagesResponse != "ERROR") {
          const languages = Object.keys(lanuagesResponse);
          if (languages.length > 0) {
            this.step4Form.programmingLanguage = languages;
          }
        }

        ElNotification({
          title: "Success",
          message: "Repository info retrieved",
          position: "top-right",
          type: "success",
        });
      }
    },
    prefillFormFromMetadataObject(otherMetadata) {
      this.step1Form.name = otherMetadata.name;
      this.step1Form.description = otherMetadata.description;
      this.step1Form.creationDate = otherMetadata.dateCreated;
      this.step1Form.firstReleaseDate = otherMetadata.datePublished;

      this.step2Form.authors = [];
      otherMetadata.author.forEach(
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
      if ("contributor" in otherMetadata) {
        otherMetadata.contributor.forEach(
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

      this.step3Form.identifier = otherMetadata.identifier;
      if ("keywords" in otherMetadata) {
        otherMetadata.keywords.forEach((keyword) => {
          this.step3Form.keywords.push({ keyword, id: uuidv4() });
        });
      }
      if ("fundingCode" in otherMetadata) {
        this.step3Form.fundingCode = otherMetadata.fundingCode;
      }
      if ("fundingOrganization" in otherMetadata) {
        this.step3Form.fundingOrganization = otherMetadata.fundingOrganization;
      }

      this.step4Form.referencePublication = otherMetadata.referencePublication;
      if ("developmentStatus" in otherMetadata) {
        this.step4Form.developmentStatus = otherMetadata.developmentStatus;
      }
      this.step4Form.isPartOf = otherMetadata.isPartOf;
    },
    checkIdentifierInput() {
      if ("source" in this.workflow) {
        if (this.workflow.source.type === "local") {
          if (this.step3Form.identifier === "" || this.step3Form.identifier === undefined) {
            this.greyOutIdentifierInput = true;
          }
        } else {
          this.greyOutIdentifierInput = false;
        }
      }
    },
    editUniqueIdentifier() {
      this.step3Form.identifier = "";
      this.greyOutIdentifierInput = false;
    },
  },
  async mounted() {
    this.$nextTick(async function () {
      this.dataset = await this.datasetStore.getCurrentDataset();

      this.workflow = this.dataset.workflows[this.workflowID];

      this.datasetStore.showProgressBar();
      this.datasetStore.setProgressBarType("zenodo");
      this.datasetStore.setCurrentStep(3);

      this.workflow.currentRoute = this.$route.path;

      if ("generateOtherMetadata" in this.workflow) {
        this.generateOtherMetadata = this.workflow.generateOtherMetadata ? "Yes" : "No";
      } else {
        this.generateOtherMetadata = "None";
      }

      if (
        this.dataset.data.Other.questions &&
        Object.keys(this.dataset.data.Other.questions).length !== 0
      ) {
        let otherForm = this.dataset.data.Other.questions;

        this.step1Form.name = otherForm.name;
        this.step1Form.description = otherForm.description;
        this.step1Form.creationDate = otherForm.creationDate;
        this.step1Form.firstReleaseDate = otherForm.firstReleaseDate;

        this.step2Form.authors = otherForm.authors;
        this.step2Form.contributors = otherForm.contributors;

        this.step3Form.identifier = otherForm.identifier;
        this.step3Form.keywords = otherForm.keywords;
        this.step3Form.fundingCode = otherForm.fundingCode;
        this.step3Form.fundingOrganization = otherForm.fundingOrganization;

        this.step4Form.referencePublication = otherForm.referencePublication;
        this.step4Form.developmentStatus = otherForm.developmentStatus;
        this.step4Form.isPartOf = otherForm.isPartOf;

        this.addIds(this.step3Form.keywords);
        this.addIds(this.step2Form.authors);
        this.addIds(this.step2Form.contributors);

        // this.originalObject.Other = JSON.parse(JSON.stringify(this.otherForm));
      } else {
        this.step1Form.name = this.dataset.name;
        this.step1Form.description = this.dataset.description;
        // this.originalObject.Other = JSON.parse(JSON.stringify(this.otherForm));

        if ("source" in this.workflow) {
          if (this.workflow.source.type === "github") {
            // this.showSpinner = true;
            // const tokenObject = await this.tokens.getToken("github");
            // const GithubAccessToken = tokenObject.token;
            // const selectedRepo = this.workflow.github.repo;
            // let response = "";
            // response = await axios
            //   .get(`${this.$server_url}/github/repo/file/contents`, {
            //     params: {
            //       access_token: GithubAccessToken,
            //       owner: selectedRepo.split("/")[0],
            //       repo: selectedRepo.split("/")[1],
            //       file_name: "codemeta.json",
            //     },
            //   })
            //   .then((response) => {
            //     return response.data;
            //   })
            //   .catch((error) => {
            //     console.error(error);
            //     return "ERROR";
            //   });
            // if (response !== "NOT_FOUND") {
            //   ElNotification({
            //     title: "Info",
            //     message: "Found a previous codemeta.json file. Loading it...",
            //     position: "top-right",
            //     type: "info",
            //   });
            //   const codeMeta = JSON.parse(response);
            //   await this.prefillFormFromMetadataObject(codeMeta);
            //   ElNotification({
            //     title: "Success",
            //     message: "Successfully loaded codemeta.json file.",
            //     position: "top-right",
            //     type: "success",
            //   });
            //   this.showSpinner = false;
            // } else {
            //   await this.prefillGithubAuthors();
            //   await this.prefillGithubMisc();
            //   this.showSpinner = false;
            // }
          }
          if (this.workflow.source.type === "local") {
            this.showSpinner = true;

            const response = await axios
              .post(`${this.$server_url}/utilities/fileexistinfolder`, {
                folder_path: this.dataset.data.Other.folderPath,
                file_name: "metadata.json",
              })
              .then((response) => {
                return response.data;
              })
              .catch((error) => {
                console.log(error);
                return "ERROR";
              });

            if (response !== "ERROR" && response !== "Not Found") {
              ElNotification({
                title: "Info",
                message: "Found a previous metadata.json file. Loading it...",
                position: "top-right",
                type: "info",
              });

              await this.prefillFormFromMetadataObject(response);

              ElNotification({
                title: "Success",
                message: "Successfully loaded metadata.json file.",
                position: "top-right",
                type: "success",
              });
            }

            this.showSpinner = false;
          }
        }
      }
      this.checkIdentifierInput();
    });
  },
};
</script>
