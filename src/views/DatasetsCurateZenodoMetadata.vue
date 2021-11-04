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
    v-loading="loading"
  >
    <div class="p-3 h-full flex flex-row items-center">
      <div class="h-full w-full">
        <div class="flex flex-col h-full pr-5">
          <span class="text-lg font-medium text-left"> Zenodo Metadata </span>
          <span class="text-left"> Lets upload your data to Zenodo. </span>

          <line-divider></line-divider>

          <span class="mb-2">
            Before we send this data over, Zenodo requires some metadata from
            you. We have filled any information we have learned from the data as
            well as your previous metadata.
          </span>

          <el-form
            :model="zenodoMetadataForm"
            :rules="rulesForZenodoMetadataForm"
            label-width="150px"
            label-position="right"
            size="small"
            @submit.prevent
          >
            <el-collapse v-model="activeNames">
              <el-collapse-item
                class="text-lg"
                title="Basic Information"
                name="basicInformation"
              >
                <div>
                  <el-form-item label="Publication Date" prop="publicationDate">
                    <el-date-picker
                      v-model="zenodoMetadataForm.publicationDate"
                      type="date"
                      placeholder="Pick a day"
                      value-format="YYYY-MM-DD"
                    >
                    </el-date-picker>
                  </el-form-item>

                  <el-form-item label="Title" prop="title">
                    <Popper
                      :hover="true"
                      offsetDistance="0"
                      content="Use a description that is easily identifiable. This will
                        be shown in the dataset selection screen and is not part
                        of your submitted metadata."
                      class="w-full"
                    >
                      <el-input v-model="zenodoMetadataForm.title" type="text">
                        text
                      </el-input>
                    </Popper>
                  </el-form-item>

                  <el-form-item label="Authors">
                    <draggable
                      tag="div"
                      :list="zenodoMetadataForm.authors"
                      item-key="id"
                      handle=".handle"
                    >
                      <template #item="{ element }">
                        <div
                          class="
                            flex flex-row
                            mb-2
                            justify-between
                            transition-all
                          "
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
                            <el-input
                              v-model="element.orcid"
                              type="text"
                              placeholder="ORCID (e.g.: 0000-0002-1825-0097)"
                            ></el-input>
                            <div class="mx-2"></div>
                          </div>
                          <div class="flex flex-row justify-evenly w-1/12">
                            <div
                              class="
                                flex
                                justify-center
                                items-center
                                handle
                                text-gray-400
                                hover:text-gray-700
                              "
                            >
                              <Icon icon="ic:outline-drag-indicator" />
                            </div>
                            <div
                              class="
                                flex
                                justify-center
                                items-center
                                text-gray-600
                                hover:text-gray-800
                                cursor-pointer
                              "
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
                      class="
                        flex
                        items-center
                        cursor-pointer
                        text-gray-500
                        hover:text-black
                        w-max
                      "
                      @click="addAuthor()"
                    >
                      <Icon icon="carbon:add" />
                      <span> Add an author </span>
                    </div>
                  </el-form-item>

                  <el-form-item label="Description" prop="description">
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

                  <el-form-item label="Version">
                    <el-popover
                      ref="popover"
                      placement="bottom"
                      :width="300"
                      trigger="hover"
                      content=""
                    >
                      <template #reference>
                        <el-input
                          v-model="zenodoMetadataForm.version"
                          type="text"
                          placeholder="1.0.4"
                        ></el-input>
                      </template>

                      <span class="break-normal text-left text-sm">
                        Optional. Mostly relevant for software and dataset
                        uploads. Any string will be accepted, but
                        semantically-versioned tag is recommended. <br />
                        See
                        <a href="https://semver.org/" target="_blank">
                          semver.org
                        </a>
                        for more information on semantic versioning.
                      </span>
                    </el-popover>
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
                      Optional. Primary language of the record. Start by typing
                      the language's common name in English, or its ISO 639 code
                      (two or three-letter code).
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
                          class="
                            flex flex-row
                            mb-2
                            justify-between
                            transition-all
                          "
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
                              class="
                                flex
                                justify-center
                                items-center
                                handle
                                text-gray-400
                                hover:text-gray-700
                              "
                            >
                              <Icon icon="ic:outline-drag-indicator" />
                            </div>
                            <div
                              class="
                                flex
                                justify-center
                                items-center
                                text-gray-600
                                hover:text-gray-800
                                cursor-pointer
                              "
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
                      class="
                        flex
                        items-center
                        cursor-pointer
                        text-gray-500
                        hover:text-black
                        w-max
                      "
                      @click="addKeyword()"
                    >
                      <Icon icon="carbon:add" />
                      <span> Add a keyword </span>
                    </div>
                  </el-form-item>

                  <el-form-item label="Additional Notes">
                    <el-input
                      v-model="zenodoMetadataForm.additionalNotes"
                      type="textarea"
                    ></el-input>
                  </el-form-item>
                </div>
              </el-collapse-item>

              <el-collapse-item title="License" name="license">
                <div>
                  <el-form-item label="Access right" prop="accessRight">
                    <el-radio-group
                      v-model="zenodoMetadataForm.license.accessRight"
                      class="flex flex-col"
                    >
                      <el-radio label="openAccess">
                        <el-icon>
                          <unlock />
                        </el-icon>
                        Open Access
                      </el-radio>
                      <el-radio label="embargoedAccess" disabled>
                        <el-icon> <remove-filled /> </el-icon> Embargoed Access
                      </el-radio>
                      <el-radio label="restrictedAccess" disabled>
                        <el-icon>
                          <key />
                        </el-icon>
                        Restricted Access
                      </el-radio>
                      <el-radio label="closedAccess" disabled>
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
                      If you cannot find the license you're looking for, include
                      a relevant LICENSE file in your record and choose one of
                      the <span class="italic"> Other </span> licenses available
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

              <!-- <el-collapse-item title="Funding" name="funding">
                <span class="text-xs">
                  Zenodo is integrated into reporting lines for research funded
                  by the European Commission via OpenAIRE. Specify grants which
                  have funded your research, and we will let your funding agency
                  know!
                </span>
                <div>
                  <p class="text-xs pt-2 text-gray-500">
                    Optional. OpenAIRE-supported projects only. For other
                    funding acknowledgements, please use the Additional Notes
                    field. Note: a human Zenodo curator will need to validate
                    your upload - you may experience a delay before it is
                    available in OpenAIRE.
                  </p>
                </div>
              </el-collapse-item> -->

              <el-collapse-item
                title="Related/alternate identifiers"
                name="relatedIdentifiers"
              >
                <p class="text-xs mb-4">
                  Specify identifiers of related publications and datasets.
                  <br />
                  Supported identifiers include: DOI, Handle, ARK, PURL, ISSN,
                  ISBN, PubMed ID, PubMed Central ID, ADS Bibliographic Code,
                  arXiv, Life Science Identifiers (LSID), EAN-13, ISTC, URNs and
                  URLs.
                  <br />
                </p>
                <div>
                  <el-form-item label="Related identifiers">
                    <draggable
                      tag="div"
                      :list="zenodoMetadataForm.relatedIdentifiers"
                      item-key="id"
                      handle=".handle"
                    >
                      <template #item="{ element }">
                        <div
                          class="
                            flex flex-row
                            mb-2
                            justify-between
                            transition-all
                          "
                        >
                          <div class="flex flex-row justify-between w-11/12">
                            <div class="mx-2 w-6/12">
                              <el-input
                                v-model="element.identifier"
                                type="text"
                                placeholder="e.g. 10.1234/foobar.56789"
                              ></el-input>
                            </div>
                            <div
                              class="mx-2 w-6/12 flex flex-row justify-evenly"
                            >
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
                            </div>
                          </div>
                          <div class="flex flex-row justify-evenly w-1/12">
                            <div
                              class="
                                flex
                                justify-center
                                items-center
                                handle
                                text-gray-400
                                hover:text-gray-700
                              "
                            >
                              <Icon icon="ic:outline-drag-indicator" />
                            </div>
                            <div
                              class="
                                flex
                                justify-center
                                items-center
                                text-gray-600
                                hover:text-gray-800
                                cursor-pointer
                              "
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
                      class="
                        flex
                        items-center
                        cursor-pointer
                        text-gray-500
                        hover:text-black
                        w-max
                      "
                      @click="addRelatedIdentifier()"
                    >
                      <Icon icon="carbon:add" />
                      <span> Add an author </span>
                    </div>
                  </el-form-item>
                </div>
              </el-collapse-item>

              <el-collapse-item title="Contributors" name="contributors">
                <div>
                  <el-form-item label="Contributors">
                    <draggable
                      tag="div"
                      :list="zenodoMetadataForm.contributors"
                      item-key="id"
                      handle=".handle"
                    >
                      <template #item="{ element }">
                        <div
                          class="
                            flex flex-row
                            mb-2
                            justify-between
                            transition-all
                          "
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
                              <el-input
                                v-model="element.orcid"
                                type="text"
                                placeholder="ORCID (e.g. 0000-0002-1825-0097)"
                              ></el-input>
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
                              class="
                                flex
                                justify-center
                                items-center
                                handle
                                text-gray-400
                                hover:text-gray-700
                              "
                            >
                              <Icon icon="ic:outline-drag-indicator" />
                            </div>
                            <div
                              class="
                                flex
                                justify-center
                                items-center
                                text-gray-600
                                hover:text-gray-800
                                cursor-pointer
                              "
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
                      class="
                        flex
                        items-center
                        cursor-pointer
                        text-gray-500
                        hover:text-black
                        w-max
                      "
                      @click="addContributor()"
                    >
                      <Icon icon="carbon:add" />
                      <span> Add an author </span>
                    </div>
                  </el-form-item>
                </div>
              </el-collapse-item>

              <el-collapse-item title="References" name="references">
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
                          class="
                            flex flex-row
                            mb-2
                            justify-between
                            transition-all
                          "
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
                              class="
                                flex
                                justify-center
                                items-center
                                handle
                                text-gray-400
                                hover:text-gray-700
                              "
                            >
                              <Icon icon="ic:outline-drag-indicator" />
                            </div>
                            <div
                              class="
                                flex
                                justify-center
                                items-center
                                text-gray-600
                                hover:text-gray-800
                                cursor-pointer
                              "
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
                      class="
                        flex
                        items-center
                        cursor-pointer
                        text-gray-500
                        hover:text-black
                        w-max
                      "
                      @click="addReference()"
                    >
                      <Icon icon="carbon:add" />
                      <span> Add a keyword </span>
                    </div>
                  </el-form-item>
                </div>
              </el-collapse-item>

              <el-collapse-item title="Journal" name="journal">
                <div>
                  <el-form-item label="Journal title">
                    <el-input
                      v-model="zenodoMetadataForm.journal.title"
                      type="text"
                    ></el-input>
                  </el-form-item>
                  <el-form-item label="Volume">
                    <el-input
                      v-model="zenodoMetadataForm.journal.volume"
                      type="text"
                    ></el-input>
                  </el-form-item>
                  <el-form-item label="Issue">
                    <el-input
                      v-model="zenodoMetadataForm.journal.issue"
                      type="text"
                    ></el-input>
                  </el-form-item>
                  <el-form-item label="Pages">
                    <el-input
                      v-model="zenodoMetadataForm.journal.pages"
                      type="text"
                    ></el-input>
                  </el-form-item>
                </div>
              </el-collapse-item>

              <el-collapse-item title="Conference" name="conference">
                <div>
                  <el-form-item label="Conference title">
                    <el-input
                      v-model="zenodoMetadataForm.conference.title"
                      type="text"
                    ></el-input>
                  </el-form-item>
                  <el-form-item label="Acronym">
                    <el-input
                      v-model="zenodoMetadataForm.conference.acronym"
                      type="text"
                    ></el-input>
                  </el-form-item>
                  <el-form-item label="Dates">
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
                  </el-form-item>
                  <el-form-item label="Place">
                    <el-input
                      v-model="zenodoMetadataForm.conference.place"
                      type="text"
                      placeholder="e.g. city, country"
                    ></el-input>
                  </el-form-item>
                  <el-form-item label="Website">
                    <el-input
                      v-model="zenodoMetadataForm.conference.website"
                      type="text"
                      placeholder="e.g. http://zenodo.org"
                    ></el-input>
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

              <el-collapse-item
                title="Book/Report/Chapter"
                name="bookReportChapter"
              >
                <p class="text-xs mb-4">
                  For parts of books and reports. <br />
                </p>
                <div>
                  <el-form-item label="Publisher">
                    <el-input
                      v-model="zenodoMetadataForm.bookReportChapter.publisher"
                      type="text"
                    ></el-input>
                  </el-form-item>
                  <el-form-item label="Place">
                    <el-input
                      v-model="zenodoMetadataForm.bookReportChapter.place"
                      type="text"
                      placeholder="e.g. city, country"
                    ></el-input>
                  </el-form-item>
                  <el-form-item label="ISBN">
                    <el-input
                      v-model="zenodoMetadataForm.bookReportChapter.isbn"
                      type="text"
                      placeholder="e.g. 0-06-251587-X"
                    ></el-input>
                  </el-form-item>
                  <el-form-item label="Book title">
                    <div class="flex flex-col">
                      <el-input
                        v-model="zenodoMetadataForm.bookReportChapter.title"
                        type="text"
                      ></el-input>
                      <p class="text-xs pt-2 text-gray-500">
                        Optional. Title of the book or report which this upload
                        is part of.
                      </p>
                    </div>
                  </el-form-item>
                  <el-form-item label="Pages">
                    <el-input
                      v-model="zenodoMetadataForm.bookReportChapter.pages"
                      type="text"
                    ></el-input>
                  </el-form-item>
                </div>
              </el-collapse-item>

              <el-collapse-item title="Thesis" name="thesis">
                <div>
                  <el-form-item label="Awarding university">
                    <el-input
                      v-model="zenodoMetadataForm.thesis.awardingUniversity"
                      type="text"
                    ></el-input>
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
                          class="
                            flex flex-row
                            mb-2
                            justify-between
                            transition-all
                          "
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
                            <el-input
                              v-model="element.orcid"
                              type="text"
                              placeholder="ORCID (e.g.: 0000-0002-1825-0097)"
                            ></el-input>
                            <div class="mx-2"></div>
                          </div>
                          <div class="flex flex-row justify-evenly w-1/12">
                            <div
                              class="
                                flex
                                justify-center
                                items-center
                                handle
                                text-gray-400
                                hover:text-gray-700
                              "
                            >
                              <Icon icon="ic:outline-drag-indicator" />
                            </div>
                            <div
                              class="
                                flex
                                justify-center
                                items-center
                                text-gray-600
                                hover:text-gray-800
                                cursor-pointer
                              "
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
                      class="
                        flex
                        items-center
                        cursor-pointer
                        text-gray-500
                        hover:text-black
                        w-max
                      "
                      @click="addSupervisor()"
                    >
                      <Icon icon="carbon:add" />
                      <span> Add a supervisor </span>
                    </div>
                  </el-form-item>
                </div>
              </el-collapse-item>

              <el-collapse-item title="Subjects" name="subjects">
                <p class="text-xs mb-4">
                  Specify subjects from a taxonomy or controlled vocabulary.
                  Each term must be uniquely identified (e.g. a URL). For free
                  form text, use the keywords field in basic information
                  section.
                  <br />
                </p>
                <div>
                  <el-form-item label="Subjects">
                    <draggable
                      tag="div"
                      :list="zenodoMetadataForm.subjects"
                      item-key="id"
                      handle=".handle"
                    >
                      <template #item="{ element }">
                        <div
                          class="
                            flex flex-row
                            mb-2
                            justify-between
                            transition-all
                          "
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
                              class="
                                flex
                                justify-center
                                items-center
                                handle
                                text-gray-400
                                hover:text-gray-700
                              "
                            >
                              <Icon icon="ic:outline-drag-indicator" />
                            </div>
                            <div
                              class="
                                flex
                                justify-center
                                items-center
                                text-gray-600
                                hover:text-gray-800
                                cursor-pointer
                              "
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
                      class="
                        flex
                        items-center
                        cursor-pointer
                        text-gray-500
                        hover:text-black
                        w-max
                      "
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
            <router-link to="/datasets" class="mx-6">
              <el-button type="danger" plain> Cancel </el-button>
            </router-link>

            <el-button
              type="primary"
              class="flex flex-row items-center"
              @click="addZenodoMetadata"
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

