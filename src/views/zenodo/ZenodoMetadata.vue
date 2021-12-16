<template>
  <div class="h-full w-full flex flex-col justify-center items-center pr-5 p-3">
    <div class="flex flex-col h-full w-full">
      <span class="text-lg font-medium text-left"> Zenodo Metadata </span>

      <span class="mb-2">
        Before we send this data over, Zenodo requires some additional
        information from you. We will use this information to create a Zenodo
        record. Please fill out the following form.
      </span>

      <el-form
        :model="zenodoMetadataForm"
        :rules="rulesForZenodoMetadataForm"
        label-width="150px"
        label-position="right"
        size="small"
        ref="zmForm"
        @submit.prevent
      >
        <el-collapse v-model="activeNames">
          <el-collapse-item class="text-lg" name="basicInformation">
            <template #title>
              <div class="w-full flex flex-row justify-between font-inter">
                <p>Basic Information</p>
                <span class="pr-2 text-gray-400"> required </span>
              </div>
            </template>

            <div>
              <el-form-item
                label="Publication Date"
                :required="true"
                :error="publicationDateErrorMessage"
              >
                <div class="flex flex-col">
                  <el-date-picker
                    v-model="zenodoMetadataForm.publicationDate"
                    type="date"
                    placeholder="Pick a day"
                    value-format="YYYY-MM-DD"
                  >
                  </el-date-picker>
                  <p class="text-xs pt-2 text-gray-500">
                    In case your upload was already published elsewhere, please
                    use the date of first publication.
                  </p>
                </div>
              </el-form-item>

              <el-form-item
                label="Title"
                prop="title"
                :error="titleErrorMessage"
                :required="true"
              >
                <el-input v-model="zenodoMetadataForm.title" type="text">
                </el-input>
              </el-form-item>

              <el-form-item
                label="Authors"
                :error="authorsErrorMessage"
                :required="true"
              >
                <draggable
                  tag="div"
                  :list="zenodoMetadataForm.authors"
                  item-key="id"
                  handle=".handle"
                >
                  <template #item="{ element }">
                    <div
                      class="flex flex-row mb-2 justify-between transition-all"
                    >
                      <div class="flex flex-row justify-between w-11/12">
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
                        <div class="flex flex-col w-full">
                          <el-input
                            v-model="element.orcid"
                            type="text"
                            placeholder="ORCID (e.g.: 0000-0002-1825-0097)"
                          ></el-input>
                          <span class="text-xs text-gray-400 mt-1 ml-2">
                            Optional
                          </span>
                        </div>
                        <div class="mx-2"></div>
                      </div>
                      <div class="flex flex-row justify-evenly w-1/12">
                        <div
                          class="flex justify-center items-start py-2 handle text-gray-400 hover:text-gray-700"
                        >
                          <Icon icon="ic:outline-drag-indicator" />
                        </div>
                        <div
                          class="flex justify-center items-start py-2 text-gray-600 hover:text-gray-800 cursor-pointer"
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

                <div
                  class="flex items-center cursor-pointer text-gray-500 hover:text-black w-max"
                  @click="addAuthor()"
                >
                  <Icon icon="carbon:add" />
                  <span> Add an author </span>
                </div>
              </el-form-item>

              <el-form-item
                label="Description"
                :error="descriptionErrorMessage"
                :required="true"
              >
                <Popper
                  :hover="true"
                  offsetDistance="0"
                  content="Use a description that is easily identifiable. This will
                        be shown in the dataset selection screen and is not part
                        of your submitted metadata."
                  class="w-full mx-0"
                >
                  <el-input
                    v-model="zenodoMetadataForm.description"
                    type="textarea"
                  ></el-input>
                </Popper>
              </el-form-item>

              <el-form-item label="Version" :error="versionErrorMessage">
                <div class="flex flex-col">
                  <el-input
                    v-model="zenodoMetadataForm.version"
                    type="text"
                    placeholder="1.0.4"
                  ></el-input>
                  <p class="text-xs pt-2 text-gray-500">
                    Optional. Mostly relevant for software and dataset uploads.
                    Any string will be accepted, but semantically-versioned tag
                    is recommended. <br />
                    See
                    <a href="https://semver.org/" target="_blank">
                      semver.org
                    </a>
                    for more information on semantic versioning.
                  </p>
                </div>
              </el-form-item>

              <el-form-item label="Language">
                <el-select
                  v-model="zenodoMetadataForm.language"
                  filterable
                  placeholder="e.g.: 'eng', 'fr' or 'Polish'"
                >
                  <el-option
                    v-for="item in languageOptions"
                    :key="item.alpha3"
                    :label="`${item.name} - ${item.alpha3}`"
                    :value="item.alpha3"
                  >
                  </el-option>
                </el-select>
                <p class="text-xs pt-2 text-gray-500">
                  Optional. Primary language of the record. Start by typing the
                  language's common name in English, or its ISO 639 code (two or
                  three-letter code).
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
              </el-form-item>

              <el-form-item label="Keywords">
                <draggable
                  tag="div"
                  :list="zenodoMetadataForm.keywords"
                  item-key="id"
                  handle=".handle"
                >
                  <template #item="{ element }">
                    <div
                      class="flex flex-row mb-2 justify-between transition-all"
                    >
                      <div class="flex flex-row justify-between w-11/12">
                        <el-input
                          v-model="element.keyword"
                          type="text"
                          placeholder=""
                        ></el-input>
                        <div class="mx-2"></div>
                      </div>
                      <div class="flex flex-row justify-evenly w-1/12">
                        <div
                          class="flex justify-center items-center handle text-gray-400 hover:text-gray-700"
                        >
                          <Icon icon="ic:outline-drag-indicator" />
                        </div>
                        <div
                          class="flex justify-center items-center text-gray-600 hover:text-gray-800 cursor-pointer"
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

                <div
                  class="flex items-center cursor-pointer text-gray-500 hover:text-black w-max"
                  @click="addKeyword()"
                >
                  <Icon icon="carbon:add" />
                  <span> Add a keyword </span>
                </div>
              </el-form-item>

              <el-form-item label="Additional Notes">
                <div class="flex flex-col">
                  <el-input
                    v-model="zenodoMetadataForm.additionalNotes"
                    type="textarea"
                  ></el-input>
                  <p class="text-xs pt-2 text-gray-500">Optional.</p>
                </div>
              </el-form-item>
            </div>
          </el-collapse-item>

          <el-collapse-item name="license">
            <template #title>
              <div class="w-full flex flex-row justify-between font-inter">
                <p>License</p>
                <span class="pr-2 text-gray-400"> required </span>
              </div>
            </template>

            <div>
              <el-form-item label="Access right" :required="true">
                <el-radio-group
                  v-model="zenodoMetadataForm.license.accessRight"
                  class="flex flex-col"
                >
                  <el-radio label="open">
                    <el-icon>
                      <unlock />
                    </el-icon>
                    Open Access
                  </el-radio>
                  <el-radio label="embargoed" disabled>
                    <el-icon> <remove-filled /> </el-icon> Embargoed Access
                  </el-radio>
                  <el-radio label="restricted" disabled>
                    <el-icon>
                      <key />
                    </el-icon>
                    Restricted Access
                  </el-radio>
                  <el-radio label="closed" disabled>
                    <el-icon>
                      <lock />
                    </el-icon>
                    Closed Access
                  </el-radio>
                </el-radio-group>
                <p class="text-xs pt-2 text-gray-500">
                  Required. Open access uploads have considerably higher
                  visibility on Zenodo.
                </p>
              </el-form-item>

              <el-form-item label="License" prop="license">
                <el-select
                  v-model="zenodoMetadataForm.license.licenseName"
                  filterable
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
                <p class="text-xs pt-2 text-gray-500">
                  Required. Selected license applies to all of your files
                  displayed on the top of the form. <br />
                  If you want to upload some of your files under different
                  licenses, please do so in separate uploads. <br />
                  If you cannot find the license you're looking for, include a
                  relevant LICENSE file in your record and choose one of the
                  <span class="italic"> Other </span> licenses available
                  <span class="italic">
                    (Other (Open), Other (Attribution) </span
                  >, etc.). <br />
                  The supported licenses in the list are harvested from
                  <a
                    href="https://opendefinition.org/"
                    target="_blank"
                    class="text-blue-500 hover:underline"
                  >
                    opendefinition.org
                  </a>
                  and
                  <a
                    href="https://spdx.org/"
                    target="_blank"
                    class="text-blue-500 hover:underline"
                  >
                    spdx.org
                  </a>
                  .
                </p>
              </el-form-item>
            </div>
          </el-collapse-item>

          <el-collapse-item name="relatedIdentifiers">
            <template #title>
              <div class="w-full flex flex-row justify-between font-inter">
                <p>Related/alternate identifiers</p>
                <span class="pr-2 text-gray-400"> recommended </span>
              </div>
            </template>

            <p class="text-xs mb-4">
              Specify identifiers of related publications and datasets.
              Supported identifiers include: DOI and URLs.
              <br />
            </p>

            <div>
              <el-form-item
                label="Related identifiers"
                :error="relatedIdentifiersErrorMessage"
              >
                <draggable
                  tag="div"
                  :list="zenodoMetadataForm.relatedIdentifiers"
                  item-key="id"
                  handle=".handle"
                >
                  <template #item="{ element }">
                    <div
                      class="flex flex-row mb-2 justify-between transition-all"
                    >
                      <div class="flex flex-row justify-between w-11/12">
                        <div class="mx-2 w-6/12">
                          <el-input
                            v-model="element.identifier"
                            type="text"
                            placeholder="e.g. 10.1234/foobar.56789"
                          ></el-input>
                        </div>
                        <div class="mx-2 w-6/12 flex flex-row justify-evenly">
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
                          <div class="mx-2 block 2xl:hidden"></div>
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
                            <p class="text-xs pt-2 text-gray-500">
                              Optional. Resource type of the related identifier.
                            </p>
                          </div>
                        </div>
                      </div>
                      <div class="flex flex-row justify-evenly w-1/12">
                        <div
                          class="flex justify-center items-center handle text-gray-400 hover:text-gray-700"
                        >
                          <Icon icon="ic:outline-drag-indicator" />
                        </div>
                        <div
                          class="flex justify-center items-center text-gray-600 hover:text-gray-800 cursor-pointer"
                        >
                          <el-popconfirm
                            title="Are you sure you want to remove this?"
                            icon-color="red"
                            confirm-button-text="Yes"
                            cancel-button-text="No"
                            @confirm="deleteRelatedIdentifier(element.id)"
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

                <div
                  class="flex items-center cursor-pointer text-gray-500 hover:text-black w-max"
                  @click="addRelatedIdentifier()"
                >
                  <Icon icon="carbon:add" />
                  <span> Add a related or alternate identifier </span>
                </div>
              </el-form-item>
            </div>
          </el-collapse-item>

          <el-collapse-item name="contributors">
            <template #title>
              <div class="w-full flex flex-row justify-between font-inter">
                <p>Contributors</p>
                <span class="pr-2 text-gray-400"> optional </span>
              </div>
            </template>

            <div>
              <el-form-item
                label="Contributors"
                :required="false"
                :error="contributorsErrorMessage"
              >
                <draggable
                  tag="div"
                  :list="zenodoMetadataForm.contributors"
                  item-key="id"
                  handle=".handle"
                >
                  <template #item="{ element }">
                    <div
                      class="flex flex-row mb-2 justify-between transition-all"
                    >
                      <div class="flex flex-row justify-between w-11/12">
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
                          <div class="flex flex-col w-full">
                            <el-input
                              v-model="element.orcid"
                              type="text"
                              placeholder="ORCID (e.g.: 0000-0002-1825-0097)"
                            ></el-input>
                            <span class="text-xs text-gray-400 mt-1 ml-2">
                              Optional
                            </span>
                          </div>
                        </div>
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
                      </div>
                      <div class="flex flex-row justify-evenly w-1/12">
                        <div
                          class="flex justify-center items-start py-2 handle text-gray-400 hover:text-gray-700"
                        >
                          <Icon icon="ic:outline-drag-indicator" />
                        </div>
                        <div
                          class="flex justify-center items-start py-2 text-gray-600 hover:text-gray-800 cursor-pointer"
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

                <div
                  class="flex items-center cursor-pointer text-gray-500 hover:text-black w-max"
                  @click="addContributor()"
                >
                  <Icon icon="carbon:add" />
                  <span> Add a contributor </span>
                </div>
              </el-form-item>
            </div>
          </el-collapse-item>

          <el-collapse-item name="references">
            <template #title>
              <div class="w-full flex flex-row justify-between font-inter">
                <p>References</p>
                <span class="pr-2 text-gray-400"> optional </span>
              </div>
            </template>

            <div>
              <el-form-item label="References">
                <draggable
                  tag="div"
                  :list="zenodoMetadataForm.references"
                  item-key="id"
                  handle=".handle"
                >
                  <template #item="{ element }">
                    <div
                      class="flex flex-row mb-2 justify-between transition-all"
                    >
                      <div class="flex flex-row justify-between w-11/12">
                        <el-input
                          v-model="element.reference"
                          type="text"
                          placeholder="e.g.: Cranmer, Kyle et al. (2014). Decouple software associated to arXiv:1401.0080."
                        ></el-input>
                        <div class="mx-2"></div>
                      </div>
                      <div class="flex flex-row justify-evenly w-1/12">
                        <div
                          class="flex justify-center items-center handle text-gray-400 hover:text-gray-700"
                        >
                          <Icon icon="ic:outline-drag-indicator" />
                        </div>
                        <div
                          class="flex justify-center items-center text-gray-600 hover:text-gray-800 cursor-pointer"
                        >
                          <el-popconfirm
                            title="Are you sure you want to remove this?"
                            icon-color="red"
                            confirm-button-text="Yes"
                            cancel-button-text="No"
                            @confirm="deleteReference(element.id)"
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

                <div
                  class="flex items-center cursor-pointer text-gray-500 hover:text-black w-max"
                  @click="addReference()"
                >
                  <Icon icon="carbon:add" />
                  <span> Add a reference </span>
                </div>
              </el-form-item>
            </div>
          </el-collapse-item>

          <el-collapse-item name="journal">
            <template #title>
              <div class="w-full flex flex-row justify-between font-inter">
                <p>Journal</p>
                <span class="pr-2 text-gray-400"> optional </span>
              </div>
            </template>

            <div>
              <el-form-item label="Journal title">
                <div class="flex flex-col">
                  <el-input
                    v-model="zenodoMetadataForm.journal.title"
                    type="text"
                  ></el-input>
                  <p class="text-xs pt-2 text-gray-500">Optional.</p>
                </div>
              </el-form-item>
              <el-form-item label="Volume">
                <div class="flex flex-col">
                  <el-input
                    v-model="zenodoMetadataForm.journal.volume"
                    type="text"
                  ></el-input>
                  <p class="text-xs pt-2 text-gray-500">Optional.</p>
                </div>
              </el-form-item>
              <el-form-item label="Issue">
                <div class="flex flex-col">
                  <el-input
                    v-model="zenodoMetadataForm.journal.issue"
                    type="text"
                  ></el-input>
                  <p class="text-xs pt-2 text-gray-500">Optional.</p>
                </div>
              </el-form-item>
              <el-form-item label="Pages">
                <div class="flex flex-col">
                  <el-input
                    v-model="zenodoMetadataForm.journal.pages"
                    type="text"
                  ></el-input>
                  <p class="text-xs pt-2 text-gray-500">Optional.</p>
                </div>
              </el-form-item>
            </div>
          </el-collapse-item>

          <el-collapse-item name="conference">
            <template #title>
              <div class="w-full flex flex-row justify-between font-inter">
                <p>Conference</p>
                <span class="pr-2 text-gray-400"> optional </span>
              </div>
            </template>

            <div>
              <el-form-item label="Conference title">
                <div class="flex flex-col">
                  <el-input
                    v-model="zenodoMetadataForm.conference.title"
                    type="text"
                  ></el-input>
                  <p class="text-xs pt-2 text-gray-500">Optional.</p>
                </div>
              </el-form-item>
              <el-form-item label="Acronym">
                <div class="flex flex-col">
                  <el-input
                    v-model="zenodoMetadataForm.conference.acronym"
                    type="text"
                  ></el-input>
                  <p class="text-xs pt-2 text-gray-500">Optional.</p>
                </div>
              </el-form-item>
              <el-form-item label="Dates">
                <div class="flex flex-col">
                  <el-date-picker
                    v-model="zenodoMetadataForm.conference.dates"
                    type="daterange"
                    range-separator="-"
                    start-placeholder="Start date"
                    end-placeholder="End date"
                    size="medium"
                    value-format="YYYY-MM-DD"
                  >
                  </el-date-picker>
                  <p class="text-xs pt-2 text-gray-500">Optional.</p>
                </div>
              </el-form-item>
              <el-form-item label="Place">
                <div class="flex flex-col">
                  <el-input
                    v-model="zenodoMetadataForm.conference.place"
                    type="text"
                    placeholder="e.g. city, country"
                  ></el-input>
                  <p class="text-xs pt-2 text-gray-500">Optional.</p>
                </div>
              </el-form-item>
              <el-form-item label="Website">
                <div class="flex flex-col">
                  <el-input
                    v-model="zenodoMetadataForm.conference.website"
                    type="text"
                    placeholder="e.g. http://zenodo.org"
                  ></el-input>
                  <p class="text-xs pt-2 text-gray-500">Optional.</p>
                </div>
              </el-form-item>
              <el-form-item label="Session">
                <div class="flex flex-col">
                  <el-input
                    v-model="zenodoMetadataForm.conference.session"
                    type="text"
                    placeholder="e.g. VI"
                  ></el-input>
                  <p class="text-xs pt-2 text-gray-500">
                    Optional. Number of session within the conference.
                  </p>
                </div>
              </el-form-item>
              <el-form-item label="Part">
                <div class="flex flex-col">
                  <el-input
                    v-model="zenodoMetadataForm.conference.part"
                    type="text"
                    placeholder="e.g. 1"
                  ></el-input>
                  <p class="text-xs pt-2 text-gray-500">
                    Optional. Number of part within a session.
                  </p>
                </div>
              </el-form-item>
            </div>
          </el-collapse-item>

          <el-collapse-item name="bookReportChapter">
            <template #title>
              <div class="w-full flex flex-row justify-between font-inter">
                <p>Book/Report/Chapter</p>
                <span class="pr-2 text-gray-400"> optional </span>
              </div>
            </template>

            <p class="text-xs mb-4">For parts of books and reports. <br /></p>
            <div>
              <el-form-item label="Publisher">
                <div class="flex flex-col">
                  <el-input
                    v-model="zenodoMetadataForm.bookReportChapter.publisher"
                    type="text"
                  ></el-input>
                  <p class="text-xs pt-2 text-gray-500">Optional.</p>
                </div>
              </el-form-item>
              <el-form-item label="Place">
                <div class="flex flex-col">
                  <el-input
                    v-model="zenodoMetadataForm.bookReportChapter.place"
                    type="text"
                    placeholder="e.g. city, country"
                  ></el-input>
                  <p class="text-xs pt-2 text-gray-500">Optional.</p>
                </div>
              </el-form-item>
              <el-form-item label="ISBN">
                <div class="flex flex-col">
                  <el-input
                    v-model="zenodoMetadataForm.bookReportChapter.isbn"
                    type="text"
                    placeholder="e.g. 0-06-251587-X"
                  ></el-input>
                  <p class="text-xs pt-2 text-gray-500">Optional.</p>
                </div>
              </el-form-item>
              <el-form-item label="Book title">
                <div class="flex flex-col">
                  <el-input
                    v-model="zenodoMetadataForm.bookReportChapter.title"
                    type="text"
                  ></el-input>
                  <p class="text-xs pt-2 text-gray-500">
                    Optional. Title of the book or report which this upload is
                    part of.
                  </p>
                </div>
              </el-form-item>
              <el-form-item label="Pages">
                <div class="flex flex-col">
                  <el-input
                    v-model="zenodoMetadataForm.bookReportChapter.pages"
                    type="text"
                  ></el-input>
                  <p class="text-xs pt-2 text-gray-500">Optional.</p>
                </div>
              </el-form-item>
            </div>
          </el-collapse-item>

          <el-collapse-item name="thesis">
            <template #title>
              <div class="w-full flex flex-row justify-between font-inter">
                <p>Thesis</p>
                <span class="pr-2 text-gray-400"> optional </span>
              </div>
            </template>

            <div>
              <el-form-item label="Awarding university">
                <div class="flex flex-col">
                  <el-input
                    v-model="zenodoMetadataForm.thesis.awardingUniversity"
                    type="text"
                  ></el-input>
                  <p class="text-xs pt-2 text-gray-500">Optional.</p>
                </div>
              </el-form-item>

              <el-form-item label="Supervisors">
                <draggable
                  tag="div"
                  :list="zenodoMetadataForm.thesis.supervisors"
                  item-key="id"
                  handle=".handle"
                >
                  <template #item="{ element }">
                    <div
                      class="flex flex-row mb-2 justify-between transition-all"
                    >
                      <div class="flex flex-row justify-between w-11/12">
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
                        <div class="flex flex-col w-full">
                          <el-input
                            v-model="element.orcid"
                            type="text"
                            placeholder="ORCID (e.g.: 0000-0002-1825-0097)"
                          ></el-input>
                          <span class="text-xs text-gray-400 mt-1 ml-2">
                            Optional
                          </span>
                        </div>
                        <div class="mx-2"></div>
                      </div>
                      <div class="flex flex-row justify-evenly w-1/12">
                        <div
                          class="flex justify-center items-start py-2 handle text-gray-400 hover:text-gray-700"
                        >
                          <Icon icon="ic:outline-drag-indicator" />
                        </div>
                        <div
                          class="flex justify-center items-start py-2 text-gray-600 hover:text-gray-800 cursor-pointer"
                        >
                          <el-popconfirm
                            title="Are you sure you want to remove this?"
                            icon-color="red"
                            confirm-button-text="Yes"
                            cancel-button-text="No"
                            @confirm="deleteSupervisor(element.id)"
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

                <div
                  class="flex items-center cursor-pointer text-gray-500 hover:text-black w-max"
                  @click="addSupervisor()"
                >
                  <Icon icon="carbon:add" />
                  <span> Add a supervisor </span>
                </div>
              </el-form-item>
            </div>
          </el-collapse-item>

          <el-collapse-item name="subjects">
            <template #title>
              <div class="w-full flex flex-row justify-between font-inter">
                <p>Subjects</p>
                <span class="pr-2 text-gray-400"> optional </span>
              </div>
            </template>

            <p class="text-xs mb-4">
              Specify subjects from a taxonomy or controlled vocabulary. Each
              term must be uniquely identified (e.g. a URL). For free form text,
              use the keywords field in basic information section.
              <br />
            </p>
            <div>
              <el-form-item
                label="Subjects"
                :error="subjectsErrorMessage"
                :required="false"
              >
                <draggable
                  tag="div"
                  :list="zenodoMetadataForm.subjects"
                  item-key="id"
                  handle=".handle"
                >
                  <template #item="{ element }">
                    <div
                      class="flex flex-row mb-2 justify-between transition-all"
                    >
                      <div class="flex flex-row justify-between w-11/12">
                        <el-input
                          v-model="element.term"
                          type="text"
                          placeholder="Term"
                        ></el-input>
                        <div class="mx-2"></div>
                        <el-input
                          v-model="element.identifier"
                          type="text"
                          placeholder="Identifier"
                        ></el-input>
                        <div class="mx-2"></div>
                      </div>
                      <div class="flex flex-row justify-evenly w-1/12">
                        <div
                          class="flex justify-center items-center handle text-gray-400 hover:text-gray-700"
                        >
                          <Icon icon="ic:outline-drag-indicator" />
                        </div>
                        <div
                          class="flex justify-center items-center text-gray-600 hover:text-gray-800 cursor-pointer"
                        >
                          <el-popconfirm
                            title="Are you sure you want to remove this?"
                            icon-color="red"
                            confirm-button-text="Yes"
                            cancel-button-text="No"
                            @confirm="deleteSubject(element.id)"
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

                <div
                  class="flex items-center cursor-pointer text-gray-500 hover:text-black w-max"
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

      <div class="w-full flex flex-row justify-center py-2">
        <el-button type="danger" plain @click="navigateBack" class="mx-6">
          Back
        </el-button>

        <el-button
          type="primary"
          class="flex flex-row items-center"
          @click="addZenodoMetadata"
          :disabled="checkInvalidStatus"
        >
          Continue
          <el-icon>
            <ArrowRightBold />
          </el-icon>
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { Icon } from "@iconify/vue";
import {
  ArrowRightBold,
  Lock,
  Unlock,
  RemoveFilled,
  Key,
} from "@element-plus/icons";
import draggable from "vuedraggable";
import { v4 as uuidv4 } from "uuid";
import semver from "semver";
import doiRegex from "doi-regex";
import { ElMessageBox, ElMessage } from "element-plus";
import _ from "lodash";

