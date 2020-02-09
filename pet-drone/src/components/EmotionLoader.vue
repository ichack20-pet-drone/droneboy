<template>
  <div>
    <v-card>
      <v-card-text align="center">
        <img :src="emotionPic" style="width: 70%" />
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
  props: {
    satisfaction: { type: Number, required: true }
  },
  data: () => ({
    cuteDrone: cuteDrone,
    happyDrone: happyDrone,
    indifferentDrone: indifferentDrone,
    sadDrone: sadDrone
  }),
  computed: {
    emotionPic() {
      if (this.satisfaction < 25) {
        return sadDrone;
      } else if (this.satisfaction < 50) {
        return indifferentDrone;
      } else if (this.satisfaction < 75) {
        return happyDrone;
      } else {
        return cuteDrone;
      }
    }
  }
};
</script>
