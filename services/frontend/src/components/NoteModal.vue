<!-- src/components/NoteModal.vue -->
<template>
  <div v-if="isVisible" class="modal-overlay">
    <div class="modal-content">
      <h3>Add a new note</h3>
      <input v-model="noteText" ref="inputRef" type="text" placeholder="Enter note" @keyup.enter="submitNote" />
      <button @click="submitNote">Add Note</button>
      <button @click="close">Cancel</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch, nextTick, onMounted, PropType } from "vue";

export default defineComponent({
  name: "NoteModal",
  props: {
    isVisible: {
      type: Boolean as PropType<boolean>,
      required: true,
    },
  },
  emits: ["close", "add-note"],
  setup(props, { emit }) {
    const noteText = ref("");
    const inputRef = ref<HTMLInputElement | null>(null);

    // Фокусируем поле ввода при открытии модалки
    onMounted(() => {
      nextTick(() => {
        inputRef.value?.focus();
      });
    });

    const close = () => {
      noteText.value = "";
      emit("close");
    };

    const submitNote = () => {
      if (noteText.value.trim()) {
        emit("add-note", noteText.value);
        close();
      }
    };

    watch(
      () => props.isVisible,
      (newVal) => {
        if (!newVal) noteText.value = "";
      },
    );

    return {
      noteText,
      inputRef,
      close,
      submitNote,
    };
  },
});
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  z-index: 10;
}
.modal-content {
  background: #ffffff;
  color: #213547;
  padding: 20px;
  border-radius: 10px;
  width: 100%;
  max-width: 360px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  text-align: center;
}
.modal-content h3 {
  margin-top: 0;
}
input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 8px;
}
button {
  margin: 5px;
  padding: 6px 12px;
}
</style>
