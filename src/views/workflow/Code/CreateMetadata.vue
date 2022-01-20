<template>
  <div
    class="flex flex-col items-center justify-center w-full h-full max-w-screen-xl p-3 px-5"
  >
    <div class="flex flex-col w-full h-full">
      <span class="text-lg font-medium text-left">
        Provide information about your research sofware
      </span>

      <line-divider></line-divider>

      <span class="mb-2">
        We will use this information to automatically include the standard
        codemeta.json and CITATION.cff file in your dataset.
      </span>

      <div>
        <div class="py-3">
          <pill-progress-bar
            :totalSteps="7"
            :currentStep="currentStep"
            @updateCurrentStep="setCurrentStep"
            :titles="pillTitles"
          />
        </div>
        <div class="py-2">
          <div v-if="currentStep == 1">
            <div
              class="mb-4 border-2 rounded-lg shadow-md form-card-content border-slate-100"
            >
              <div class="w-full px-4 py-2 bg-gray-100">
                <span
                  class="text-lg font-semibold pointer-events-none text-primary-600"
                >
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
                  <el-form-item label="Software name" prop="name">
                    <div class="flex flex-row items-center">
                      <el-input
                        v-model="step1Form.name"
                        placeholder="My Software"
                      ></el-input>
                      <form-help-content
                        popoverContent="The name of the software"
                      ></form-help-content>
                    </div>
                  </el-form-item>

                  <el-form-item
                    label="Software description/abstract"
                    prop="description"
                  >
                    <div class="flex flex-row items-center">
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
                    <div class="flex flex-row items-center">
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
                    <div class="flex flex-row items-center">
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
            <div
              class="flex justify-center w-full px-5 space-x-4 form-navigation-buttons"
            >
              <button
                @click="prevFormStep"
                class="primary-plain-button"
                size="medium"
                :disabled="checkInvalidStatus"
              >
                <el-icon><back-icon /></el-icon>
                Back
              </button>
              <!-- :plain="!lastStep" -->
              <button
                class="primary-button"
                @click="navigateToStep2FromStep1"
                :disabled="checkInvalidStatus"
              >
                Next
                <el-icon><right-icon /></el-icon>
              </button>
            </div>
          </div>

          <div v-if="currentStep == 2">
            <div
              class="mb-4 border-2 rounded-lg shadow-md form-card-content border-slate-100"
            >
              <div class="w-full px-4 py-2 bg-gray-100">
                <span
                  class="text-lg font-semibold pointer-events-none text-primary-600"
                >
                  Authors and Contributors
                </span>
              </div>
              <div class="p-4">
                <el-form
                  :model="step2Form"
                  label-width="160px"
                  label-position="top"
                  size="large"
                  ref="s2Form"
                  @submit.prevent
                  class="py-4"
                >
                  <el-form-item
                    label="Authors"
                    :error="authorsErrorMessage"
                    required
                  >
                    <draggable
                      tag="div"
                      :list="step2Form.authors"
                      item-key="id"
                      handle=".handle"
                    >
                      <template #item="{ element }">
                        <div
                          class="flex flex-row justify-between mb-2 transition-all"
                        >
                          <div class="flex flex-row justify-between w-11/12">
                            <el-input
                              v-model="element.givenName"
                              type="text"
                              placeholder="Given name"
                            ></el-input>

                            <div class="mx-2"></div>

                            <el-input
                              v-model="element.familyName"
                              type="text"
                              placeholder="Family name"
                            ></el-input>

                            <div class="mx-2"></div>

                            <el-input
                              v-model="element.affiliation"
                              type="text"
                              placeholder="Affiliation"
                            ></el-input>

                            <div class="flex flex-col w-full mx-2">
                              <el-input
                                v-model="element.email"
                                type="text"
                                placeholder="E-mail address"
                              ></el-input>
                              <span class="mt-1 ml-2 text-xs text-gray-400">
                                Optional
                              </span>
                            </div>

                            <div class="flex flex-col w-full mx-2">
                              <el-input
                                v-model="element.orcid"
                                type="text"
                                placeholder="ORCID (e.g.: 0000-0002-1825-0097)"
                              ></el-input>
                              <span class="mt-1 ml-2 text-xs text-gray-400">
                                Optional
                              </span>
                            </div>
                          </div>
                          <div
                            class="flex flex-row items-start w-1/12 py-2 justify-evenly"
                          >
                            <div
                              class="flex items-center justify-center text-gray-400 handle hover:text-gray-700"
                            >
                              <Icon icon="ic:outline-drag-indicator" />
                            </div>
                            <div
                              class="flex items-center justify-center text-gray-600 cursor-pointer hover:text-gray-800"
                            >
                              <el-popconfirm
                                title="Are you sure you want to remove this?"
                                icon-color="red"
                                confirm-button-text="Yes"
                                cancel-button-text="No"
                                @confirm="deleteAuthor(element.id)"
                              >
                                <template #reference>
                                  <Icon icon="bx:bx-x" />
                                </template>
                              </el-popconfirm>
                            </div>
                          </div>
                        </div>
                      </template>
                    </draggable>
                  </el-form-item>

                  <div
                    class="flex items-center mb-6 text-sm text-gray-500 cursor-pointer hover:text-black w-max"
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

                  <el-form-item
                    label="Contributors"
                    :error="contributorsErrorMessage"
                  >
                    <draggable
                      tag="div"
                      :list="step2Form.contributors"
                      item-key="id"
                      handle=".handle"
                    >
                      <template #item="{ element }">
                        <div
                          class="flex flex-row justify-between mb-2 transition-all"
                        >
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

                          <div class="flex flex-row justify-between w-11/12">
                            <div class="w-1/5 mr-2">
                              <el-input
                                v-model="element.givenName"
                                type="text"
                                placeholder="Given name"
                              ></el-input>
                            </div>

                            <div class="w-1/5 mx-2">
                              <el-input
                                v-model="element.familyName"
                                type="text"
                                placeholder="Family name"
                              ></el-input>
                            </div>

                            <div class="w-1/5 mx-2">
                              <el-input
                                v-model="element.affiliation"
                                type="text"
                                placeholder="Affiliation"
                              ></el-input>
                            </div>

                            <div class="flex flex-col w-1/5 mx-2">
                              <el-input
                                v-model="element.email"
                                type="text"
                                placeholder="E-mail address"
                              ></el-input>
                              <span class="mt-1 ml-2 text-xs text-gray-400">
                                Optional
                              </span>
                            </div>

                            <div class="flex flex-col w-1/5 mx-2">
                              <el-input
                                v-model="element.orcid"
                                type="text"
                                placeholder="ORCID (e.g. 0000-0002-1825-0097)"
                              ></el-input>
                              <span class="mt-1 ml-2 text-xs text-gray-400">
                                Optional
                              </span>
                            </div>
                          </div>
                          <div
                            class="flex flex-row items-start w-1/12 py-2 justify-evenly"
                          >
                            <div
                              class="flex items-center justify-center text-gray-400 handle hover:text-gray-700"
                            >
                              <Icon icon="ic:outline-drag-indicator" />
                            </div>
                            <div
                              class="flex items-center justify-center text-gray-600 cursor-pointer hover:text-gray-800"
                            >
                              <el-popconfirm
                                title="Are you sure you want to remove this?"
                                icon-color="red"
                                confirm-button-text="Yes"
                                cancel-button-text="No"
                                @confirm="deleteContributor(element.id)"
                              >
                                <template #reference>
                                  <Icon icon="bx:bx-x" />
                                </template>
                              </el-popconfirm>
                            </div>
                          </div>
                        </div>
                      </template>
                    </draggable>
                  </el-form-item>

                  <div
                    class="flex items-center text-sm text-gray-500 cursor-pointer hover:text-black w-max"
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
            <div
              class="flex justify-center w-full px-5 space-x-4 form-navigation-buttons"
            >
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
              class="mb-4 border-2 rounded-lg shadow-md form-card-content border-slate-100"
            >
              <div class="w-full px-4 py-2 bg-gray-100">
                <span
                  class="text-lg font-semibold pointer-events-none text-primary-600"
                >
                  Discoverability
                </span>
              </div>
              <div class="p-4">
                <el-form
                  :model="step3Form"
                  label-width="160px"
                  label-position="top"
                  size="large"
                  ref="s3Form"
                  @submit.prevent
                  class="py-4"
                >
                  <el-form-item label="Application category">
                    <div class="flex flex-row items-center">
                      <el-select
                        v-model="step3Form.applicationCategory"
                        filterable
                        allow-create
                        placeholder="Select an application category"
                        class="w-full"
                      >
                        <el-option
                          v-for="item in applicationCategoryOptions"
                          :key="item"
                          :label="item"
                          :value="item"
                        >
                        </el-option>
                      </el-select>
                      <form-help-content
                        popoverContent="Type of application, e.g. scientific, business, etc."
                      ></form-help-content>
                    </div>
                  </el-form-item>

                  <el-form-item label="Keywords" required>
                    <draggable
                      tag="div"
                      :list="step3Form.keywords"
                      item-key="id"
                      handle=".handle"
                    >
                      <template #item="{ element }">
                        <div
                          class="flex flex-row justify-between mb-2 transition-all"
                        >
                          <div class="flex flex-row justify-between w-11/12">
                            <el-input
                              v-model="element.keyword"
                              type="text"
                              placeholder="orbit"
                              v-on:keyup.enter="addKeyword"
                              :ref="element.id"
                            ></el-input>
                            <div class="mx-2"></div>
                          </div>
                          <div class="flex flex-row w-1/12 justify-evenly">
                            <div
                              class="flex items-center justify-center text-gray-400 handle hover:text-gray-700"
                            >
                              <Icon icon="ic:outline-drag-indicator" />
                            </div>
                            <div
                              class="flex items-center justify-center text-gray-600 cursor-pointer hover:text-gray-800"
                            >
                              <el-popconfirm
                                title="Are you sure you want to remove this?"
                                icon-color="red"
                                confirm-button-text="Yes"
                                cancel-button-text="No"
                                @confirm="deleteKeyword(element.id)"
                              >
                                <template #reference>
                                  <Icon icon="bx:bx-x" />
                                </template>
                              </el-popconfirm>
                            </div>
                          </div>
                        </div>
                      </template>
                    </draggable>
                  </el-form-item>

                  <div
                    class="flex items-center pb-3 text-sm text-gray-500 cursor-pointer hover:text-black w-max"
                    @click="addKeyword"
                  >
                    <Icon icon="carbon:add" />
                    <span> Add a keyword </span>
                    <form-help-content
                      popoverContent="Keywords relevant to your software"
                    ></form-help-content>
                  </div>

                  <el-form-item label="Funding code">
                    <div class="flex flex-row items-center">
                      <el-input
                        v-model="step3Form.funding.code"
                        type="text"
                        placeholder="PRA_2018_73"
                      ></el-input>
                      <form-help-content
                        popoverContent="Code of the grant funding this software (comma separate if multiple)"
                      ></form-help-content>
                    </div>
                  </el-form-item>

                  <el-form-item label="Funding organization">
                    <div class="flex flex-row items-center">
                      <el-input
                        v-model="step3Form.funding.organization"
                        type="text"
                        placeholder="University of California, San Francisco"
                      ></el-input>
                      <form-help-content
                        popoverContent="The organization funding this software (comma separate if multiple)"
                      ></form-help-content>
                    </div>
                  </el-form-item>
                </el-form>
              </div>
            </div>
            <div
              class="flex justify-center w-full px-5 space-x-4 form-navigation-buttons"
            >
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
              class="mb-4 border-2 rounded-lg shadow-md form-card-content border-slate-100"
            >
              <div class="w-full px-4 py-2 bg-gray-100">
                <span
                  class="text-lg font-semibold pointer-events-none text-primary-600"
                >
                  Development tools
                </span>
              </div>
              <div class="p-4">
                <el-form
                  :model="step4Form"
                  label-width="160px"
                  label-position="top"
                  size="large"
                  ref="s4Form"
                  @submit.prevent
                  class="py-4"
                >
                  <el-form-item
                    label="Code repository"
                    :error="codeRepositoryErrorMessage"
                  >
                    <div class="flex flex-row items-center">
                      <el-input
                        v-model="step4Form.codeRepository"
                        placeholder="https://github.com/fairdataihub/SODA-for-COVID-19-Research"
                      ></el-input>
                      <form-help-content
                        popoverContent="Link to the repository where the un-compiled, human readable code and related code is located (SVN, Git, GitHub, CodePlex, institutional GitLab instance, etc.)"
                      ></form-help-content>
                    </div>
                  </el-form-item>

                  <el-form-item
                    label="Continuous integration"
                    :error="continuousIntegrationErrorMessage"
                  >
                    <div class="flex flex-row items-center">
                      <el-input
                        v-model="step4Form.continuousIntegration"
                        placeholder="https://www.travis-ci.com/fairdataihub/FairShare"
                      ></el-input>
                      <form-help-content
                        popoverContent="Link to continuous integration service (Travis, CircleCI, etc.)"
                      ></form-help-content>
                    </div>
                  </el-form-item>

                  <el-form-item
                    label="Issue Tracker"
                    :error="issueTrackerErrorMessage"
                  >
                    <div class="flex flex-row items-center">
                      <el-input
                        v-model="step4Form.issueTracker"
                        placeholder="https://github.com/fairdataihub/SODA-for-COVID-19-Research/issues"
                      ></el-input>
                      <form-help-content
                        popoverContent="Link to issue tracker (Jira, GitHub issues, etc.)"
                      ></form-help-content>
                    </div>
                  </el-form-item>

                  <el-form-item
                    label="Related links"
                    :error="relatedLinksErrorMessage"
                  >
                    <draggable
                      tag="div"
                      :list="step4Form.relatedLinks"
                      item-key="id"
                      handle=".handle"
                    >
                      <template #item="{ element }">
                        <div
                          class="flex flex-row justify-between mb-2 transition-all"
                        >
                          <div class="flex flex-row justify-between w-11/12">
                            <el-input
                              v-model="element.link"
                              type="text"
                              placeholder="https://github.com/fairdataihub/SODA-for-COVID-19-Research"
                            ></el-input>
                            <div class="mx-2"></div>
                          </div>
                          <div class="flex flex-row w-1/12 justify-evenly">
                            <div
                              class="flex items-center justify-center text-gray-400 handle hover:text-gray-700"
                            >
                              <Icon icon="ic:outline-drag-indicator" />
                            </div>
                            <div
                              class="flex items-center justify-center text-gray-600 cursor-pointer hover:text-gray-800"
                            >
                              <el-popconfirm
                                title="Are you sure you want to remove this?"
                                icon-color="red"
                                confirm-button-text="Yes"
                                cancel-button-text="No"
                                @confirm="deleteRelatedLink(element.id)"
                              >
                                <template #reference>
                                  <Icon icon="bx:bx-x" />
                                </template>
                              </el-popconfirm>
                            </div>
                          </div>
                        </div>
                      </template>
                    </draggable>
                  </el-form-item>

                  <div
                    class="flex items-center text-sm text-gray-500 cursor-pointer hover:text-black w-max"
                    @click="addRelatedLink"
                  >
                    <Icon icon="carbon:add" />
                    <span> Add a related link </span>
                    <form-help-content
                      popoverContent="Link to documents, software, tools, etc. related to your software"
                    ></form-help-content>
                  </div>
                </el-form>
              </div>
            </div>
            <div
              class="flex justify-center w-full px-5 space-x-4 form-navigation-buttons"
            >
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
                @click="navigateToStep5FromStep4"
                :disabled="checkInvalidStatus"
              >
                Next
                <el-icon><right-icon /></el-icon>
              </button>
            </div>
          </div>

          <div v-if="currentStep == 5">
            <div
              class="mb-4 border-2 rounded-lg shadow-md form-card-content border-slate-100"
            >
              <div class="w-full px-4 py-2 bg-gray-100">
                <span
                  class="text-lg font-semibold pointer-events-none text-primary-600"
                >
                  Run-time environment
                </span>
              </div>
              <div class="p-4">
                <el-form
                  :model="step5Form"
                  label-width="160px"
                  label-position="top"
                  size="large"
                  ref="s5Form"
                  @submit.prevent
                  class="py-4"
                >
                  <el-form-item label="Programming Language" required>
                    <div class="flex flex-row items-center">
                      <el-select
                        v-model="step5Form.programmingLanguage"
                        multiple
                        filterable
                        allow-create
                        default-first-option
                        placeholder="C#, Java, Python 3"
                        class="w-full"
                      >
                        <el-option
                          v-for="item in programmingLanguageOptions"
                          :key="item.value"
                          :label="item.label"
                          :value="item.value"
                        >
                        </el-option>
                      </el-select>
                      <form-help-content
                        popoverContent="All programming languages used in this software. Select from the suggested list or type your own."
                      ></form-help-content>
                    </div>
                  </el-form-item>

                  <el-form-item label="Runtime platform">
                    <div class="flex flex-row items-center">
                      <el-select
                        v-model="step5Form.runtimePlatform"
                        multiple
                        filterable
                        allow-create
                        default-first-option
                        placeholder=".Net, Java"
                        class="w-full"
                      >
                        <el-option
                          v-for="item in runtimePlatformOptions"
                          :key="item.value"
                          :label="item.label"
                          :value="item.value"
                        >
                        </el-option>
                      </el-select>
                      <form-help-content
                        popoverContent="All runtime platforms used in this software. Select from the suggested list or type your own."
                      ></form-help-content>
                    </div>
                  </el-form-item>

                  <el-form-item label="Operating system">
                    <div class="flex flex-row items-center">
                      <el-select
                        v-model="step5Form.operatingSystem"
                        multiple
                        filterable
                        allow-create
                        default-first-option
                        placeholder="Linux, Windows"
                        class="w-full"
                      >
                        <el-option
                          v-for="item in operatingSystemOptions"
                          :key="item.value"
                          :label="item.label"
                          :value="item.value"
                        >
                        </el-option>
                      </el-select>
                      <form-help-content
                        popoverContent="All operating systems this software can run on.  Select from the suggested list or type your own."
                      ></form-help-content>
                    </div>
                  </el-form-item>

                  <el-form-item label="Other software requirements">
                    <draggable
                      tag="div"
                      :list="step5Form.otherSoftwareRequirements"
                      item-key="id"
                      handle=".handle"
                    >
                      <template #item="{ element }">
                        <div
                          class="flex flex-row justify-between mb-2 transition-all"
                        >
                          <div class="flex flex-row justify-between w-11/12">
                            <el-input
                              v-model="element.link"
                              type="text"
                              placeholder="Python 3.4 or https://github.com/pst/requests"
                            ></el-input>
                            <div class="mx-2"></div>
                          </div>
                          <div class="flex flex-row w-1/12 justify-evenly">
                            <div
                              class="flex items-center justify-center text-gray-400 handle hover:text-gray-700"
                            >
                              <Icon icon="ic:outline-drag-indicator" />
                            </div>
                            <div
                              class="flex items-center justify-center text-gray-600 cursor-pointer hover:text-gray-800"
                            >
                              <el-popconfirm
                                title="Are you sure you want to remove this?"
                                icon-color="red"
                                confirm-button-text="Yes"
                                cancel-button-text="No"
                                @confirm="
                                  deleteOtherSoftwareRequirements(element.id)
                                "
                              >
                                <template #reference>
                                  <Icon icon="bx:bx-x" />
                                </template>
                              </el-popconfirm>
                            </div>
                          </div>
                        </div>
                      </template>
                    </draggable>
                  </el-form-item>

                  <div
                    class="flex items-center text-sm text-gray-500 cursor-pointer hover:text-black w-max"
                    @click="addOtherSoftwareRequirements"
                  >
                    <Icon icon="carbon:add" />
                    <span> Add an additional software requirement </span>
                    <form-help-content
                      popoverContent="Required software to run/compile/use this software."
                    ></form-help-content>
                  </div>
                </el-form>
              </div>
            </div>
            <div
              class="flex justify-center w-full px-5 space-x-4 form-navigation-buttons"
            >
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
              class="mb-4 border-2 rounded-lg shadow-md form-card-content border-slate-100"
            >
              <div class="w-full px-4 py-2 bg-gray-100">
                <span
                  class="text-lg font-semibold pointer-events-none text-primary-600"
                >
                  Current version of the software
                </span>
              </div>
              <div class="p-4">
                <el-form
                  :model="step6Form"
                  label-width="160px"
                  label-position="top"
                  size="large"
                  ref="s6Form"
                  @submit.prevent
                  class="py-4"
                >
                  <el-form-item
                    label="Current version"
                    :error="versionErrorMessage"
                  >
                    <div class="flex flex-row items-center">
                      <el-input
                        v-model="step6Form.currentVersion"
                        placeholder="1.5.6"
                      ></el-input>
                      <form-help-content
                        popoverContent="Version number of this software"
                      ></form-help-content>
                    </div>
                  </el-form-item>

                  <el-form-item label="Current version release date">
                    <div class="flex flex-row items-center">
                      <el-date-picker
                        v-model="step6Form.currentVersionReleaseDate"
                        type="date"
                        placeholder="Pick a day"
                        value-format="YYYY-MM-DD"
                      >
                      </el-date-picker>
                      <form-help-content
                        popoverContent="The date on which the current version was released"
                      ></form-help-content>
                    </div>
                  </el-form-item>

                  <el-form-item
                    label="Current version download URL"
                    :error="currentVersionDownloadLinkErrorMessage"
                  >
                    <div class="flex flex-row items-center">
                      <el-input
                        v-model="step6Form.currentVersionDownloadLink"
                        type="url"
                        placeholder="https://www.python.org/downloads/release/python-3100/"
                      ></el-input>
                      <form-help-content
                        popoverContent="URL to download the current version of this software"
                      ></form-help-content>
                    </div>
                  </el-form-item>

                  <el-form-item label="Current version release notes">
                    <div class="flex flex-row items-center">
                      <el-input
                        v-model="step6Form.currentVersionReleaseNotes"
                        type="textarea"
                        placeholder="Change log: Added this new feature &#10;Bugfixes: Squashed some bugs"
                      ></el-input>
                      <form-help-content
                        popoverContent="Release notes for the current version of this software"
                      ></form-help-content>
                    </div>
                  </el-form-item>
                </el-form>
              </div>
            </div>
            <div
              class="flex justify-center w-full px-5 space-x-4 form-navigation-buttons"
            >
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
              class="mb-4 border-2 rounded-lg shadow-md form-card-content border-slate-100"
            >
              <div class="w-full px-4 py-2 bg-gray-100">
                <span
                  class="text-lg font-semibold pointer-events-none text-primary-600"
                >
                  Current version of the software
                </span>
              </div>
              <div class="p-4">
                <el-form
                  :model="step7Form"
                  label-width="160px"
                  label-position="top"
                  size="large"
                  ref="s7Form"
                  @submit.prevent
                  class="py-4"
                >
                  <el-form-item label="Reference publication">
                    <div class="flex flex-row items-center">
                      <el-input
                        v-model="step7Form.referencePublication"
                        type="text"
                        placeholder="https://doi.org/10.100/xyz123"
                      ></el-input>
                      <form-help-content
                        popoverContent="Link to the scholarly publication that describes the software"
                      ></form-help-content>
                    </div>
                  </el-form-item>

                  <el-form-item label="Development status">
                    <div class="flex flex-row items-center">
                      <el-select
                        v-model="step7Form.developmentStatus"
                        filterable
                        placeholder=""
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

                  <el-form-item
                    label="Is part of"
                    :error="isPartOfErrorMessage"
                  >
                    <div class="flex flex-row items-center">
                      <el-input
                        v-model="step7Form.isPartOf"
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
            <div
              class="flex justify-center w-full px-5 space-x-4 form-navigation-buttons"
            >
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

          <div>
            <Vue3Lottie
              :animationData="SaveLottieJSON"
              :width="100"
              :height="100"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Icon } from "@iconify/vue";
