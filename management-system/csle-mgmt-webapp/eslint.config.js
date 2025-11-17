import eslint from '@eslint/js';
import globals from 'globals';
import pluginN from 'eslint-plugin-n';
import pluginPromise from 'eslint-plugin-promise';
import pluginReact from 'eslint-plugin-react';
import eslintConfigPrettier from 'eslint-config-prettier';

export default [
  {
    files: ['**/*.{js,jsx}'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      parserOptions: {
        ecmaFeatures: {
          jsx: true,
        },
      },
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
    plugins: {
      'react': pluginReact,
      'n': pluginN,
      'promise': pluginPromise,
    },
    settings: {
      react: {
        version: 'detect',
      },
    },
  },
  eslint.configs.recommended,
  pluginN.configs['flat/recommended-script'],
  pluginPromise.configs['flat/recommended'],
  {
    ...pluginReact.configs.flat.recommended,
    ...pluginReact.configs.flat['jsx-runtime'],
  },
  eslintConfigPrettier,
];