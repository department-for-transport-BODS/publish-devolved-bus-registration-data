import React from "react";
import Footer from "../Layout/Footer";
import FullColumnLayout from "../Layout/Layout";
import UploadCSV from "../components/UploadCSV";
type Props = {
  isLoggedIn?: boolean;
};

const UploadCSVPage: React.FC<Props> = ({isLoggedIn=false}) => {
const [isloading, setIsLoading] = React.useState<boolean>(false);

  return (
    <>
      <FullColumnLayout
        title="Temp Page"
        description="Temp Page"
        hideCookieBanner={true}
        isLoggedIn={isLoggedIn}
      >
        {isloading && <h1>Loading...</h1>}
        {!isloading && <UploadCSV setIsLoading={setIsLoading} />}
      </FullColumnLayout>
      <Footer />
    </>
  );
};

export default UploadCSVPage;
