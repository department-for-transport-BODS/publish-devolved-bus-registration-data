import React from 'react';
import { render } from '@testing-library/react';
import App from './App';

const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

jest.mock('aws-amplify', () => ({
  Amplify: { configure: jest.fn() },
}));

jest.mock('aws-amplify/auth', () => ({
  getCurrentUser: jest.fn().mockRejectedValue(new Error('Not authenticated')),
  signIn: jest.fn(),
  confirmSignIn: jest.fn(),
  resetPassword: jest.fn(),
  confirmResetPassword: jest.fn(),
  signOut: jest.fn(),
}));

jest.mock('@aws-amplify/ui-react', () => ({
  useAuthenticator: jest.fn(() => ({ signOut: jest.fn() })),
}));

jest.mock('react-head', () => ({
  HeadProvider: ({ children }: { children: React.ReactNode }) => <>{children}</>,
  Title: ({ children }: { children: React.ReactNode }) => <title>{children}</title>,
  Meta: () => null,
  Link: () => null,
}));

jest.mock('universal-cookie', () =>
  jest.fn().mockImplementation(() => ({
    get: jest.fn(),
    set: jest.fn(),
    remove: jest.fn(),
  }))
);

const navigateTo = (path: string) => window.history.pushState({}, '', path);

describe('App snapshots', () => {
  beforeEach(() => {
    navigateTo('/');
    mockNavigate.mockClear();
  });

  it('renders the home page (/) correctly', () => {
    const { asFragment } = render(<App />);
    expect(asFragment()).toMatchSnapshot();
  });

  it('renders the /login page correctly', () => {
    navigateTo('/login');
    const { asFragment } = render(<App />);
    expect(asFragment()).toMatchSnapshot();
  });

  it('renders the /home-options page correctly', () => {
    navigateTo('/home-options');
    const { asFragment } = render(<App />);
    expect(asFragment()).toMatchSnapshot();
  });

  it('renders the /contact-us page correctly', () => {
    navigateTo('/contact-us');
    const { asFragment } = render(<App />);
    expect(asFragment()).toMatchSnapshot();
  });

  it('renders the /privacy-statement page correctly', () => {
    navigateTo('/privacy-statement');
    const { asFragment } = render(<App />);
    expect(asFragment()).toMatchSnapshot();
  });

  it('renders the /accessibility-statement page correctly', () => {
    navigateTo('/accessibility-statement');
    const { asFragment } = render(<App />);
    expect(asFragment()).toMatchSnapshot();
  });

  it('renders the /cookie-page page correctly', () => {
    navigateTo('/cookie-page');
    const { asFragment } = render(<App />);
    expect(asFragment()).toMatchSnapshot();
  });

  it('renders the /find-registered-services page correctly', () => {
    navigateTo('/find-registered-services');
    const { asFragment } = render(<App />);
    expect(asFragment()).toMatchSnapshot();
  });

  it.each([
    '/upload-csv',
    '/partly-uploaded',
    '/successfully-uploaded',
    '/registrations',
    '/pre-validation',
    '/view-registrations',
    '/registration-details',
  ])('protected route %s renders null while awaiting auth', (path) => {
    navigateTo(path);
    const { asFragment } = render(<App />);
    expect(asFragment()).toMatchSnapshot();
  });
});
