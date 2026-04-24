import type { AppProps, NextWebVitalsMetric } from "next/app";
import "../index.css";
import "../App.css";
import "../Sass/App.scss";
import "kainossoftwareltd-govuk-react-kainos/dist/index.css";

export default function CustomApp({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />;
}

export function reportWebVitals(metric: NextWebVitalsMetric) {
  if (process.env.NODE_ENV === "development") {
    console.debug("[web-vitals]", metric);
  }
}
