import MyButton from "./Button.vue";

// More on default export: https://storybook.js.org/docs/vue/writing-stories/introduction#default-export
export default {
  title: "Components/Button",
  component: MyButton,
  // More on argTypes: https://storybook.js.org/docs/vue/api/argtypes
  argTypes: {
    onClick: {},
  },
};

// More on component templates: https://storybook.js.org/docs/vue/writing-stories/introduction#using-args
const Template = (args) => ({
  // Components used in your story `template` are defined in the `components` object
  components: { MyButton },
  // The story's `args` need to be mapped into the template through the `setup()` method
  setup() {
    return { args };
  },
  // And then the `args` are bound to your component with `v-bind="args"`
  template: '<my-button v-bind="args" />',
  // add some text to the top of the story
  info: {
    // more on info: https://storybook.js.org/docs/vue/writing-stories/introduction#info-section
    text: `
      This is a storybook for the Button component.
    `,
  },
});

export const Primary = Template.bind({});
// More on args: https://storybook.js.org/docs/vue/writing-stories/args
Primary.args = {
  primary: true,
  plain: false,
  label: "Primary Button",
};
Primary.parameters = {
  docs: {
    source: {
      code: `<button class="primary-button">Primary Button</button>`,
      language: "html",
      format: true,
      type: "auto",
    },
  },
};

export const PrimaryDisabled = Template.bind({});
PrimaryDisabled.args = {
  primary: true,
  plain: false,
  disabled: true,
  label: "Primary Button",
};
PrimaryDisabled.parameters = {
  docs: {
    source: {
      code: `<button class="primary-button" disabled>Primary Button</button>`,
      language: "html",
      format: true,
      type: "auto",
    },
  },
};

export const PrimaryPlain = Template.bind({});
PrimaryPlain.args = {
  primary: true,
  plain: true,
  label: "Primary Button",
};

PrimaryPlain.parameters = {
  docs: {
    source: {
      code: `<button class="primary-plain-button">Primary Button</button>`,
      language: "html",
      format: true,
      type: "auto",
    },
  },
};

export const Secondary = Template.bind({});
Secondary.args = {
  secondary: true,
  plain: false,
  label: "Secondary Button",
};
Secondary.parameters = {
  docs: {
    source: {
      code: `<button class="secondary-button">Secondary Button</button>`,
      language: "html",
      format: true,
      type: "auto",
    },
  },
};

export const SecondaryPlain = Template.bind({});
SecondaryPlain.args = {
  secondary: true,
  plain: true,
  label: "Secondary Button",
};
SecondaryPlain.parameters = {
  docs: {
    source: {
      code: `<button class="secondary-plain-button">Secondary Button</button>`,
      language: "html",
      format: true,
      type: "auto",
    },
  },
};

export const Danger = Template.bind({});
Danger.args = {
  danger: true,
  plain: false,
  label: "Danger Button",
};
Danger.parameters = {
  docs: {
    source: {
      code: `<button class="danger-button">Danger Button</button>`,
      language: "html",
      format: true,
      type: "auto",
    },
  },
};

export const DangerPlain = Template.bind({});
DangerPlain.args = {
  danger: true,
  plain: true,
  label: "Danger Button",
};
DangerPlain.parameters = {
  docs: {
    source: {
      code: `<button class="danger-plain-button">Danger Button</button>`,
      language: "html",
      format: true,
      type: "auto",
    },
  },
};

export const PrimaryWithIcon = Template.bind({});
PrimaryWithIcon.args = {
  primary: true,
  plain: false,
  label: "Primary Button",
  showIcon: true,
};
PrimaryWithIcon.parameters = {
  docs: {
    source: {
      code: `
      <button class="primary-button">
        <Icon icon="ic:baseline-auto-fix-high" class="mx-2 h-5 w-5" /> Primary Button
      </button>`,
      language: "html",
      format: false,
      type: "auto",
    },
  },
};
