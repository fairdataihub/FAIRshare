<template>
    <div></div>
</template>

<script>
import { ElMessageBox, ElMessage } from "element-plus";

export default {
  
  setup() {
      ElMessageBox.confirm(
        "Deleting API key will disconnect SODA from the software. Continue?",
        "Warning",
        {
          confirmButtonText: "OK",
          cancelButtonText: "Cancel",
          type: "warning",
        }
      )
        .then(async () => {
          await ElMessage({
            type: "success",
            message: "Delete completed",
          });
        })
        .catch(async () => {
          await ElMessage({
            type: "info",
            message: "Delete canceled",
          });
        });
  },
};
</script>