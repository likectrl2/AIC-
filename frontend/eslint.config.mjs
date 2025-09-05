import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
import nextPlugin from '@next/eslint-plugin-next';
import reactPlugin from 'eslint-plugin-react';
import hooksPlugin from 'eslint-plugin-react-hooks';
import eslintConfigPrettier from 'eslint-config-prettier';

/** @type {import('eslint').Linter.FlatConfig[]} */
const eslintConfig = tseslint.config(
  // 全局忽略文件
  {
    ignores: [
      'node_modules/',
      '.next/',
      'out/',
      'public/',
      'next-env.d.ts',
    ],
  },

  // 1. 基础配置 (ESLint 官方推荐)
  eslint.configs.recommended,

  // 2. TypeScript 支持
  ...tseslint.configs.recommended,

  // 3. React & Next.js 配置
  {
    files: ['**/*.{js,mjs,cjs,ts,jsx,tsx}'],
    plugins: {
      '@next/next': nextPlugin,
      'react': reactPlugin,
      'react-hooks': hooksPlugin,
    },
    rules: {
      ...nextPlugin.configs.recommended.rules,
      ...nextPlugin.configs['core-web-vitals'].rules,
      ...reactPlugin.configs.recommended.rules,
      ...hooksPlugin.configs.recommended.rules,
      'react/react-in-jsx-scope': 'off', // Next.js 和 React 17+ 不需要
      'react/prop-types': 'off', // 在 TypeScript 项目中通常不需要
    },
    settings: {
      react: {
        version: 'detect', // 自动检测 React 版本
      },
    },
  },

  // 4. Prettier 配置 (必须放在最后！)
  // 这个配置会关闭所有与 Prettier 冲突的 ESLint 规则
  eslintConfigPrettier
);

export default eslintConfig;