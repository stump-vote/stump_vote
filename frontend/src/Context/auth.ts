import { createContext, useContext } from 'react';

// const response = {
//   id: 2,
//   username: 'zrose',
//   email: 'zackrose@gmail.com',
//   last_name: 'Rose',
//   first_name: 'Zack',
//   is_staff: true,
//   is_superuser: true,
// };

export type AppState = {
  status: 'pending' | 'error' | 'success' | null;
  error: ErrorEvent | null;
  user: {
    id?: number;
    username?: string;
    email?: string;
    last_name?: string;
    first_name?: string;
    is_staff?: boolean;
    is_superuser?: boolean;
  } | null;
};

export const defaultAppState = {
  user: {},
  status: null,
};

export const AuthContext = createContext<AppState | typeof defaultAppState>(
  defaultAppState
);

export function useAuthState() {
  const state = useContext(AuthContext);
  const isPending = state?.status === 'pending';
  const isError = state?.status === 'error';
  const isSuccess = state?.status === 'success';
  const isAuthenticated = state?.user && isSuccess;
  return {
    ...state,
    user: state?.user || {},
    isPending,
    isError,
    isSuccess,
    isAuthenticated,
  };
}
