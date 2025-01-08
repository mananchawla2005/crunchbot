/** @type {import('tailwindcss').Config} */
export default {
  content: [],
  theme: {
    extend: {
      typography: ({ theme }) => ({
        white: {
          css: {
            '--tw-prose-body': theme.colors.white,
            '--tw-prose-headings': theme.colors.white,
            '--tw-prose-lead': theme.colors.white,
            '--tw-prose-links': theme.colors.white,
            '--tw-prose-bold': theme.colors.white,
            '--tw-prose-counters': theme.colors.white,
            '--tw-prose-bullets': theme.colors.white,
            '--tw-prose-hr': theme.colors.white,
            '--tw-prose-quotes': theme.colors.white,
            '--tw-prose-quote-borders': theme.colors.white,
            '--tw-prose-captions': theme.colors.white,
            '--tw-prose-code': theme.colors.white,
            '--tw-prose-pre-code': theme.colors.white,
            // '--tw-prose-pre-bg': theme.colors.white,
            '--tw-prose-th-borders': theme.colors.white,
            '--tw-prose-td-borders': theme.colors.white,
            '--tw-prose-invert-body': theme.colors.black,
            '--tw-prose-invert-headings': theme.colors.black,
            '--tw-prose-invert-lead': theme.colors.black,
            '--tw-prose-invert-links': theme.colors.black,
            '--tw-prose-invert-bold': theme.colors.black,
            '--tw-prose-invert-counters': theme.colors.black,
            '--tw-prose-invert-bullets': theme.colors.black,
            '--tw-prose-invert-hr': theme.colors.black,
            '--tw-prose-invert-quotes': theme.colors.black,
            '--tw-prose-invert-quote-borders': theme.colors.black,
            '--tw-prose-invert-captions': theme.colors.black,
            '--tw-prose-invert-code': theme.colors.black,
            '--tw-prose-invert-pre-code': theme.colors.black,
            '--tw-prose-invert-pre-bg': theme.colors.black,
            '--tw-prose-invert-th-borders': theme.colors.black,
            '--tw-prose-invert-td-borders': theme.colors.black,
          },
        },
      }),
    },
  },
  plugins: [require('@tailwindcss/typography')],
}

