<template>
  <div>
    <v-card height="670px">
      <v-card-text>
        <v-textarea
          filled
          readonly
          rounded
          :value="msg"
          height="630px"
        ></v-textarea>
      </v-card-text>
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
