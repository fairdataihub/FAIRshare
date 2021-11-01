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

          <span class="mb-2">
            Before we send this data over, Zenodo requires some metadata from
            you. We have filled any information we have learned from the data as
            well as your previous metadata.
          </span>

          <el-form
            :model="zenodoMetadataForm"
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
                  <el-form-item label="Publication Date">
                    <el-date-picker
                      v-model="zenodoMetadataForm.publicationDate"
                      type="date"
                      placeholder="Pick a day"
                    >
                    </el-date-picker>
                  </el-form-item>

                  <el-form-item label="Title" >
                    <Popper :hover="true"
                      content="Use a description that is easily identifiable. This will
                        be shown in the dataset selection screen and is not part
                        of your submitted metadata."
                    >
                      <el-input
                        v-model="zenodoMetadataForm.title"
                        type="text"
                      > text </el-input>
                    </Popper>

                    <el-popover
                      ref="popover"
                      placement="bottom"
                      :width="300"
                      trigger="manual"
                    >
                      <template #reference>
                        <el-input
                          v-model="zenodoMetadataForm.title"
                          type="text"
                        ></el-input>
                      </template>

                      <span class="break-normal text-left text-sm">
                        Use a description that is easily identifiable. This will
                        be shown in the dataset selection screen and is not part
                        of your submitted metadata.
                      </span>
                    </el-popover>
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
                                @confirm="
                                  deleteAuthor(
                                    element.name,
                                    element.affiliation,
                                    element.orcid
                                  )
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

                  <el-form-item label="Description">
                    <el-popover
                      ref="popover"
                      placement="bottom"
                      :width="300"
                      trigger="hover"
                      content=""
                    >
                      <template #reference>
                        <el-input
                          v-model="zenodoMetadataForm.description"
                          type="textarea"
                        ></el-input>
                      </template>

                      <span class="break-normal text-left text-sm">
                        Use a description that is easily identifiable. This will
                        be shown in the dataset selection screen and is not part
                        of your submitted metadata.
                      </span>
                    </el-popover>
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
                    <el-popover
                      ref="popover"
                      placement="bottom"
                      :width="300"
                      trigger="manual"
                    >
                      <template #reference>
                        <el-input
                          v-model="zenodoMetadataForm.language"
                          type="text"
                          placeholder="e.g.: 'eng', 'fr' or 'Polish'"
                        ></el-input>
                      </template>

                      <span class="break-normal text-left text-sm">
                        Optional. Primary language of the record. Start by
                        typing the language's common name in English, or its ISO
                        639 code (two or three-letter code).
                        <br />
                        See
                        <a href="https://semver.org/" target="_blank">
                          ISO 639 language codes list
                        </a>
                        for more information.
                      </span>
                    </el-popover>
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
                  <el-form-item label="Access right">
                    <div class="flex flex-col">
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
                          <el-icon> <remove-filled /> </el-icon> Embargoed
                          Access
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
                    </div>
                  </el-form-item>

                  <el-form-item label="Access right">
                    <div class="flex flex-col">
                      <el-select
                        v-model="zenodoMetadataForm.license.licenseName"
                        filterable
                        placeholder="Select a license"
                      >
                        <el-option
                          v-for="item in licenseOptions"
                          :key="item.value"
                          :label="item.label"
                          :value="item.value"
                        >
                        </el-option>
                      </el-select>
                      <p class="text-xs pt-2 text-gray-500">
                        Required. Selected license applies to all of your files
                        displayed on the top of the form. If you want to upload
                        some of your files under different licenses, please do
                        so in separate uploads. If you cannot find the license
                        you're looking for, include a relevant LICENSE file in
                        your record and choose one of the
                        <span class="italic"> Other </span> licenses available
                        <span class="italic">
                          (Other (Open), Other (Attribution) </span
                        >, etc.). The supported licenses in the list are
                        harvested from
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
                    </div>
                  </el-form-item>
                  <el-form-item label=""> </el-form-item>
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
                <span class="text-xs">
                  Specify identifiers of related publications and datasets.
                  Supported identifiers include: DOI, Handle, ARK, PURL, ISSN,
                  ISBN, PubMed ID, PubMed Central ID, ADS Bibliographic Code,
                  arXiv, Life Science Identifiers (LSID), EAN-13, ISTC, URNs and
                  URLs.
                </span>
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
                            <el-input
                              v-model="element.identifier"
                              type="text"
                              placeholder="e.g. 10.1234/foobar.56789"
                            ></el-input>
                            <div class="mx-2"></div>
                            <el-input
                              v-model="element.relationship"
                              type="text"
                            ></el-input>
                            <div class="mx-2"></div>
                            <el-input
                              v-model="element.resourceType"
                              type="text"
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
                                @confirm="
                                  deleteRelatedIdentifier(
                                    element.identifier,
                                    element.relationship,
                                    element.resourceType
                                  )
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
                            <el-input
                              v-model="element.name"
                              type="text"
                              placeholder="Family Name, Given Name"
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
                              placeholder="ORCID (e.g. 0000-0002-1825-0097)"
                            ></el-input>
                            <div class="mx-2"></div>
                            <el-input
                              v-model="element.contributorType"
                              type="text"
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
                                @confirm="
                                  deleteContributor(
                                    element.name,
                                    element.affiliation,
                                    element.orcid,
                                    element.contributorType
                                  )
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
                <span class="text-xs"> For parts of books and reports. </span>
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
                        v-model="zenodoMetadataForm.bookReportChapter.bookTitle"
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
                                @confirm="
                                  deleteSupervisor(
                                    element.name,
                                    element.affiliation,
                                    element.orcid
                                  )
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
                                @confirm="
                                  deleteSubject(
                                    element.term,
                                    element.identifier
                                  )
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
              @click="navigateToSelectDestination"
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

