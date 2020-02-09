<template>
  <div>
    <v-container>
      <v-row>
        <v-col>
          <MessageLog />
        </v-col>
        <v-col>
          <EmotionLoader />
          <SatisfactionSlider />
          <Tips />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import io from "socket.io-client";
const BASE_URL = "http://localhost:23333";
const socket = io(BASE_URL);

import MessageLog from "@/components/MessageLog";
import EmotionLoader from "@/components/EmotionLoader";
import SatisfactionSlider from "@/components/SatisfactionSlider";
import Tips from "@/components/Tips";

export default {
  name: "Main",
  components: {
    MessageLog,
    EmotionLoader,
    SatisfactionSlider,
    Tips
  },
  methods: {
    test() {
      console.log("hi");
      socket.emit("my other event", { sth: "sth" });
    }
  }
};
</script>
