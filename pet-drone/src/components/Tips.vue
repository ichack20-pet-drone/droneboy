<template>
  <div>
    <v-dialog v-model="dialog" width="500">
      <template v-slot:activator="{ on }">
        <v-btn color="red lighten-2" dark block v-on="on">
          Tips
        </v-btn>
      </template>

      <v-card>
        <v-card-subtitle class="grey lighten-2 pa-3" primary-title>
          Tutorial
        </v-card-subtitle>

        <v-card-text>
          <div class="display-1 pa-3 text-center">Welcome to Tamagucci!</div>

          <div>
            Control your Tamagucci with voice commands:
          </div>

          <div class="pa-3">
            <li>“Wake up” or “Let’s go” to start a session</li>
            <li>“Stop” or “End flight” to end a session</li>
            <li>Say directions to move the drone</li>
            <li>At high satisfaction levels it can flip!</li>
          </div>

          <div>
            Compliment the drone to make it happier or it’ll get grumpy and stop
            listening to you. Commands don’t need to be exactly worded, but
            simple sentences will work better.
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  name: "Tips",
  data: () => ({
    dialog: false
  })
};
</script>