import { useDatasetsStore } from "../store/datasets";

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
      activeNames: ["basicInformation", "license", "subjects"],
      drag: true,
      licenseOptions: [
        {
          value: "CC0-1.0",
          label: "CC0 1.0 Universal (CC0 1.0) - Attribution",
        },
        {
          value: "CC-BY-4.0",
          label: "CC BY 4.0 Attribution (CC BY 4.0)",
        },
      ],
      zenodoMetadataForm: {
        publicationDate: "",
        title: "",
        authors: [],
        description: "",
        version: "",
        language: "",
        keywords: [],
        additionalNotes: "",
        license: {
          accessRight: "openAccess",
          licenseName: "",
          embargoDate: "",
          conditions: "",
        },
        grants: [
          {
            grantInstitution: "",
            grantName: "",
          },
        ],
        relatedIdentifiers: [],
        contributors: [],
        references: [],
        journal: {
          title: "",
          volume: "",
          issue: "",
          pages: "",
          year: "",
        },
        conference: {
          title: "",
          acronym: "",
          dates: "",
          place: "",
          website: "",
          session: "",
          part: "",
        },
        bookReportChapter: {
          publisher: "",
          place: "",
          isbn: "",
          bookTitle: "",
          pages: "",
        },
        thesis: {
          awardingUniversity: "",
          supervisors: [],
        },
        subjects: [],
      },
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
    navigateToSelectDestination() {
      this.datasetStore.updateCurrentDataset(this.dataset);

      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/selectDestination`;
      this.$router.push({ path: routerPath });
    },
    addIds(array) {
      array.forEach((element, index) => {
        element.id = index;
      });
    },
    addSubject() {
      if (this.zenodoMetadataForm.subjects.length === 0) {
        this.zenodoMetadataForm.subjects.push({
          term: "",
          identifier: "",
          id: 0,
        });
      } else {
        this.zenodoMetadataForm.subjects.push({
          term: "",
          identifier: "",
          id:
            this.zenodoMetadataForm.subjects[
              this.zenodoMetadataForm.subjects.length - 1
            ].id + 1,
        });
      }
    },
    deleteSubject(term, identifier) {
      this.zenodoMetadataForm.subjects =
        this.zenodoMetadataForm.subjects.filter((subject) => {
          return subject.term !== term && subject.identifier !== identifier;
        });
    },
    addAuthor() {
      if (this.zenodoMetadataForm.authors.length === 0) {
        this.zenodoMetadataForm.authors.push({
          contributorType: "",
          name: "",
          affiliation: "",
          orcid: "",
          id: 0,
        });
      } else {
        this.zenodoMetadataForm.authors.push({
          contributorType: "",
          name: "",
          affiliation: "",
          orcid: "",
          id:
            this.zenodoMetadataForm.authors[
              this.zenodoMetadataForm.authors.length - 1
            ].id + 1,
        });
      }
    },
    deleteAuthor(name, affiliation, orcid) {
      this.zenodoMetadataForm.authors = this.zenodoMetadataForm.authors.filter(
        (author) => {
          return (
            author.name !== name &&
            author.affiliation !== affiliation &&
            author.orcid !== orcid
          );
        }
      );
    },
    addKeyword() {
      if (this.zenodoMetadataForm.keywords.length === 0) {
        this.zenodoMetadataForm.keywords.push({
          keyword: "",
          id: 0,
        });
      } else {
        this.zenodoMetadataForm.keywords.push({
          keyword: "",
          id:
            this.zenodoMetadataForm.keywords[
              this.zenodoMetadataForm.keywords.length - 1
            ].id + 1,
        });
      }
    },
    deleteKeyword(id) {
      this.zenodoMetadataForm.keywords =
        this.zenodoMetadataForm.keywords.filter((keyword) => {
          return keyword.id !== id;
        });
    },
    addRelatedIdentifier() {
      if (this.zenodoMetadataForm.relatedIdentifiers.length === 0) {
        this.zenodoMetadataForm.relatedIdentifiers.push({
          identifier: "",
          relationship: "",
          resourceType: "",
          id: 0,
        });
      } else {
        this.zenodoMetadataForm.relatedIdentifiers.push({
          identifier: "",
          relationship: "",
          resourceType: "",
          id:
            this.zenodoMetadataForm.relatedIdentifiers[
              this.zenodoMetadataForm.relatedIdentifiers.length - 1
            ].id + 1,
        });
      }
    },
    deleteRelatedIdentifier(identifier, relationship, resourceType) {
      this.zenodoMetadataForm.relatedIdentifiers =
        this.zenodoMetadataForm.relatedIdentifiers.filter(
          (relatedIdentifier) => {
            return (
              relatedIdentifier.identifier !== identifier &&
              relatedIdentifier.relationship !== relationship &&
              relatedIdentifier.resourceType !== resourceType
            );
          }
        );
    },
    addContributor() {
      if (this.zenodoMetadataForm.contributors.length === 0) {
        this.zenodoMetadataForm.contributors.push({
          contributorType: "",
          name: "",
          affiliation: "",
          orcid: "",
          id: 0,
        });
      } else {
        this.zenodoMetadataForm.contributors.push({
          contributorType: "",
          name: "",
          affiliation: "",
          orcid: "",
          id:
            this.zenodoMetadataForm.contributors[
              this.zenodoMetadataForm.contributors.length - 1
            ].id + 1,
        });
      }
    },
    deleteContributor(name, affiliation, orcid, contributorType) {
      this.zenodoMetadataForm.contributors =
        this.zenodoMetadataForm.contributors.filter((contributor) => {
          return (
            contributor.name !== name &&
            contributor.affiliation !== affiliation &&
            contributor.orcid !== orcid &&
            contributor.contributorType !== contributorType
          );
        });
    },
    addReference() {
      if (this.zenodoMetadataForm.references.length === 0) {
        this.zenodoMetadataForm.references.push({
          reference: "",
          id: 0,
        });
      } else {
        this.zenodoMetadataForm.references.push({
          reference: "",
          id:
            this.zenodoMetadataForm.references[
              this.zenodoMetadataForm.references.length - 1
            ].id + 1,
        });
      }
    },
    deleteReference(id) {
      this.zenodoMetadataForm.references =
        this.zenodoMetadataForm.references.filter((reference) => {
          return reference.id !== id;
        });
    },
    addSupervisor() {
      if (this.zenodoMetadataForm.thesis.supervisors.length === 0) {
        this.zenodoMetadataForm.thesis.supervisors.push({
          name: "",
          affiliation: "",
          orcid: "",
          id: 0,
        });
      } else {
        this.zenodoMetadataForm.thesis.supervisors.push({
          name: "",
          affiliation: "",
          orcid: "",
          id:
            this.zenodoMetadataForm.thesis.supervisors[
              this.zenodoMetadataForm.thesis.supervisors.length - 1
            ].id + 1,
        });
      }
    },
    deleteSupervisor(name, affiliation, orcid) {
      this.zenodoMetadataForm.thesis.supervisors =
        this.zenodoMetadataForm.thesis.supervisors.filter((supervisor) => {
          return (
            supervisor.name !== name &&
            supervisor.affiliation !== affiliation &&
            supervisor.orcid !== orcid
          );
        });
    },
  },
  mounted() {
    this.dataset = this.datasetStore.currentDataset;
    this.workflow = this.dataset.workflows[this.workflowID];

    this.addIds(this.zenodoMetadataForm.subjects);

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
</style>
