<script setup lang="ts">
import { ref, computed } from 'vue'

// --- State ---
const startDate = ref('')
const endDate = ref('')
const matchingDates = ref<string[]>([]) 
const count = ref<number | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

const targetDay = ref(15)
const targetWeekday = ref(5) // 5 = Saturday

const weekdays = [
  { val: 0, label: 'Monday' },
  { val: 1, label: 'Tuesday' },
  { val: 2, label: 'Wednesday' },
  { val: 3, label: 'Thursday' },
  { val: 4, label: 'Friday' },
  { val: 5, label: 'Saturday' },
  { val: 6, label: 'Sunday' },
]

const isFormValid = computed(() => {
  if (!startDate.value || !endDate.value) return false
  return startDate.value <= endDate.value
})

const dateOrderError = computed(() => {
  if (startDate.value && endDate.value && startDate.value > endDate.value) {
    return "End date must be after start date."
  }
  return null
})

function formatMonthYear(dateString: string): string {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('en-US', { 
    month: 'short', 
    year: 'numeric' 
  }).format(date).replace(' ', '-')
}

// --- API Interaction ---
async function findMatchingDates() {
  loading.value = true
  error.value = null
  matchingDates.value = []
  count.value = null

  try {
    const API_BASE = import.meta.env.VITE_API_URL || ''
    
    // FIX 1: Defined params ONLY ONCE with all 4 values
    const params = new URLSearchParams({
      start_date: startDate.value,
      end_date: endDate.value,
      weekday: targetWeekday.value.toString(),
      day_of_month: targetDay.value.toString()
    })

    // FIX 2: Updated URL to match Backend ("/matching-dates")
    const response = await fetch(`${API_BASE}/api/v1/dates/matching-dates?${params.toString()}`)

    if (!response.ok) {
      if (response.status === 429) throw new Error("You are going too fast! Please wait a minute.")
      if (response.status === 422) throw new Error("Invalid dates provided.")
      throw new Error(`Server Error: ${response.statusText}`)
    }

    const data = await response.json()
    matchingDates.value = data.matching_dates
    count.value = data.saturday_count

  } catch (err: any) {
    console.error(err)
    error.value = err.message || "An unexpected error occurred."
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="app-container">
    <div class="card">
      <header>
        <h1>🗓️ Date Finder</h1>
        <p class="subtitle">Find specific weekdays between two dates.</p>
      </header>

      <div class="form-group">
        <div class="input-wrapper">
          <label for="start">Start Date</label>
          <input type="date" id="start" v-model="startDate" :max="endDate" />
        </div>

        <div class="input-wrapper">
          <label for="end">End Date</label>
          <input type="date" id="end" v-model="endDate" :min="startDate" />
        </div>

        <!-- New Row for Specifics -->
        <div class="form-row">
            <div class="input-wrapper full-width">
                <label>Weekday</label>
                <!-- FIX 3: Added styles for select to match inputs -->
                <select v-model="targetWeekday" class="styled-input">
                    <option v-for="d in weekdays" :key="d.val" :value="d.val">
                        {{ d.label }}
                    </option>
                </select>
            </div>
            <div class="input-wrapper full-width">
                <label>Day of Month</label>
                <input type="number" v-model="targetDay" min="1" max="31" class="styled-input" />
            </div>
        </div> <!-- FIX 4: Fixed closing div tag typo -->
      </div>

      <div v-if="dateOrderError" class="validation-msg">{{ dateOrderError }}</div>
      <div v-if="error" class="error-banner">⚠️ {{ error }}</div>

      <div class="actions">
        <button 
          class="calculate-btn"
          :disabled="!isFormValid || loading"
          @click="findMatchingDates"
        >
          <span v-if="loading" class="loader"></span>
          <span v-else>Find Dates</span>
        </button>
      </div>

      <!-- Result List Area -->
      <div v-if="count !== null" class="result-area">
        <div class="result-header">
          <span class="count-badge">{{ count }} Matches Found</span>
        </div>
        
        <div v-if="count > 0" class="date-grid">
          <div 
            v-for="(date, index) in matchingDates" 
            :key="index" 
            class="date-chip"
          >
            {{ formatMonthYear(date) }}
          </div>
        </div>
        
        <div v-else class="no-results">
          No matches found in this range.
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
/* Keeping existing layout styles... */
.app-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  color: #333;
}
.card {
  background: white;
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.05);
  width: 100%;
  max-width: 450px;
}
header { text-align: center; margin-bottom: 2rem; }
h1 { font-size: 1.5rem; margin: 0; color: #1a1a1a; }
.subtitle { color: #666; font-size: 0.9rem; margin-top: 0.5rem; }
.form-group { display: flex; flex-direction: column; gap: 1.25rem; margin-bottom: 1rem; }
.input-wrapper { display: flex; flex-direction: column; gap: 0.5rem; }
label { font-size: 0.85rem; font-weight: 600; color: #444; }

/* SHARED STYLES FOR INPUTS AND SELECTS */
input[type="date"], 
.styled-input { 
  padding: 0.75rem; 
  border: 2px solid #e0e0e0; 
  border-radius: 8px; 
  font-size: 1rem; 
  width: 100%; 
  outline: none; 
  transition: border-color 0.2s;
  background-color: white;
}
input[type="date"]:focus, 
.styled-input:focus { 
  border-color: #3b82f6; 
}

/* NEW: Side by Side layout */
.form-row {
    display: flex;
    gap: 1rem;
}
.full-width {
    flex: 1; /* Makes them share width equally */
}

.actions { margin-bottom: 2rem; }
.calculate-btn { width: 100%; padding: 0.85rem; background-color: #3b82f6; color: white; border: none; border-radius: 8px; font-size: 1rem; font-weight: 600; cursor: pointer; display: flex; justify-content: center; align-items: center; }
.calculate-btn:hover:not(:disabled) { background-color: #2563eb; }
.calculate-btn:disabled { background-color: #cbd5e1; cursor: not-allowed; }
.loader { width: 20px; height: 20px; border: 3px solid #ffffff; border-bottom-color: transparent; border-radius: 50%; display: inline-block; animation: rotation 1s linear infinite; }
@keyframes rotation { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
.validation-msg { color: #ef4444; font-size: 0.85rem; margin-bottom: 1rem; text-align: center; }
.error-banner { background-color: #fef2f2; border: 1px solid #fee2e2; color: #b91c1c; padding: 0.75rem; border-radius: 8px; margin-bottom: 1.5rem; text-align: center; }

.result-area { margin-top: 1rem; border-top: 1px solid #eee; padding-top: 1.5rem; }
.result-header { text-align: center; margin-bottom: 1rem; }
.count-badge { background-color: #eff6ff; color: #1d4ed8; font-weight: 700; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; }
.date-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.75rem; max-height: 300px; overflow-y: auto; padding-right: 5px; }
.date-chip { background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.75rem; text-align: center; font-family: monospace; font-weight: 600; color: #334155; font-size: 0.95rem; }
.no-results { text-align: center; color: #64748b; font-style: italic; margin-top: 1rem; }
</style>