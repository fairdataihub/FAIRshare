<template>
  <div class="page-Container">
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
                backgroundColor:
                  this.manager.checkApiKey('github') == ''
                    ? 'lightgray'
                    : 'lightgreen',
              }"
            ></span>
          </div>
          <div class="centering-Container">
            <div
              class="app-Card-Status-Text"
              :style="{
                color:
                  this.manager.checkApiKey('github') == ''
                    ? 'gray'
                    : 'lightgreen',
              }"
            >
              {{
                this.manager.checkApiKey("github") == ""
                  ? "Disconnected"
                  : "Connected"
              }}
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
            type="text"
            class="button"
            @click="openDialog($event, 'github')"
            >{{
              this.manager.checkApiKey("github") == ""
                ? "Connect"
                : "Disconnect"
            }}</el-button
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
                backgroundColor:
                  this.manager.checkApiKey('zenodo') == ''
                    ? 'lightgray'
                    : 'lightgreen',
              }"
            ></span>
          </div>
          <div class="centering-Container">
            <div
              class="app-Card-Status-Text"
              :style="{
                color:
                  this.manager.checkApiKey('zenodo') == ''
                    ? 'gray'
                    : 'lightgreen',
              }"
            >
              {{
                this.manager.checkApiKey("zenodo") == ""
                  ? "Disconnected"
                  : "Connected"
              }}
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
            type="text"
            class="button"
            @click="openDialog($event, 'zenodo')"
            >{{
              this.manager.checkApiKey("zenodo") == ""
                ? "Connect"
                : "Disconnect"
            }}</el-button
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
            <span class="dot disconnected-Dot"></span>
          </div>
          <div class="centering-Container">
            <div class="app-Card-Status-Text disconnected-Text">
              {{
                this.manager.checkApiKey("placeholder") == ""
                  ? "Disconnected"
                  : "Connected"
              }}
            </div>
          </div>
        </div>
        <div class="centering-Container center">
          <span
            >Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
            eiusmod tempor incididunt ut labore et dolore magna aliqua.
            Convallis aenean et tortor at risus viverra adipiscing at. Est velit
            egestas dui id ornare arcu odio ut sem.</span
          >
        </div>
        <div class="centering-Container bottom">
          <el-button type="text" class="button">{{
            this.manager.checkApiKey("placeholder") == ""
              ? "Connect"
              : "Disconnect"
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
            <span class="dot disconnected-Dot"></span>
          </div>
          <div class="centering-Container">
            <div class="app-Card-Status-Text disconnected-Text">
              {{
                this.manager.checkApiKey("placeholder") == ""
                  ? "Disconnected"
                  : "Connected"
              }}
            </div>
          </div>
        </div>
        <div class="centering-Container center">
          <span
            >Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
            eiusmod tempor incididunt ut labore et dolore magna aliqua.
            Convallis aenean et tortor at risus viverra adipiscing at. Est velit
            egestas dui id ornare arcu odio ut sem.</span
          >
        </div>
        <div class="centering-Container bottom">
          <el-button type="text" class="button">{{
            this.manager.checkApiKey("placeholder") == ""
              ? "Connect"
              : "Disconnect"
          }}</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useManage } from "../../store/manage";
import { ElMessageBox } from "element-plus";
import { ElNotification } from "element-plus";
export default {
  name: "ManageAccount",
  setup() {
    const manager = useManage();
    function useAPIkey(key) {
      let errorFound = false;
      ElMessageBox.prompt("Please input your API key", "", {
        confirmButtonText: "OK",
        cancelButtonText: "Cancel",
      })
        .then(({ value }) => {
          try {
            manager.addApiKey(key, value);
          } catch (e) {
            console.log(e);
            errorFound = true;
          }
          console.log(errorFound);
          if (!errorFound) {
            ElNotification({
              type: "success",
              message: "Saved successfully",
              position: "bottom-right",
              duration: 2000,
            });
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
        .then(() => {
          try {
            manager.addApiKey(key, "");
          } catch (e) {
            errorFound = true;
          }
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
    return { manager, openDialog };
  },
  data() {
    return {};
  },
  methods: {
    openWebsite(url) {
      require("electron").shell.openExternal(url);
    },
  },
};
</script>

<style scoped>
.page-Container {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  gap: 5vw;
  padding-top: 5vh;
  padding-bottom: 5vh;
  overflow: scroll;
  padding-left: 12vw;
  padding-right: 12vw;
  box-sizing: border-box;
}

.app-Card {
  display: flex;
  height: 20vh;
  width: 100%;
  padding: 0px;
  padding-top: 1vh;
  border-radius: 0.25em;
  box-shadow: 0 2px 3px rgba(0, 0, 0, 0.15);
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

.app-Card::after {
  border-radius: 5px;
  opacity: 0;
  transition: all 0.6s cubic-bezier(0.165, 0.84, 0.44, 1);
}

.app-Card:hover {
  transform: scale(1.013, 1.013);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.app-Card:hover::after {
  opacity: 1;
}
.dot {
  height: 1.5vmin;
  width: 1.5vmin;
  border-radius: 50%;
  display: inline-block;
}

.app-Card-Status-Text {
  font-size: 1.5vmin;
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
  font-size: 1.8vmin !important;
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
}

.link-Font {
  color: #409eff;
}

.el-button--text {
  font-size: 1.8vmin;
}
</style>
