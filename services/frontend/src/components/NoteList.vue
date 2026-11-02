<!-- src/components/NoteList.vue -->
<template>
  <div class="note-list">
    <h2>My Notes</h2>
    <ul class="notes">
      <li v-for="note in notes" :key="note.date" class="note-card">
        <p class="note-text">{{ note.note }}</p>
        <time class="note-date" :datetime="note.date">{{ formatDate(note.date) }}</time>
      </li>
    </ul>
    <button class="add-btn" @click="openModal">+</button>

    <NoteModal
      v-if="isModalOpen"
      :isVisible="isModalOpen"
      @close="closeModal"
      @add-note="addNote"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import NoteModal from "./NoteModal.vue";

interface Note {
  note: string;
  date: string;
}

export default defineComponent({
  name: "NoteList",
  components: {
    NoteModal,
  },
  setup() {
    const notes = ref<Note[]>([]);
    const isModalOpen = ref(false);

    // Получаем URL API из переменной окружения
    const apiUrl = import.meta.env.VITE_API_URL;

    const loadNotes = async () => {
      try {
        const response = await fetch(`${apiUrl}/notes`);
        if (!response.ok) {
          throw new Error(`Ошибка HTTP: ${response.status}`);
        }
        notes.value = await response.json();
      } catch (error) {
        console.error("Не удалось загрузить заметки:", error);
      }
    };

    onMounted(() => {
      loadNotes();
    });

    const openModal = () => {
      isModalOpen.value = true;
    };

    const closeModal = () => {
      isModalOpen.value = false;
    };

    const addNote = async (text: string) => {
      const newNote = { note: text, date: new Date().toISOString() };
      try {
        const response = await fetch(`${apiUrl}/notes`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(newNote),
        });
        if (!response.ok) {
          throw new Error(`Ошибка HTTP: ${response.status}`);
        }
        const createdNote = await response.json();
        notes.value.push(createdNote);
        closeModal();
      } catch (error) {
        console.error("Не удалось добавить заметку:", error);
      }
    };

    const formatDate = (date: string) => {
      return new Date(date).toLocaleString();
    };

    return {
      notes,
      isModalOpen,
      openModal,
      closeModal,
      addNote,
      formatDate,
    };
  },
});
</script>

<style scoped>
.note-list {
  width: 100%;
  max-width: 640px;
  margin: auto;
}
.notes {
  list-style: none;
  margin: 0 0 16px;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.note-card {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 16px;
  padding: 12px 16px;
  border-radius: 10px;
  background: rgba(128, 128, 128, 0.12);
  text-align: left;
}
.note-text {
  margin: 0;
  min-width: 0;
  overflow-wrap: anywhere;
}
.note-date {
  flex-shrink: 0;
  font-size: 0.8em;
  opacity: 0.7;
  white-space: nowrap;
}
.add-btn {
  margin-top: 4px;
  padding: 5px 14px;
  font-size: 1.5em;
  line-height: 1.2;
}
</style>
