import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { MemoryRouter, Route, Routes, useLocation, useNavigate } from "react-router-dom";
import { getCurrentUser } from "aws-amplify/auth";
import RequireAuth from "./RequireAuth";

jest.mock("aws-amplify/auth", () => ({
  getCurrentUser: jest.fn(),
}));

const Protected = () => <p>Protected content</p>;

const LocationDisplay = () => {
  const location = useLocation();
  const navigate = useNavigate();
  return (
    <>
      <p data-testid="location">{location.pathname + location.search}</p>
      <button onClick={() => navigate(-1)}>Back</button>
    </>
  );
};

const renderAt = () =>
  render(
    <MemoryRouter initialEntries={["/previous", "/upload-csv"]} initialIndex={1}>
      <Routes>
        <Route path="/upload-csv" element={<RequireAuth component={Protected} />} />
        <Route path="*" element={null} />
      </Routes>
      <LocationDisplay />
    </MemoryRouter>
  );

const currentPath = () => screen.getByTestId("location").textContent;

describe("RequireAuth", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("renders the page when the user is signed in", async () => {
    (getCurrentUser as jest.Mock).mockResolvedValue({ username: "user" });

    renderAt();

    expect(await screen.findByText("Protected content")).toBeInTheDocument();
  });

  it("replaces the protected page with login so back does not return to it", async () => {
    const consoleError = jest.spyOn(console, "error").mockImplementation(() => undefined);
    (getCurrentUser as jest.Mock).mockRejectedValue(new Error("signed out"));

    renderAt();

    expect(await screen.findByText("/login?to=upload-csv")).toBeInTheDocument();
    expect(screen.queryByText("Protected content")).toBeNull();

    fireEvent.click(screen.getByRole("button", { name: "Back" }));

    expect(currentPath()).toBe("/previous");
    consoleError.mockRestore();
  });
});
