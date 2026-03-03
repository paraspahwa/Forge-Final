/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    domains: ['api.segmind.com', 'localhost', 'r2.cloudflarestorage.com'],
  },
  async rewrites() {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    return [
      {
        source: '/api/:path*',
        destination: `${apiUrl}/api/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
