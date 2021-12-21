module.exports = {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
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

  plugins: [
    require("@tailwindcss/line-clamp"),
    require("tailwindcss-debug-screens"),
  ],
};
