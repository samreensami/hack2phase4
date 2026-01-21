/** @type {import('next').NextConfig} */
const nextConfig = {
  typescript: {
    ignoreBuildErrors: true,
  },
e
  eslint: {
    ignoreDuringBuilds: true,
  },
};

module.exports = nextConfig;
