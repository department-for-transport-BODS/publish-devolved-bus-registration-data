import type { AppProps, NextWebVitalsMetric } from "next/app";
import "../../index.css";
import "../styles/App.css";
import "../styles/App.scss";
import "kainossoftwareltd-govuk-react-kainos/dist/index.css";
import { config } from "../utils/Config";

export default function CustomApp({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />;
}

export function reportWebVitals(metric: NextWebVitalsMetric) {
  if (config.env === "development") {
    console.debug("[web-vitals]", metric);
  }
}
