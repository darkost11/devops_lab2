<!-- src/App.vue -->
<template>
  <div id="app">
    <NoteList />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import NoteList from "./components/NoteList.vue";

export default defineComponent({
  name: "App",
  components: {
    NoteList,
  },
});
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
