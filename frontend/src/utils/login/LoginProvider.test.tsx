import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
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

const mockReload = jest.fn();
const originalLocation = window.location;

beforeAll(() => {
  Object.defineProperty(window, "location", {
    configurable: true,
    value: { ...originalLocation, reload: mockReload },
  });
});

afterAll(() => {
  Object.defineProperty(window, "location", {
    configurable: true,
    value: originalLocation,
  });
});

const renderSignedIn = async () => {
  (getCurrentUser as jest.Mock).mockResolvedValue({ username: "user" });
  render(
    <CustomProvider>
      <Header />
    </CustomProvider>
  );
  return screen.findByRole("button", { name: "Sign Out" });
};

describe("Sign out", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("waits for Amplify signOut to complete before reloading the page", async () => {
    let resolveSignOut: () => void = () => undefined;
    (signOut as jest.Mock).mockReturnValue(
      new Promise<void>((resolve) => {
        resolveSignOut = resolve;
      })
    );

    fireEvent.click(await renderSignedIn());

    expect(signOut).toHaveBeenCalledTimes(1);
    expect(mockReload).not.toHaveBeenCalled();
    expect(mockCookieRemove).not.toHaveBeenCalled();

    resolveSignOut();

    await waitFor(() => expect(mockReload).toHaveBeenCalledTimes(1));
    expect(mockCookieRemove).toHaveBeenCalledWith("stage_id");
    expect(mockCookieRemove).toHaveBeenCalledWith("access-type");
    expect(screen.queryByRole("button", { name: "Sign Out" })).toBeNull();
  });

  it("still clears local state and reloads if signOut rejects", async () => {
    const consoleError = jest.spyOn(console, "error").mockImplementation(() => undefined);
    (signOut as jest.Mock).mockRejectedValue(new Error("network"));

    fireEvent.click(await renderSignedIn());

    await waitFor(() => expect(mockReload).toHaveBeenCalledTimes(1));
    expect(mockCookieRemove).toHaveBeenCalledWith("stage_id");
    expect(mockCookieRemove).toHaveBeenCalledWith("access-type");
    consoleError.mockRestore();
  });
});

