import prettier from "prettier/standalone";
import prettierBabel from "prettier/parser-babel";

import "../src/assets/css/index.css";

export const parameters = {
  actions: { argTypesRegex: "^on[A-Z].*" },
  controls: {
    matchers: {
      color: /(background|color)$/i,
      date: /Date$/,
    },
  },
  docs: {
    transformSource: (input) =>
      prettier.format(input, {
        parser: "babel",
        plugins: [prettierBabel],
      }),
  },
};
