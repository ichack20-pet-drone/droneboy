<template>
  <div>
    <v-container>
      <div v-if="name !== 'Don\'t know yet'" class="display-1 text-center">
        Hi {{ name }}
      </div>
      <div v-else class="display-1 text-center">
        Welcome!
      </div>
      <v-row>
        <v-col style="height: 700px">
          <MessageLog class="justify-space-between pa-2" :msg="msg" />
        </v-col>
        <v-col style="height: 700px">
          <EmotionLoader
            class="justify-space-between pa-2"
            :satisfaction="satisfaction"
          />
          <SatisfactionSlider
            class="justify-space-between pa-2"
            :satisfaction="satisfaction"
            :compliments="compliments"
            :scoldings="scoldings"
            :commands="commands"
          />
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
  data: () => ({
    name: "Don't know yet",
    satisfaction: 0,
    commands: 0,
    compliments: 0,
    scoldings: 0,
    msg: ""
  }),
  mounted() {
    socket.on("STAT", data => {
      if (Object.keys(data.data).length === 5) {
        this.name = data.data.playerName;
        this.satisfaction = data.data.satisfaction;
        this.commands = data.data.commands;
        this.compliments = data.data.compliments;
        this.scoldings = data.data.scoldings;
      }
    });

    socket.on("UPDATE", data => {
      this.name = data.data.playerName;
      this.satisfaction = data.data.satisfaction;
      this.commands = data.data.commands;
      this.compliments = data.data.compliments;
      this.scoldings = data.data.scoldings;
    });

    socket.on("MSG", data => {
      this.msg += data.data.message + "\n";
    });
  }
};
</script>
