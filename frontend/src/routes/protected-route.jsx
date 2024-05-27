import { Navigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { isEmpty, isNull } from "lodash";
export const ProtectedRoute = ({ children }) => {
  const { user } = useAuth();
  if (isEmpty(user) || isNull(user)) {
    return <Navigate to="/login" />;
  }
  return children;
};