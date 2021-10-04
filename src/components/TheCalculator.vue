<template>
  <div class="flex flex-col justify-center items-center p-3 text-xl font-mono">
    <p class="p-2">Input something like <code>1 + 1</code>.</p>
    <p>
      This calculator supports <code>+-*/^()</code>, whitespaces, and integers
      and floating numbers.
    </p>

    <div class="m-2">
      <el-input v-model="inputExpression" placeholder="1 + 2" />
    </div>
    <el-button type="primary" plain @click="calcSum">Calculate</el-button>
    <br />
    <span class="label"> {{ result }}</span>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "TheCalculator",
  data() {
    return {
      requestObject: {
        key: "Hello world from Electron!",
      },
      inputExpression: "1 + 2",
      result: "",
    };
  },
  methods: {
    calcSum: function () {
      if (this.inputExpression != "") {
        let reqObj = { expression: this.inputExpression };
        axios
          .post(`${this.SERVERURL}/add`, reqObj)
          .then((response) => {
            this.result = `Result = ${response.data}`;
          })
          .catch(function (error) {
            console.error(error);
          });
      }
    },
  },
  mounted() {
    axios
      .get(`${this.SERVERURL}/echo`)
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  },
};
</script>

<style>
body,
html {
  background-color: rgb(224, 223, 223);
  height: 99%;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

#result {
  margin: 30px;
}
</style>
