<template>
  <div
    class="
      page-Container
      h-screen
      w-full
      flex flex-col
      items-center
      overflow-scroll
      box-border
    "
  >
    <div class="app-Card">
      <div class="image-Container">
        <img src="../../assets/github.jpeg" class="image" />
      </div>
      <div class="app-Card-Content">
        <div class="app-Card-Status">
          <div class="centering-Container">
            <span
              class="dot"
              :style="{
                backgroundColor: status.githubToken[0],
              }"
            ></span>
          </div>

          <div class="centering-Container">
            <div
              class="app-Card-Status-Text"
              :style="{
                color: status.githubToken[1],
              }"
            >
              {{ status.githubToken[2] }}
            </div>
          </div>

          <div class="centering-Container tag-Container">
            <el-tag
              v-if="status.githubToken[2] === 'Connected'"
              type="success"
              effect="plain"
            >
              <el-avatar
                shape="square"
                size="small"
                src="https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png"
              ></el-avatar>
              {{ status.githubToken[4] }}
            </el-tag>
          </div>
        </div>
        <div class="centering-Container center">
          <span
            >Connect with your github account by using an access token or OAuth.
            Please see more details at
            <button
              type="text"
              class="link-Font"
              @click="
                openWebsite(
                  'https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token'
                )
              "
            >
              github access token documentation
            </button>
          </span>
        </div>
        <div class="centering-Container bottom">
          <el-button
            v-if="OAuthButtonVisable"
            plain
            class="button"
            @click="connectOAuth('githubOAuth')"
            >Connect via OAuth</el-button
          >
          <GithubTokenConnection></GithubTokenConnection>
        </div>
      </div>
    </div>

    <div class="app-Card">
      <div class="image-Container">
        <img
          src="https://about.zenodo.org/static/img/logos/zenodo-black-2500.png"
          class="image"
        />
      </div>
      <div class="app-Card-Content">
        <div class="app-Card-Status">
          <div class="centering-Container">
            <span
              class="dot"
              :style="{
                backgroundColor: status.zenodoToken[0],
              }"
            ></span>
          </div>

          <div class="centering-Container">
            <div
              class="app-Card-Status-Text"
              :style="{
                color: status.zenodoToken[1],
              }"
            >
              {{ status.zenodoToken[2] }}
            </div>
          </div>

          <div class="centering-Container tag-Container">
            <el-tag
              v-if="status.zenodoToken[2] === 'Connected'"
              type="success"
              effect="plain"
            >
              <el-avatar
                shape="square"
                size="small"
                src="https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png"
              ></el-avatar>
              {{ status.zenodoToken[4] }}
            </el-tag>
          </div>
        </div>
        <div class="centering-Container center">
          <span
            >Connect with your zenodo account by using an access token. Please
            see more details at
            <button
              type="text"
              class="link-Font"
              @click="
                openWebsite('https://developers.zenodo.org/#quickstart-upload')
              "
            >
              zenodo access token documentation
            </button>
          </span>
        </div>
        <div class="centering-Container bottom">
          <el-button
            plain
            :type="status.zenodoToken[5]"
            class="button"
            @click="openDialog('zenodoToken')"
            >{{ status.zenodoToken[3] }}</el-button
          >
        </div>
      </div>
    </div>

    <Dialog
      v-model="dialogVisable"
      :numInput="dialogNumInput"
      :headers="dialogHeaders"
      :callback="getInputs"
    ></Dialog>
  </div>
</template>

