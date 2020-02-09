<template>
  <div>
    <v-card>
      <v-card-text>
        <img :src="emotionPic" />
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
const cuteDrone = require("@/asset/cute_drone.png");
const happyDrone = require("@/asset/happy_drone.png");
const indifferentDrone = require("@/asset/indifferent_drone.png");
const sadDrone = require("@/asset/sad_drone.png");

export default {
  name: "EmotionLoader",
  data: () => ({
    cuteDrone: cuteDrone,
    happyDrone: happyDrone,
    indifferentDrone: indifferentDrone,
    sadDrone: sadDrone
  }),
  computed: {
    emotionPic() {
      return happyDrone;
    }
  }
};
</script>
