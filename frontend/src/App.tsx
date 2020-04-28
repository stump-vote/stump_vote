import React, { useState, useEffect, ReactNode } from 'react';
import { getUser } from 'Services';
import {
  AuthContext,
  AppState,
  defaultAppState,
  useAuthState,
} from 'Context/auth';
import LoginPage from 'Components/Pages/LoginPage';

function AuthProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<AppState | typeof defaultAppState>(
    defaultAppState
  );
  useEffect(() => {
    getUser().then(
      (user) => setState({ status: 'success', error: null, user }),
      (error) => setState({ status: 'error', error, user: null })
    );
  }, []);

  return (
    <AuthContext.Provider value={state}>
      {state.status === 'pending' ? (
        'Loading...'
      ) : state.status === 'error' ? (
        <div>
          Oh no
          <div>
            <pre>{state.error?.message}</pre>
          </div>
        </div>
      ) : (
        children
      )}
    </AuthContext.Provider>
  );
}

function AuthenticatedSite() {
  return (
    <>
      <h1>You are logged in</h1>
      <button onClick={() => console.log('get user Info!')}>
        Get User Info
      </button>
    </>
  );
}

function UnauthenticatedSite() {
  return <LoginPage />;
}

function Home() {
  const { user } = useAuthState();
  return user ? <AuthenticatedSite /> : <UnauthenticatedSite />;
}

function App() {
  return (
    <AuthProvider>
      <div>
        <h1>Stump *</h1>
        <p>Start voting</p>
        <Home />
      </div>
    </AuthProvider>
  );
}

export default App;
