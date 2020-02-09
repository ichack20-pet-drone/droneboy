<template>
  <div>
    <v-card min-height="500">
      <v-card-text>{{ msg }}</v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  name: "MessageLog",
  props: {
    msg: { type: String, required: true }
  }
};
</script>
