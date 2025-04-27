// App.jsx
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Home from './features/home/todo.page';
import Login from './features/authentication/account.page';
import { Provider } from 'react-redux';
import { AuthProvider } from './hooks/useAuth';
import { ProtectedRoute } from "./routes/protected-route";
import store from './redux/store';
import { ThemeProvider } from './hooks/useTheme';
import { Navigate } from "react-router-dom";



const App = () => {
  return (
    <Provider store={store}>
      <AuthProvider>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route
              path="/"
              element={
                <ProtectedRoute>
                  <Home />
                </ProtectedRoute>
              }
            />
            <Route path="*" element={<Navigate to="/login" />} />
          </Routes>
        </ThemeProvider>
      </AuthProvider>
    </Provider>
  );
};

export default App;
