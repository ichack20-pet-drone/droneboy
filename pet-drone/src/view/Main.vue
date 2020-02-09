<template>
  <div>
    <v-btn @click="test">Test</v-btn>
  </div>
</template>

<script>
import io from "socket.io-client";

const BASE_URL = "http://localhost:23333";
const socket = io(BASE_URL);

export default {
  name: "Main",
  methods: {
    test() {
      console.log("hi");
      socket.emit("my other event", { sth: "sth" });
    }
  }
};
</script>
