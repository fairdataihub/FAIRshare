<template>
  <div class="h-screen w-full flex flex-row">Home</div>
</template>

<script>
// import licensesJSON from "../assets/supplementalFiles/licenses.json";

export default {
  name: "HomePage",
  data() {
    return {
      // licenseOptions: licensesJSON.licenses,
      // sortedLicenses: [],
    };
  },
  methods: {
    // SortArray(x, y) {
    //   return x.name.localeCompare(y.name);
    // },
  },
  mounted() {
    // sort licenses alphabetically
    // this.sortedLicenses = this.licenseOptions.sort(this.SortArray);
    // console.log(this.sortedLicenses);
  },
};
</script>
