import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  // State
  const sidebarCollapsed = ref(false)
  const loading = ref(false)
  const breadcrumbs = ref([])

  // Actions
  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  function setLoading(val) {
    loading.value = val
  }

  function setBreadcrumbs(items) {
    breadcrumbs.value = items
  }

  return {
    sidebarCollapsed,
    loading,
    breadcrumbs,
    toggleSidebar,
    setLoading,
    setBreadcrumbs,
  }
})
