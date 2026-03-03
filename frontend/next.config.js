/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    domains: ['api.segmind.com', 'localhost', 'r2.cloudflarestorage.com'],
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL}/api/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
