/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "export",
  reactStrictMode: true,
  transpilePackages: ["kainossoftwareltd-govuk-react-kainos"],
  images: {
    unoptimized: true,
  },
};

export default nextConfig;