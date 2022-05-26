<template>
  <button type="button" :class="classes" @click="onClick" :disabled="disabled">
    <Icon v-if="showIcon" icon="ic:baseline-auto-fix-high" class="mx-2 h-5 w-5" /> {{ label }}
  </button>
</template>

<script>
import "./button.css";
import "./assets/index.css";
import { reactive, computed } from "vue";
import { Icon } from "@iconify/vue";

/**
 *  All the buttons used in FAIRshare are showcased here. They are all styled with the same base styles.
 *
 *  The style of the button is handled by CSS classes at the moment. I should replace it with a importable component.
 *
 */

export default {
  name: "my-button",
  components: { Icon },
  props: {
    label: {
      type: String,
      required: true,
    },
    primary: {
      type: Boolean,
      default: false,
    },
    secondary: {
      type: Boolean,
      default: false,
    },
    danger: {
      type: Boolean,
      default: false,
    },
    plain: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    showIcon: {
      type: Boolean,
      default: false,
    },
  },

  emits: ["click"],

  setup(props, { emit }) {
    props = reactive(props);
    return {
      classes: computed(() => ({
        "primary-button": props.primary && !props.plain,
        "primary-plain-button": props.primary && props.plain,
        "secondary-button": props.secondary && !props.plain,
        "secondary-plain-button": props.secondary && props.plain,
        "danger-button": props.danger && !props.plain,
        "danger-plain-button": props.danger && props.plain,
      })),
      onClick() {
        emit("click");
      },
    };
  },
};
</script>
