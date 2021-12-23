module.exports = {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        lato: ["Lato"],
        inter: ["Inter"],
        asap: ["Asap"],
      },
      colors: {
        primary: {
          //currently using 100-600
          50: "#FFEDD5",
          100: "#FFF7ED",
          200: "#BAE6FD",
          300: "#FDBA74",
          400: "#38BDF8",
          500: "#0EA5E9",
          600: "#171717",
          700: "#0369A1",
          800: "#075985",
          900: "#0C4A6E",
        },
        secondary: {
          //currently using 100, 300 and 600
          50: "#FDF4FF",
          100: "#DBEAFE",
          200: "#D1FAE5",
          300: "#93C5FD",
          400: "#E879F9",
          500: "#D946EF",
          600: "#171717",
          700: "#A21CAF",
          800: "#86198F",
          900: "#064E3B",
        },
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
