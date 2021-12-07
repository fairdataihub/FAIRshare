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

          <div class="centering-Container tag-Container">
            <el-tag
              v-if="status.github[2] === 'Connected'"
              type="success"
              effect="plain"
            >
              <el-avatar shape="square" size="small" src='https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png'></el-avatar>
              {{ status.github[4] }}
            </el-tag>
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
          <el-button plain :type="status.github[5]" class="button" @click="openDialog('github')">{{
            status.github[3]
          }}</el-button>
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
          <el-button plain :type="status.zenodo[5]" class="button" @click="openDialog('zenodo')">{{
            status.zenodo[3]
          }}</el-button>
        </div>
      </div>
    </div>

    <Dialog v-model="dialogFormVisible"></Dialog>
  </div>
</template>

<script>
import { useTokenStore } from "../../store/access";
import { h } from 'vue'
import { ElMessageBox } from "element-plus";
import { ElNotification } from "element-plus";
import { ref } from "vue";
import { ElLoading } from "element-plus";
import Dialog from "../../components/dialogs/Dialog";
export default {
  name: "ManageAccount",
  components: {Dialog},
  setup() {
    const manager = useTokenStore();
    const githubOffline = ref(true);
    const zenodoOffline = ref(true);
    const status = ref({
      github: ["lightgrey", "grey", "Not connected", "Connect", "", ""],
      zenodo: ["lightgrey", "grey", "Not connected", "Connect", "", ""],
    });

    function updateStatus(key, userName) {
      manager.getToken(key).then((value) => {
        if (key == "github") {
          if (value == "NO_TOKEN_FOUND") {
            githubOffline.value = true;
            status.value.github = [
              "lightgrey",
              "grey",
              "Not connected",
              "Connect",
              userName,
              ""
            ];
          } else {
            githubOffline.value = false;
            status.value.github = [
              "lightgreen",
              "lightgreen",
              "Connected",
              "Disconnect",
              userName,
              "danger"
            ];
          }
        }

        if (key == "zenodo") {
          if (value == "NO_TOKEN_FOUND") {
            zenodoOffline.value = true;
            status.value.zenodo = [
              "lightgrey",
              "grey",
              "Not connected",
              "Connect",
              userName,
              ""
            ];
          } else {
            zenodoOffline.value = false;
            status.value.zenodo = [
              "lightgreen",
              "lightgreen",
              "Connected",
              "Disconnect",
              userName,
              "danger"
            ];
          }
        }
      });
    }

    function useAPIkey(key) {
      if(key == "github"){
        ElMessageBox.prompt("Please input your API key", "", {
        confirmButtonText: "OK",
        cancelButtonText: "Cancel",
      })
        .then(async ({ value }) => {
            processGithub(key, value);
        })
        .catch(() => {
          ElNotification({
            type: "info",
            message: "Input canceled",
            position: "bottom-right",
            duration: 2000,
          });
        });
      } else if (key == "zenodo"){
        ElMessageBox({
        title: 'Message',
        message: h('div', null, [
          h('el-input', null, ''),
          h('i', { style: 'color: teal' }, 'VNode'),
        ]),
        showCancelButton: true,
        confirmButtonText: 'OK',
        cancelButtonText: 'Cancel',
      })
        .then(async ({ value }) => {

            processZenodo(key, value);
          
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
        let name = await manager.getZenodoUser(value)
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
        let name = await manager.getGithubUser()
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
      if (status.value[s][3] == "Connect") {
        if (s == "github" || s == "zenodo") {
          useAPIkey(s);
        }
      } else if (status.value[s][3] == "Disconnect") {
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
    return {
      dialogFormVisible: true
    };
  },
  methods: {
    openWebsite(url) {
      window.ipcRenderer.send("open-link-in-browser", url);
    },
  },
  async mounted() {
    let keys = await this.manager.loadTokens();
    let githubUserName = "";
    let zenodoUserName = "";
    console.log("keys ", keys)
    if (keys.includes("github")) {
      githubUserName = await this.manager.getGithubUser();
    } else if (keys.includes("zenodo")) {
      zenodoUserName = await this.manager.getZenodoUser();
    }

    this.updateStatus("github", githubUserName);
    this.updateStatus("zenodo", zenodoUserName);
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

.el-avatar--small{
  height: 12px;
  width: 12px;
  line-height: 12px;
}
</style>
