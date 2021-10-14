module.exports = {
  mode: "jit",
  purge: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      fontFamily: {
        lato: ["Lato"],
        inter: ["Inter"],
        asap: ["Asap"],
      },
    },
    debugScreens: {
      position: ["bottom", "left"],
    },
  },
  variants: {
    extend: {
      transitionProperty: ["responsive", "motion-safe", "motion-reduce"],
    },
  },
  plugins: [
    require("@tailwindcss/line-clamp"),
    require("tailwindcss-debug-screens"),
  ],
};
