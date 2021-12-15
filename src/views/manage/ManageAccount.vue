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
              v-if="status.githubToken[2].slice(0, 9) === 'Connected'"
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
          <GithubOAuthConnection :callback="reRenderByChild"></GithubOAuthConnection
          >
          <GithubTokenConnection
            :callback="reRenderByChild"
          ></GithubTokenConnection>
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
              v-if="status.zenodoToken[2].slice(0, 9) === 'Connected'"
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
          <ZenodoTokenConnection
            :callback="reRenderByChild"
          ></ZenodoTokenConnection>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useTokenStore } from "../../store/access";
import { ref } from "vue";
import GithubTokenConnection from "../../components/serviceIntegration/GithubTokenConnection";
import ZenodoTokenConnection from "../../components/serviceIntegration/ZenodoTokenConnection";
import GithubOAuthConnection from "../../components/serviceIntegration/GithubOAuthConnection";
export default {
  name: "ManageAccount",
  components: { GithubTokenConnection, ZenodoTokenConnection, GithubOAuthConnection },
  setup() {
    const manager = useTokenStore();
    const connectionList = ref(new Set([]));
    const status = ref({
      githubToken: [
        "lightgrey",
        "grey",
        "initial status",
        "Connect token",
        "",
        "",
      ],
      zenodoToken: [
        "lightgrey",
        "grey",
        "initial status",
        "Connect token",
        "",
        "",
      ],
    });


    function reRenderByChild() {
      updateStatus();
    }

    function updateStatus() {
      manager.getGithubTokenConnected().then(async (res) => {
        if (!res) {
          connectionList.value.delete("githubToken");
          status.value.githubToken = [
            "lightgrey",
            "grey",
            "checking status...",
            "Connect token",
            "",
            "",
          ];
          checkGithubConnectionMethods();
        } else {
          connectionList.value.add("githubToken");
          await manager.getGithubUser("githubToken").then((name) => {
            status.value.githubToken = [
              "lightgreen",
              "lightgreen",
              "checking status...",
              "Disconnect",
              name,
              "danger",
            ];
          });
          checkGithubConnectionMethods();
        }
      });

      manager.getZenodoTokenConnected().then(async (res) => {
        if (!res) {
          connectionList.value.delete("zenodoToken");
          status.value.zenodoToken = [
            "lightgrey",
            "grey",
            "checking status...",
            "Connect token",
            "",
            "",
          ];
          checkZenodoConnectionMethods();
        } else {
          connectionList.value.add("zenodoToken");
          await manager.readZenodoUser("zenodoToken").then((name) => {
            status.value.zenodoToken = [
              "lightgreen",
              "lightgreen",
              "checking status...",
              "Disconnect",
              name,
              "danger",
            ];
          });
          checkZenodoConnectionMethods();
        }
      });

      manager.getGithubOAuthConnected().then(async (res) => {
        if (!res) {
          connectionList.value.delete("githubOAuth");
          status.value.githubToken = [
            "lightgrey",
            "grey",
            "checking status...",
            "Connect token",
            "",
            "",
          ];
          checkGithubConnectionMethods();
        } else {
          connectionList.value.add("githubOAuth");
          await manager.getGithubUser("githubOAuth").then((name) => {
            status.value.githubToken = [
              "lightgreen",
              "lightgreen",
              "checking status...",
              "Disconnect",
              name,
              "danger",
            ];
          });
          checkGithubConnectionMethods();
        }
      });
    }

    function checkGithubConnectionMethods() {
      if (
        connectionList.value.has("githubToken") &&
        connectionList.value.has("githubOAuth")
      ) {
        status.value.githubToken[2] = "Connected via token and account";
      } else if (connectionList.value.has("githubOAuth")) {
        status.value.githubToken[2] = "Connected via account";
      } else if (connectionList.value.has("githubToken")) {
        status.value.githubToken[2] = "Connected via token";
      } else {
        status.value.githubToken[2] = "Not connected";
      }
    }

    function checkZenodoConnectionMethods() {
      if (
        connectionList.value.has("zenodoToken") &&
        connectionList.value.has("zenodoOAuth")
      ) {
        status.value.zenodoToken[2] = "Connected via token and account";
      } else if (connectionList.value.has("zenodoOAuth")) {
        status.value.zenodoToken[2] = "Connected via account";
      } else if (connectionList.value.has("zenodoToken")) {
        status.value.zenodoToken[2] = "Connected via token";
      } else {
        status.value.zenodoToken[2] = "Not connected";
      }
    }

    return {
      manager,
      status,
      updateStatus,
      reRenderByChild,
      connectionList,
    };
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