<script>
import { useTokenStore } from "../../store/access";
import { ElMessageBox } from "element-plus";
import { ElNotification } from "element-plus";
import { ref } from "vue";
import { ElLoading } from "element-plus";
import Dialog from "../../components/dialogs/Dialog";
import GithubTokenConnection from "../../components/serviceIntegration/GithubTokenConnection";
export default {
  name: "ManageAccount",
  components: { Dialog, GithubTokenConnection },
  setup() {
    const manager = useTokenStore();
    const githubOffline = ref(true);
    const zenodoOffline = ref(true);
    const dialogVisable = ref(false);
    const dialogOpener = ref(null);
    const dialogNumInput = ref(null);
    const dialogHeaders = ref([]);
    const OAuthButtonVisable = ref(true);
    const backgroundHasResponse = ref(false);
    const spinnerGlobal = ref(null);
    const status = ref({
      githubToken: [
        "lightgrey",
        "grey",
        "Not connected",
        "Connect token",
        "",
        "",
      ],
      zenodoToken: [
        "lightgrey",
        "grey",
        "Not connected",
        "Connect token",
        "",
        "",
      ],
    });

    async function getInputs(response) {
      dialogVisable.value = false;
      if (response[0] == "OK") {
        if (dialogOpener.value == "githubToken") {
          await processGithub(response[1]);
        } else if (dialogOpener.value == "zenodoToken") {
          await processZenodo(response[1]);
        }
        console.log("dialogOpener: ", dialogOpener.value);
      } else {
        ElNotification({
          type: "info",
          message: "Input canceled",
          position: "bottom-right",
          duration: 2000,
        });
      }
    }

    function updateStatus() {
      manager.getGithubTokenConnected().then((res) => {
        if (!res) {
          status.value.githubToken = [
            "lightgrey",
            "grey",
            "Not connected",
            "Connect token",
            "",
            "",
          ];
        } else {
          manager.getGithubUser("githubToken").then((name) => {
            console.log("name now: ", name);
            status.value.githubToken = [
              "lightgreen",
              "lightgreen",
              "Connected",
              "Disconnect",
              name,
              "danger",
            ];
          });
        }
      });
    }

    function useAPIkey(key) {
      if (key == "githubToken") {
        dialogOpener.value = "githubToken";
        dialogNumInput.value = 1;
        dialogHeaders.value = ["githubToken access token"];
      } else if (key == "zenodoToken") {
        dialogOpener.value = "zenodoToken";
        dialogNumInput.value = 2;
        dialogHeaders.value = ["zenodoToken access token", "Token nick name"];
      }
      dialogVisable.value = true;
    }

    function createLoading() {
      const loading = ElLoading.service({
        lock: true,
        text: "Verifying...",
      });
      return loading;
    }

    async function processZenodo(userInput) {
      console.log("user Input: ", userInput);
      let key = "zenodoToken";
      let spinner = createLoading();
      let errorFound = false;
      let value = userInput[0];

      if (await manager.checkZenodoToken(value)) {
        let name = userInput[1];
        let tokenObject = {};
        try {
          tokenObject.token = value;
          tokenObject.name = name;

          await manager.saveToken(key, tokenObject);
        } catch (e) {
          console.log(e);
          errorFound = true;
        }

        updateStatus(key, name);

        if (!errorFound) {
          ElNotification({
            type: "success",
            message: "Saved successfully",
            position: "bottom-right",
            duration: 2000,
          });
        }
      } else {
        ElNotification({
          type: "error",
          message: "Cannot verify the token provided",
          position: "bottom-right",
          duration: 2000,
        });
      }
      spinner.close();
    }

    async function processGithub(userInput) {
      let key = "githubToken";
      let value = userInput[0];
      let spinner = createLoading();
      let errorFound = false;
      if (await manager.checkGithubToken(value)) {
        let tokenObject = {};
        try {
          tokenObject.token = value;
          await manager.saveToken(key, tokenObject);
        } catch (e) {
          console.log(e);
          errorFound = true;
        }
        let name = await manager.getGithubUser();
        tokenObject.name = name;
        await manager.saveToken(key, tokenObject);
        updateStatus(key, name);
        if (!errorFound) {
          ElNotification({
            type: "success",
            message: "Saved successfully",
            position: "bottom-right",
            duration: 2000,
          });
        }
      } else {
        ElNotification({
          type: "error",
          message: "Cannot verify the token provided",
          position: "bottom-right",
          duration: 2000,
        });
      }
      spinner.close();
    }

    function APIkeyWarning(key) {
      let errorFound = false;
      ElMessageBox.confirm(
        "Disconnecting will delete the access token stored. Continue?",
        "Warning",
        {
          confirmButtonText: "OK",
          cancelButtonText: "Cancel",
          type: "warning",
        }
      )
        .then(async () => {
          try {
            await manager.deleteToken(key);
          } catch (e) {
            errorFound = true;
          }
          updateStatus(key, "");
          if (!errorFound) {
            ElNotification({
              type: "success",
              message: "Deleted",
              position: "bottom-right",
              duration: 2000,
            });
            OAuthButtonVisable.value = true;
          }
        })
        .catch(() => {
          ElNotification({
            type: "info",
            message: "Delete canceled",
            position: "bottom-right",
            duration: 2000,
          });
        });
    }
    const openDialog = (s) => {
      if (status.value[s][3] == "Connect token") {
        if (s == "githubToken" || s == "zenodoToken") {
          useAPIkey(s);
        }
      } else if (status.value[s][3] == "Disconnect") {
        if (s == "githubToken" || s == "zenodoToken") {
          APIkeyWarning(s);
        }
      }
    };

    async function connectOAuth(key) {
      if (key == "githubOAuth") {
        spinnerGlobal.value = createLoading();
        window.ipcRenderer.send("OAuth-Github", "test");
      }
    }
    return {
      manager,
      openDialog,
      githubOffline,
      zenodoOffline,
      status,
      updateStatus,
      createLoading,
      dialogVisable,
      getInputs,
      dialogOpener,
      dialogNumInput,
      dialogHeaders,
      OAuthButtonVisable,
      connectOAuth,
      backgroundHasResponse,
      spinnerGlobal,
      processGithub,
    };
  },
  watch: {
    // whenever question changes, this function will run
    backgroundHasResponse: function () {
      console.log("catched!");
      this.manager.getToken("githubOAuth").then((res) => {
        this.processGithub([res.token]);
        this.spinnerGlobal.close();
        this.OAuthButtonVisable = false;
        this.manager.checkGithubToken(res.token).then((res) => {
          console.log("check???: ", res);
        });
      });
    },
  },
  data() {
    return {
      dialogFormVisible: true,
    };
  },
  methods: {
    openWebsite(url) {
      window.ipcRenderer.send("open-link-in-browser", url);
    },
  },
  async mounted() {
    window.ipcRenderer.on("OAuth-Github-Reply", async (_e, _arg) => {
      if (_arg == "failed") {
        ElNotification({
          type: "error",
          message: "Login failed",
          position: "bottom-right",
          duration: 2000,
        });
        this.spinnerGlobal.close();
      } else if (this.manager.checkGithubToken(_arg)) {
        console.log("passed!");
        let tokenObject = {};
        tokenObject.token = _arg;
        await this.manager.saveToken("githubOAuth", tokenObject);
        let name = await this.manager.getGithubUser("githubOAuth",);
        tokenObject.name = name;
        await this.manager.saveToken("githubOAuth", tokenObject);
        this.backgroundHasResponse = true;
      }
    });

    await this.manager.loadTokens();
    this.updateStatus();
  },
};
</script>

