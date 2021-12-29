<template>
  <div
    class="
      h-full
      w-full
      flex flex-col
      justify-center
      items-center
      p-3
      px-5
      max-w-screen-lg
    "
  >
    <div class="flex flex-col h-full w-full">
      <span class="font-medium"> Start a new data curation project </span>
      <span> Fill out some general details about your dataset here. </span>

      <el-divider> </el-divider>

      <el-form
        ref="datasetForm"
        :model="datasetForm"
        label-width="150px"
        @submit.prevent
        :rules="rules"
      >
        <el-form-item label="Project name" prop="datasetName">
          <el-input v-model="datasetForm.datasetName"></el-input>
        </el-form-item>

        <el-form-item label="Project description">
          <el-popover
            ref="popover"
            placement="bottom"
            :width="300"
            trigger="manual"
          >
            <template #reference>
              <el-input
                v-model="datasetForm.datasetDescription"
                type="textarea"
              ></el-input>
            </template>

            <span class="break-normal text-left text-sm">
              Use a description that is easily identifiable. This will be shown
              in the dataset selection screen and is not part of your submitted
              metadata.
            </span>
          </el-popover>
        </el-form-item>

        <el-form-item
          label="Data type"
          prop="dataType"
          class="createNewProjectFormItemContainer"
        >
          <el-checkbox-group
            v-model="datasetForm.dataType"
            class="checkbox-group"
          >
            <div class="flex gap-4">
              <el-checkbox
                border
                name="type1"
                class="single-check-box"
                label="Research software"
              >
                <div class="flex flex-col items-center">
                  <monitor class="h-6 w-6"></monitor>
                  <span class="text-xs">Research</span>
                  <span class="text-xs">software</span>
                </div>
              </el-checkbox>

              <el-checkbox border name="type" class="single-check-box" label="Immunology">
                <div class="flex flex-col items-center">
                  <Icon icon="mdi:virus-outline" class="h-6 w-6"/>
                  <span class="text-xs">Immunology</span>
                </div>
              </el-checkbox>

              <el-checkbox border name="type" class="single-check-box" label="Epidemiology">
                <div class="flex flex-col items-center">
                  <Icon icon="healthicons:virus-patient-outline" class="h-6 w-6"/>
                  <span class="text-xs">Epidemiology</span>
                </div>
              </el-checkbox>
            <!-- </div>

            <div class="flex"> -->
              <el-checkbox border name="type" class="single-check-box" label="Genomic">
                <div class="flex flex-col items-center">
                  <Icon icon="uil:dna" class="h-6 w-6"/>
                  <span class="text-xs">Genomic</span>
                </div>
              </el-checkbox>

              <el-checkbox border name="type" class="single-check-box" label="Document">
                <div class="flex flex-col items-center">
                  <document class="h-6 w-6"></document>
                  <span class="text-xs">Document</span>
                </div>
              </el-checkbox>

              <el-checkbox border name="type" class="single-check-box" label="Media">
                <div class="flex flex-col items-center">
                  <video-play class="h-6 w-6"></video-play>
                  <span class="text-xs">Media</span>
                </div>
              </el-checkbox>
            </div>

          </el-checkbox-group>
        </el-form-item>

        <div class="py-2 flex flex-row justify-center space-x-4">
          <el-button @click="cancelNewDataset" type="danger" plain>
            <el-icon><d-arrow-left /></el-icon> Cancel
          </el-button>

          <button class="primary-button" @click="submitForm('datasetForm')">
            Create new project <el-icon><d-arrow-right /></el-icon>
          </button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
import { v4 as uuidv4 } from "uuid";
import { useDatasetsStore } from "../../store/datasets";
import { ElNotification } from "element-plus";
import { Icon } from '@iconify/vue';
export default {
  name: "CreateNewProject",
  components: {
		Icon,
	},
  data() {
    return {
      datasetStore: useDatasetsStore(),
      datasetForm: {
        datasetName: "",
        datasetDescription: "",
        dataType: [],
      },
      rules: {
        datasetName: [
          {
            required: true,
            message: "Please type a dataset name",
            trigger: "blur",
          },
        ],
        dataType: [
          {
            type: "array",
            required: true,
            message: "Please select at least one data type",
            trigger: "change",
          },
        ],
      },
    };
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          const datasetID = uuidv4();
          const datasetImage = `https://avatars.dicebear.com/api/jdenticon/${uuidv4()}.svg`;

          const index = this.datasetForm.dataType.indexOf("Research software");

          if (index !== -1) {
            this.datasetForm.dataType[index] = "Code";
          }

          let dataset = {
            id: datasetID,
            image: datasetImage,
            name: this.datasetForm.datasetName,
            description: this.datasetForm.datasetDescription,
            dataType: this.datasetForm.dataType,
            data: {},
            workflowConfirmed: false,
          };

          dataset.data.general = {
            questions: {},
          };

          for (const type of dataset.dataType) {
            let tempType = type;
            console.log(type);
            if (tempType == "Research software") {
              tempType = "Code";
            }
            dataset.data[tempType] = {
              uploaded: false,
              questions: {},
            };
          }

          this.datasetStore.addDataset(dataset, datasetID);

          ElNotification({
            type: "success",
            message: "Created your new project!",
            position: "bottom-right",
            duration: 3000,
          });

          this.$router.push({ path: `/datasets/new/${datasetID}/confirm` });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    cancelNewDataset() {
      this.$router.push({ name: "ShowAllProjects" });
    },
  },
  mounted() {
    document
      .querySelectorAll(
        ".createNewProjectFormItemContainer .el-checkbox__label"
      )
      .forEach((el) => {
        el.style.paddingLeft = "0px";
      });

    document
      .querySelectorAll(".createNewProjectFormItemContainer .el-checkbox")
      .forEach((el) => {
        el.style.display = "flex";
        el.style.flexDirection = "column-reverse";
        el.style.gap = "2px";
      });
    document
      .querySelectorAll(
        ".createNewProjectFormItemContainer .el-checkbox__input"
      )
      .forEach((el) => {
        el.style.display = "none";
      });
    
    document
      .querySelectorAll(
        ".createNewProjectFormItemContainer .el-checkbox.is-bordered"
      )
      .forEach((el) => {
        el.style.padding = "0px";
        // el.style.width = "100px";
        // el.style.height = "100px";
      });

      document
      .querySelectorAll(
        ".createNewProjectFormItemContainer .el-checkbox.is-bordered+.el-checkbox.is-bordered"
      )
      .forEach((el) => {
        el.style.marginLeft = "0px";
      });

      document
      .querySelectorAll(
        ".createNewProjectFormItemContainer .el-checkbox"
      )
      .forEach((el) => {
        el.style.marginRight = "0px";
      });
  },
};
</script>
<style scoped>
.checkbox-group {
  display: flex;
  flex-direction: column;
  padding-top: 10px;
  box-sizing: border-box;
  gap: 20px;
}
.single-check-box {
  width: 100px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
