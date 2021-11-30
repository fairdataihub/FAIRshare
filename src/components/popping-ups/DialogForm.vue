<template>
  <el-dialog>
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
        <div class="centering-Container fix-Width">
          <div class="inputBar-Header">Access Token</div>
        </div>
        <el-input
          class="inputBar"
          size="large"
          v-model="input1"
          placeholder="Please Input"
        />
      </div>
      <div class="bottom">
        <el-button type="text" class="button" @click="closeDialogFromParent"
          >SAVE</el-button
        >
      </div>
    </div>
  </el-dialog>
</template>

<script>
import { ref } from "vue";
import { useManage } from "../../store/manage";
export default {
  props: {
    callback: { type: Function },
    selected: { type: String },
  },
  setup() {
    const manager = useManage();
    return {
      input1: ref(""),
      input2: ref(""),
      manager,
    };
  },
  methods: {
    closeDialogFromParent() {
      if (this.selected == "zenodo" || this.selected == "github") {
        this.manager.addApiKey(this.selected, this.input1);
      }
      this.callback();
    },
  },
};
</script>

<style scoped>
.el-button--text {
  font-size: 1.3vw;
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

.inputBar-Header {
  font-size: 1.4vw;
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
