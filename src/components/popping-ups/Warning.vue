<template>
  <el-dialog title="Alert">
    <div class="dialog-Container">
      <!-- <div class="inputField">
          <div class="centering-Container fix-Width">
              <div class="inputBar-Header">User Name</div>
          </div>
        <el-input class="inputBar" size="large" v-model="input1" placeholder="User Name" />
      </div>

      <div class="inputField">
          <div class="centering-Container fix-Width">
              <div class="inputBar-Header">Password</div>
          </div>
        <el-input class="inputBar" size="large" v-model="input2" placeholder="Password" />
      </div> -->
      <div class="inputField">
        <div class="centering-Container">
          <div class="Warning-text">
            Disconnecting will delete the access token stored. Continue?
          </div>
        </div>
      </div>
      <div class="bottom">
        <el-button type="text" class="button" @click="closeWarningFromParent"
          >Confirm</el-button
        >
      </div>
    </div>
  </el-dialog>
</template>

<script>
import { useManage } from "../../store/manage";
import { ElNotification } from "element-plus";
export default {
  props: {
    callback: { type: Function },
    selected: { type: String },
  },
  setup() {
    const manager = useManage();
    return {
      manager,
    };
  },
  methods: {
    async closeWarningFromParent() {
      let errorFound = false;
      if (this.selected == "zenodo" || this.selected == "github") {
        try {
          this.manager.addApiKey(this.selected, "");
        } catch (e) {
          errorFound = true;
        }
      }
      await this.callback();
      if (!errorFound) {
        ElNotification({
          type: "success",
          message: "Deleted",
          position: "bottom-right",
          duration: 2000,
        });
      }
    },
  },
};
</script>

<style scoped>
.el-button--text {
  font-size: 1vw;
}

.centering-Container {
  display: flex;
  align-items: center;
  justify-content: center;
}

.fix-Width {
  width: 10vw;
}

.dialog-Container {
  display: flex;
  flex-direction: column;
  gap: 2vh;
}

.inputField {
  display: flex;
  gap: 1vw;
}

.Warning-text {
  font-size: 1vw;
}

.inputBar {
  width: 30vw;
}

.bottom {
  display: flex;
  align-items: flex-end;
  justify-content: flex-end;
}
</style>
