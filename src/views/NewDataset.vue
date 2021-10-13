<template>
  <div class="h-screen w-full flex flex-row items-center overflow-y-auto">
    <div class="p-3 h-full flex flex-row items-center">
      <div class="flex flex-col h-full">
        <span class="font-inter text-base font-medium">
          Create a new dataset
        </span>
        <span class="font-inter text-base">
          Fill out some general details about your dataset here.
        </span>
        <el-divider content-position="left" class="font-inter">
          Click on one of the datasets below</el-divider
        >

        <el-form ref="form" :model="form" label-width="120px" @submit.prevent>
          <el-form-item label="Activity name">
            <el-input v-model="form.name"></el-input>
          </el-form-item>
          <el-form-item label="Activity zone">
            <el-select
              v-model="form.region"
              placeholder="please select your zone"
            >
              <el-option label="Zone one" value="shanghai"></el-option>
              <el-option label="Zone two" value="beijing"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Activity time">
            <el-col :span="11">
              <el-date-picker
                v-model="form.date1"
                type="date"
                placeholder="Pick a date"
                style="width: 100%"
              ></el-date-picker>
            </el-col>
            <el-col class="line" :span="2">-</el-col>
            <el-col :span="11">
              <el-time-picker
                v-model="form.date2"
                placeholder="Pick a time"
                style="width: 100%"
              ></el-time-picker>
            </el-col>
          </el-form-item>
          <el-form-item label="Instant delivery">
            <el-switch v-model="form.delivery"></el-switch>
          </el-form-item>
          <el-form-item label="Activity type">
            <el-checkbox-group v-model="form.type">
              <el-checkbox label="Online activities" name="type"></el-checkbox>
              <el-checkbox
                label="Promotion activities"
                name="type"
              ></el-checkbox>
              <el-checkbox label="Offline activities" name="type"></el-checkbox>
              <el-checkbox
                label="Simple brand exposure"
                name="type"
              ></el-checkbox>
            </el-checkbox-group>
          </el-form-item>
          <el-form-item label="Resources">
            <el-radio-group v-model="form.resource">
              <el-radio label="Sponsor"></el-radio>
              <el-radio label="Venue"></el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="Activity form">
            <el-input v-model="form.desc" type="textarea"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary">Create</el-button>
            <el-button>Cancel</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
// import { Icon } from "@iconify/vue";
// import { v4 as uuidv4 } from "uuid";

export default {
  name: "NewDataset",
  // components: { Icon },

  data() {
    return {
      form: {
        name: "",
        region: "",
        date1: "",
        date2: "",
        delivery: false,
        type: [],
        resource: "",
        desc: "",
      },
    };
  },
  methods: {},
  mounted() {},
};
</script>

<style>
#unpublishedDatasets::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
  background-color: #f5f5f5;
}

#unpublishedDatasets::-webkit-scrollbar {
  width: 6px;
  background-color: #f5f5f5;
}

#unpublishedDatasets::-webkit-scrollbar-thumb {
  background-color: #424242;
}

::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
  background-color: #f5f5f5;
}

::-webkit-scrollbar {
  width: 6px;
  background-color: #f5f5f5;
}

::-webkit-scrollbar-thumb {
  background-color: #424242;
}
</style>
