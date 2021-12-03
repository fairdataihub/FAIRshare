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
                backgroundColor: status.github[0],
              }"
            ></span>
          </div>
          <div class="centering-Container">
            <div
              class="app-Card-Status-Text"
              :style="{
                color: status.github[1],
              }"
            >
              {{ status.github[2] }}
            </div>
          </div>
        </div>
        <div class="centering-Container center">
          <span
            >Connect with your github account by using an access token. Please
            see more details at
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
            plain
            class="button"
            @click="openDialog($event, 'github')"
            >{{ status.github[3] }}</el-button
          >
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
                backgroundColor: status.zenodo[0],
              }"
            ></span>
          </div>
          <div class="centering-Container">
            <div
              class="app-Card-Status-Text"
              :style="{
                color: status.zenodo[1],
              }"
            >
              {{ status.zenodo[2] }}
            </div>
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
            class="button"
            @click="openDialog($event, 'zenodo')"
            >{{ status.zenodo[3] }}</el-button
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useTokenStore } from "../../store/access";
import { ElMessageBox } from "element-plus";
import { ElNotification } from "element-plus";
import { ref } from "vue";
import { ElLoading } from "element-plus";
export default {
  name: "ManageAccount",
  setup() {
    const manager = useTokenStore();
    const githubOffline = ref(true);
    const zenodoOffline = ref(true);
    const status = ref({
      github: ["lightgrey", "grey", "Disconnected", "Connect"],
      zenodo: ["lightgrey", "grey", "Disconnected", "Connect"],
    });

    function updateStatus(key) {
      manager.getToken(key).then((value) => {
        if (key == "github") {
          if (value == "NO_TOKEN_FOUND") {
            githubOffline.value = true;
            status.value.github = [
              "lightgrey",
              "grey",
              "Disconnected",
              "Connect",
            ];
          } else {
            githubOffline.value = false;
            status.value.github = [
              "lightgreen",
              "lightgreen",
              "Connected",
              "Disconnect",
            ];
          }
        }

        if (key == "zenodo") {
          if (value == "NO_TOKEN_FOUND") {
            zenodoOffline.value = true;
            status.value.zenodo = [
              "lightgrey",
              "grey",
              "Disconnected",
              "Connect",
            ];
          } else {
            zenodoOffline.value = false;
            status.value.zenodo = [
              "lightgreen",
              "lightgreen",
              "Connected",
              "Disconnect",
            ];
          }
        }
      });
    }

    function useAPIkey(key) {
      ElMessageBox.prompt("Please input your API key", "", {
        confirmButtonText: "OK",
        cancelButtonText: "Cancel",
      })
        .then(async ({ value }) => {
          if (key == "zenodo") {
            processZenodo(key, value);
          } else if (key == "github") {
            processGithub(key, value);
          }
        })
        .catch(() => {
          ElNotification({
            type: "info",
            message: "Input canceled",
            position: "bottom-right",
            duration: 2000,
          });
        });
    }

    function createLoading() {
      const loading = ElLoading.service({
        lock: true,
        text: "Verifying...",
      });
      return loading;
    }

    async function processZenodo(key, value) {
      let spinner = createLoading();
      let errorFound = false;
      if (await manager.checkZenodoToken(value)) {
        try {
          await manager.saveToken(key, value);
        } catch (e) {
          console.log(e);
          errorFound = true;
        }
        updateStatus(key);
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

    async function processGithub(key, value) {
      let spinner = createLoading();
      let errorFound = false;
      if (await manager.checkGithubToken(value)) {
        try {
          await manager.saveToken(key, value);
        } catch (e) {
          console.log(e);
          errorFound = true;
        }
        updateStatus(key);
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
          updateStatus(key);
          if (!errorFound) {
            ElNotification({
              type: "success",
              message: "Deleted",
              position: "bottom-right",
              duration: 2000,
            });
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
    const openDialog = (e, s) => {
      if (e.target.innerHTML == "Connect") {
        if (s == "github" || s == "zenodo") {
          useAPIkey(s);
        }
      } else if (e.target.innerHTML == "Disconnect") {
        if (s == "github" || s == "zenodo") {
          APIkeyWarning(s);
        }
      }
    };
    return {
      manager,
      openDialog,
      githubOffline,
      zenodoOffline,
      status,
      updateStatus,
      createLoading,
    };
  },
  data() {
    return {};
  },
  methods: {
    openWebsite(url) {
      window.ipcRenderer.send("open-link-in-browser", url);
    },
  },
  async mounted() {
    await this.manager.loadTokens();
    this.updateStatus("github");
    this.updateStatus("zenodo");
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
  height: 10%;
  display: flex;
  gap: 0.5vw;
}

.centering-Container {
  display: flex;
  align-items: center;
  justify-content: center;
}

.center {
  height: 60%;
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
}

.link-Font {
  color: #409eff;
}

.el-button {
  padding: 0px;
  min-height: 0px;
  padding-top: 1vh;
  padding-bottom: 1vh;
  padding-left: 1vw;
  padding-right: 1vw;
}
</style>
