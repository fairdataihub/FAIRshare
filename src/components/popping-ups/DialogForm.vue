<template>
  <el-dialog>
    <div class="dialog-Container">
      <div class="inputField">
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
import { ref } from 'vue'
export default {
  props: {
    callback: { type: Function },
  },
  setup() {
    return {
      input1: ref(''),
      input2: ref(''),
    }
  },
  methods: {
    closeDialogFromParent() {
      this.callback();
    },
  },
};
</script>

<style scoped>
.el-button--text {
  font-size: 1.5vw;
}

.centering-Container {
  display: flex;
  align-items: center;
  justify-content: right;
}

.fix-Width{
    width: 10vw;
}

.dialog-Container{
    display: flex;
    flex-direction: column;
    gap: 2vh;
}

.inputField {
  display: flex;
  gap: 1vw;
}

.inputBar-Header{
    font-size: 1.4vw;

}

.inputBar{
    width: 30vw;
}

.bottom{
    display: flex;
    align-items: flex-end;
    justify-content: flex-end;
}
</style>
