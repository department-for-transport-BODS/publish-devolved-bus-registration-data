import React, { Dispatch, useEffect, useState } from "react";
import { v4 as uuidv4 } from "uuid";
type PaginationProps = {
  pagesCount: number;
  currentPage: number;
  setCurrentPage: Dispatch<number>;
};

const PaginationComponent: React.FC<PaginationProps> = ({
  pagesCount,
  setCurrentPage,
  currentPage,
}) => {
  const clickHandler = (e: any) => {
    e.preventDefault();
    console.log(e.target.innerText);
    if (e.target.rel === "prev") {
      if (currentPage === 1) return null;

      setCurrentPage(currentPage - 1);
      return null;
    }
    if (e.target.rel === "next") {
      if (currentPage === pagesCount) return null;
      setCurrentPage(currentPage + 1);
      return null;
    }
    setCurrentPage(parseInt(e.target.innerText));
    return null;
  };
  const [threePages, setThreePages] = useState([
    currentPage - 1,
    currentPage,
    currentPage + 1,
  ]);
  useEffect(() => {
    if (currentPage === 1) return setThreePages([1, 2, 3]);
    if (pagesCount === 2) return setThreePages([1, 2]);
    if (currentPage === pagesCount)
      return setThreePages([currentPage - 2, currentPage - 1, currentPage]);
    if (currentPage < pagesCount)
      setThreePages([currentPage - 1, currentPage, currentPage + 1]);
  }, [currentPage, pagesCount]);

  const paginationStyle = {
    display: "flex",
    justifyContent: "space-evenly",
  };
  const spacerStyle = {
    height: "20px",
  };
  return (
    <>
      {pagesCount > 1 ? (
        <div style={paginationStyle} className="paginated-results">
          <nav className="govuk-pagination" aria-label="Pagination">
            {currentPage === 1 ? (
              <div style={{ width: "119.29px" }}></div>
            ) : (
              <div className="govuk-pagination__prev">
                <a
                  className="govuk-link govuk-pagination__link"
                  href="#"
                  rel="prev"
                  onClick={clickHandler}
                >
                  <svg
                    className="govuk-pagination__icon govuk-pagination__icon--prev"
                    xmlns="http://www.w3.org/2000/svg"
                    height="13"
                    width="15"
                    aria-hidden="true"
                    focusable="false"
                    viewBox="0 0 15 13"
                  >
                    <path d="m6.5938-0.0078125-6.7266 6.7266 6.7441 6.4062 1.377-1.449-4.1856-3.9768h12.896v-2h-12.984l4.2931-4.293-1.414-1.414z"></path>
                  </svg>
                  <span className="govuk-pagination__link-title">
                    Previous<span className="govuk-visually-hidden"> page</span>
                  </span>
                </a>
              </div>
            )}
            <ul className="govuk-pagination__list">
              {currentPage >2 && pagesCount !== 3 ?  (
                <li className="govuk-pagination__item govuk-pagination__item--ellipses three-dots">
                  ...
                </li>
              ) : (
                <></>
              )}
              {threePages.map((page) => (
                <li className={`govuk-pagination__item `} key={uuidv4()}>
                  <a
                    className={`govuk-pagination__link ${
                      currentPage === page ? "current-page" : "govuk-link"
                    }`}
                    data-current-page={page}
                    href="#"
                    aria-label={`Page ${page}`}
                    id="bagination_numbers"
                    onClick={clickHandler}
                  >
                    {page}
                  </a>
                </li>
              ))}
              {currentPage + 1 < pagesCount  && pagesCount >3 ? (
                <li className="govuk-pagination__item govuk-pagination__item--ellipses three-dots">
                  ...
                </li>
              ) : (
                <></>
              )}
            </ul>
            {currentPage === pagesCount ? (
              <div style={{ width: "87.77px" }}></div>
            ) : (
              <div className="govuk-pagination__next">
                <a
                  className="govuk-link govuk-pagination__link"
                  href="#"
                  rel="next"
                  onClick={clickHandler}
                >
                  <span className="govuk-pagination__link-title">
                    Next<span className="govuk-visually-hidden"> page</span>
                  </span>
                  <svg
                    className="govuk-pagination__icon govuk-pagination__icon--next"
                    xmlns="http://www.w3.org/2000/svg"
                    height="13"
                    width="15"
                    aria-hidden="true"
                    focusable="false"
                    viewBox="0 0 15 13"
                  >
                    <path d="m8.107-0.0078125-1.4136 1.414 4.2926 4.293h-12.986v2h12.896l-4.1855 3.9766 1.377 1.4492 6.7441-6.4062-6.7246-6.7266z"></path>
                  </svg>
                </a>
              </div>
            )}
          </nav>
        </div>
      ) : (
        <div style={spacerStyle}></div>
      )}
    </>
  );
};

export default PaginationComponent;
