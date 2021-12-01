import { defineStore } from "pinia";
export const useManage = defineStore({
  // id is required so that Pinia can connect the store to the devtools
  id: "manageAccount",
  state: () => ({
    statusText: "Disconnected",
    apiKeys: { zenodo: "", github: "", placeholder: "" },
  }),
  getters: {
    getStatusText() {
      return this.statusText;
    },
  },
  actions: {
    checkApiKey(value) {
      return this.apiKeys[value];
    },

    async changeStatus(newStatus) {
      try {
        this.statusText = newStatus;
      } catch (error) {
        console.log(error);
      }
    },

    async changeApiKey(key, value) {
      try {
        this.apiKeys[key] = value;
        return "OK";
      } catch (error) {
        console.log(error);
        return "ERROR";
      }
    },
  },
});
