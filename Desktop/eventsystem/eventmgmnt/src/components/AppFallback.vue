<template>
  <div class="middle-box text-center animated fadeInDown">
    <h1>404</h1>
    <h3 class="font-bold">Page Not Found</h3>

    <div class="error-desc">
      Sorry, but the page you are looking for has note been found. Try checking
      the URL for error, then hit the refresh button on your browser.
    </div>
  </div>
</template>

<script>
export default {
  name: "AppFallback",
  created() {
    document.body.className = "gray-bg";
  },
};
</script>

<style scoped></style>
