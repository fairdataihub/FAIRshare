<template>
  <div class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium"> Figshare Metadata </span>

      <span class="mb-2">
        Before we send this data over, Figshare requires some additional information from you. We
        will use this information to create a Figshare article. Please fill out the following form.
      </span>

      <el-form
        :model="zenodoMetadataForm"
        :rules="rulesForZenodoMetadataForm"
        label-width="150px"
        label-position="right"
        size="large"
        ref="zmForm"
        @submit.prevent
      >
        <el-collapse v-model="activeNames">
          <el-collapse-item
            class="zenodo-collapse-item my-1 border-2 border-gray-100"
            name="basicInformation"
          >
            <template #title>
              <div class="flex w-full flex-row items-center justify-between font-inter">
                <p class="px-4 text-sm font-semibold text-blue-500">Basic Information</p>
                <span class="pr-2 text-gray-400"> required </span>
              </div>
            </template>

            <div class="p-4">
              <el-form-item label="Publication date" prop="publicationDate">
                <div class="flex flex-col">
                  <el-date-picker
                    v-model="zenodoMetadataForm.publicationDate"
                    type="date"
                    placeholder="Pick a day"
                    value-format="YYYY-MM-DD"
                  >
                  </el-date-picker>
                  <p class="pt-1 text-xs text-gray-500">
                    In case your upload was already published elsewhere, please use the date of
                    first publication.
                  </p>
                </div>
              </el-form-item>

              <el-form-item label="Title" prop="title">
                <el-input v-model="zenodoMetadataForm.title" type="text"> </el-input>
              </el-form-item>

              <el-form-item label="Authors" prop="authors">
                <draggable
                  tag="div"
                  :list="zenodoMetadataForm.authors"
                  item-key="id"
                  handle=".handle"
                  class="w-full"
                >
                  <template #item="{ element }">
                    <div class="mb-2 flex flex-row justify-between transition-all">
                      <div class="flex w-11/12 flex-row justify-between">
                        <el-input
                          v-model="element.name"
                          type="text"
                          placeholder="Family name, given names"
                          class="h-[40px]"
                        ></el-input>
                        <div class="mx-2"></div>
                        <el-input
                          v-model="element.affiliation"
                          type="text"
                          placeholder="Affiliation"
                          class="h-[40px]"
                        ></el-input>
                        <div class="mx-2"></div>
                        <div class="flex w-full flex-col">
                          <el-input
                            v-model="element.orcid"
                            type="text"
                            placeholder="ORCID (e.g.: 0000-0002-1825-0097)"
                          ></el-input>
                          <span class="mt-1 ml-2 text-xs text-gray-400"> Optional </span>
                        </div>
                        <div class="mx-2"></div>
                      </div>
                      <div class="flex w-1/12 flex-row justify-evenly pt-4">
                        <div
                          class="handle flex items-start justify-center text-gray-400 hover:text-gray-700"
                        >
                          <Icon icon="ic:outline-drag-indicator" />
                        </div>
                        <div class="flex items-start justify-center text-gray-500 transition-all">
                          <el-popconfirm
                            title="Are you sure you want to remove this?"
                            icon-color="red"
                            confirm-button-text="Yes"
                            cancel-button-text="No"
                            @confirm="deleteAuthor(element.id)"
                          >
                            <template #reference>
                              <el-icon class="cursor-pointer hover:text-gray-800">
                                <delete-filled />
                              </el-icon>
                            </template>
                          </el-popconfirm>
                        </div>
                      </div>
                    </div>
                  </template>
                </draggable>

                <div
                  class="flex w-max cursor-pointer items-center text-gray-500 hover:text-black"
                  @click="addAuthor()"
                >
                  <Icon icon="carbon:add" />
                  <span> Add an author </span>
                </div>
              </el-form-item>

              <el-form-item label="Description" prop="description">
                <VuePopper
                  :hover="true"
                  offsetDistance="0"
                  content="Use a description that is easily identifiable. This will
                        be shown in the dataset selection screen and is not part
                        of your submitted metadata."
                  class="mx-0 w-full"
                >
                  <el-input v-model="zenodoMetadataForm.description" type="textarea"></el-input>
                </VuePopper>
              </el-form-item>

              <el-form-item label="Version" prop="version">
                <div class="flex w-full flex-col">
                  <el-input
                    v-model="zenodoMetadataForm.version"
                    type="text"
                    placeholder="1.0.4"
                  ></el-input>
                  <p class="pt-1 text-xs text-gray-500">
                    Optional. Mostly relevant for software and dataset uploads. Any string will be
                    accepted, but semantically-versioned tag is recommended. <br />
                    See
                    <a href="https://semver.org/" target="_blank"> semver.org </a>
                    for more information on semantic versioning.
                  </p>
                </div>
              </el-form-item>

              <el-form-item label="Language">
                <div class="w-full">
                  <el-select
                    v-model="zenodoMetadataForm.language"
                    filterable
                    placeholder="e.g.: 'eng', 'fr' or 'Polish'"
                    class="w-full"
                  >
                    <el-option
                      v-for="item in languageOptions"
                      :key="item.alpha3"
                      :label="`${item.name} - ${item.alpha3}`"
                      :value="item.alpha3"
                    >
                    </el-option>
                  </el-select>
                  <p class="pt-1 text-xs text-gray-500">
                    Optional. Primary language of the record. Start by typing the language's common
                    name in English, or its ISO 639 code (two or three-letter code).
                    <br />
                    See
                    <a
                      href="https://www.loc.gov/standards/iso639-2/php/code_list.php"
                      target="_blank"
                    >
                      ISO 639 language codes list
                    </a>
                    for more information.
                  </p>
                </div>
              </el-form-item>

              <el-form-item label="Keywords">
                <draggable
                  tag="div"
                  :list="zenodoMetadataForm.keywords"
                  item-key="id"
                  handle=".handle"
                  class="w-full"
                >
                  <template #item="{ element }">
                    <div class="mb-2 flex flex-row justify-between transition-all">
                      <div class="flex w-11/12 flex-row justify-between">
                        <el-input v-model="element.keyword" type="text" placeholder=""></el-input>
                        <div class="mx-2"></div>
                      </div>
                      <div class="flex w-1/12 flex-row justify-evenly">
                        <div
                          class="handle flex items-center justify-center text-gray-400 hover:text-gray-700"
                        >
                          <Icon icon="ic:outline-drag-indicator" />
                        </div>
                        <div class="flex items-center justify-center text-gray-500 transition-all">
                          <el-popconfirm
                            title="Are you sure you want to remove this?"
                            icon-color="red"
                            confirm-button-text="Yes"
                            cancel-button-text="No"
                            @confirm="deleteKeyword(element.id)"
                          >
                            <template #reference>
                              <el-icon class="cursor-pointer hover:text-gray-800">
                                <delete-filled />
                              </el-icon>
                            </template>
                          </el-popconfirm>
                        </div>
                      </div>
                    </div>
                  </template>
                </draggable>

                <div
                  class="flex w-max cursor-pointer items-center text-gray-500 hover:text-black"
                  @click="addKeyword()"
                >
                  <Icon icon="carbon:add" />
                  <span> Add a keyword </span>
                </div>
              </el-form-item>

              <el-form-item label="Additional Notes">
                <div class="flex w-full flex-col">
                  <el-input v-model="zenodoMetadataForm.additionalNotes" type="textarea"></el-input>
                  <p class="pt-1 text-xs text-gray-500">Optional.</p>
                </div>
              </el-form-item>
            </div>
          </el-collapse-item>

          <el-collapse-item
            name="license"
            class="zenodo-collapse-item my-1 border-2 border-gray-100"
          >
            <template #title>
              <div class="flex w-full flex-row items-center justify-between font-inter">
                <p class="px-4 text-sm font-semibold text-blue-500">License</p>
                <span class="pr-2 text-gray-400"> required </span>
              </div>
            </template>

            <div class="p-4">
              <el-form-item label="Access right" :required="true">
                <div class="flex flex-col">
                  <el-radio-group v-model="zenodoMetadataForm.license.accessRight">
                    <div class="flex flex-col">
                      <el-radio label="open">
                        <el-icon>
                          <unlock-icon />
                        </el-icon>
                        Open Access
                      </el-radio>
                      <el-radio label="embargoed" disabled>
                        <el-icon> <remove-filled /> </el-icon> Embargoed Access
                      </el-radio>
                      <el-radio label="restricted" disabled>
                        <el-icon>
                          <key-icon />
                        </el-icon>
                        Restricted Access
                      </el-radio>
                      <el-radio label="closed" disabled>
                        <el-icon>
                          <lock-icon />
                        </el-icon>
                        Closed Access
                      </el-radio>
                    </div>
                  </el-radio-group>
                  <p class="pt-1 text-xs text-gray-500">
                    Required. Open access uploads have considerably higher visibility on Zenodo.
                  </p>
                </div>
              </el-form-item>

              <el-form-item label="License" prop="license">
                <el-select
                  v-model="zenodoMetadataForm.license.licenseName"
                  filterable
                  disabled
                  placeholder="Select a license"
                  class="w-full"
                >
                  <el-option
                    v-for="item in licenseOptions"
                    :key="item.licenseId"
                    :label="item.name"
                    :value="item.licenseId"
                  >
                  </el-option>
                </el-select>
                <p class="pt-2 text-xs text-gray-500">
                  Required. Selected license applies to all of your files displayed on the top of
                  the form. <br />
                  If you want to upload some of your files under different licenses, please do so in
                  separate uploads. <br />
                  If you cannot find the license you're looking for, include a relevant LICENSE file
                  in your record and choose one of the
                  <span class="italic"> Other </span> licenses available
                  <span class="italic"> (Other (Open), Other (Attribution) </span>, etc.). <br />
                  The supported licenses in the list are harvested from
                  <a
                    href="https://opendefinition.org/"
                    target="_blank"
                    class="text-blue-500 hover:underline"
                  >
                    opendefinition.org
                  </a>
                  and
                  <a href="https://spdx.org/" target="_blank" class="text-blue-500 hover:underline">
                    spdx.org
                  </a>
                  .
                </p>
              </el-form-item>
            </div>
          </el-collapse-item>

          <el-collapse-item
            name="relatedIdentifiers"
            class="zenodo-collapse-item my-1 border-2 border-gray-100"
          >
            <template #title>
              <div class="flex w-full flex-row items-center justify-between font-inter">
                <p class="px-4 text-sm font-semibold text-blue-500">
                  Related/alternate identifiers
                </p>
                <span class="pr-2 text-gray-400"> recommended </span>
              </div>
            </template>

            <div class="p-4">
              <p class="mb-4 text-xs">
                Specify identifiers of related publications and datasets. Supported identifiers
                include: DOI and URLs.
                <br />
              </p>
              <el-form-item label="Related identifiers" :error="relatedIdentifiersErrorMessage">
                <draggable
                  tag="div"
                  :list="zenodoMetadataForm.relatedIdentifiers"
                  item-key="id"
                  handle=".handle"
                  class="w-full"
                >
                  <template #item="{ element }">
                    <div class="mb-2 flex flex-row justify-between transition-all">
                      <div class="flex w-11/12 flex-row justify-between">
                        <div class="mx-2 w-6/12">
                          <el-input
                            v-model="element.identifier"
                            type="text"
                            placeholder="e.g. 10.1234/foobar.56789"
                          ></el-input>
                        </div>
                        <div class="mx-2 flex w-6/12 flex-row justify-evenly">
                          <el-select
                            v-model="element.relationship"
                            filterable
                            placeholder="Select a relationship"
                          >
                            <el-option
                              v-for="item in relatedIdentifierRelationships"
                              :key="item.value"
                              :label="item.label"
                              :value="item.value"
                            >
                            </el-option>
                          </el-select>
                          <div class="mx-2 block"></div>
                          <div class="flex flex-col">
                            <el-select
                              v-model="element.resourceType"
                              placeholder="Select a resource type"
                            >
                              <el-option-group
                                v-for="group in relatedIdentifierTypes"
                                :key="group.label"
                                :label="group.label"
                                v-show="group.options"
                              >
                                <el-option
                                  v-for="item in group.options"
                                  :key="item.value"
                                  :label="item.label"
                                  :value="item.value"
                                >
                                </el-option>
                              </el-option-group>
                            </el-select>
                            <p class="pt-2 text-xs text-gray-500">
                              Optional. Resource type of the related identifier.
                            </p>
                          </div>
                        </div>
                      </div>
                      <div class="flex w-1/12 flex-row justify-evenly pt-4">
                        <div
                          class="handle flex items-start justify-center text-gray-400 hover:text-gray-700"
                        >
                          <Icon icon="ic:outline-drag-indicator" />
                        </div>
                        <div class="flex items-start justify-center text-gray-500 transition-all">
                          <el-popconfirm
                            title="Are you sure you want to remove this?"
                            icon-color="red"
                            confirm-button-text="Yes"
                            cancel-button-text="No"
                            @confirm="deleteRelatedIdentifier(element.id)"
                          >
                            <template #reference>
                              <el-icon class="cursor-pointer hover:text-gray-800">
                                <delete-filled />
                              </el-icon>
                            </template>
                          </el-popconfirm>
                        </div>
                      </div>
                    </div>
                  </template>
                </draggable>

                <div
                  class="flex w-max cursor-pointer items-center text-gray-500 hover:text-black"
                  @click="addRelatedIdentifier()"
                >
                  <Icon icon="carbon:add" />
                  <span> Add a related or alternate identifier </span>
                </div>
              </el-form-item>
            </div>
          </el-collapse-item>

          <el-collapse-item
            name="contributors"
            class="zenodo-collapse-item my-1 border-2 border-gray-100"
          >
            <template #title>
              <div class="flex w-full flex-row items-center justify-between font-inter">
                <p class="px-4 text-sm font-semibold text-blue-500">Contributors</p>
                <span class="pr-2 text-gray-400"> optional </span>
              </div>
            </template>

            <div class="p-4">
              <el-form-item label="Contributors" prop="contributors">
                <draggable
                  tag="div"
                  :list="zenodoMetadataForm.contributors"
                  item-key="id"
                  handle=".handle"
                  class="w-full"
                >
                  <template #item="{ element }">
                    <div class="mb-2 flex flex-row justify-between transition-all">
                      <div class="flex w-11/12 flex-row justify-between">
                        <div class="mx-2 md:w-2/12 lg:w-3/12 xl:w-max">
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
                        <div class="w-3/12">
                          <el-input
                            v-model="element.name"
                            type="text"
                            placeholder="Family Name, Given Name"
                          ></el-input>
                        </div>
                        <div class="mx-2 w-3/12">
                          <el-input
                            v-model="element.affiliation"
                            type="text"
                            placeholder="Affiliation"
                          ></el-input>
                        </div>
                        <div class="mx-2 w-3/12">
                          <div class="flex w-full flex-col">
                            <el-input
                              v-model="element.orcid"
                              type="text"
                              placeholder="ORCID (e.g.: 0000-0002-1825-0097)"
                            ></el-input>
                            <span class="mt-1 ml-2 text-xs text-gray-400"> Optional </span>
                          </div>
                        </div>
                      </div>
                      <div class="flex w-1/12 flex-row justify-evenly pt-4">
                        <div
                          class="handle flex items-start justify-center text-gray-400 hover:text-gray-700"
                        >
                          <Icon icon="ic:outline-drag-indicator" />
                        </div>
                        <div class="flex items-start justify-center text-gray-500 transition-all">
                          <el-popconfirm
                            title="Are you sure you want to remove this?"
                            icon-color="red"
                            confirm-button-text="Yes"
                            cancel-button-text="No"
                            @confirm="deleteContributor(element.id)"
                          >
                            <template #reference>
                              <el-icon class="cursor-pointer hover:text-gray-800">
                                <delete-filled />
                              </el-icon>
                            </template>
                          </el-popconfirm>
                        </div>
                      </div>
                    </div>
                  </template>
                </draggable>

                <div
                  class="flex w-max cursor-pointer items-center text-gray-500 hover:text-black"
                  @click="addContributor()"
                >
                  <Icon icon="carbon:add" />
                  <span> Add a contributor </span>
                </div>
              </el-form-item>
            </div>
          </el-collapse-item>

          <el-collapse-item
            name="references"
            class="zenodo-collapse-item my-1 border-2 border-gray-100"
          >
            <template #title>
              <div class="flex w-full flex-row items-center justify-between font-inter">
                <p class="px-4 text-sm font-semibold text-blue-500">References</p>
                <span class="pr-2 text-gray-400"> optional </span>
              </div>
            </template>

            <div class="p-4">
              <el-form-item label="References">
                <draggable
                  tag="div"
                  :list="zenodoMetadataForm.references"
                  item-key="id"
                  handle=".handle"
                  class="w-full"
                >
                  <template #item="{ element }">
                    <div class="mb-2 flex flex-row justify-between transition-all">
                      <div class="flex w-11/12 flex-row justify-between">
                        <el-input
                          v-model="element.reference"
                          type="text"
                          placeholder="e.g.: Cranmer, Kyle et al. (2014). Decouple software associated to arXiv:1401.0080."
                        ></el-input>
                        <div class="mx-2"></div>
                      </div>
                      <div class="flex w-1/12 flex-row justify-evenly pt-4">
                        <div
                          class="handle flex items-start justify-center text-gray-400 hover:text-gray-700"
                        >
                          <Icon icon="ic:outline-drag-indicator" />
                        </div>
                        <div class="flex items-start justify-center text-gray-500 transition-all">
                          <el-popconfirm
                            title="Are you sure you want to remove this?"
                            icon-color="red"
                            confirm-button-text="Yes"
                            cancel-button-text="No"
                            @confirm="deleteReference(element.id)"
                          >
                            <template #reference>
                              <el-icon class="cursor-pointer hover:text-gray-800">
                                <delete-filled />
                              </el-icon>
                            </template>
                          </el-popconfirm>
                        </div>
                      </div>
                    </div>
                  </template>
                </draggable>

                <div
                  class="flex w-max cursor-pointer items-center text-gray-500 hover:text-black"
                  @click="addReference()"
                >
                  <Icon icon="carbon:add" />
                  <span> Add a reference </span>
                </div>
              </el-form-item>
            </div>
          </el-collapse-item>

          <el-collapse-item
            name="journal"
            class="zenodo-collapse-item my-1 border-2 border-gray-100"
          >
            <template #title>
              <div class="flex w-full flex-row items-center justify-between font-inter">
                <p class="px-4 text-sm font-semibold text-blue-500">Journal</p>
                <span class="pr-2 text-gray-400"> optional </span>
              </div>
            </template>

            <div class="p-4">
              <el-form-item label="Journal title">
                <div class="flex w-full flex-col">
                  <el-input v-model="zenodoMetadataForm.journal.title" type="text"></el-input>
                  <p class="pt-2 text-xs text-gray-500">Optional.</p>
                </div>
              </el-form-item>
              <el-form-item label="Volume">
                <div class="flex w-full flex-col">
                  <el-input v-model="zenodoMetadataForm.journal.volume" type="text"></el-input>
                  <p class="pt-2 text-xs text-gray-500">Optional.</p>
                </div>
              </el-form-item>
              <el-form-item label="Issue">
                <div class="flex w-full flex-col">
                  <el-input v-model="zenodoMetadataForm.journal.issue" type="text"></el-input>
                  <p class="pt-2 text-xs text-gray-500">Optional.</p>
                </div>
              </el-form-item>
              <el-form-item label="Pages">
                <div class="flex w-full flex-col">
                  <el-input v-model="zenodoMetadataForm.journal.pages" type="text"></el-input>
                  <p class="pt-2 text-xs text-gray-500">Optional.</p>
                </div>
              </el-form-item>
            </div>
          </el-collapse-item>

          <el-collapse-item
            name="conference"
            class="zenodo-collapse-item my-1 border-2 border-gray-100"
          >
            <template #title>
              <div class="flex w-full flex-row items-center justify-between font-inter">
                <p class="px-4 text-sm font-semibold text-blue-500">Conference</p>
                <span class="pr-2 text-gray-400"> optional </span>
              </div>
            </template>

            <div class="p-4">
              <el-form-item label="Conference title">
                <div class="flex w-full flex-col">
                  <el-input v-model="zenodoMetadataForm.conference.title" type="text"></el-input>
                  <p class="pt-2 text-xs text-gray-500">Optional.</p>
                </div>
              </el-form-item>
              <el-form-item label="Acronym">
                <div class="flex w-full flex-col">
                  <el-input v-model="zenodoMetadataForm.conference.acronym" type="text"></el-input>
                  <p class="pt-2 text-xs text-gray-500">Optional.</p>
                </div>
              </el-form-item>
              <el-form-item label="Dates">
                <div class="flex w-full flex-col">
                  <el-date-picker
                    v-model="zenodoMetadataForm.conference.dates"
                    type="daterange"
                    range-separator="-"
                    start-placeholder="Start date"
                    end-placeholder="End date"
                    size="large"
                    value-format="YYYY-MM-DD"
                  >
                  </el-date-picker>
                  <p class="pt-2 text-xs text-gray-500">Optional.</p>
                </div>
              </el-form-item>
              <el-form-item label="Place">
                <div class="flex w-full flex-col">
                  <el-input
                    v-model="zenodoMetadataForm.conference.place"
                    type="text"
                    placeholder="e.g. city, country"
                  ></el-input>
                  <p class="pt-2 text-xs text-gray-500">Optional.</p>
                </div>
              </el-form-item>
              <el-form-item label="Website">
                <div class="flex w-full flex-col">
                  <el-input
                    v-model="zenodoMetadataForm.conference.website"
                    type="text"
                    placeholder="e.g. http://zenodo.org"
                  ></el-input>
                  <p class="pt-2 text-xs text-gray-500">Optional.</p>
                </div>
              </el-form-item>
              <el-form-item label="Session">
                <div class="flex w-full flex-col">
                  <el-input
                    v-model="zenodoMetadataForm.conference.session"
                    type="text"
                    placeholder="e.g. VI"
                  ></el-input>
                  <p class="pt-2 text-xs text-gray-500">
                    Optional. Number of session within the conference.
                  </p>
                </div>
              </el-form-item>
              <el-form-item label="Part">
                <div class="flex w-full flex-col">
                  <el-input
                    v-model="zenodoMetadataForm.conference.part"
                    type="text"
                    placeholder="e.g. 1"
                  ></el-input>
                  <p class="pt-2 text-xs text-gray-500">
                    Optional. Number of part within a session.
                  </p>
                </div>
              </el-form-item>
            </div>
          </el-collapse-item>

          <el-collapse-item
            name="bookReportChapter"
            class="zenodo-collapse-item my-1 border-2 border-gray-100"
          >
            <template #title>
              <div class="flex w-full flex-row items-center justify-between font-inter">
                <p class="px-4 text-sm font-semibold text-blue-500">Book/Report/Chapter</p>
                <span class="pr-2 text-gray-400"> optional </span>
              </div>
            </template>

            <div class="p-4">
              <p class="mb-4 text-sm">For parts of books and reports. <br /></p>
              <el-form-item label="Publisher">
                <div class="flex w-full flex-col">
                  <el-input
                    v-model="zenodoMetadataForm.bookReportChapter.publisher"
                    type="text"
                  ></el-input>
                  <p class="pt-2 text-xs text-gray-500">Optional.</p>
                </div>
              </el-form-item>
              <el-form-item label="Place">
                <div class="flex w-full flex-col">
                  <el-input
                    v-model="zenodoMetadataForm.bookReportChapter.place"
                    type="text"
                    placeholder="e.g. city, country"
                  ></el-input>
                  <p class="pt-2 text-xs text-gray-500">Optional.</p>
                </div>
              </el-form-item>
              <el-form-item label="ISBN">
                <div class="flex w-full flex-col">
                  <el-input
                    v-model="zenodoMetadataForm.bookReportChapter.isbn"
                    type="text"
                    placeholder="e.g. 0-06-251587-X"
                  ></el-input>
                  <p class="pt-2 text-xs text-gray-500">Optional.</p>
                </div>
              </el-form-item>
              <el-form-item label="Book title">
                <div class="flex w-full flex-col">
                  <el-input
                    v-model="zenodoMetadataForm.bookReportChapter.title"
                    type="text"
                  ></el-input>
                  <p class="pt-2 text-xs text-gray-500">
                    Optional. Title of the book or report which this upload is part of.
                  </p>
                </div>
              </el-form-item>
              <el-form-item label="Pages">
                <div class="flex w-full flex-col">
                  <el-input
                    v-model="zenodoMetadataForm.bookReportChapter.pages"
                    type="text"
                  ></el-input>
                  <p class="pt-2 text-xs text-gray-500">Optional.</p>
                </div>
              </el-form-item>
            </div>
          </el-collapse-item>

          <el-collapse-item
            name="thesis"
            class="zenodo-collapse-item my-1 border-2 border-gray-100"
          >
            <template #title>
              <div class="flex w-full flex-row items-center justify-between font-inter">
                <p class="px-4 text-sm font-semibold text-blue-500">Thesis</p>
                <span class="pr-2 text-gray-400"> optional </span>
              </div>
            </template>

            <div class="p-4">
              <el-form-item label="Awarding university">
                <div class="flex w-full flex-col">
                  <el-input
                    v-model="zenodoMetadataForm.thesis.awardingUniversity"
                    type="text"
                  ></el-input>
                  <p class="pt-2 text-xs text-gray-500">Optional.</p>
                </div>
              </el-form-item>

              <el-form-item label="Supervisors">
                <draggable
                  tag="div"
                  :list="zenodoMetadataForm.thesis.supervisors"
                  item-key="id"
                  handle=".handle"
                  class="w-full"
                >
                  <template #item="{ element }">
                    <div class="mb-2 flex flex-row justify-between transition-all">
                      <div class="flex w-11/12 flex-row justify-between">
                        <el-input
                          v-model="element.name"
                          type="text"
                          placeholder="Family name, given names"
                        ></el-input>
                        <div class="mx-2"></div>
                        <el-input
                          v-model="element.affiliation"
                          type="text"
                          placeholder="Affiliation"
                        ></el-input>
                        <div class="mx-2"></div>
                        <div class="flex w-full flex-col">
                          <el-input
                            v-model="element.orcid"
                            type="text"
                            placeholder="ORCID (e.g.: 0000-0002-1825-0097)"
                          ></el-input>
                          <span class="mt-1 ml-2 text-xs text-gray-400"> Optional </span>
                        </div>
                        <div class="mx-2"></div>
                      </div>
                      <div class="flex w-1/12 flex-row justify-evenly pt-4">
                        <div
                          class="handle flex items-start justify-center text-gray-400 hover:text-gray-700"
                        >
                          <Icon icon="ic:outline-drag-indicator" />
                        </div>
                        <div class="flex items-start justify-center text-gray-500 transition-all">
                          <el-popconfirm
                            title="Are you sure you want to remove this?"
                            icon-color="red"
                            confirm-button-text="Yes"
                            cancel-button-text="No"
                            @confirm="deleteSupervisor(element.id)"
                          >
                            <template #reference>
                              <el-icon class="cursor-pointer hover:text-gray-800">
                                <delete-filled />
                              </el-icon>
                            </template>
                          </el-popconfirm>
                        </div>
                      </div>
                    </div>
                  </template>
                </draggable>

                <div
                  class="flex w-max cursor-pointer items-center text-gray-500 hover:text-black"
                  @click="addSupervisor()"
                >
                  <Icon icon="carbon:add" />
                  <span> Add a supervisor </span>
                </div>
              </el-form-item>
            </div>
          </el-collapse-item>

          <el-collapse-item
            name="subjects"
            class="zenodo-collapse-item my-1 border-2 border-gray-100"
          >
            <template #title>
              <div class="flex w-full flex-row items-center justify-between font-inter">
                <p class="px-4 text-sm font-semibold text-blue-500">Subjects</p>
                <span class="pr-2 text-gray-400"> optional </span>
              </div>
            </template>

            <div class="p-4">
              <p class="mb-4 text-xs">
                Specify subjects from a taxonomy or controlled vocabulary. Each term must be
                uniquely identified (e.g. a URL). For free form text, use the keywords field in
                basic information section.
                <br />
              </p>
              <el-form-item label="Subjects" prop="subjects">
                <draggable
                  tag="div"
                  :list="zenodoMetadataForm.subjects"
                  item-key="id"
                  handle=".handle"
                  class="w-full"
                >
                  <template #item="{ element }">
                    <div class="mb-2 flex flex-row justify-between transition-all">
                      <div class="flex w-11/12 flex-row justify-between">
                        <el-input v-model="element.term" type="text" placeholder="Term"></el-input>
                        <div class="mx-2"></div>
                        <el-input
                          v-model="element.identifier"
                          type="text"
                          placeholder="Identifier"
                        ></el-input>
                        <div class="mx-2"></div>
                      </div>
                      <div class="flex w-1/12 flex-row justify-evenly pt-4">
                        <div
                          class="handle flex items-start justify-center text-gray-400 hover:text-gray-700"
                        >
                          <Icon icon="ic:outline-drag-indicator" />
                        </div>
                        <div class="flex items-start justify-center text-gray-500 transition-all">
                          <el-popconfirm
                            title="Are you sure you want to remove this?"
                            icon-color="red"
                            confirm-button-text="Yes"
                            cancel-button-text="No"
                            @confirm="deleteSubject(element.id)"
                          >
                            <template #reference>
                              <el-icon class="cursor-pointer hover:text-gray-800">
                                <delete-filled />
                              </el-icon>
                            </template>
                          </el-popconfirm>
                        </div>
                      </div>
                    </div>
                  </template>
                </draggable>

                <div
                  class="flex w-max cursor-pointer items-center text-gray-500 hover:text-black"
                  @click="addSubject()"
                >
                  <Icon icon="carbon:add" />
                  <span> Add a subject </span>
                </div>
              </el-form-item>
            </div>
          </el-collapse-item>
        </el-collapse>
      </el-form>

      <div class="flex w-full flex-row justify-center space-x-4 py-6">
        <button class="primary-plain-button" @click="navigateBack">
          <el-icon><d-arrow-left /></el-icon> Back
        </button>

        <button class="primary-button" @click="addZenodoMetadata" :disabled="checkInvalidStatus">
          Continue <el-icon> <d-arrow-right /> </el-icon>
        </button>

        <warning-confirm
          ref="warningConfirm"
          title="Warning"
          @messageConfirmed="confirmNavigateBackSave('ok')"
          @messageCancel="confirmNavigateBackSave('cancel')"
          confirmButtonText="Save and go back"
          cancelButtonText="Don't save and go back"
        >
          <p class="text-center text-base text-gray-500">
            You have some unsaved changes. Do you want to save your edits?
          </p>
        </warning-confirm>
      </div>
    </div>
    <fade-transition>
      <div class="fixed bottom-1 right-2" v-if="savingSpinner">
        <Vue3Lottie
          :animationData="$helix_spinner"
          :width="60"
          :height="60"
          :loop="1"
          @onComplete="savingSpinner = false"
        />
      </div>
      <div v-else>
        <app-docs-link url="curate-and-share/add-zenodo-metadata" position="bottom-4" />
      </div>
    </fade-transition>
  </div>
