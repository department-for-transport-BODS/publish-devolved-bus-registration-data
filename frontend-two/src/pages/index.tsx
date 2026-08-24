import dynamic from "next/dynamic";

const AppClient = dynamic(() => import("../client/AppClient"), { ssr: false });

export default function HomePage() {
  return <AppClient />;
}
