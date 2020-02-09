<template>
  <div>
    <v-card>
      <v-card-title>Stats</v-card-title>
      <v-card-text>
        <div>
          Satisfaction
          <v-progress-linear v-model="satisfaction" reactive height="30">
            {{ currentSatisfaction }}%
          </v-progress-linear>
        </div>
        <v-divider />
        <div>Total Commands: {{ commands }}</div>
        <v-divider />
        <div>Compliments: {{ compliments }}</div>
        <v-divider />
        <div>Scoldings: {{ scoldings }}</div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  name: "SatisfactionSlider",
  props: {
    satisfaction: { type: Number, required: true },
    compliments: { type: Number, required: true },
    scoldings: { type: Number, required: true },
    commands: { type: Number, required: true }
  },
  computed: {
    currentSatisfaction() {
      return Math.ceil(this.satisfaction);
    }
  }
};
</script>