</template>

<script>
import { Icon } from "@iconify/vue";
import draggable from "vuedraggable";
import { v4 as uuidv4 } from "uuid";
import semver from "semver";
import doiRegex from "doi-regex";
import { ElMessage } from "element-plus";
import validator from "validator";

import _ from "lodash";

import { useDatasetsStore } from "@/store/datasets";
import licensesJSON from "@/assets/supplementalFiles/licenses.json";
import contributorTypesJSON from "@/assets/supplementalFiles/contributorTypes.json";
import zenodoMetadataOptions from "@/assets/supplementalFiles/zenodoMetadataOptions.json";
import languagesJSON from "@/assets/supplementalFiles/zenodoLanguages.json";

export default {
  name: "FigshareMetadata",
  components: {
    draggable,
    Icon,
  },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      dataset: {},
      workflowID: this.$route.params.workflowID,
      workflow: {},
      loading: true,
      savingSpinner: true,
      activeNames: [],
      drag: true,
      licenseOptions: licensesJSON.licenses,
      languageOptions: languagesJSON.languages,
      relatedIdentifierRelationships: zenodoMetadataOptions.relatedIdentifierRelationships,
      relatedIdentifierTypes: zenodoMetadataOptions.relatedIdentifierTypes,
      contributorTypes: contributorTypesJSON.contributorTypes,
      zenodoMetadataForm: zenodoMetadataOptions.defaultForm,
      relatedIdentifiersErrorMessage: "",
      invalidStatus: {},
      rulesForZenodoMetadataForm: {
        publicationDate: [
          {
            required: true,
            message: "Publication date is required",
            trigger: "blur",
          },
        ],
        title: [
          {
            required: true,
            message: "Required.",
            trigger: "blur",
          },
        ],
        authors: [
          {
            required: true,
            validator: this.authorValidator,
            trigger: "blur",
          },
        ],
        description: [
          {
            required: true,
            message: "Required.",
            trigger: "blur",
          },
        ],
        license: [
          {
            required: true,
            message: "Required. Selected license applies to all of your files in the dataset.",
            trigger: "change",
          },
        ],
        version: [
          {
            required: false,
            validator: this.versionValidator,
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
        subjects: [
          {
            required: false,
            validator: this.subjectValidator,
            trigger: "blur",
          },
        ],
      },
      originalObject: {},
    };
  },
  computed: {
    dragOptions() {
      return {
        animation: 200,
        disabled: false,
      };
    },
    checkInvalidStatus() {
      if (this.$refs.zmForm) {
        this.$refs.zmForm.validate();
      }

      if (this.invalidStatus == {}) {
        return true;
      }

      for (const key in this.invalidStatus) {
        if (this.invalidStatus[key]) {
          return true;
        }
      }

      return false;
    },
  },
  methods: {
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

    subjectValidator(_rule, value, callback) {
      if (value.length > 0) {
        for (let subject of value) {
          if (subject.term === undefined || subject.term.trim() === "") {
            callback(new Error("Please provide a valid and identifiable subject"));
            return;
          }

          const validIdentifier = validator.isURL(subject.identifier);

          if (!validIdentifier) {
            callback(
              new Error(
                "Please provide a valid identifier. Your identifier has to be in the form of a URL"
              )
            );
            return;
          }
        }
      }
      callback();
    },
    addSubject() {
      this.zenodoMetadataForm.subjects.push({
        term: "",
        identifier: "",
        id: uuidv4(),
      });
    },
    deleteSubject(id) {
      this.zenodoMetadataForm.subjects = this.zenodoMetadataForm.subjects.filter((subject) => {
        return subject.id !== id;
      });
    },

    authorValidator(_rule, value, callback) {
      if (value.length > 0) {
        for (let author of value) {
          if (
            author.name === undefined ||
            author.name.trim() === "" ||
            author.affiliation === undefined ||
            author.affiliation.trim() === ""
          ) {
            callback(new Error("Name and Affiliation for each author is mandatory"));
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
              callback(new Error("ORCID is not valid"));
            }
          }
        }
      } else {
        callback(new Error("Please provide at least one author"));
        return;
      }
      callback();
    },
    addAuthor() {
      this.zenodoMetadataForm.authors.push({
        name: "",
        affiliation: "",
        orcid: "",
        id: uuidv4(),
      });
    },
    deleteAuthor(id) {
      this.zenodoMetadataForm.authors = this.zenodoMetadataForm.authors.filter((author) => {
        return author.id !== id;
      });
    },

    addKeyword() {
      this.zenodoMetadataForm.keywords.push({
        keyword: "",
        id: uuidv4(),
      });
    },
    deleteKeyword(id) {
      this.zenodoMetadataForm.keywords = this.zenodoMetadataForm.keywords.filter((keyword) => {
        return keyword.id !== id;
      });
    },
    addRelatedIdentifier() {
      this.zenodoMetadataForm.relatedIdentifiers.push({
        identifier: "",
        relationship: "",
        resourceType: "",
        id: uuidv4(),
      });
    },
    deleteRelatedIdentifier(id) {
      this.zenodoMetadataForm.relatedIdentifiers =
        this.zenodoMetadataForm.relatedIdentifiers.filter((relatedIdentifier) => {
          return relatedIdentifier.id !== id;
        });
    },

    contributorValidator(_rule, value, callback) {
      if (value.length > 0) {
        for (let contributor of value) {
          if (
            contributor.name === undefined ||
            contributor.name.trim() === "" ||
            contributor.affiliation === undefined ||
            contributor.affiliation.trim() === ""
          ) {
            callback(new Error("Name and Affiliation for each contributor is mandatory"));
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

          console.log(contributor.contributorType, "+", contributor);
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
      this.zenodoMetadataForm.contributors.push({
        contributorType: "",
        name: "",
        affiliation: "",
        orcid: "",
        id: uuidv4(),
      });
    },
    deleteContributor(id) {
      this.zenodoMetadataForm.contributors = this.zenodoMetadataForm.contributors.filter(
        (contributor) => {
          return contributor.id !== id;
        }
      );
      this.$refs.zmForm.validate();
    },

    addReference() {
      this.zenodoMetadataForm.references.push({
        reference: "",
        id: uuidv4(),
      });
    },
    deleteReference(id) {
      this.zenodoMetadataForm.references = this.zenodoMetadataForm.references.filter(
        (reference) => {
          return reference.id !== id;
        }
      );
    },
    addSupervisor() {
      this.zenodoMetadataForm.thesis.supervisors.push({
        name: "",
        affiliation: "",
        orcid: "",
        id: uuidv4(),
      });
    },
    deleteSupervisor(id) {
      this.zenodoMetadataForm.thesis.supervisors =
        this.zenodoMetadataForm.thesis.supervisors.filter((supervisor) => {
          return supervisor.name !== id;
        });
    },

    versionValidator(_rule, value, callback) {
      if (value != "" && semver.valid(semver.coerce(value)) === null) {
        callback(new Error("Please provide a valid version number"));
        return;
      } else {
        callback();
      }
    },

    addZenodoMetadata(_evt, shouldNavigateBack = false) {
      if (this.zenodoMetadataForm.authors.length == 0) {
        ElMessage.error("Please add at least one author.");
      }

      if (this.zenodoMetadataForm.publicationDate === "") {
        ElMessage.error("Please add a publication date.");
        return;
      }

      if (this.zenodoMetadataForm.license.licenseName === "") {
        ElMessage.error("Please select a license.");
        return;
      }

      this.workflow = this.dataset.workflows[this.workflowID];

      this.workflow.expandOptions = [];

      this.workflow.destination.zenodo.questions = this.zenodoMetadataForm;
      this.datasetStore.updateCurrentDataset(this.dataset);
      this.datasetStore.syncDatasets();

      if (shouldNavigateBack) {
        // console.log("shouldNavigateBack");
        this.$router.push(
          `/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/selectDestination`
        );
        return;
      }

      let routerPath = "";

      if ("source" in this.workflow) {
        if (this.workflow.source.type === "github") {
          routerPath = `/datasets/${this.datasetID}/${this.workflowID}/github/zenodoConnection`;
        }
        if (this.workflow.source.type === "local") {
          routerPath = `/datasets/${this.datasetID}/${this.workflowID}/zenodo/accessToken`;
        }
      } else {
        routerPath = `/datasets/${this.datasetID}/${this.workflowID}/zenodo/accessToken`;
      }

      // const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/zenodo/accessToken`;
      this.$router.push({ path: routerPath });

      //validate first
    },
    prefillZenodoQuestions() {
      if (
        "questions" in this.dataset.data.general &&
        Object.keys(this.dataset.data.general.questions).length !== 0
      ) {
        const generalForm = this.dataset.data.general.questions;
        // console.log(generalForm);

        let date = new Date();

        this.zenodoMetadataForm.publicationDate = `${date.getFullYear()}-${(date.getMonth() + 1)
          .toString()
          .padStart(2, "0")}-${date.getDate().toString().padStart(2, "0")}`;

        if ("name" in generalForm) {
          this.zenodoMetadataForm.title = generalForm.name;
        }

        if ("description" in generalForm) {
          this.zenodoMetadataForm.description = generalForm.description;
        }

        if ("keywords" in generalForm) {
          this.zenodoMetadataForm.keywords = [];
          generalForm.keywords.forEach((element) => {
            this.zenodoMetadataForm.keywords.push({
              keyword: element.keyword,
              id: uuidv4(),
            });
          });
        }

        if ("license" in generalForm) {
          this.zenodoMetadataForm.license.licenseName = generalForm.license;
        }

        if ("authors" in generalForm) {
          let authors = generalForm.authors;
          let newAuthors = [];
          authors.forEach((author) => {
            let authorName = "";

            if (author.familyName) {
              authorName = author.familyName + ", " + author.givenName;
            } else {
              authorName = author.givenName;
            }

            let newAuthor = {
              name: authorName,
              affiliation: author.affiliation,
              orcid: author.orcid,
              id: uuidv4(),
            };
            newAuthors.push(newAuthor);
          });
          this.zenodoMetadataForm.authors = newAuthors;
        }

        if ("contributors" in generalForm) {
          let contributors = generalForm.contributors;
          let newContributors = [];
          contributors.forEach((contributor) => {
            let newContributor = {
              contributorType: contributor.contributorType,
              name: contributor.familyName + ", " + contributor.givenName,
              affiliation: contributor.affiliation,
              orcid: contributor.orcid,
              id: uuidv4(),
            };
            newContributors.push(newContributor);
          });
          this.zenodoMetadataForm.contributors = newContributors;

          this.activeNames.indexOf("contributors") === -1
            ? this.activeNames.push("contributors")
            : null;
        }

        if (
          "newVersion" in this.workflow.destination.zenodo &&
          this.workflow.destination.zenodo.newVersion
        ) {
          if (this.zenodoMetadataForm.keywords.length == 0) {
            if ("keywords" in this.workflow.destination.zenodo.selectedDeposition.metadata) {
              this.workflow.destination.zenodo.selectedDeposition.metadata.keywords.forEach(
                (keyword) => {
                  this.zenodoMetadataForm.keywords.push({
                    keyword,
                    id: uuidv4(),
                  });
                }
              );
            }
          }

          if (this.zenodoMetadataForm.authors.length == 0) {
            if ("creators" in this.workflow.destination.zenodo.selectedDeposition.metadata) {
              this.workflow.destination.zenodo.selectedDeposition.metadata.creators.forEach(
                ({ name, affiliation, orcid }) => {
                  this.zenodoMetadataForm.authors.push({
                    name,
                    affiliation,
                    orcid,
                    id: uuidv4(),
                  });
                }
              );
            }
          }

          if (this.zenodoMetadataForm.contributors.length == 0) {
            if ("contributors" in this.workflow.destination.zenodo.selectedDeposition.metadata) {
              this.workflow.destination.zenodo.selectedDeposition.metadata.contributors.forEach(
                ({ name, type, affiliation, orcid }) => {
                  this.zenodoMetadataForm.contributors.push({
                    name,
                    contributorType: type,
                    affiliation,
                    orcid,
                    id: uuidv4(),
                  });
                }
              );

              this.activeNames.indexOf("contributors") === -1
                ? this.activeNames.push("contributors")
                : null;
            }
          }

          if ("notes" in this.workflow.destination.zenodo.selectedDeposition.metadata) {
            this.zenodoMetadataForm.additionalNotes =
              this.workflow.destination.zenodo.selectedDeposition.metadata.notes;
          }

          if (
            "related_identifiers" in this.workflow.destination.zenodo.selectedDeposition.metadata
          ) {
            this.zenodoMetadataForm.relatedIdentifiers = [];
            this.workflow.destination.zenodo.selectedDeposition.metadata.related_identifiers.forEach(
              ({ identifier, relation, resource_type }) => {
                this.zenodoMetadataForm.relatedIdentifiers.push({
                  identifier,
                  relationship: relation,
                  resourceType: resource_type,
                  id: uuidv4(),
                });
              }
            );

            this.activeNames.indexOf("relatedIdentifiers") === -1
              ? this.activeNames.push("relatedIdentifiers")
              : null;
          }

          if ("references" in this.workflow.destination.zenodo.selectedDeposition.metadata) {
            this.zenodoMetadataForm.references = [];
            this.workflow.destination.zenodo.selectedDeposition.metadata.references.forEach(
              (reference) => {
                this.zenodoMetadataForm.references.push({
                  reference,
                  id: uuidv4(),
                });
              }
            );

            this.activeNames.indexOf("references") === -1
              ? this.activeNames.push("references")
              : null;
          }

          if ("version" in this.workflow.destination.zenodo.selectedDeposition.metadata) {
            this.zenodoMetadataForm.version =
              this.workflow.destination.zenodo.selectedDeposition.metadata.version;
          }
          if ("language" in this.workflow.destination.zenodo.selectedDeposition.metadata) {
            this.zenodoMetadataForm.language =
              this.workflow.destination.zenodo.selectedDeposition.metadata.language;
          }

          if ("journal_title" in this.workflow.destination.zenodo.selectedDeposition.metadata) {
            this.zenodoMetadataForm.journal.title =
              this.workflow.destination.zenodo.selectedDeposition.metadata.journal_title;

            this.activeNames.indexOf("journal") === -1 ? this.activeNames.push("journal") : null;
          }
          if ("journal_volume" in this.workflow.destination.zenodo.selectedDeposition.metadata) {
            this.zenodoMetadataForm.journal.volume =
              this.workflow.destination.zenodo.selectedDeposition.metadata.journal_volume;

            this.activeNames.indexOf("journal") === -1 ? this.activeNames.push("journal") : null;
          }
          if ("journal_issue" in this.workflow.destination.zenodo.selectedDeposition.metadata) {
            this.zenodoMetadataForm.journal.issue =
              this.workflow.destination.zenodo.selectedDeposition.metadata.journal_issue;

            this.activeNames.indexOf("journal") === -1 ? this.activeNames.push("journal") : null;
          }
          if ("journal_pages" in this.workflow.destination.zenodo.selectedDeposition.metadata) {
            this.zenodoMetadataForm.journal.pages =
              this.workflow.destination.zenodo.selectedDeposition.metadata.journal_pages;

            this.activeNames.indexOf("journal") === -1 ? this.activeNames.push("journal") : null;
          }

          if ("conference_title" in this.workflow.destination.zenodo.selectedDeposition.metadata) {
            this.zenodoMetadataForm.conference.title =
              this.workflow.destination.zenodo.selectedDeposition.metadata.conference_title;

            this.activeNames.indexOf("conference") === -1
              ? this.activeNames.push("conference")
              : null;
          }
          if (
            "conference_acronym" in this.workflow.destination.zenodo.selectedDeposition.metadata
          ) {
            this.zenodoMetadataForm.conference.acronym =
              this.workflow.destination.zenodo.selectedDeposition.metadata.conference_acronym;

            this.activeNames.indexOf("conference") === -1
              ? this.activeNames.push("conference")
              : null;
          }
          // Will have to comeback to this one
          // if (
          //   "conference_dates" in
          //   this.workflow.destination.zenodo.selectedDeposition.metadata
          // ) {
          //   this.zenodoMetadataForm.conference.dates =
          //     this.workflow.destination.zenodo.selectedDeposition.metadata.conference_dates;
          // }
          if ("conference_place" in this.workflow.destination.zenodo.selectedDeposition.metadata) {
            this.zenodoMetadataForm.conference.place =
              this.workflow.destination.zenodo.selectedDeposition.metadata.conference_place;

            this.activeNames.indexOf("conference") === -1
              ? this.activeNames.push("conference")
              : null;
          }
          if ("conference_url" in this.workflow.destination.zenodo.selectedDeposition.metadata) {
            this.zenodoMetadataForm.conference.website =
              this.workflow.destination.zenodo.selectedDeposition.metadata.conference_url;

            this.activeNames.indexOf("conference") === -1
              ? this.activeNames.push("conference")
              : null;
          }
          if (
            "conference_session" in this.workflow.destination.zenodo.selectedDeposition.metadata
          ) {
            this.zenodoMetadataForm.conference.session =
              this.workflow.destination.zenodo.selectedDeposition.metadata.conference_session;

            this.activeNames.indexOf("conference") === -1
              ? this.activeNames.push("conference")
              : null;
          }
          if (
            "conference_session_part" in
            this.workflow.destination.zenodo.selectedDeposition.metadata
          ) {
            this.zenodoMetadataForm.conference.part =
              this.workflow.destination.zenodo.selectedDeposition.metadata.conference_session_part;

            this.activeNames.indexOf("conference") === -1
              ? this.activeNames.push("conference")
              : null;
          }

          if ("imprint_publisher" in this.workflow.destination.zenodo.selectedDeposition.metadata) {
            this.zenodoMetadataForm.bookReportChapter.publisher =
              this.workflow.destination.zenodo.selectedDeposition.metadata.imprint_publisher;

            this.activeNames.indexOf("bookReportChapter") === -1
              ? this.activeNames.push("bookReportChapter")
              : null;
          }
          if ("imprint_isbn" in this.workflow.destination.zenodo.selectedDeposition.metadata) {
            this.zenodoMetadataForm.bookReportChapter.isbn =
              this.workflow.destination.zenodo.selectedDeposition.metadata.imprint_isbn;

            this.activeNames.indexOf("bookReportChapter") === -1
              ? this.activeNames.push("bookReportChapter")
              : null;
          }
          if ("imprint_place" in this.workflow.destination.zenodo.selectedDeposition.metadata) {
            this.zenodoMetadataForm.bookReportChapter.place =
              this.workflow.destination.zenodo.selectedDeposition.metadata.imprint_place;

            this.activeNames.indexOf("bookReportChapter") === -1
              ? this.activeNames.push("bookReportChapter")
              : null;
          }
          if ("partof_title" in this.workflow.destination.zenodo.selectedDeposition.metadata) {
            this.zenodoMetadataForm.bookReportChapter.title =
              this.workflow.destination.zenodo.selectedDeposition.metadata.partof_title;

            this.activeNames.indexOf("bookReportChapter") === -1
              ? this.activeNames.push("bookReportChapter")
              : null;
          }
          if ("partof_pages" in this.workflow.destination.zenodo.selectedDeposition.metadata) {
            this.zenodoMetadataForm.bookReportChapter.pages =
              this.workflow.destination.zenodo.selectedDeposition.metadata.partof_pages;

            this.activeNames.indexOf("bookReportChapter") === -1
              ? this.activeNames.push("bookReportChapter")
              : null;
          }

          if ("thesis_university" in this.workflow.destination.zenodo.selectedDeposition.metadata) {
            this.zenodoMetadataForm.thesis.awardingUniversity =
              this.workflow.destination.zenodo.selectedDeposition.metadata.thesis_university;

            this.activeNames.indexOf("thesis") === -1 ? this.activeNames.push("thesis") : null;
          }
          if (
            "thesis_supervisors" in this.workflow.destination.zenodo.selectedDeposition.metadata
          ) {
            this.zenodoMetadataForm.thesis.supervisors = [];
            this.workflow.destination.zenodo.selectedDeposition.metadata.thesis_supervisors.forEach(
              ({ name, affiliation, orcid }) => {
                this.zenodoMetadataForm.thesis.supervisors.push({
                  name,
                  affiliation,
                  orcid,
                  id: uuidv4(),
                });
              }
            );

            this.activeNames.indexOf("thesis") === -1 ? this.activeNames.push("thesis") : null;
          }

          if ("subjects" in this.workflow.destination.zenodo.selectedDeposition.metadata) {
            this.zenodoMetadataForm.subjects = [];
            this.workflow.destination.zenodo.selectedDeposition.metadata.subjects.forEach(
              ({ term, identifier }) => {
                this.zenodoMetadataForm.subjects.push({
                  term,
                  identifier,
                  id: uuidv4(),
                });
              }
            );

            this.activeNames.indexOf("subjects") === -1 ? this.activeNames.push("subjects") : null;
          }
        }
      }
    },
    confirmNavigateBackSave(response) {
      if (response == "ok") {
        // save changes
        this.addZenodoMetadata(true, true);
      } else if (response == "cancel") {
        // don't save changes
        this.$router.push({
          path: `/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/selectDestination`,
        });
      }
    },
    navigateBack() {
      let newChanges = false;

      if (!_.isEqual(this.originalObject, this.zenodoMetadataForm)) {
        newChanges = true;
      }

      if (newChanges) {
        this.$refs.warningConfirm.show();
      } else {
        this.$router.push({
          path: `/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/selectDestination`,
        });
      }
    },
  },
  watch: {
    "zenodoMetadataForm.relatedIdentifiers": {
      handler(val) {
        // console.log(val);
        if (val.length === 0) {
          this.relatedIdentifiersErrorMessage = "";
          this.invalidStatus.relatedIdentifiers = false;
        } else {
          for (let relatedIdentifier of val) {
            if (relatedIdentifier.identifier === "") {
              this.relatedIdentifiersErrorMessage = "Please provide a related identifier.";
              this.$refs.zmForm.validate();
              this.invalidStatus.relatedIdentifiers = true;
              break;
            } else if (relatedIdentifier.identifier != "") {
              console.log(doiRegex().test(relatedIdentifier.identifier));
              let validIdentifier = false;

              if (
                doiRegex().test(relatedIdentifier.identifier) ||
                validator.isURL(relatedIdentifier.identifier)
              ) {
                validIdentifier = true;
              }

              if (!validIdentifier) {
                this.relatedIdentifiersErrorMessage =
                  "Please provide a valid identifier. Your identifier has to be either a DOI or URL";
                this.$refs.zmForm.validate();
                this.invalidStatus.relatedIdentifiers = true;
                break;
              } else {
                this.relatedIdentifiersErrorMessage = "";
                this.invalidStatus.relatedIdentifiers = false;
              }
            } else {
              this.relatedIdentifiersErrorMessage = "";
              this.invalidStatus.relatedIdentifiers = false;
            }
          }
        }
      },
      deep: true,
    },
  },
  async mounted() {
    this.loading = this.$loading({
      lock: true,
      text: "Loading",
      fullscreen: true,
      background: "rgba(0, 0, 0, 0.7)",
    });

    this.zenodoMetadataForm = zenodoMetadataOptions.defaultForm;

    this.dataset = JSON.parse(JSON.stringify(await this.datasetStore.getCurrentDataset()));

    this.workflow = this.dataset.workflows[this.workflowID];

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(5);

    this.workflow.currentRoute = this.$route.path;

    if (this.workflow.expandOptions.length === 0) {
      this.activeNames = ["basicInformation", "license"];
      // this.activeNames = ["relatedIdentifiers"];
    } else {
      this.activeNames = this.workflow.expandOptions;
      this.workflow.expandOptions = [];
    }

    const testvar = true;

    if (
      this.workflow.destination.zenodo.questions &&
      Object.keys(this.workflow.destination.zenodo.questions).length !== 0 &&
      !testvar
    ) {
      this.zenodoMetadataForm = this.workflow.destination.zenodo.questions;

      this.initializeEmptyObjects(this.zenodoMetadataForm, this.zenodoMetadataForm.license);
      this.initializeEmptyObjects(this.zenodoMetadataForm, this.zenodoMetadataForm.journal);
      this.initializeEmptyObjects(this.zenodoMetadataForm, this.zenodoMetadataForm.conference);
      this.initializeEmptyObjects(
        this.zenodoMetadataForm,
        this.zenodoMetadataForm.bookReportChapter
      );
      this.initializeEmptyObjects(this.zenodoMetadataForm, this.zenodoMetadataForm.thesis);

      const generalForm = this.dataset.data.general.questions;
      this.zenodoMetadataForm.license.licenseName = generalForm.license;

      this.addIds(this.zenodoMetadataForm.authors);
      this.addIds(this.zenodoMetadataForm.keywords);
      this.addIds(this.zenodoMetadataForm.relatedIdentifiers);
      this.addIds(this.zenodoMetadataForm.contributors);
      this.addIds(this.zenodoMetadataForm.references);
      this.addIds(this.zenodoMetadataForm.thesis.supervisors);
      this.addIds(this.zenodoMetadataForm.subjects);
      this.loading.close();

      this.originalObject = JSON.parse(JSON.stringify(this.zenodoMetadataForm));
    } else {
      this.prefillZenodoQuestions();

      this.originalObject = JSON.parse(JSON.stringify(this.zenodoMetadataForm));

      this.loading.close();
    }

    // Add the functions here to check the pre saved values for on mounted.
    // decide if the intermdiate data is saved in workflow or data.
  },
};
// CHANGE TO ONE FORM SINCE THAT iS BETTER
</script>

<style lang="postcss" scoped>
.handle {
  cursor: move;
}

.el-select-group > .el-select-dropdown__item {
  margin-left: 5px;
}
</style>
