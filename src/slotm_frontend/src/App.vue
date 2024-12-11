<template>
  <div id="app">
    <h1>Slot Machine</h1>
    <div class="slot-machine">
      <div class="reels">
        <div v-for="(reel, index) in reels" :key="index" class="reel">
          {{ reel }}
        </div>
      </div>
      <button @click="spinReels" :disabled="loading">Spin</button>
      <p v-if="message">{{ message }}</p>
      <p>Credits: {{ credits }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      reels: ["🍒", "🍋", "🍉"], // Initial reel symbols
      credits: 100, // Default credits
      message: "",
      loading: false, // Spin button state
    };
  },
  methods: {
    async spinReels() {
      this.loading = true;
      this.message = "";
      try {
        console.log("Sending request to backend...");
        const response = await fetch("http://127.0.0.1:8080/spin", {
          method: "POST",
        });
        console.log("Response received:", response);

        // Check response status
        if (!response.ok) {
          const error = await response.json();
          console.error("Backend returned an error:", error);
          this.message = error.error || "An unexpected error occurred.";
          return;
        }

        const data = await response.json();
        console.log("Parsed response data:", data);

        // Update UI with backend response
        this.reels = data.reels;
        this.credits = data.credits;
        this.message = data.payout > 0
          ? `You win ${data.payout} credits!`
          : "Try again!";
      } catch (error) {
        console.error("Fetch failed:", error);
        this.message = "Something went wrong. Please try again.";
      } finally {
        this.loading = false;
        console.log("Request completed.");
      }
    },
  },
};
</script>

<style scoped>
#app {
  text-align: center;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  margin-top: 50px;
}

.slot-machine {
  margin: auto;
  max-width: 300px;
}

.reels {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.reel {
  font-size: 2em;
  margin: 0 10px;
  border: 2px solid #ccc;
  padding: 10px;
  width: 50px;
  text-align: center;
  border-radius: 5px;
  animation: spin 1s ease-out;
}

button {
  font-size: 1em;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #0056b3;
}

p {
  font-size: 1em;
  margin-top: 10px;
}

@keyframes spin {
  0% {
    transform: translateY(-50px);
  }
  100% {
    transform: translateY(0);
  }
}
</style>






