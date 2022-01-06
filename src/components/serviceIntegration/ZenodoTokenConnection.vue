<template>
  <div class="buttonContainer">
    <AppDialog
      v-if="dialogVisable"
      v-model="dialogVisable"
      :numInput="dialogNumInput"
      :headers="dialogHeaders"
      :callback="getInputs"
    ></AppDialog>
  </div>
</template>

<script>
import { useTokenStore } from "../../store/access";
import { ref } from "vue";
import { ElNotification } from "element-plus";
import { ElLoading } from "element-plus";
import AppDialog from "../dialogs/AppDialog";
export default {
  name: "ZenodoTokenConnection",
  components: { AppDialog },
  props: {
    callback: { type: Function },
  },
  setup() {
    const dialogVisable = ref(false);
    const dialogHeaders = ref(null);
    const dialogNumInput = ref(null);
    return {
      dialogVisable,
      dialogHeaders,
      dialogNumInput,
    };
  },
  data() {
    return {
      manager: useTokenStore(),
    };
  },
  computed: {
    connectedToZenodoByToken() {
      return (
        "zenodo" in this.manager.accessTokens &&
        this.manager.accessTokens.zenodo.type == "token"
      );
    },
  },
  methods: {
    createLoading() {
      const loading = ElLoading.service({
        lock: true,
        text: "Verifying...",
      });
      return loading;
    },
    openDialog() {
      this.useAPIkey();
    },
    async getInputs(response) {
      this.dialogVisable = false;
      if (response[0] == "OK") {
        await this.processZenodo(response[1]);
      } else {
        ElNotification({
          type: "info",
          message: "Input canceled",
          position: "bottom-right",
          duration: 2000,
        });
        this.callback();
      }
    },

    async processZenodo(userInput) {
      let key = "zenodo";
      let value = userInput[0];
      let spinner = this.createLoading();
      let errorFound = false;
      if (await this.manager.verifyZenodoToken(value)) {
        let tokenObject = {};
        let name = userInput[1];
        try {
          tokenObject.token = value;
          tokenObject.name = name;
          tokenObject.type = "token";
          await this.manager.saveToken(key, tokenObject);
        } catch (e) {
          // console.log(e);
          errorFound = true;
        }
        if (!errorFound) {
          ElNotification({
            type: "success",
            message: "Connected to Zenodo successfully",
            position: "bottom-right",
            duration: 2000,
          });
          this.callback();
        }
      } else {
        ElNotification({
          type: "error",
          message: "Could not verify the token provided",
          position: "bottom-right",
          duration: 2000,
        });
        this.callback();
      }
      spinner.close();
    },

    useAPIkey() {
      this.dialogNumInput = 2;
      this.dialogHeaders = ["Zenodo access token", "Token nick name"];
      this.dialogVisable = true;
    },
  },
  async mounted() {
    await this.manager.loadTokens();
    this.openDialog();
  },
};
</script>