import draggable from "vuedraggable";
import { v4 as uuidv4 } from "uuid";
import { ElMessageBox, ElMessage, ElNotification } from "element-plus";
import Vue3Lottie from "vue3-lottie";
// import semver from "semver";
// import _ from "lodash";

import { useDatasetsStore } from "@/store/datasets";

import PillProgressBar from "@/components/ui/PillProgressBar.vue";

import contributorTypesJSON from "@/assets/supplementalFiles/contributorTypes.json";
import repoStatusJSON from "@/assets/supplementalFiles/repoStatus.json";
import codeMetadataJSON from "@/assets/supplementalFiles/codeMetadata.json";

import SaveLottieJSON from "@/assets/lotties/saveLottie.json";

const emailRegex =
  /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

export default {
  name: "CodeCreateMetadata",
  components: {
    draggable,
    Icon,
    PillProgressBar,
    Vue3Lottie,
    // FormCardContent,
  },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      currentStep: 1,
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
      applicationCategoryOptions: codeMetadataJSON.applicationCategoryOptions,
      repoStatusOptions: repoStatusJSON.repoStatus,
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
      step3Form: {
        applicationCategory: "",
        keywords: [],
        funding: {
          code: "",
          organization: "",
        },
      },
      step4Form: {
        codeRepository: "",
        continuousIntegration: "",
        issueTracker: "",
        relatedLinks: [],
      },
      step5Form: {
        programmingLanguage: [],
        runtimePlatform: [],
        operatingSystem: [],
        otherSoftwareRequirements: [],
      },
      step6Form: {
        currentVersion: "",
        currentVersionReleaseDate: "",
        currentVersionDownloadLink: "",
        currentVersionReleaseNotes: "",
      },
      step7Form: {
        referencePublication: "",
        developmentStatus: "",
        isPartOf: "",
      },
      authorsErrorMessage: "",
      contributorsErrorMessage: "",
      isPartOfErrorMessage: "",
      versionErrorMessage: "",
      currentVersionDownloadLinkErrorMessage: "",
      relatedLinksErrorMessage: "",
      issueTrackerErrorMessage: "",
      continuousIntegrationErrorMessage: "",
      codeRepositoryErrorMessage: "",
      invalidStatus: {},
      originalObject: {},
    };
  },
  watch: {
    "step2Form.authors": {
      handler(val) {
        // if (val.length === 0) {
        //   this.authorsErrorMessage = "Please provide at least one author.";
        //   this.invalidStatus.authors = true;
        //   this.$refs.cmForm.validate();
        //   return;
        // } else {
        //   this.authorsErrorMessage = ""; //clear error message
        //   this.invalidStatus.authors = false;
        // }

        if (val.length > 0) {
          for (let author of val) {
            if (author.name === "" || author.affiliation === "") {
              this.authorsErrorMessage =
                "Name and Affiliation for each author is mandatory";
              this.invalidStatus.authors = true;
              this.$refs.s2Form.validate();
              break;
            } else {
              this.authorsErrorMessage = "";
              this.invalidStatus.authors = false;
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

              if (checkDigit === orcid.substr(-1)) {
                this.authorsErrorMessage = "";
                this.invalidStatus.authors = false;
              } else {
                // console.log("invalid orcid");
                this.authorsErrorMessage = "ORCID is not valid";
                this.$refs.s2Form.validate();
                this.invalidStatus.authors = true;
                break;
              }

              // validate email
              if (author.email !== "") {
                if (!emailRegex.test(author.email)) {
                  this.authorsErrorMessage = "Email is not valid";
                  this.$refs.s2Form.validate();
                  this.invalidStatus.authors = true;
                  break;
                } else {
                  this.authorsErrorMessage = "";
                  this.invalidStatus.authors = false;
                }
              }
            }
          }
        } else {
          this.authorsErrorMessage = "";
          this.invalidStatus.authors = false;
        }
      },
      deep: true,
    },
    "step2Form.contributors": {
      handler(val) {
        if (val.length > 0) {
          for (let contributor of val) {
            if (contributor.name === "" || contributor.affiliation === "") {
              this.contributorsErrorMessage =
                "Name and Affiliation for each contributor is mandatory";
              this.invalidStatus.contributors = true;
              this.$refs.s2Form.validate();
              break;
            } else {
              this.contributorsErrorMessage = "";
              this.invalidStatus.contributors = false;
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

              if (checkDigit === orcid.substr(-1)) {
                this.contributorsErrorMessage = "";
                this.invalidStatus.contributors = false;
              } else {
                // console.log("invalid orcid");
                this.contributorsErrorMessage = "ORCID is not valid";
                this.$refs.s2Form.validate();
                this.invalidStatus.contributors = true;
                break;
              }
            }

            // validate email
            if (contributor.email !== "") {
              if (!emailRegex.test(contributor.email)) {
                this.contributorsErrorMessage = "Email is not valid";
                this.$refs.s2Form.validate();
                this.invalidStatus.contributors = true;
                break;
              } else {
                this.contributorsErrorMessage = "";
                this.invalidStatus.contributors = false;
              }
            }

            // validate contributor role
            if (contributor.contributorType === "") {
              this.contributorsErrorMessage =
                "Please select contributor type for each contributor";
              this.invalidStatus.contributors = true;
              this.$refs.s2Form.validate();
              break;
            } else {
              this.contributorsErrorMessage = "";
              this.invalidStatus.contributors = false;
            }
          }
        } else {
          this.contributorsErrorMessage = "";
          this.invalidStatus.contributors = false;
        }
      },
      deep: true,
    },
    // "step6Form.currentVersion": {
    //   handler(val) {
    //     if (val != "" && semver.valid(val) === null) {
    //       this.versionErrorMessage = "Please provide a valid version number.";
    //       this.$refs.cmForm.validate();
    //       this.invalidStatus.version = true;
    //       return;
    //     } else {
    //       this.versionErrorMessage = "";
    //       this.invalidStatus.version = false;
    //     }
    //   },
    //   deep: true,
    // },
    "step7Form.isPartOf": {
      handler(val) {
        if (val != "") {
          let validIdentifier = false;

          const regexp =
            /^(?:(?:https?|ftp):\/\/)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/\S*)?$/;

          if (regexp.test(val)) {
            validIdentifier = true;
          } else {
            validIdentifier = false;
          }

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
    "step4Form.codeRepository": {
      handler(val) {
        if (val != "") {
          let validIdentifier = false;

          const regexp =
            /^(?:(?:https?|ftp):\/\/)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/\S*)?$/;

          if (regexp.test(val)) {
            validIdentifier = true;
          } else {
            validIdentifier = false;
          }

          if (!validIdentifier) {
            this.codeRepositoryErrorMessage = "Please provide a valid URL";
            this.$refs.s4Form.validate();
            this.invalidStatus.codeRepository = true;
            return;
          } else {
            this.codeRepositoryErrorMessage = "";
            this.invalidStatus.codeRepository = false;
          }
        } else {
          this.codeRepositoryErrorMessage = "";
          this.invalidStatus.codeRepository = false;
        }
      },
      deep: true,
    },
    "step4Form.continuousIntegration": {
      handler(val) {
        if (val != "") {
          let validIdentifier = false;

          const regexp =
            /^(?:(?:https?|ftp):\/\/)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/\S*)?$/;

          if (regexp.test(val)) {
            validIdentifier = true;
          } else {
            validIdentifier = false;
          }

          if (!validIdentifier) {
            this.continuousIntegrationErrorMessage =
              "Please provide a valid URL";
            this.$refs.s4Form.validate();
            this.invalidStatus.continuousIntegration = true;
            return;
          } else {
            this.continuousIntegrationErrorMessage = "";
            this.invalidStatus.continuousIntegration = false;
          }
        } else {
          this.continuousIntegrationErrorMessage = "";
          this.invalidStatus.continuousIntegration = false;
        }
      },
      deep: true,
    },
    "step4Form.issueTracker": {
      handler(val) {
        if (val != "") {
          let validIdentifier = false;

          const regexp =
            /^(?:(?:https?|ftp):\/\/)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/\S*)?$/;

          if (regexp.test(val)) {
            validIdentifier = true;
          } else {
            validIdentifier = false;
          }

          if (!validIdentifier) {
            this.issueTrackerErrorMessage = "Please provide a valid URL";
            this.$refs.s4Form.validate();
            this.invalidStatus.issueTracker = true;
            return;
          } else {
            this.issueTrackerErrorMessage = "";
            this.invalidStatus.issueTracker = false;
          }
        } else {
          this.issueTrackerErrorMessage = "";
          this.invalidStatus.issueTracker = false;
        }
      },
      deep: true,
    },
    "step6Form.currentVersionDownloadLink": {
      handler(val) {
        if (val != "") {
          let validIdentifier = false;

          const regexp =
            /^(?:(?:https?|ftp):\/\/)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/\S*)?$/;

          if (regexp.test(val)) {
            validIdentifier = true;
          } else {
            validIdentifier = false;
          }

          if (!validIdentifier) {
            this.currentVersionDownloadLinkErrorMessage =
              "Please provide a valid URL";
            this.$refs.s6Form.validate();
            this.invalidStatus.currentVersionDownloadLink = true;
            return;
          } else {
            this.currentVersionDownloadLinkErrorMessage = "";
            this.invalidStatus.currentVersionDownloadLink = false;
          }
        } else {
          this.currentVersionDownloadLinkErrorMessage = "";
          this.invalidStatus.currentVersionDownloadLink = false;
        }
      },
      deep: true,
    },
    "step4Form.relatedLinks": {
      handler(val) {
        if (val.length > 0) {
          for (let relatedLink of val) {
            if (relatedLink.link !== "") {
              let validIdentifier = false;

              const regexp =
                /^(?:(?:https?|ftp):\/\/)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/\S*)?$/;

              if (regexp.test(relatedLink.link)) {
                validIdentifier = true;
              } else {
                validIdentifier = false;
              }

              if (!validIdentifier) {
                this.relatedLinksErrorMessage = "Please provide a valid URL";
                this.$refs.s4Form.validate();
                this.invalidStatus.relatedLinks = true;
                break;
              } else {
                this.relatedLinksErrorMessage = "";
                this.invalidStatus.relatedLinks = false;
              }
            }
          }
        } else {
          this.relatedLinksErrorMessage = "";
          this.invalidStatus.relatedLinks = false;
        }
      },
      deep: true,
    },
  },
  computed: {
    //check if code workflow is present
    codePresent() {
      if ("type" in this.workflow) {
        return this.workflow.type.includes("Code");
      }
      return false;
    },
    developmentStatus() {
      const that = this;

      function getStatus(repoStatus) {
        return that.repoStatusOptions.find(
          (status) => status.value === repoStatus
        );
      }

      if (
        "developmentStatus" in this.step7Form &&
        this.step7Form.developmentStatus != ""
      ) {
        const status = this.step7Form.developmentStatus;
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
    async prevFormStep() {
      ElNotification.closeAll();
      ElNotification({
        title: "Saving...",
        message: "Saving your current entries",
        position: "bottom-right",
        type: "info",
        duration: 500,
      });

      if (this.currentStep - 1 > 0) {
        this.currentStep--;
      } else {
        this.navigateBack();
      }
    },
    async nextFormStep() {
      const totalSteps = 7;

      if (this.currentStep + 1 > totalSteps) {
        if (!this.checkInvalidStatus) {
          this.navigateToSelectDestination();
        }
      } else {
        this.currentStep++;
      }
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
        ElMessage.error("Please add at least one author.");
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
        ElMessage.error("Please add at least one keyword.");
        return;
      }

      this.$refs["s3Form"].validate(async (valid) => {
        if (valid) {
          await this.saveCurrentEntries();
          this.setCurrentStep(4);
        }
      });
    },
    navigateToStep5FromStep4() {
      this.$refs["s4Form"].validate(async (valid) => {
        if (valid) {
          await this.saveCurrentEntries();
          this.setCurrentStep(5);
        }
      });
    },
    navigateToStep6FromStep5() {
      if (this.step5Form.programmingLanguage.length <= 0) {
        ElMessage.error("Please add at least one programming language.");
        return;
      }
      this.$refs["s5Form"].validate(async (valid) => {
        if (valid) {
          await this.saveCurrentEntries();
          this.setCurrentStep(6);
        }
      });
    },
    navigateToStep7FromStep6() {
      this.$refs["s6Form"].validate(async (valid) => {
        if (valid) {
          await this.saveCurrentEntries();
          this.setCurrentStep(7);
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
    addKeyword() {
      const uuid = uuidv4();
      this.step3Form.keywords.push({
        keyword: "",
        id: uuid,
      });
      this.focusOnElementRef(uuid);
    },
    deleteKeyword(id) {
      this.step3Form.keywords = this.step3Form.keywords.filter((keyword) => {
        return keyword.id !== id;
      });
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
      this.step2Form.contributors = this.step2Form.contributors.filter(
        (contributor) => {
          return contributor.id !== id;
        }
      );
    },
    addRelatedLink() {
      this.step4Form.relatedLinks.push({
        link: "",
        id: uuidv4(),
      });
    },
    deleteRelatedLink(id) {
      this.step4Form.relatedLinks = this.step4Form.relatedLinks.filter(
        (relatedLink) => {
          return relatedLink.id !== id;
        }
      );
    },
    addOtherSoftwareRequirements() {
      this.step5Form.otherSoftwareRequirements.push({
        link: "",
        id: uuidv4(),
      });
    },
    deleteOtherSoftwareRequirements(id) {
      this.step5Form.otherSoftwareRequirements =
        this.step5Form.otherSoftwareRequirements.filter(
          (otherSoftwareRequirement) => {
            return otherSoftwareRequirement.id !== id;
          }
        );
    },
    filterArrayOfObjects(array, key) {
      return array.filter((element) => {
        return element[key] !== "";
      });
    },
    async saveCurrentEntries() {
      ElNotification.closeAll();
      ElNotification({
        title: "Saving...",
        message: "Saving your current entries",
        position: "bottom-right",
        type: "info",
        duration: 500,
      });

      this.dataset.data.general.questions.name = this.step1Form.name;
      this.dataset.data.general.questions.description =
        this.step1Form.description;

      this.step3Form.keywords = this.filterArrayOfObjects(
        this.step3Form.keywords,
        "keyword"
      );

      this.dataset.data.general.questions.keywords = this.step3Form.keywords;
      this.dataset.data.general.questions.authors = this.step2Form.authors;
      this.dataset.data.general.questions.contributors =
        this.step2Form.contributors;
      this.dataset.data.general.questions.funding = this.step3Form.funding;
      this.dataset.data.general.questions.referencePublication =
        this.step7Form.referencePublication;

      this.step4Form.relatedLinks = this.filterArrayOfObjects(
        this.step4Form.relatedLinks,
        "link"
      );

      this.step5Form.otherSoftwareRequirements = this.filterArrayOfObjects(
        this.step5Form.otherSoftwareRequirements,
        "link"
      );

      if (this.codePresent) {
        let codeForm = {};

        codeForm.name = this.step1Form.name;
        codeForm.description = this.step1Form.description;
        codeForm.creationDate = this.step1Form.creationDate;
        codeForm.firstReleaseDate = this.step1Form.firstReleaseDate;

        codeForm.authors = this.step2Form.authors;
        codeForm.contributors = this.step2Form.contributors;

        codeForm.keywords = this.step3Form.keywords;
        codeForm.funding = this.step3Form.funding;
        codeForm.applicationCategory = this.step3Form.applicationCategory;

        codeForm.codeRepository = this.step4Form.codeRepository;
        codeForm.continuousIntegration = this.step4Form.continuousIntegration;
        codeForm.issueTracker = this.step4Form.issueTracker;
        codeForm.relatedLinks = this.step4Form.relatedLinks;

        codeForm.programmingLanguage = this.step5Form.programmingLanguage;
        codeForm.runtimePlatform = this.step5Form.runtimePlatform;
        codeForm.operatingSystem = this.step5Form.operatingSystem;
        codeForm.otherSoftwareRequirements =
          this.step5Form.otherSoftwareRequirements;

        codeForm.currentVersion = this.step6Form.currentVersion;
        codeForm.currentVersionReleaseDate =
          this.step6Form.currentVersionReleaseDate;
        codeForm.currentVersionDownloadLink =
          this.step6Form.currentVersionDownloadLink;
        codeForm.currentVersionReleaseNotes =
          this.step6Form.currentVersionReleaseNotes;

        codeForm.referencePublication = this.step7Form.referencePublication;
        codeForm.developmentStatus = this.step7Form.developmentStatus;
        codeForm.isPartOf = this.step7Form.isPartOf;

        this.dataset.data.Code.questions = codeForm;
      }

      await this.datasetStore.updateCurrentDataset(this.dataset);
      await this.datasetStore.syncDatasets();
    },
    async navigateToSelectDestination(_evt, shouldNavigateBack = false) {
      await this.saveCurrentEntries();

      if (shouldNavigateBack) {
        this.$router.push({
          path: `/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/selectFolder`,
        });
        return;
      }

      const routerPath = `/datasets/${this.dataset.id}/${this.workflowID}/Code/pickLicense`;

      this.$router.push({ path: routerPath });
    },
    navigateBack() {
      let newChanges = false;

      // if (!newChanges && !_.isEqual(this.originalObject.Code, this.codeForm)) {
      //   newChanges = true;
      // }

      if (newChanges) {
        ElMessageBox.confirm(
          "You have some unsaved changes. Do you want to save your edits?",
          "Warning",
          {
            confirmButtonText: "Save and go back",
            cancelButtonText: "Don't save and go back",
            type: "warning",
          }
        )
          .then(() => {
            // save changes
            this.navigateToSelectDestination(true, true);
          })
          .catch(() => {
            // don't save changes
            this.$router.push({
              path: `/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/Code/reviewStandards`,
            });
          });
      } else {
        this.$router.push({
          path: `/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/Code/reviewStandards`,
        });
      }
    },
  },
  mounted() {
    this.$nextTick(async function () {
      this.dataset = await this.datasetStore.getCurrentDataset();

      this.workflow = this.dataset.workflows[this.workflowID];

      this.datasetStore.showProgressBar();
      this.datasetStore.setProgressBarType("zenodo");
      this.datasetStore.setCurrentStep(3);

      if (this.codePresent) {
        if (
          this.dataset.data.Code.questions &&
          Object.keys(this.dataset.data.Code.questions).length !== 0
        ) {
          let codeForm = this.dataset.data.Code.questions;

          this.step1Form.name = codeForm.name;
          this.step1Form.description = codeForm.description;
          this.step1Form.creationDate = codeForm.creationDate;
          this.step1Form.firstReleaseDate = codeForm.firstReleaseDate;

          this.step2Form.authors = codeForm.authors;
          this.step2Form.contributors = codeForm.contributors;

          this.step3Form.keywords = codeForm.keywords;
          this.step3Form.funding = codeForm.funding;
          this.step3Form.applicationCategory = codeForm.applicationCategory;

          this.step4Form.codeRepository = codeForm.codeRepository;
          this.step4Form.continuousIntegration = codeForm.continuousIntegration;
          this.step4Form.issueTracker = codeForm.issueTracker;
          this.step4Form.relatedLinks = codeForm.relatedLinks;

          this.step5Form.programmingLanguage = codeForm.programmingLanguage;
          this.step5Form.runtimePlatform = codeForm.runtimePlatform;
          this.step5Form.operatingSystem = codeForm.operatingSystem;
          this.step5Form.otherSoftwareRequirements =
            codeForm.otherSoftwareRequirements;

          this.step6Form.currentVersion = codeForm.currentVersion;
          this.step6Form.currentVersionReleaseDate =
            codeForm.currentVersionReleaseDate;
          this.step6Form.currentVersionDownloadLink =
            codeForm.currentVersionDownloadLink;
          this.step6Form.currentVersionReleaseNotes =
            codeForm.currentVersionReleaseNotes;

          this.step7Form.referencePublication = codeForm.referencePublication;
          this.step7Form.developmentStatus = codeForm.developmentStatus;
          this.step7Form.isPartOf = codeForm.isPartOf;

          // this.initializeEmptyObjects(this.codeForm, this.codeForm.funding);
          this.initializeEmptyObjects(this.step3Form, this.step3Form.funding);

          this.addIds(this.step3Form.keywords);
          this.addIds(this.step2Form.authors);
          this.addIds(this.step2Form.contributors);

          this.addIds(this.step4Form.relatedLinks);
          this.addIds(this.step5Form.otherSoftwareRequirements);

          // this.originalObject.Code = JSON.parse(JSON.stringify(this.codeForm));
        } else {
          this.step1Form.name = this.dataset.name;
          this.step1Form.description = this.dataset.description;
          // this.originalObject.Code = JSON.parse(JSON.stringify(this.codeForm));
        }
      }
    });
  },
};
</script>
