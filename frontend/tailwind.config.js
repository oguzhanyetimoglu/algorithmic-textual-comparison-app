/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["~/components/**/*.{html,js,vue}", "~/pages/**/*.{html,js,vue}"],
  theme: {
    extend: {
      brightness: {
        '90': '.9',
      },
      height: {
        '1/4': '25vh',
        '1/2': '50vh',
        '3/4': '75vh',
        'full': '100vh',
      }
    }
  },
  variants: {
    extend: {
      brightness: ['hover', 'focus'],
    },
  },
  plugins: [],
};