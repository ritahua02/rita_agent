/** @type {import('next').NextConfig} */
const nextConfig = {
  // 生成独立可运行的构建产物，便于 Docker 打包（体积更小、不依赖完整 node_modules）
  output: 'standalone'
};

export default nextConfig;
