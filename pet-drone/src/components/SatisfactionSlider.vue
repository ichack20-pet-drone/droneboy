<template>
  <div>
    <v-card>
      <v-card-title>Satisfaction</v-card-title>
      <v-card-text>
        <v-progress-linear v-model="satisfaction" reactive height="30">
          {{ currentSatisfaction }}%
        </v-progress-linear>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  name: "SatisfactionSlider",
  data: () => ({
    satisfaction: 50
  }),
  computed: {
    currentSatisfaction() {
      return Math.ceil(this.satisfaction);
    }
  }
};
</script>