<style scoped>
.page-Container {
  gap: 5vw;
  padding-top: 5vh;
  padding-bottom: 5vh;
}

.app-Card {
  display: flex;
  height: 20vh;
  width: 70%;
  padding: 0px;
  padding-top: 1vh;
  border-radius: 0.25em;
  box-shadow: 0 3px 5px rgba(0, 0, 0, 0.15);
  transition: all 0.6s cubic-bezier(0.165, 0.84, 0.44, 1);
  box-sizing: border-box;
}

.image-Container {
  height: 100%;
  width: 30%;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.app-Card-Content {
  display: flex;
  flex-direction: column;
  width: 70%;
  gap: 1vh;
  box-sizing: border-box;
}

.dot {
  height: 12px;
  width: 12px;
  border-radius: 50%;
  display: inline-block;
}

.disconnected-Text {
  color: grey;
}

.disconnected-Dot {
  background-color: lightgray;
}

.app-Card-Status {
  height: 15%;
  display: flex;
  gap: 0.5vw;

  box-sizing: border-box;
}

.centering-Container {
  display: flex;
  align-items: center;
  justify-content: center;
}

.center {
  height: 55%;
  padding-top: 0.5vh;
  padding-bottom: 0.5vh;
  padding-right: 0.8vw;
  box-sizing: border-box;
  align-items: flex-start;
  justify-content: flex-start;
  overflow: auto;
  color: rgb(99, 99, 99);
}
::-webkit-scrollbar {
  display: none;
}

.bottom {
  height: 30%;
  justify-content: flex-end;
  padding-right: 2.2vw;
  box-sizing: border-box;
  padding-bottom: 1vh;
  display: flex;
  gap: 1vw;
}

.link-Font {
  color: #409eff;
}

.tag-Container {
  box-sizing: border-box;
  margin-left: 0.5vw;
}

.el-button {
  padding: 0px;
  min-height: 0px;
  padding-top: 1vh;
  padding-bottom: 1vh;
  padding-left: 1vw;
  padding-right: 1vw;
}

.el-tag {
  padding: 0px;
  min-height: 0px;
  height: auto;
  line-height: 0px;
  padding-top: 0.4vh;
  padding-bottom: 0.4vh;
  padding-left: 0.5vw;
  padding-right: 0.5vw;
  font-size: 15px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.el-tag--plain.el-tag--success {
  --el-tag-background-color: white;
  --el-tag-border-color: lightgreen;
  --el-tag-font-color: lightgreen;
  --el-tag-hover-color: lightgreen;
}

.el-avatar--small {
  height: 12px;
  width: 12px;
  line-height: 12px;
}
</style>
