import { createContext, useContext, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { useLocalStorage } from "./useLocalStorage";
import { isEmpty, isNull } from "lodash";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useLocalStorage("user", null);
    const navigate = useNavigate();

    const login = (userData) => {
        setUser(userData);
        if (!isEmpty(userData)) {
            navigate("/");
        }
    };

    const logout = () => {
        setUser(null);
        if (isNull(user)) {
            navigate("/login");
        }
    };

    const value = useMemo(() => ({ user, login, logout, setUser }), [user]);

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);