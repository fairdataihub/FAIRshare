<script setup>
import "@/assets/css/index.css";
import LoadingCubeGrid from "./LoadingCubeGrid.vue";
import LoadingEllipsis from "./LoadingEllipsis.vue";
import LoadingFoldingCube from "./LoadingFoldingCube.vue";
import LoadingPulseCircle from "./LoadingPulseCircle.vue";
</script>

<template>
  <Story title="Spinners">
    <Variant title="About" icon="bi:filetype-doc">
      <p>All these spinners are CSS only.</p>
      <p>Might need explicit sizes to be defined</p>
    </Variant>
    <Variant title="Cube grid" icon="fa:spinner">
      <LoadingCubeGrid class="h-5 w-5" />
    </Variant>
    <Variant title="Ellipsis" icon="fa:spinner">
      <LoadingEllipsis class="h-5 w-5" />
    </Variant>
    <Variant title="Folding cube" icon="fa:spinner">
      <LoadingFoldingCube class="h-5 w-5" />
    </Variant>
    <Variant title="Pulse circle" icon="fa:spinner">
      <LoadingPulseCircle class="h-5 w-5" />
    </Variant>
  </Story>
</template>
