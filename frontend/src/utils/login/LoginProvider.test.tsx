import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { MemoryRouter, useLocation, useNavigate } from "react-router-dom";
import { getCurrentUser, signOut } from "aws-amplify/auth";
import CustomProvider from "./LoginProvider";
import Header from "../../Layout/Header";

const mockCookieRemove = jest.fn();

jest.mock("aws-amplify/auth", () => ({
  getCurrentUser: jest.fn(),
  signIn: jest.fn(),
  signOut: jest.fn(),
}));

jest.mock("universal-cookie", () =>
  // Plain class rather than jest.fn(): CRA's resetMocks would wipe a mockImplementation.
  class {
    get = jest.fn();
    set = jest.fn();
    remove = (...args: unknown[]) => mockCookieRemove(...args);
  }
);

const LocationDisplay = () => {
  const location = useLocation();
  const navigate = useNavigate();
  return (
    <>
      <p data-testid="location">{location.pathname}</p>
      <button onClick={() => navigate(-1)}>Back</button>
    </>
  );
};

// History is [/previous, /upload-csv], so after a replace-navigation to "/",
// going back should skip the signed-in page and land on /previous.
const renderSignedIn = async () => {
  (getCurrentUser as jest.Mock).mockResolvedValue({ username: "user" });
  render(
    <CustomProvider>
      <MemoryRouter initialEntries={["/previous", "/upload-csv"]} initialIndex={1}>
        <Header />
        <LocationDisplay />
      </MemoryRouter>
    </CustomProvider>
  );
  return screen.findByRole("button", { name: "Sign Out" });
};

const currentPath = () => screen.getByTestId("location").textContent;

describe("Sign out", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("waits for Amplify signOut to complete before navigating home", async () => {
    let resolveSignOut: () => void = () => undefined;
    (signOut as jest.Mock).mockReturnValue(
      new Promise<void>((resolve) => {
        resolveSignOut = resolve;
      })
    );

    fireEvent.click(await renderSignedIn());

    expect(signOut).toHaveBeenCalledTimes(1);
    expect(currentPath()).toBe("/upload-csv");
    expect(mockCookieRemove).not.toHaveBeenCalled();

    resolveSignOut();

    await waitFor(() => expect(currentPath()).toBe("/"));
    expect(mockCookieRemove).toHaveBeenCalledWith("stage_id");
    expect(mockCookieRemove).toHaveBeenCalledWith("access-type");
    expect(screen.queryByRole("button", { name: "Sign Out" })).toBeNull();
  });

  it("replaces the current page so back does not return to it", async () => {
    (signOut as jest.Mock).mockResolvedValue(undefined);

    fireEvent.click(await renderSignedIn());
    await waitFor(() => expect(currentPath()).toBe("/"));

    fireEvent.click(screen.getByRole("button", { name: "Back" }));

    expect(currentPath()).toBe("/previous");
  });

  it("still clears local state and navigates home if signOut rejects", async () => {
    const consoleError = jest.spyOn(console, "error").mockImplementation(() => undefined);
    (signOut as jest.Mock).mockRejectedValue(new Error("network"));

    fireEvent.click(await renderSignedIn());

    await waitFor(() => expect(currentPath()).toBe("/"));
    expect(mockCookieRemove).toHaveBeenCalledWith("stage_id");
    expect(mockCookieRemove).toHaveBeenCalledWith("access-type");
    consoleError.mockRestore();
  });
});
