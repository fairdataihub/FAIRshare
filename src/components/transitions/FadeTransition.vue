<template>
  <transition name="fade" mode="out-in" appear>
    <slot></slot>
  </transition>
</template>

<script>
export default {
  name: "FadeTransition",
};
</script>
