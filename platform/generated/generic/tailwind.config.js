module.exports = {
  content: [
    './src/app/**/*.{ts,tsx,js,jsx}',
    './src/components/**/*.{ts,tsx,js,jsx}'
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: '#0b3d91',
          light: '#254fbb'
        },
        neutral: {
          100: '#f7fafc',
          700: '#374151'
        }
      }
    }
  },
  plugins: [],
};
