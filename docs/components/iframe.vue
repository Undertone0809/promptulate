<template>
  <iframe :src="src" frameborder="0" allowfullscreen></iframe>
</template>

<script>
export default {
  name: 'IFrame',
  props: {
    src: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
iframe {
  width: 100%;
  height: 600px;
  border: none;
  border-radius: 4px;
  overflow: hidden;
}
</style>