import { useDatasetsStore } from "../../store/datasets";
import licensesJSON from "../../assets/supplementalFiles/licenses.json";
import contributorTypesJSON from "../../assets/supplementalFiles/contributorTypes.json";
import zenodoMetadataOptions from "../../assets/supplementalFiles/zenodoMetadataOptions.json";
import languagesJSON from "../../assets/supplementalFiles/zenodoLanguages.json";

export default {
  name: "ZenodoMetadata",
  components: {
    ArrowRightBold,
    Lock,
    Unlock,
    RemoveFilled,
    Key,
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
      activeNames: [],
      drag: true,
      licenseOptions: licensesJSON.licenses,
      languageOptions: languagesJSON.languages,
      relatedIdentifierRelationships:
        zenodoMetadataOptions.relatedIdentifierRelationships,
      relatedIdentifierTypes: zenodoMetadataOptions.relatedIdentifierTypes,
      contributorTypes: contributorTypesJSON.contributorTypes,
      zenodoMetadataForm: zenodoMetadataOptions.defaultForm,
      authorsErrorMessage: "",
      contributorsErrorMessage: "",
      subjectsErrorMessage: "",
      titleErrorMessage: "",
      descriptionErrorMessage: "",
      publicationDateErrorMessage: "",
      versionErrorMessage: "",
      relatedIdentifiersErrorMessage: "",
      invalidStatus: {},
      rulesForZenodoMetadataForm: {
        title: [
          {
            required: true,
            message: "Required.",
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
            message:
              "Required. Selected license applies to all of your files displayed on the top of the form.",
            trigger: "change",
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
      console.log(this.invalidStatus);

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
    addSubject() {
      this.zenodoMetadataForm.subjects.push({
        term: "",
        identifier: "",
        id: uuidv4(),
      });
    },
    deleteSubject(id) {
      this.zenodoMetadataForm.subjects =
        this.zenodoMetadataForm.subjects.filter((subject) => {
          return subject.id !== id;
        });
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
      this.zenodoMetadataForm.authors = this.zenodoMetadataForm.authors.filter(
        (author) => {
          return author.id !== id;
        }
      );
    },
    addKeyword() {
      this.zenodoMetadataForm.keywords.push({
        keyword: "",
        id: uuidv4(),
      });
    },
    deleteKeyword(id) {
      this.zenodoMetadataForm.keywords =
        this.zenodoMetadataForm.keywords.filter((keyword) => {
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
        this.zenodoMetadataForm.relatedIdentifiers.filter(
          (relatedIdentifier) => {
            return relatedIdentifier.id !== id;
          }
        );
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
      this.zenodoMetadataForm.contributors =
        this.zenodoMetadataForm.contributors.filter((contributor) => {
          return contributor.id !== id;
        });
    },
    addReference() {
      this.zenodoMetadataForm.references.push({
        reference: "",
        id: uuidv4(),
      });
    },
    deleteReference(id) {
      this.zenodoMetadataForm.references =
        this.zenodoMetadataForm.references.filter((reference) => {
          return reference.id !== id;
        });
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
    addZenodoMetadata(_evt, shouldNavigateBack = false) {
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

      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/zenodo/review`;
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

        this.zenodoMetadataForm.publicationDate = `${date.getFullYear()}-${
          date.getMonth() + 1
        }-${date.getDate()}`;

        if ("name" in generalForm) {
          this.zenodoMetadataForm.title = generalForm.name;
        }

        if ("description" in generalForm) {
          this.zenodoMetadataForm.description = generalForm.description;
        }

        if ("keywords" in generalForm) {
          this.zenodoMetadataForm.keywords = generalForm.keywords;
        }

        if ("authors" in generalForm) {
          let authors = generalForm.authors;
          let newAuthors = [];
          authors.forEach((author) => {
            let newAuthor = {
              name: author.familyName + ", " + author.givenName,
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
        }
      }
    },
    navigateBack() {
      let newChanges = false;

      if (!_.isEqual(this.originalObject, this.zenodoMetadataForm)) {
        newChanges = true;
      }

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
            this.addZenodoMetadata(true, true);
          })
          .catch(() => {
            // don't save changes
            this.$router.push({
              path: `/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/selectDestination`,
            });
          });
      } else {
        this.$router.push({
          path: `/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/selectDestination`,
        });
      }
    },
  },
  watch: {
    "zenodoMetadataForm.authors": {
      handler(val) {
        if (val.length === 0) {
          this.authorsErrorMessage = "Please provide at least one author.";
          this.invalidStatus.authors = true;
          this.$refs.zmForm.validate();
          return;
        } else {
          this.authorsErrorMessage = ""; //clear error message
          this.invalidStatus.authors = false;
        }

        if (val.length > 0) {
          for (let author of val) {
            if (author.name === "" || author.affiliation === "") {
              // console.log("author error");
              this.authorsErrorMessage =
                "Name and Affiliation for each author is mandatory";
              this.invalidStatus.authors = true;
              this.$refs.zmForm.validate();
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
                // console.log(digit);
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
                this.$refs.zmForm.validate();
                this.invalidStatus.authors = true;
                break;
              }
            }
          }
        }
      },
      deep: true,
    },
    "zenodoMetadataForm.contributors": {
      handler(val) {
        if (val.length > 0) {
          for (let contributor of val) {
            if (contributor.name === "" || contributor.affiliation === "") {
              // console.log("contributor error");
              this.contributorsErrorMessage =
                "Name and Affiliation for each contributor is mandatory";
              this.$refs.zmForm.validate();
              this.invalidStatus.contributors = true;
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
                this.$refs.zmForm.validate();
                this.invalidStatus.contributors = true;
                break;
              }
            }
          }
        }
      },
      deep: true,
    },
    "zenodoMetadataForm.publicationDate": {
      handler(val) {
        if (val === "" || val === null) {
          this.publicationDateErrorMessage =
            "Please provide the date of publication.";
          this.$refs.zmForm.validate();
          this.invalidStatus.publicationDate = true;
          return;
        } else {
          this.publicationDateErrorMessage = "";
          this.invalidStatus.publicationDate = false;
        }
      },
      deep: true,
    },
    "zenodoMetadataForm.title": {
      handler(val) {
        if (val === "") {
          this.titleErrorMessage =
            "Please provide a valid and descriptive title.";
          this.$refs.zmForm.validate();
          this.invalidStatus.title = true;
          return;
        } else {
          this.titleErrorMessage = "";
          this.invalidStatus.title = false;
        }
      },
      deep: true,
    },
    "zenodoMetadataForm.license": {
      handler(val) {
        const value = val.licensename;
        if (value === "") {
          // this.titleErrorMessage =
          ("Please provide a valid and descriptive title.");
          this.$refs.zmForm.validate();
          this.invalidStatus.license = true;
          return;
        } else {
          // this.titleErrorMessage = "";
          this.invalidStatus.license = false;
        }
      },
      deep: true,
    },
    "zenodoMetadataForm.description": {
      handler(val) {
        if (val === "") {
          this.descriptionErrorMessage =
            "Please provide a valid and identifiable description.";
          this.$refs.zmForm.validate();
          this.invalidStatus.description = true;
          return;
        } else {
          this.descriptionErrorMessage = "";
          this.invalidStatus.description = false;
        }
      },
      deep: true,
    },
    "zenodoMetadataForm.version": {
      handler(val) {
        if (val != "" && semver.valid(val) === null) {
          this.versionErrorMessage = "Please provide a valid version number.";
          this.$refs.zmForm.validate();
          this.invalidStatus.version = true;
          return;
        } else {
          this.versionErrorMessage = "";
          this.invalidStatus.version = false;
        }
      },
      deep: true,
    },
    "zenodoMetadataForm.relatedIdentifiers": {
      handler(val) {
        // console.log(val);
        if (val.length === 0) {
          this.relatedIdentifiersErrorMessage = "";
          this.invalidStatus.relatedIdentifiers = false;
        } else {
          for (let relatedIdentifier of val) {
            // console.log(relatedIdentifier.identifier);
            if (relatedIdentifier.identifier === "") {
              this.relatedIdentifiersErrorMessage =
                "Please provide a related identifier.";
              this.$refs.zmForm.validate();
              this.invalidStatus.relatedIdentifiers = true;
              break;
            } else if (relatedIdentifier.identifier != "") {
              let validIdentifier = false;

              if (doiRegex().test(relatedIdentifier.identifier)) {
                validIdentifier = true;
              }

              if (!validIdentifier) {
                try {
                  new URL(relatedIdentifier.identifier);
                  validIdentifier = true;
                } catch (_) {
                  validIdentifier = false;
                }
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
    "zenodoMetadataForm.subjects": {
      handler(val) {
        if (val.length > 0) {
          for (let subject of val) {
            if (subject.term === "") {
              // console.log("subject error");
              this.subjectsErrorMessage =
                "Please provide a valid and identifiable subject.";
              this.$refs.zmForm.validate();
              this.invalidStatus.subjects = true;
              break;
            } else {
              let validIdentifier = false;

              try {
                new URL(subject.identifier);
                validIdentifier = true;
              } catch (_) {
                validIdentifier = false;
              }

              if (!validIdentifier) {
                this.subjectsErrorMessage =
                  "Please provide a valid identifier. Your identifier has to be in the form of a URL";
                this.$refs.zmForm.validate();
                this.invalidStatus.subjects = true;
                break;
              } else {
                this.subjectsErrorMessage = "";
                this.invalidStatus.subjects = false;
              }
            }
          }
        } else {
          this.subjectsErrorMessage = "";
          this.invalidStatus.subjects = false;
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

    this.dataset = JSON.parse(
      JSON.stringify(await this.datasetStore.getCurrentDataset())
    );

    this.workflow = this.dataset.workflows[this.workflowID];

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(4);

    if (this.workflow.expandOptions.length === 0) {
      this.activeNames = ["basicInformation", "license"];
      // this.activeNames = ["relatedIdentifiers"];
    } else {
      this.activeNames = this.workflow.expandOptions;
      this.workflow.expandOptions = [];
    }

    if (
      this.workflow.destination.zenodo.questions &&
      Object.keys(this.workflow.destination.zenodo.questions).length !== 0
    ) {
      this.zenodoMetadataForm = this.workflow.destination.zenodo.questions;

      this.initializeEmptyObjects(
        this.zenodoMetadataForm,
        this.zenodoMetadataForm.license
      );
      this.initializeEmptyObjects(
        this.zenodoMetadataForm,
        this.zenodoMetadataForm.journal
      );
      this.initializeEmptyObjects(
        this.zenodoMetadataForm,
        this.zenodoMetadataForm.conference
      );
      this.initializeEmptyObjects(
        this.zenodoMetadataForm,
        this.zenodoMetadataForm.bookReportChapter
      );
      this.initializeEmptyObjects(
        this.zenodoMetadataForm,
        this.zenodoMetadataForm.thesis
      );

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

<style lang="postcss">
.handle {
  cursor: move;
}

.el-select-group > .el-select-dropdown__item {
  margin-left: 5px;
}
</style>