import { useDatasetsStore } from "../store/datasets";
import licensesJSON from "../assets/supplementalFiles/licenses.json";
import contributorTypesJSON from "../assets/supplementalFiles/contributorTypes.json";
import zenodoMetadataOptions from "../assets/supplementalFiles/zenodoMetadataOptions.json";
import languagesJSON from "../assets/supplementalFiles/zenodoLanguages.json";

export default {
  name: "DatasetsCurateZenodoMetadata",
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
      rulesForZenodoMetadataForm: zenodoMetadataOptions.defaultRules,
    };
  },
  computed: {
    dragOptions() {
      return {
        animation: 200,
        disabled: false,
      };
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
    addZenodoMetadata() {
      //validate first
      this.workflow = this.dataset.workflows[this.workflowID];

      this.workflow.expandOptions = [];

      this.workflow.destination.zenodo.questions = this.zenodoMetadataForm;
      this.datasetStore.updateCurrentDataset(this.dataset);
      this.datasetStore.syncDatasets();

      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/zenodo/review`;
      this.$router.push({ path: routerPath });
    },
  },
  async mounted() {
    this.loading = true;

    this.dataset = await this.datasetStore.getCurrentDataset();

    this.workflow = this.dataset.workflows[this.workflowID];

    if (this.workflow.expandOptions.length === 0) {
      this.activeNames = ["basicInformation", "license"];
    } else {
      this.activeNames = this.workflow.expandOptions;
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
    }

    this.loading = false;

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
