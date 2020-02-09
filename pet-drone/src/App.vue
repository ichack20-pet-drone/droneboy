<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-spacer />
      <v-toolbar-title>{{ title }}</v-toolbar-title>
      <v-spacer />
    </v-app-bar>

    <v-content>
      <Main />
    </v-content>
  </v-app>
</template>

<script>
import Main from "@/view/Main.vue";

export default {
  name: "App",
  components: { Main },
  data: () => ({
    title: "Tamagucci"
  })
};
</script>
